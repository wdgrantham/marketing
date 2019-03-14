#from bs4 import BeautifulSoup
#from selenium import webdriver
import json
import datetime

#shop_url = "https://sonlet.com/shops/march-14/" #usually Sonnie sends this each week
#browse_shortlink = ""

#To Do: get the products from the picks shop
def get_picks(shop_url):
  browser = webdriver.Chrome()#busted right here
  browser.get(shop_url)
  html = browser.page_source
  soup = BeautifulSoup(html,'lxml')
  a = soup.findAll('section')
  #result will be to grab the 6 product titles and their
  #respective images and add them to the dictionary or the
  #json file or both
  return html
#print(get_picks('https://sonlet.com/shops/march-14/'))

#To Do: Generate the image for the email
#The work around to doing this is changinng the design of
#the email to use a non-brand text for the LTR Date in the
#hero image and using the highlight and underline as a
#background image that can stay stable for both the images
def create_images(ltr_date,name_promo)
  hero_image = something
  img_promo = somethingElse
  

def write_email(json_filename):
  #read in the html template for sonlet shops that contains liquid
  #statements to be replaced in this weeks email
  with open('template_shops_email.html','r') as html_template:
    html = html_template.read()
  #print(html)

  #read in the json file as a python dictionary to be used 
  #to replace liquid statements in the html template
  with open('json/' + str(json_filename),'r') as json_file:
    json_text = json_file.read()
    json_replacements = eval(json_text)
  #print(json_replacements)

  #replace all the liquid statements in the htlm file with
  #the values from the json file
  for aKey, aValue in json_replacements.items():
    aKey = aKey.replace(aKey.lower(),'{{'+str(aKey)+'}}')#adds the {{}} syntax to the keys so that the html template can read like liquid
    html = html.replace(aKey.lower(), aValue) #replaces the liquid statements (json keys) with the proper values (json values)
  #print(html)

  #write the new sonlet picks email
  today = datetime.datetime.now().strftime("%y%m%d")
  #print(today)
  with open('emails/' + str(today) +'picks_email.html','w') as sonlet_picks_email:
    sonlet_picks_email.write(html)
    
  print("Sonlet Picks Email was written successfully")
  
#write_email('march_14.json')

#To Do: Send the email and the json object to the CIO API triggered
#email campaign
