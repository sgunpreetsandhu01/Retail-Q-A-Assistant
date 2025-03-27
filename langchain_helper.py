import langchain
import langgraph
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.vectorstores import Chroma
from langchain.prompts import SemanticSimilarityExampleSelector, FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts.prompt import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from secretkeys import database_info
from few_shots import few_shots
from chromadb.config import Settings
import streamlit as st
import pymysql
import os

from dotenv import load_dotenv
load_dotenv()

def get_few_shot_db_chain():
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo",openai_api_key=os.environ['OPENAI_API_KEY'])

    db_user = database_info['db_user']
    db_pass = database_info['db_passwd']
    db_host = database_info['db_host']
    db_name = database_info['db_name']

    #Connecting to MySQL Database
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}",sample_rows_in_table_info=3)

    #Creating strings of few shots example
    to_vectorize = [" ".join(example.values()) for example in few_shots]

    #Loading the huggingface embedding model
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    #Creating Vector database
    vectorstore = Chroma.from_texts(
        to_vectorize,embedding = embeddings,
        metadatas=few_shots,
        persist_directory="./chroma_db",  # 👈 stores vector DB locally
        )

    #Creating example selector which selects semenatically similar examples from vector db
    example_selector = SemanticSimilarityExampleSelector(
    vectorstore = vectorstore,
    k=2 #number of similar examples to select
    ) 

    #Creating example prompt template
    example_prompt = PromptTemplate(
    input_variables = ["Question","SQLQuery","SQLResult","Answer"],
    template = "\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}"
    )

    #Creating Few Shot Prompt template
    few_shot_prompt = FewShotPromptTemplate(
        example_selector = example_selector,
        example_prompt = example_prompt,
        prefix = _mysql_prompt,
        suffix = PROMPT_SUFFIX,
        input_variables = ['input','table_info','top_k'],
    )

    #Creating the chain
    chain = SQLDatabaseChain.from_llm(llm,db,verbose=True,prompt=few_shot_prompt)
    return chain

if __name__ == '__main__':
    chain = get_few_shot_db_chain()
    print(chain.invoke("How many total t shirts are left in the stock?"))