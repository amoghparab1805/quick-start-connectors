from langchain_community.llms import OCIGenAI
from langchain_community.embeddings import OCIGenAIEmbeddings

EMBEDDINGS = OCIGenAIEmbeddings(
    model_id="cohere.embed-english-light-v3.0",
    service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
    compartment_id="ocid1.compartment.oc1..aaaaaaaaaqeg2ttl"
                   "2rz6so5gvae7grmumjuijvm7rxeelqg4dzis2eybrk5a",
    model_kwargs={"temperature": 0.5, "top_p": 0.75, "max_tokens": 4000}
)

query = "This is a query in English."
response = EMBEDDINGS.embed_query(query)
#print(response)

llm = OCIGenAI(
    model_id="cohere.command",
    service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
    compartment_id="ocid1.compartment.oc1..aaaaaaaaaqeg2ttl"
                   "2rz6so5gvae7grmumjuijvm7rxeelqg4dzis2eybrk5a",
)

response = llm.invoke("Tell me one fact about earth", temperature=0.7)
print(response)

from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(input_variables=["query"], template="{query}")

llm_chain = LLMChain(llm=llm, prompt=prompt)

response = llm_chain.invoke("what is the capital of france?")
print(response)


from sqlalchemy import create_engine
from sqlalchemy import text
from langchain import OpenAI, Cohere, SQLDatabase, SQLDatabaseChain

un = os.environ.get("PYTHON_USERNAME")
pw = os.environ.get("PYTHON_PASSWORD")
# directory containing the extracted wallet.zip tnsnames.ora file
cd = os.environ.get("PYTHON_CONFIG_DIR")
# directory containing the extracted wallet.zip ewallet.pem file
wloc = os.environ.get("PYTHON_PEM_DIR")
# wallet password created when downloading the wallet
wpw = os.environ.get("PYTHON_WALLET_PASSWORD")
# connect name from the tnsnames.ora file, like 'myclouddb_low'
cs = os.environ.get("PYTHON_CONNECT_ALIAS")
engine = create_engine(
    f'oracle+oracledb://:@',
    connect_args={
        "user": un,
        "password": pw,
        "dsn": cs,
        "config_dir": cd,
        "wallet_location": wloc,
        "wallet_password": wpw,
    })

db = SQLDatabase(engine)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
db_chain.run("Is Casey Brown in the database?")
