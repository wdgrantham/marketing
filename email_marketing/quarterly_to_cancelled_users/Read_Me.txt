Read Me - Send the quarterly newsletter to cancelled users
~~~~~~~~~~
These are the steps to follow to prepare and send a quarterly newsletter.  Basic python experience and experience dealing with CSV files either with excel, google sheets (doesn't work well for large files), or terminal commands (cut and append) are recommended.  HTML, inlines css, and creative skills required to draft the email. 

_____________________

Step 1 - Design and draft the quarterly newsletter to cancelled users using Customer.IO and a basic text editor with a live browser preview funtionality, I prefer Brackets. Use spelling and grammar editor, such as the free version of Grammarly, to ensure that your grammar and spelling are correct once you've finished drafting.  You may need to seek help from a graphic designer for image editing, if images are important to your email design.

Step 2 - Send a live preview of the email to yourself using Customer.io test functionality.  Check that the email is legible on both desktop and mobile devices.  Click all your links and ensure they function and direct the recipient to the right page. 

Step 3 - Send the email to Mitch and Sonnie for approval.  Make any changes requested by the bosses.  Send it to someone who is not involved in the company (like a close friend or family member, I prefer using my wife but sometimes my brother will have to do, he's not nearly as attractive and doesn't distract me as much.)

Step 4 - Set up a triggered campaingn in Customer IO.  Use a previous quarterly email send as a template.  The template is set up so that the emails sent over the course of three days (Tuesday, Wednesday, Thursday) so that in the event of lots of respondents to the customer support email, the customer support team is not overwhelmed.  Currently, the template is staggered to send three emails on each day, 2 hours apart. The template consists of one email for each of nine group numbers.  Copy the email drafted above into each of the triggered campaign emails.  Ensure that the email contains an attribute filter that pertains to the appropriate "group_no" value, to ensure that only contacts in that group number are sent the correct email. 

Step 5 - Update the cancelled users contacts in customer.io to assign sending groups to new contacts.  As of writing this email, there are 9 sending groups of approximately 2000 contacts each (18,000 total contacts).  You will need to assign the next 2,000 contacts to group 10, then 11, and so forth, so as to properly stagger the email sends appropriately. Upate the contact using the pythons script called 'updateContact.py' as follows: 
        a. Create a csv file that contains two columns: customerio contact id (named cancelled_id) and sending group no (named group_no). Save the csv in a new folder called 'Cancelled_Users_Quarterly_Newsletter_Q[]-20[]'.  Name the csv 'cancelled_ids.csv'.  Ensure that there the file name is spelled correctly and that the csv file is set up correctly. 
        b. Copy the file updateContact.py to your new folder
        c. Open a terminal window, navigate to your new folder with a command such as cd documents/newsletters/cancelled_users_quarterly_newsletter
        d. Type the command 'python -v' and ensure you are running python version 2.7.x
        e. Type the command 'python updateContact.py' the terminal window should print or display the contact thats are being updated by showing a message as follows: 
        "Added group_no 6 to id 516558." 

Step 6 - Verify that the contacts have been updated by creating Segment in Custom.io and view that the contacts are updated.  Open Customer.io, ensure you are on the correct workspace (ShopTheRoe or PopItUp), click "Segments", and "Create New".  Name the segment, and create the segment based on the Attribute "group_no" and the value equal to the number that you updated such as "10". Click Save.  Confirm that the number of contacts updated is equal to the number in the segment.  

Step 7 - Return to your triggered campaign that you set up in step 5, ensure that you have added any additional emails with a filter that corresponds to the group number to ensure that contacts that have cancelled since the last email have been added to the campaign and will receive the email. 

Step 8 - Review the triggered campaign.  Set the conversion goal to "Enter the Segment Reactivated their subscription".  Select send campaign to "Existing and Future Contacts" (because we have set up filters for each email that is sent, future contacts will not actually receive emails). Click Start campaign. 

Step 9 - Review the campaign periodically to ensure that it is sending correctly. Review the Fresh Desk inbox and triggered campaign overview periodically to monitor campaingn responses and performance. 