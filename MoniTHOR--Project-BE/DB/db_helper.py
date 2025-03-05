import psycopg2
import json
from logger.logs import logger
import json
from contextlib import contextmanager

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

class PostgresDB:
    def __init__(self, storedb, myuser, mypassword, host=config['DB_SERVER'], port=config['DB_PORT']):
        self.dbname = storedb
        self.user = myuser
        self.password = mypassword
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            
        except Exception as e:
            logger.debug(f"Error connecting to database: {e}")


    
    
    def get_data(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            logger.debug(f"Error getting data: {e}")
            return None
    

    
    def update_data(self, query, data):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, data)
            self.connection.commit()
            cursor.close()            
        except Exception as e:
            logger.debug(f"Error updating data: {e}")

    def close(self):
        if self.connection:
            self.connection.close()           
            
def db_get_domains(username):
    db = PostgresDB("storedb", "myuser", "mypassword")
    db.connect()
    if not db.connection:
        logger.debug("Error: Unable to connect to the database.")
        return None
    
    query = "SELECT domains FROM users WHERE username = %s"
    result = db.get_data(query, (username,))        
    db.close()
    return result


@contextmanager
def get_db_connection(dbname, user, password):
    db = PostgresDB(dbname, user, password)
    db.connect()
    try:
        yield db
    finally:
        db.close()




def db_add_domain_for_user(username, domain):
    newDomain = {'domain': domain, 'status': 'unknown', 'ssl_expiration': 'unknown', 'ssl_issuer': 'unknown'}
    
    logger.debug(f"Attempting to add domain {domain} for user {username}")

    try:
        with get_db_connection("storedb", "myuser", "mypassword") as db:
            query = """
            UPDATE users
            SET domains = domains || %s::jsonb
            WHERE username = %s;
            """
            logger.debug(f"Executing query: {query}")
            db.update_data(query, (json.dumps([newDomain]), username))
            logger.debug(f"Domain {domain} successfully added for user {username}")
    except Exception as e:
        logger.debug(f"Error updating domain for user {username}: {e}")

    



def db_update_domains(username, new_domains):

    logger.debug(f"Overriding domains for user {username}")

    try:
        with get_db_connection("storedb", "myuser", "mypassword") as db:
            query = """
            UPDATE users
            SET domains = %s::jsonb
            WHERE username = %s;
            """
            logger.debug(f"Executing query: {query}")
            db.update_data(query, (json.dumps(new_domains), username))
            logger.debug(f"Domains for user {username} successfully overridden")
    except Exception as e:
        logger.debug(f"Error overriding domains for user {username}: {e}")

    





def db_get_password(username):
    db = PostgresDB("storedb", "myuser", "mypassword")
    db.connect()    
    query = "SELECT password FROM users WHERE username = %s"
    data = db.get_data(query, (username,))        
    db.close()
    return data[0][0]
    
def db_add_user(username, password):
    db = PostgresDB("storedb", "myuser", "mypassword")
    db.connect()
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    data = (username, password)
    db.update_data(query, data)
    db.close()
    
    
def db_is_user_exist(username):
    db = PostgresDB("storedb", "myuser", "mypassword")
    db.connect()
    query = "SELECT 1 FROM users WHERE username = %s"
    data = db.get_data(query, (username,))
    db.close()
    try:
        status=len(data) > 0
    except:
        status=0
    return status
    

def db_update_domain(username, domain_name, status_code, ssl_expiration, ssl_issuer):        
    db = PostgresDB("storedb", "myuser", "mypassword")
    db.connect()
    query = """
        UPDATE domains
        SET status_code = %s,
        ssl_expiration = %s,
        ssl_issuer = %s
        WHERE domain_name = %s AND username = %s;
    """
    data = (status_code, ssl_expiration, ssl_issuer, domain_name, username)
    db.update_data(query, data)
    db.close()

# def db_add_domain(username, domain_name, status_code='unknown', ssl_expiration='unknown', ssl_issuer='unknown'):
#     db = PostgresDB("storedb", "myuser", "mypassword")
#     db.connect()
#     query = """
#         INSERT INTO domains (username, domain_name, status_code, ssl_expiration, ssl_issuer)
#         VALUES (%s, %s, %s, %s, %s);
#     """
#     data = (username, domain_name, status_code, ssl_expiration, ssl_issuer)
#     db.update_data(query, data)
#     db.close()



def db_remove_domain(username, domain_name):
    db = PostgresDB("storedb", "myuser", "mypassword")
    db.connect()
    query = "DELETE FROM domains WHERE domain_name = %s AND username = %s"
    data = (domain_name, username)
    db.update_data(query, data)
    db.close()



