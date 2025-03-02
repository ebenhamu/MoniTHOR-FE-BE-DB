from datetime import datetime, timezone
import requests
import json
import concurrent.futures
from queue import Queue
import time
from pythonBE import check_certificate 
import os
from logger.logs import logger
from DB.db_helper import db_update_domain , db_get_domains

# livness and ssl info function , for single domain file "all=False" , for domains file "all=True"
# function will read Domain/Domains file and will update relevant fields in file 
# 'domain','status_code',"ssl_expiration","ssl_Issuer" 

def livness_check (username):
    # Measure start time
    logger.debug(f'Function "livness_check" is invoked by User- {username}')
    start_date_time = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M")
    start_time = time.time()    
    urls_queue = Queue()
    analyzed_urls_queue = Queue()                 
   
    data = db_get_domains(username)      

    for d in data :        
        urls_queue.put(d[0]) 
         
    numberOfDomains=urls_queue.qsize()
    logger.info(f"Total URLs to check: {numberOfDomains}")

    # Define the URL checking function with a timeout and result storage
    def check_url():
        while not urls_queue.empty():
            url = urls_queue.get()
                                   
            
            result = {'domain': url, 'status_code': 'FAILED' ,"ssl_expiration":'FAILED',"ssl_Issuer": 'FAILED' }  # Default to FAILED
            
            try:
                response = requests.get(f'http://{url}', timeout=5)
                logger.info(f"URL To Check:{url}")
                if response.status_code == 200:                    
                    certInfo=check_certificate.certificate_check(url) 
                    result = {'domain': url, 'status_code': 'OK' ,"ssl_expiration":certInfo[0],"ssl_Issuer": certInfo[1][:30]}  # Default to FAILED
                    
                    db_update_domain(username,url,'OK',certInfo[0], certInfo[1][:30])
            except requests.exceptions.RequestException:
                db_update_domain(username,url,'FAILED','FAILED','FAILED')                
            finally:                
                analyzed_urls_queue.put(result)  # Add result to analyzed queue
                urls_queue.task_done()

    # Generate report after all URLs are analyzed
    def generate_report():
        results = []
        urls_queue.join()  # Wait for all URL checks to finish

        # Collect results from analyzed queue
        while not analyzed_urls_queue.empty():
            results.append(analyzed_urls_queue.get())
            analyzed_urls_queue.task_done()

       # Write results to JSON file
   

    # Run URL checks in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as liveness_threads_pool:
        # Submit URL check tasks
        futures = [liveness_threads_pool.submit(check_url) for _ in range(100)]
        # Generate report after tasks complete
        liveness_threads_pool.submit(generate_report)

    urls_queue.join()  # Ensure all URLs are processed

    # Measure end time
    end_time = time.time()
    elapsed_time = end_time - start_time

    logger.debug(f"URL liveness check complete in {elapsed_time:.2f} seconds.")
    

    data = db_get_domains(username)   

    results = [
    {
        'domain': domain[0],
        'status_code': domain[1],
        'ssl_expiration': domain[2],
        'ssl_Issuer': domain[3]
    }
    for domain in data ]



    start_date_time=start_date_time+' (UTC)'
    resultsData={ 'results':results,'start_date_time':start_date_time,'numberOfDomains':str(numberOfDomains) }
    return resultsData














