# This Python file uses the following encoding: utf-8

from bs4 import BeautifulSoup
from selenium import webdriver
import json
import datetime
import requests
import re
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

#returns html text without html tags and metadata
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
  
#p = '''<p>One of the features of <a href="https://headwayapp.co/sonlet-updates/sonlet-social-is-here!!!-63134" rel="noopener noreferrer" target="_blank">Sonlet Social</a> is that shoppers' party activity (likes/claims) is pushed to their followers.  This helps generate interest in the party (good for the consultant) and improves discoverability (good for everybody).</p>'''
#print(strip_tags(p))
  
#returns a summary of html article... right now is the first sentence of the paragraph with all the html tags stripped out
def get_summary(html):
  t = strip_tags(html)
  p = re.split('[;.?!]', t)
  return p[0]

#returns a list of images from an html article
def get_images(html):
  images = []
  soup = BeautifulSoup(html, features="html.parser")
  imgs = soup.find_all('img')
  for img in imgs:
    try:
      images.append(img['src'])
    except:
      images.append(img['data-src'])
  return(images)

#converts a datetime stamp (e.g. 2018-12-11T10:08:55 ) into the seconds since epoch
def dt_2_e(date_time):
  k = re.split('[-T:Z]', date_time)
  k = ' '.join(k).split()
  l = [int(x) for x in k]
  s = (datetime.datetime(l[0],l[1],l[2],l[3],l[4]) - datetime.datetime(1970,1,1)).total_seconds()
  return s
#dt_2_e('2019-04-26T20:19:43Z')

#Cleans a string or integer for common user spelling errors in tags
def c_str(a_value):
  s = str(a_value).strip().lower().replace('_','').replace('-','').replace('~','').replace(' ','').replace('/','').replace('|','')
  return s
#print(c_str(' ~n-o e|m/ail_ '))

#checks whether an article is approved for the newsletter by checking tags
def is_approved(list_tags):
  is_approved = True
  nix_tags = ['dontemail','dontsend', 'noemail', 'nonewsletter', 'noannounce', 'nopublish', 'hide']
  for tag in list_tags:
    if c_str(tag) in nix_tags:
      is_approved = False
  return is_approved

#j = ['New feature', 'shipping labels', ' ~d-ont e|m/ail_ ' ]
#print j
#print(is_approved(j))

#Gets the article title, images, text, summary, and date for the articles that have been published on headway
def get_headway(headway_url):
  browser = webdriver.Chrome()#Make sure that you have a chromewebdriver installed in the system path
  browser.get(headway_url)
  html = browser.page_source
  browser.quit()
  soup = BeautifulSoup(html, features="html.parser")
  articles = soup.find_all('div', class_="changelogItem")
  articles_json = []
  #images = []
  for article in articles:
    soup = BeautifulSoup(str(article), features="html.parser")
    date_time = dt_2_e(str(soup.find('time')['datetime']))
    title = soup.h2.text
    link = 'https://headwayapp.co' + str(soup.find('a')['href'])
    article_id = link.split('-')[-1]
    text = soup('p')
    summary = get_summary(str(text[0]))
    images = get_images(str(article))
    articles_json.append({'id': article_id, 'datetime': date_time, 'images': images, 'link': link, 'summary': summary, 'text': str(text), 'title': title, 'type': 'headway-update'})
  #return json.dumps(articles_json, sort_keys=True, indent=2)
  return articles_json
#print(get_headway('https://headwayapp.co/sonlet-updates'))

def get_wp_media(blog_url, media_id):
  url = blog_url + 'wp-json/wp/v2/media/' + str(media_id)
  media = requests.get(url).text
  pm = json.loads(media)
  try:
    image = pm['guid']['rendered']
  except:
    image = ''
  return(image)
#print(get_wp_media('https://blog.sonlet.com/', 260))

#Creates a dictionary of the tags in a wordpress blog
def get_wp_tags(blog_url):
  tags_url = blog_url + '/wp-json/wp/v2/tags'
  tags = json.loads(requests.get(tags_url).text)
  tids = []
  names = []
  for tag in tags:
    tids.append(tag['id'])
    names.append(tag['name'])
  tags_dict = dict(zip(tids, names))
  return tags_dict

def get_articles_dict(articles_json):
  a_ids = []
  a_objects = []
  for article in articles_json:
    a_ids.append(article['id'])
    a_objects.append(article)
  return dict(zip(a_ids, a_objects))

#Gets posts from wordpress API https://developer.wordpress.org/rest-api/reference/posts/#list-posts
def get_wordpress(blog_url):
  posts_url = blog_url + '/wp-json/wp/v2/posts'
  tags_dict = get_wp_tags(blog_url)
  response = requests.get(posts_url)
  headers = response.headers
  total_articles = headers['X-WP-Total']
  total_pages = int(headers['X-WP-TotalPages'])
  articles = []
  articles_json = []
  posts_page = int(0)
  while posts_page < total_pages:
    l = posts_page < total_pages
    nextUrl = posts_url + '?page=' +str(posts_page + 1) + '&per_page=10'
    posts = requests.get(nextUrl).text
    articles.extend(json.loads(posts))
    posts_page += 1

  for article in articles:
    article_tags = []
    for tag in article['tags']: article_tags.append(tags_dict[tag])
    if is_approved(article_tags):
      article_id = article['id']
      date_time = dt_2_e(article['date'].encode('utf-8'))
      title = article['title']['rendered'].encode('utf-8')
      link = article['link'].encode('utf-8')
      text = article['content']['rendered'].encode('utf-8')
      excerpt = strip_tags(article['excerpt']['rendered'].encode('utf-8'))
      summary = get_summary(str(text))
      images = []
      try:
        img = get_wp_media('https://blog.sonlet.com/', article['featured_media'])
        if img != '': images.append(img)
      finally: 
        imgs = get_images(str(article))
        images.extend(imgs)
        articles_json.append({'id': article_id, 'datetime': date_time, 'images': images, 'link': link, 'summary': summary, 'title': title, 'excerpt': excerpt, 'type': 'wp-blog'})
  #return(json.dumps(articles_json, indent=2, sort_keys=True))
  return articles_json
  #return(json.dumps(get_articles_dict(articles_json), indent=2))
#print(get_wordpress('https://blog.sonlet.com'))

#Get posts from squarespace api https://developers.squarespace.com/view-json-data
def get_squarespace(blog_url):
  articles_json = []
  json_url = blog_url + '/?format=json'
  posts = json.loads(requests.get(json_url).text)
  articles = posts['items']
  nextPageUrl = posts['pagination']['nextPageUrl']
  while nextPageUrl:
    nextUrl = blog_url + str(nextPageUrl) + '&format=json'
    posts = json.loads(requests.get(nextUrl).text)
    articles.extend(posts['items'])
    try:
      nextPageUrl = posts['pagination']['nextPageUrl']
    except:
      nextPageUrl = False
  for article in articles:
    article_tags = article['tags']
    if is_approved(article_tags):
      article_id = article['id'][-5:]
      date_time = article['publishOn']
      title = article['title'].encode('utf-8')
      #print title
      link = blog_url.split('?')[0] + str(article['fullUrl'].encode('utf-8'))
      text = article['body'].encode('utf-8')
      summary = get_summary(text)
      excerpt = strip_tags(article['excerpt']).encode('utf-8')
      images = []
      try:
        img = article['assetUrl']
        images.append(img)
      finally:
        imgs = get_images(article['body'].encode('utf-8'))
        images.extend(imgs)
      articles_json.append({'id': article_id, 'datetime': date_time, 'images': images, 'link': link, 'excerpt': excerpt, 'summary': summary, 'title': title, 'type': 'sp-blog'})
  return articles_json
  #return(json.dumps(articles_json, indent=2, sort_keys=True))
#print get_squarespace('https://blog.popitup.com')

def get_payload(articles_json):#To Do: Update this
  root = {}
  data = {}
  root['data'] = data
  data['articles'] = articles_json
  data['articles_count'] = len(articles_json)
  data['article_ids'] = articles_json.keys()
  
  return root
  #print json.dumps(data, indent=2, sort_keys=True)

#Sends the email and the json object to the CIO API triggered broadcast
def send_event_to_cio(site_id, api_key, campaign_id, payload):
  # ShopTheRoe API credentials
  #site_id = '6d30b69c3d9afe45835b'
  #api_key = 'd3951fc08db29107a260'
  # ShopTheRoeDEV API Credentials
  #site_id = 'ecd4c1f87a7c225c8b15'
  #api_key = 'de73ab4598fc76b789c8'
  # PopItUp API credentials
  #site_id = '0dfefb1081f03692b8ce'
  #api_key = '9d368b1ddbe561236ab0'
  
  # Request data
  # **NOTE** Replace ':id' with your API triggered campaign id in the 'url' string
  auth = (site_id, api_key)
  url = 'https://api.customer.io/v1/api/campaigns/' + str(campaign_id) + '/triggers'
  print(url)
  headers = {'Content-Type': 'application/json'}
  payload = json.dumps(payload)
  #print(payload)
  
  # Send POST request to trigger API triggered campaign
  r = requests.post(url=url, auth=auth, headers=headers, data=payload)

  # Check response status code. 200 is good, everything else is probably not good
  if r.status_code == 200:
      print("Success!")
  else:
      print("Error: {}".format(r.text))
      
def send_piu_newsletter():
  a = get_squarespace('https://blog.popitup.com')
  b = get_payload(a)
  #print json.dumps(b, sort_keys=True, indent=2)
  send_event_to_cio('0dfefb1081f03692b8ce', '9d368b1ddbe561236ab0', 9, b)

def send_sonlet_newsletter():
  a = get_wordpress('https://blog.sonlet.com')
  b = get_headway('https://headwayapp.co/sonlet-updates')
  c = a.extend(b)
  d = get_articles_dict(a)
  e = get_payload(d)
  #print json.dumps(e, indent=2)
  send_event_to_cio('6d30b69c3d9afe45835b', 'd3951fc08db29107a260', 31, e)

#get_headway('https://headwayapp.co/sonlet-updates') #complete
#get_wordpress('https://blog.sonlet.com')#complete To Do: Unicode isn't processing correctly in the email subject

#get_squarespace('https://blog.popitup.com/') #complete --> Doesnt currently use a JSON Dictionary, but given that it's more simple, it may not be needed at the moment.

#get_payload() #complete
#send_event_to_cio() #complete
#send_piu_newsletter() #complete
#send_sonlet_newsletter() #complete

