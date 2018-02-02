import csv
import customerio
import os
import sys

event = "sonletWaitlist"

#Log into CustomerIO
from customerio import CustomerIO
cio = CustomerIO("6d30b69c3d9afe45835b", "d3951fc08db29107a260")

#Iterate through the CSV and add new contacts to Customer.IO
with open('cio_upload4.csv','rb') as csvDataFile:   
    csvReader = csv.reader(csvDataFile)
    addfields=[[row[0],row[2],row[3],row[4],row[5],row[6]] for row in csvReader][1:]
               
    for row in addfields:
        created_at, company, email, new_id, first_name, last_name = row
        
        cio.identify(id=(new_id), email=(email), first_name=(first_name), last_name=(last_name), created_at=(created_at), company=(company))
                 
        print "Added {} with id {} to customer.io contacts and added the attributes first_name:{}, last_name:{}, created_at:{}, and company: {}.".format(email, new_id, first_name, last_name, created_at, company)
        
        cio.track(customer_id=(new_id), name='sonletWaitlist')
        
        print "Added the event {} to Customer.IO user with id {}".format(event,new_id)
        
                         
sys.stdout.flush()
            