import os
import json
from logger.logs import logger
from  DB.db_helper import add_user,get_user_password,is_user_exists

  
def register_user (userName,password1,password2) :
    logger.debug(f'Register Functions is invoked with new User:{userName}')
    successMessage = {'message' : "Registered successfully"}
    failureMessage = {'message' : "Username already taken"}
    emptyMessage = {'message' : "Username or password is Empty"}
    passwordMessage = {'message' : "Passwords do not match"}

    
    if password1 != password2:
        return passwordMessage
   
    if (is_user_exists(userName)):
        return failureMessage
    
    # check if the user name and password empty 
    if not userName or not password1 or not password2:
        return emptyMessage
    

    
    add_user(userName,password1)
    logger.info(f'New User is created - {userName}')       
    return successMessage


# Login function
def login_user (userName,password) :
        
    logger.debug(f'Login Functions is invoked with User:{userName}')
    successMessage = { 'message' : "Login Successful"}
    failureMessage = { 'message' : "error : invalid user name or password"}        
    

    # get user password from DB
    logger.log("Getting user password from DB")
    if (password==get_user_password(userName)):
        return successMessage
    else:
        return failureMessage


    
    
def is_user_exist (userName) :
        
    logger.debug(f'Cheking if user {userName} exist')
    successMessage = { 'message' : "User exist"}
    failureMessage = { 'message' : "User or User file is not exist"} 
    
        
    # Create users file if not exist 
    if not os.path.exists('./users.json'):
        return failureMessage
        
    # loadin current data fro users file and convert to list 
    with open('users.json', 'r') as f:
        current_info = json.load(f)
        currentListOfUsers=list(current_info)   
    
    # checking is user in file , if yes , validating password 
    for user in currentListOfUsers :            
        if user['username'] == userName:    
            return successMessage             
    return failureMessage
