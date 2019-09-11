# This Python file uses the following encoding: utf-8

import datetime
import string
import random

from firebase import firebase

def removed_deleted_newsletters():#To Do: periodically remove all newsletters with an id "toDelete" from the database
    pass
    

class Blog_article:
    """A blog article that will be sent in a message."""
    
    def __init__(self, account_id, article_id, datetime, title, text, summary, blog_url, blog_type, tags=[], categories=[], is_approved=True, excerpt=None, images=[], link=None):
        self.account_id = account_id #required
        self.article_id = article_id #required
        self.datetime = datetime #required
        self.title = title #required
        self.text = text #required
        self.summary = summary #required
        self.blog_url = blog_url #required
        self.blog_type = blog_type #required
        self.tags = tags
        self.categories = categories
        self.is_approved = is_approved
        self.excerpt = excerpt
        self.images = images
        self.link = link
        #self.created = datetime.datetime.now() #todo... don't know why this is busted
    
    def del_article(self):
        self.account_id = 'toDelete'
        print(f'Deleted article {self.article_id}')

    def approve_article(self):
        self.is_approved = True
        print(f'Blog article {self.article_id} is approved.')
        
    def unapprove_article(self):
        self.is_approved = False
        print(f'Blog article {self.article_id} is unapproved.')
        
class Product:
    """A product that will be sent in a message"""
    
    def __init__(self, account_id, product_id, product_name=None, product_description=None, product_variant={}, product_images=[], product_price=None, product_cost=None, product_link=None, product_shipping=None, is_approved=True):
        self.account_id = account_id #required
        self.product_id = product_id #required
        self.product_name = product_name
        self.product_description = product_description
        self.product_variant = product_variant
        self.product_images = product_images
        self.product_price = product_price
        self.product_cost = product_cost
        self.product_link = product_link
        self.product_shipping = product_shipping
        self.is_approved = is_approved
        self.created = datetime.datetime.now()
        
    def del_product(self):
        self.account_id = 'toDelete'
        print(f'Deleted product {self.product_id}')
    
    def approve_product(self):
        self.is_approved = True
        print(f'Product {self.product_id} is approved.')
        
    def unapprove_product(self):
        self.is_approved = False
        print(f'Product {self.product_id} is unapproved.')

class Blog:
    """A blog with articles"""
    def __init__(self, blog_url, account_id):
        self.blog_url = blog_url
        self.account_id = account_id
        self.created = datetime.datetime.now()
    
class Wp_blog(Blog):
    """A Wordpress blog with blog articles"""
    
    def __init__(self, blog_url, account_id):
        super().__init__(blog_url, account_id)
    
    def get_wp_articles(self):
        self.last_synced = datetime.datetime.now()
        print('getting squarespace blog articles from ' + self.blog_url)
    
    def send_newsletter(self):
        print('sending newsletter for squarespace blog articles from ' + self.blog_url)

class Sp_blog(Blog):
    """A SquareSpace blog with blog articles"""
    
    def __init__(self, blog_url, account_id):
        super().__init__(blog_url, account_id)
    
    def get_sp_articles(self):
        datetime.datetime.now()
        print('getting squarespace blog articles from ' + self.blog_url)
    
    def send_newsletter(self):
        print('sending newsletter for squarespace blog articles from ' + self.blog_url)
        
class Store:
    pass
        
class sonlet_party:
    pass

class popitup_party: 
    pass

class shopify_store: 
    pass

class etsy_store:
    pass

#http://docs.developer.amazonservices.com/en_US/dev_guide/index.html
class amazon_seller_store:#
    pass

class Account:
    """An account, which may be owned by one or multiple users."""
    def __init__(self, user_ids=[1], account_name=None, account_image=None, account_type='user'):
        self.account_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8)) #created automatically
        self.user_ids = user_ids #required
        self.account_name = account_name 
        self.account_image = account_image
        self.account_type = account_type #required
        self.created = datetime.datetime.now()
        
    def add_user(self, user_id):
        self.user_ids.append(user_id)
        print(f'Added user id {user_id} to account with id {self.account_id}')
        
    def del_user(self, user_id):
        self.user_ids.remove(user_id)
        print(f'Removed user id {user_id} from account with id {self.account_id}')
        
    def del_account(self):
        self.user_ids = []
        print(f"Your account {self.account_id} has been deleted.")
        
class Newsletter:
    """An email newsletter from a blog or online store"""
    
    def __init__(self, account_id, from_email_address, to_recipients,  email_subject, email_content, cc_recipients=[], bcc_recipients=[], email_template=None, blog_article_ids=[], product_ids=[]):
        self.account_id = account_id
        self.from_email_address = from_email_address #required
        self.to_recipients = to_recipients #required
        self.email_subject = email_subject #required
        self.email_content = email_content #required
        self.cc_recipients = cc_recipients
        self.bcc_recipients = bcc_recipients
        self.email_template = email_template
        self.blog_article_ids = blog_article_ids
        self.product_ids = product_ids
        self.newsletter_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        self.created = datetime.datetime.now()
        
    def send_newsletter(self):
        print(f"Sending newsletter {self.newsletter_id} soon.")
        
    def schedule_newsletter(self, date_scheduled):
        print(f"Scheduled newsletter {self.newsletter_id} to send at {date_scheduled}.")
        
    def del_newsletter(self):
        self.account_id = 'toDelete'
        print(f"Deleted newsletter {self.newsletter_id}")
    
    def create_email_template(self):
        pass#To do: figure out how to make a newsletter into a template
    
class Email_template:
    """HTML email template"""
    
    def __init__(
        self, 
        account_id, 
        template_html,
        template_name = None,
        unsubscribe_link = 'https://domain.com/account_name/unsubscribe', 
        template_styles = None, 
        sender_physical_address = None,
        sender_logo = None,
        user_ids = [1]
    ):
        self.account_id = account_id #required
        self.template_html = template_html #required
        self.template_name = template_name
        self.unsubscribe_link = unsubscribe_link
        self.template_styles = template_styles
        self.sender_physical_address = sender_physical_address 
        self.sender_logo = sender_logo
        self.user_ids = user_ids
        self.email_template_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        self.created = datetime.datetime.now()
        
    def share_template(self, user_id):
        self.user_ids.append(user_id)
        print(f'Shared template {self.email_template_id} with user {user_id}.')
        
    def unshare_template(self, user_id):
        self.user_ids.remove(user_id)
        print(f'Removed user {user_id} from template id {self.email_template_id}.')
        
    def del_email_template(self):
        self.account_id = 'toDelete'
        self.user_ids = []
        print(f'Deleted email template {self.email_template_id}.')
    
class Contact:
    
    """A contact to receive a message."""
    
    def __init__(self, account_id, email1, contact_id=None, first_name=None, last_name=None, phone1=None, phone1_subscribed=True, email1_subscribed=True, newsletters_sent=[]):
        self.account_id = account_id #required
        self.email1 = email1 #required
        self.contact_id = contact_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone1 = phone1
        self.phone1_subscribed = phone1_subscribed
        self.email1_subscribed = email1_subscribed
        self.newsletters_received = newsletters_sent
        self.created = datetime.datetime.now()
        if self.contact_id == None: self.contact_id = email1
        
    def unsubscribe_email(self):
        self.email1_subscribed = False
        print(f'Unsubscribed email {self.email1} from account {self.account_id}.')
    
    def subscribe_email(self):
        self.email1_subscribed = True
        print(f'Subscribed email {self.email1} to account {self.account_id}.')
        
    def del_contact(self):
        self.account_id = 'toDelete'
        print(f'Deleted contact {self.contact_id}.')

#Some Tests
def run_tests():      
    article1 = Blog_article('an_account_id','someArticleId', 201905151200, 'Some Title', 'Some text from an article', 'An article summary', 'https://thereagain.blog.com', 'wp')
    print(article1.blog_url)
    article1.del_article()
    article1.approve_article()
    article1.unapprove_article()
    product1 = Product('an_account_id', 'someId', 'My Awesome Product')
    print(product1.product_name)
    product1.del_product()
    product1.approve_product()
    product1.unapprove_product()
    b1 = Sp_blog('https://blog.popitup.com','a1')
    print(b1.blog_url)
    print(b1.created)
    b2 = Wp_blog('https://blog.sonlet.com', 'a2')
    print(b2.blog_url)
    print(b2.created)
    b1.get_sp_articles()
    b1.send_newsletter()
    b2.get_wp_articles()
    b2.send_newsletter()
    a1 = Account()
    print(a1.user_ids)
    a1.add_user(10)
    a1.del_user(1)
    a1.del_account()
    n1 = Newsletter('a1','from@email.com', ['email1@example.com', 'email2@example.com', 'email3@example.com'], 'This is the email subject', 'This is all the email content that I can come up with')
    print(n1.to_recipients)
    n1.send_newsletter()
    n1.schedule_newsletter(201905111400)
    n1.del_newsletter()
    t1 = Email_template('a1', 'some html that would represent an email with liquid code included for replacing stuff', 'My First Email Template')
    print(t1.template_name)
    t1.share_template(10)
    t1.unshare_template(1)
    t1.del_email_template()
    c1 = Contact('a1', 'john@example.com','2558')
    print(c1.contact_id)
    c1.contact_id = 'jsjsjsjs'
    print(c1.contact_id)
    c1.unsubscribe_email()
    c1.subscribe_email()
    c1.del_contact()

#run_tests()

