from environs import Env

env = Env()
env.read_env()

PSQL_USERNAME = env.str("PSQL_USERNAME")
PSQL_PASSWORD = env.str("PSQL_PASSWORD")

HOST = "localhost"
PORT = "5432"

# Connect to the default 'postgres' database
DATABASE = "holy_cluster"

GENERAL_DB_URL = f"postgresql+psycopg2://{PSQL_USERNAME}:{PSQL_PASSWORD}@{HOST}:{PORT}"
DB_URL = f"{GENERAL_DB_URL}/{DATABASE}"


# Parameters for the API
UI_DIR = env.str("UI_DIR")
