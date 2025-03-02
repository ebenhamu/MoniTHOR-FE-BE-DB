import random
from DB.db_helper import db_add_user, db_add_domain ,db_is_user_exist

def generate_users_and_domains(filename, num_users=100):
    all_characters = '0123456789'

    for i in range(1, num_users + 1):
        tag = str(i).zfill(2)
        username = f'tester_{tag}'
        if (not db_is_user_exist(username)):
            db_add_user(username, username)
        
        with open(filename, 'r') as infile:
            for line in infile:
                db_add_domain(username, line.strip())

def main():
    filename = './userdata/Domains_for_upload.txt'
    generate_users_and_domains(filename)

if __name__ == '__main__':
    main()
