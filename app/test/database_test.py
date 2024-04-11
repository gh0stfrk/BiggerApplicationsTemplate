from .config import database_config

def configure_database(app):
    database_config.configure_test_database(app)
    
def drop_database():
    database_config.drop_test_database()
    
def truncate_table(table):
    database_config.truncate_table(table)

def truncate_tables(tables):
    database_config.truncate_tables(tables)