import oracledb
from dotenv import load_dotenv
import os
import csv

env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path=env_path)

user = os.getenv('ORACLE_USER')
password = os.getenv('ORACLE_PASSWORD')
dsn = os.getenv('ORACLE_DSN')
config_dir = os.getenv('ORACLE_CONFIG_DIR')
wallet_password = os.getenv('ORACLE_WALLET_PASSWORD')
wallet_location = os.getenv('ORACLE_WALLET_LOCATION')

#user="admin"
#password="Auto_MY_ADW_1234"
#dsn="my_adw_high"
#config_dir="/scratch/tls_wallet"
#wallet_location="/scratch/tls_wallet"
#wallet_password="Auto_MY_ADB_Wallet"
connection = oracledb.connect(user=user, password=password, dsn=dsn, config_dir=config_dir, wallet_location=wallet_location, wallet_password=wallet_password)
cursor = connection.cursor()

table_name = 'abc'

csv_file_path = 'abc.csv'

# Read CSV file and get columns
with open(csv_file_path, 'r') as file:
    reader = csv.reader(file)
    headers = next(reader)

# Create table query
create_table_query = f"""
CREATE TABLE {table_name} (
    {", ".join(f"{col} VARCHAR2(255)" for col in headers)}
)
"""
cursor.execute(create_table_query)
print(f'Table "{table_name}" created successfully.')

# Insert data into the table
with open(csv_file_path, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        insert_query = f"""
        INSERT INTO {table_name} ({", ".join(headers)})
        VALUES ({", ".join([f"'{row[col]}'" for col in headers])})
        """
        cursor.execute(insert_query)


connection.commit()
cursor.close()
connection.close()

print(f'Data loaded into table "{table_name}" successfully.')

