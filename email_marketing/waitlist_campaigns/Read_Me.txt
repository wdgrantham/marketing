Read Me - Sending emails to folks on our Wait list
~~~~~~~

Taking waitlist or opt-ins from a Google From, adding them to Customer.IO or your email service provider, and sending out responses.  Includes a look at the liquid code written in customer.io to customize the email based on a particular segmentation created based on the email opt-in form. 

Step 1 - Export the Google Form responses to CSV

Step 2 - Add or update the contacts from the Google Form to Customer.IO contacts or your email service provider contacts.  In my case, I tried to identify whether a contact was already in my contacts using the email address the respondent replied with.  If the email address matched, I bookmarked the Customer_ID assigned to the email in Customer_IO contacts so that my script would update the contact and I could keep track of the contact continuously in my database.  If the user was not in my contacts, then I assigned the user a unique ID and my script below will add the contact to Customer.IO.  

Step 3 - Run the script addContact.py to add contacts to customer.io that are needed along with an unique Event name that can be used to identify the contacts in Customer.io.  In this case, I named the event "sonletWaitlist". 

Step 4 - Confirm the contacts were added and updated correctly by creating a segment in Customer.IO and confirming that the total number of rows in the CSV respondents matches the number of contacts in the segment. 

Step 5 - Create a new triggered campaing based on the segment you created in Step 4.  I use triggered campaingns so that I can easily add follow-up emails and follow-up offers to the same groups later on if needed.  The triggered campaing should be setup to send to "Existing and Future contacts that enter the segment", and ensure that if the Event is being added dynamically (and not just by the script you ran above) the contact is relevant to new contacts entering the segment. Schedule the triggered campaign using an appropriate "Time Window" event in Customer.io. 

Step 6 - Create your email creative, test, get approval, get third party review. 

Step 7 - Review the triggered campaign and start the campaign.  