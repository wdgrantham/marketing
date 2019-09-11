# This Python file uses the following encoding: utf-8

from bs4 import BeautifulSoup
from selenium import webdriver
import json
import datetime
import requests

#shop_url = "https://sonlet.com/shops/march-14/" #usually Sonnie sends this each week
#browse_shortlink = ""

#Gets the product images and titles from the picks shop
def get_picks(shop_url):
  browser = webdriver.Chrome()#Make sure that you have a chromewebdriver installed in the system path
  browser.get(shop_url)
  html = browser.page_source
  soup = BeautifulSoup(html, features="html.parser")
  products = soup.find_all('div', class_="Card--product")
  products_json = []
  for product in products:
    soup = BeautifulSoup(str(product), features="html.parser")
    name = soup.a.div.h6.text
    img = soup.figure.img['src']
    products_json.append({'name': name, 'img': img})
  return json.dumps(products_json)
#print(get_picks('https://sonlet.com/shops/mayberrys-featured/'))


def get_json_payload(json_filename):
  
  with open('json/' + str(json_filename),'r+') as json_file:
    today = datetime.datetime.now().strftime("%y%m%d")
    json_text = json_file.read()
    json_object = eval(json_text)
  
  return json_object
  #print(json_object)
  
#This function is no longer used now that the CIO API triggered campaigns are working
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

#Sends the email and the json object to the CIO API triggered broadcast
def send_event_to_cio(campaign_id, json_filename):
  # ShopTheRoe API credentials
  site_id = '6d30b69c3d9afe45835b'
  api_key = 'd3951fc08db29107a260'
  # ShopTheRoeDEV API Credentials
  #site_id = 'ecd4c1f87a7c225c8b15'
  #api_key = 'de73ab4598fc76b789c8'
  
  # Request data
  # **NOTE** Replace ':id' with your API triggered campaign id in the 'url' string
  auth = (site_id, api_key)
  url = 'https://api.customer.io/v1/api/campaigns/' + str(campaign_id) + '/triggers'
  print(url)
  headers = {'Content-Type': 'application/json'}
  payload = json.dumps(get_json_payload(json_filename))
  #print(payload)
  
  # Send POST request to trigger API triggered campaign
  r = requests.post(url=url, auth=auth, headers=headers, data=payload)

  # Check response status code. 200 is good, everything else is probably not good
  if r.status_code == 200:
      print("Success!")
  else:
      print("Error: {}".format(r.text))
      
# campaign ID for ShopTheRoeDev is 12 & ShopTheRoe is 30 
send_event_to_cio('30', 'april_25.json')
