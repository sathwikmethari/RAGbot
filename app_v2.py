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