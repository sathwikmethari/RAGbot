import os
import streamlit as st
from utils import *
from few_shots.few_shots_v2 import few_shots_list_of_dict
from langchain_cohere import ChatCohere
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.vectorstores import Chroma 
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX
from types import MethodType

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

db_user = os.getenv("USER")
db_password = os.getenv("PASSWORD")
db_host = os.getenv("HOST")
db_name = os.getenv("NAME")

os.environ["COHERE_API_KEY"]=os.getenv("COHERE_API_KEY")        # Set the cohere api key
os.environ["LANGCHAIN_TRACING_V2"]="true"                       # Enable tracing
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")  # Set the project name

SQLDatabaseChain.model_rebuild()  # Rebuild the model before usage

try:
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",sample_rows_in_table_info=5)
    print("Successfully connected to the database!")
except:
    print("Failed to connect to the database. Please check your credentials.")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

to_vectorize = [" ".join(example.values()) for example in few_shots_list_of_dict]
vectorstore = Chroma.from_texts(
    to_vectorize, 
    embeddings, 
    metadatas=few_shots_list_of_dict, 
    ids=[str(i) for i in range(len(to_vectorize))]  # Ensure unique IDs
)
# Example selector using semantic similarity
example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vectorstore,
    k=5,
)

mysql_prompt = """You are a MySQL Expert and T-shirt inventory manager. Given an input question, first create a syntactically correct MySQL query to run. 
Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. 
You can order the results to return the most informative data in the database.
Never query for all columns from a table, You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
Pay attention to use only the column names you see in the tables, Only query for columns that exist. Also, pay close attention to which column is in which table.
NEVER wrap the SQL query in markdown backticks or any formatting like ```sql,

# Use the following format:

# Question: Question here
# SQLQuery: Query to run with no pre-amble

# No pre-amble.
# """

prompt2="""You are a MySQL Expert and T-shirt inventory manager.
User asked a question:{question}\n
SQL Results: {output}

Give user friendly responses based on the SQL results.
If the result is None, the ask user a follow up question.

# Use the following format:
Follow up question: The item you are looking for is out of stock. Do you want to be reminded, what other items are in stock?
"""


example_prompt = PromptTemplate(
    input_variables=["Question", "SQLQuery"],
    template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\n",
)

few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,  # assumed defined earlier
    example_prompt=example_prompt,
    prefix=mysql_prompt,
    suffix=PROMPT_SUFFIX,  # assumed defined earlier
    input_variables=["Question", "SQLQuery"],
)

memory = ConversationBufferWindowMemory(k=10, return_messages=True)

# def clean_sql_query(query):
#     return query.replace("```sql", "").replace("```", "").strip()

llm = ChatCohere(model="command-a-03-2025")  # your model

chatbot = SQLDatabaseChain.from_llm(
    llm=llm,
    db=db,
    memory=memory,
    verbose=True,
    prompt=few_shot_prompt,
    use_query_checker=True
)

def clean_sql_query(query):
    return query.replace("```sql", "").replace("```", "").strip()

def clean_and_run(self, query: str):
    cleaned_query = clean_sql_query(query)
    return self._execute(cleaned_query)
chatbot.database.run = MethodType(clean_and_run, chatbot.database)
response = chatbot.run("What colors are available in the inventory?")
print(response)

# st.title("RAG Chatbot")
# input_text=st.text_input("What question do you have in mind?")

# if input_text:
#     container = st.container(border=True)
#     try:
#         response = chatbot.invoke(input_text)
#         container.write(response)
#     except:
#         container.write("Sorry, I am not able to answer this question.")