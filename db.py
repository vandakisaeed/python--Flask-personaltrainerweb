import psycopg2
from .config import BaseConfig
 
def get_connection():
    return psycopg2.connect(BaseConfig.PG_URI)