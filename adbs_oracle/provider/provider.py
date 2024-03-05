#import logging
#import os
#import oracledb
#from flask import current_app as app
#import time
#
#from dotenv import load_dotenv
#
#load_dotenv()
#
#user = os.getenv('ORACLE_USER')
#password = os.getenv('ORACLE_PASSWORD')
#dsn = os.getenv('ORACLE_DSN')
#config_dir = os.getenv('ORACLE_CONFIG_DIR')
#wallet_password = os.getenv('ORACLE_WALLET_PASSWORD')
#wallet_location = os.getenv('ORACLE_WALLET_LOCATION')
#connection_string = os.getenv('ORACLE_TLS_CONNECTION_STRING')
#
#logger = logging.getLogger(__name__)
#
#def search(query):
#    conn = oracledb.connect(user=user, password=password, dsn=dsn, config_dir=config_dir, wallet_location=wallet_location, wallet_password=wallet_password)
#    #conn = oracledb.connect(user=user, password=password, dsn=connection_string, config_dir=config_dir)
#    cursor = conn.cursor()
#    cursor.execute(f"SELECT * FROM employees WHERE last_name = '{query}'")
#    data = cursor.fetchall()
#
#    conn.close()
#    return data

import logging
import os
import oracledb
from flask import current_app as app
import time

from dotenv import load_dotenv

from langchain_community.llms import OCIGenAI
from langchain.chains import LLMChain
from langchain.chains import create_sql_query_chain
from langchain_core.prompts import PromptTemplate
from sqlalchemy import create_engine
from sqlalchemy import text
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.llms import OpenAI, Cohere
from langchain_community.utilities import SQLDatabase

load_dotenv()

user = os.getenv('ORACLE_USER')
password = os.getenv('ORACLE_PASSWORD')
dsn = os.getenv('ORACLE_DSN')
config_dir = os.getenv('ORACLE_CONFIG_DIR')
wallet_password = os.getenv('ORACLE_WALLET_PASSWORD')
wallet_location = os.getenv('ORACLE_WALLET_LOCATION')
connection_string = os.getenv('ORACLE_TLS_CONNECTION_STRING')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
logger = logging.getLogger(__name__)

def search(query):
    #conn = oracledb.connect(user=user, password=password, dsn=dsn, config_dir=config_dir, wallet_location=wallet_location, wallet_password=wallet_password)
    #conn = oracledb.connect(user=user, password=password, dsn=connection_string, config_dir=config_dir)
    #cursor = conn.cursor()
    #cursor.execute(f"SELECT * FROM employees WHERE last_name = '{query}'")
    #data = cursor.fetchall()
    #conn.close()


    llm = OCIGenAI(
        model_id="cohere.command",
        service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
        compartment_id="ocid1.compartment.oc1..aaaaaaaaaqeg2ttl"
                    "2rz6so5gvae7grmumjuijvm7rxeelqg4dzis2eybrk5a",
    )
    
    openai = OpenAI(model_name="davinci-002")
    
    engine = create_engine(
        f'oracle+oracledb://:@',
        connect_args={
            "user": user,
            "password": password,
            "dsn": dsn,
            "config_dir": config_dir,
            "wallet_location": wallet_location,
            "wallet_password": wallet_password,
        })

    db = SQLDatabase(engine)
    db_chain = create_sql_query_chain(llm, db)
    response = db_chain.invoke({"question": query})

    #db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
    #db_chain.run(query)
    #return
    print("GENERATED SQL STATEMENT ---->", response)
    
    response = response.rstrip(';') if response.endswith(';') else response
    #response = response+"'" if "WHERE" in response and not response.endswith("'") else response

    print("UPDATE SQL STATEMENT ---->", response)

    return {"sql": response, "output": db.run(response)}
