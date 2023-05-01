# Need to create a globally accessible database object
# Database config is in the src/datacon.py file

from src.datacon import DataCon

datacon = DataCon().get_instance()
db = datacon.get_db()
