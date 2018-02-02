import csv
import customerio
import os
import sys

#event = "sonletWaitlist"

#Log into CustomerIO
from customerio import CustomerIO
cio = CustomerIO("6d30b69c3d9afe45835b", "d3951fc08db29107a260")

#Iterate through the CSV and add new contacts to Customer.IO
with open('cancelled_id.csv','rb') as csvDataFile:   
    csvReader = csv.reader(csvDataFile)
    addfields=[[row[0],row[1]] for row in csvReader][1:]
               
    for row in addfields:
        cancelled_id, group_no = row
        
        cio.identify(id=(cancelled_id), group_no=(group_no))
                 
        print "Added group_no {} to id {}.".format(group_no, cancelled_id)
                                 
sys.stdout.flush()
            