import os
 
class BaseConfig:
    PG_URI = os.getenv('PG_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')