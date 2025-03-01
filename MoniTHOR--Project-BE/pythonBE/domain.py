import os
import json
import re
from logger.logs import logger
from DB.db_helper import db_add_domain,db_remove_domain,db_get_domains,db_update_domain


def add_domain (userName,domain) :
    logger.debug(f'Function is invoked {userName}, {domain}')
    successMessage = { 'message' : "Domain successfully added"}
    failureMessageExist = { 'message' : "Domain already exist in file"}
    failureMessageNotValid = { 'message' : "Invalid Domain Name"}
    
    domain=domain.replace('"','')
    
    if not is_valid_domain(domain):
        return failureMessageNotValid

    
    
    currentListOfDomains=db_get_domains(userName)      

       
    for d in currentListOfDomains :             
        if d[0] == domain:            
            return failureMessageExist

    
    
    if len(currentListOfDomains) < 100 :        
        db_add_domain(userName,domain)              
        return successMessage



def remove_domain (userName,domain) :
    logger.debug(f'Function is invoked {userName}, {domain}')
    successMessage = { 'message' : "Domain successfully removed"}
    errorOnRemoveMessage = { 'message' : "Error in remove domain from DB"}
    failureMessageNotValid = { 'message' : "Invalid Domain Name"}
        
    domain=domain.replace('"','')
    
    if not is_valid_domain(domain):
        return failureMessageNotValid   
     
    try:   
        db_remove_domain(userName,domain)       
        return successMessage
    
    except:
        return errorOnRemoveMessage
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





