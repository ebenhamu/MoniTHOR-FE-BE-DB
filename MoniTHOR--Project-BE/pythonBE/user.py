import os
import json
from logger.logs import logger
from  DB.db_helper import db_add_user,get_user_password,db_is_user_exist

  
def register_user (userName,password1,password2) :
    logger.debug(f'Register Functions is invoked with new User:{userName}')
    successMessage = {'message' : "Registered successfully"}
    failureMessage = {'message' : "Username already taken"}
    emptyMessage = {'message' : "Username or password is Empty"}
    passwordMessage = {'message' : "Passwords do not match"}

    
    if password1 != password2:
        return passwordMessage
   
    if (db_is_user_exist(userName)):
        return failureMessage
    
    # check if the user name and password empty 
    if not userName or not password1 or not password2:
        return emptyMessage
    

    
    db_add_user(userName,password1)
    logger.info(f'New User is created - {userName}')       
    return successMessage


# Login function
def login_user (userName,password) :
        
    logger.debug(f'Login Functions is invoked with User:{userName}')
    successMessage = { 'message' : "Login Successful"}
    failureMessage = { 'message' : "error : invalid user name or password"}        
    

    # get user password from DB
    logger.info("Getting user password from DB")
    if (password==get_user_password(userName)):
        return successMessage
    else:
        return failureMessage


    
    
def is_user_exist (userName) :
        
    logger.debug(f'Cheking if user {userName} exist')
    successMessage = { 'message' : "User exist"}
    failureMessage = { 'message' : "User is not exist"} 
    
    if db_is_user_exist(userName):                
       return successMessage             
    else:
        return failureMessage
