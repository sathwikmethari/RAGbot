import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
#from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma  
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory #for memory
import tensorflow as tf

from pydantic import BaseModel
from langchain_core.callbacks import Callbacks

from few_shots import few_shots_list_of_dict  #Importing the few_shots_list_of_dict from few_shots.py file


load_dotenv()  # take environment variables from .env (especially openai api key)

import warnings
warnings.filterwarnings("ignore")


#%pip install pymysql
db_user = "root"
db_password = "justdoit"
db_host = "localhost"
db_name = "Project_tshirts"

os.environ["GOOGLE_API_KEY"]=os.getenv("GOOGLE_API_KEY") # Set the google api key
os.environ["LANGCHAIN_TRACING_V2"]="true"                # Enable tracing
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT") # Set the project name

class BaseCache(BaseModel):
    pass


SQLDatabaseChain.model_rebuild()  # Rebuild the model before usage

db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",sample_rows_in_table_info=5)

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1, max_tokens=50)

# Load sentence-transformers model for embedding
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

to_vectorize = [" ".join(example.values()) for example in few_shots_list_of_dict]
vectorstore = Chroma.from_texts(
    to_vectorize, embeddings, metadatas=few_shots_list_of_dict, 
    ids=[str(i) for i in range(len(to_vectorize))]  # Ensure unique IDs
)
# Example selector using semantic similarity
example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vectorstore,
    k=2,
)
mysql_prompt = """You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use CURDATE() function to get the current date, if the question involves "today".
    
Use the following format:
    
Question: Question here
SQLQuery: Query to run with no pre-amble
SQLResult: Result of the SQLQuery
Answer: Final answer here
    
No pre-amble.
"""

example_prompt = PromptTemplate(
    input_variables=["Question", "SQLQuery", "SQLResult","Answer",],
    template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
    )

few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix=mysql_prompt,
    suffix=PROMPT_SUFFIX,
    input_variables=["input", "table_info", "top_k"], #These variables are used in the prefix and suffix
    )
memory = ConversationBufferWindowMemory(k=5, return_messages=True)
chatbot = SQLDatabaseChain.from_llm(llm, db, memory=memory, verbose=True, prompt=few_shot_prompt)

#def clean_sql_query(query):
    #return query.replace("```sql", "").replace("```", "").strip()
import streamlit as st
st.title("Intern Project")
input_text=st.text_input("What question do you have in mind?")

if input_text:
    container = st.container(border=True)
    try:
        container.write(chatbot.invoke(input_text)['result'])
    except:
        container.write("Sorry, I am not able to answer this question.")

