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
