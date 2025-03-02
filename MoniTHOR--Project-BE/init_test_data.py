import random
from DB.db_helper import db_add_user, db_add_domain ,db_is_user_exist

def generate_users_and_100_domains(filename, num_users=100):
    
    for i in range(1, num_users + 1):
        tag = str(i).zfill(2)
        username = f'tester_{tag}'
        if (not db_is_user_exist(username)):
            print(f"adding user {username}")
            db_add_user(username, username)
        
        with open(filename, 'r') as infile:
            for line in infile:
                if (db_is_user_exist(username)):
                    db_add_domain(username, line.strip())


def generate_users_with_one_domain(filename, num_users=100):
    

    for i in range(1, num_users + 1):
        tag = str(i).zfill(2)
        username = f'tester1_{tag}'
        if (not db_is_user_exist(username)):
            print(f"adding user {username}")
            db_add_user(username, username)
    i=1
    with open(filename, 'r') as infile:
        for line in infile:
            tag = str(i).zfill(2)
            username = f'tester1_{tag}'
            if (db_is_user_exist(username)):
                db_add_domain(username, line.strip())
            i=i+1

def main():
    filename = './userdata/Domains_for_upload.txt'
    generate_users_with_one_domain(filename)
    generate_users_and_100_domains(filename)
    
    

if __name__ == '__main__':
    main()
