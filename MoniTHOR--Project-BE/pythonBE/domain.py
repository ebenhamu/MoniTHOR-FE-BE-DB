import os
import json
import re
from logger.logs import logger
from DB.db_helper import db_add_domain_for_user,db_get_domains,db_update_domains


def add_domain (userName,domain) :
    logger.debug(f'Function is invoked {userName}, {domain}')
    successMessage = { 'message' : "Domain successfully added"}
    failureMessageExist = { 'message' : "Domain already exist in file"}
    failureMessageNotValid = { 'message' : "Invalid Domain Name"}
    failureMessageExistListisFull = { 'message' : "List of domains is full"}
    
    domain=domain.replace('"','')
    
    if not is_valid_domain(domain):
        return failureMessageNotValid
   
    domains=db_get_domains(userName)[0][0]  
       
    for d in domains:
        if (d['domain']==domain):
                return failureMessageExist       
    
    if (len(domains)) < 100 :                
        db_add_domain_for_user(userName,domain)
        return successMessage
    else:
        failureMessageExistListisFull




def remove_domain (userName,domain) :
    logger.debug(f'Function is invoked {userName}, {domain}')
    successMessage = { 'message' : "Domain successfully removed"}
    errorOnRemoveMessage = { 'message' : "Error in remove domain from DB"}
    failureMessageNotValid = { 'message' : "Invalid Domain Name"}
    notInFileMessage = {'message' : "Not in list"}
        
    domain=domain.replace('"','')
    
    if not is_valid_domain(domain):
        return failureMessageNotValid   
     
    currentListOfDomains = db_get_domains(userName)[0][0]
    msg=notInFileMessage
    newList=[]
    for d in currentListOfDomains :        
        if d['domain'] == domain:
            msg=successMessage
        else:
            newList.append(d) 
    db_update_domains(userName,newList)   
    return msg
# function to read from file a list of domain and add to domain file.

def add_bulk(userName,fileName):
    fileName=fileName.replace('"','')
    logger.debug(f"File: {fileName}, User: {userName}")
    

    
    if not os.path.exists(fileName):
        return "File Not Exist"
    
    try:
        with open(fileName, 'r') as infile:
            for line in infile:
                add_domain(userName,line.strip())
    
    except Exception as e:        
        return (str(e))
     
    return "Bulk upload finished"






# Function to validate the domain name

def is_valid_domain(s):    
    # Regex to check valid Domain Name
    pattern= r"^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|([a-zA-Z0-9][a-zA-Z0-9-_]{1,61}[a-zA-Z0-9]))\.([a-zA-Z]{2,6}|[a-zA-Z0-9-]{2,30}\.[a-zA-Z]{2,3})$"         
    
    # Return string matche value - bool
    return bool(re.match(pattern,s))





