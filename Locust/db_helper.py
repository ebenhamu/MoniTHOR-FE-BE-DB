import psycopg2
import json
import logger.logs 

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
            print(f"Error connecting to database: {e}")

    def get_data(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print(f"Error getting data: {e}")
            return None

    def update_data(self, query, data):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, data)
            self.connection.commit()
            cursor.close()            
        except Exception as e:
            print(f"Error updating data: {e}")

    def close(self):
        if self.connection:
            self.connection.close()           
            


   
def get_user_password(username):
    db = PostgresDB("storedb", "myuser", "mypassword")
    db.connect()
    usr = username
    query = "SELECT password FROM users WHERE username like %s"
    data = db.get_data(query, (usr,))        
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
    return len(data) > 0
    

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

def db_add_domain(username, domain_name, status_code='unknown', ssl_expiration='unknown', ssl_issuer='unknown'):
    db = PostgresDB("storedb", "myuser", "mypassword")
    db.connect()
    query = """
        INSERT INTO domains (username, domain_name, status_code, ssl_expiration, ssl_issuer)
        VALUES (%s, %s, %s, %s, %s);
    """
    data = (username, domain_name, status_code, ssl_expiration, ssl_issuer)
    db.update_data(query, data)
    db.close()



def db_remove_domain(username, domain_name):
    db = PostgresDB("storedb", "myuser", "mypassword")
    db.connect()
    query = "DELETE FROM domains WHERE domain_name = %s AND username = %s"
    data = (domain_name, username)
    db.update_data(query, data)
    db.close()

def db_get_domains(username):
    db = PostgresDB("storedb", "myuser", "mypassword")
    db.connect()
    query = "SELECT domain_name, status_code, ssl_expiration, ssl_issuer FROM domains WHERE username = %s"
    data = db.get_data(query, (username,))
    db.close()
    return data


# # Example usage:
# if __name__ == "__main__":
#     print(get_user_password('David'))
#db_update_domain('David','facebook.com','dadssssd','ff','ss')
#add_user('dddd','dddd')
#     remove_domain('David','google.com')
#     print(get_domains('David'))