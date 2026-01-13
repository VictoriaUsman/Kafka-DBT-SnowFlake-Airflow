import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

connector_config = {
    "name": "postgres-connector",
    "config": {
        "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
        "database.hostname": os.getenv("POSTGRES_HOST"),      # postgres
        "database.port": os.getenv("POSTGRES_PORT"),          # 5432
        "database.user": os.getenv("POSTGRES_USER"),          # postgres
        "database.password": os.getenv("POSTGRES_PASSWORD"),  # postgres
        "database.dbname": os.getenv("POSTGRES_DB"),          # postgres
        "topic.prefix": "Ian_Tristan_Server",
        "table.include.list": "public.customers,public.accounts,public.transactions",
        "plugin.name": "pgoutput",
        "slot.name": "banking_slot",
        "publication.autocreate.mode": "filtered",
        "tombstones.on.delete": "false",
        "decimal.handling.mode": "double",
        "snapshot.mode": "initial"
    }
}

# Send request to Debezium Connect
url = "http://localhost:8083/connectors"
headers = {"Content-Type": "application/json"}

response = requests.post(url, headers=headers, data=json.dumps(connector_config))

if response.status_code == 201:
    print("✅ Connector created successfully!")
elif response.status_code == 409:
    print("⚠️ Connector already exists.")
else:
    print(f"❌ Failed to create connector ({response.status_code}): {response.text}")
