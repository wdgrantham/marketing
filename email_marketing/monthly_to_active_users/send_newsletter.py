# This Python file uses the following encoding: utf-8
# This Python file must use Python 3.XXX to process unicode.  Tested in Python 3.7.3

from bs4 import BeautifulSoup
from selenium import webdriver
import json
import datetime
import requests
import re
from html.parser import HTMLParser
import operator
from operator import itemgetter
import random
import html.entities
from jinja2 import Environment, PackageLoader, select_autoescape
import sys
from write_emails import send_email
from premailer import transform

sys.dont_write_bytecode = True

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
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
    #print('Stripped html: ', t, 'List of summary objects: ', p)
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
        print('id: ' , article_id, ' title: ', title)
        text = soup('p')
        summary = get_summary(str(text).replace('[', '').replace(']', '').replace('>,', '>')).strip()
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

# Removes HTML or XML character references and entities from a text string.
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return chr(int(text[3:-1], 16))
                else:
                    return chr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)
#print(unescape('Women&#8217;s Pockets are Inferior. &#8211; An article from pudding.cool'))

#Gets posts from wordpress API https://developer.wordpress.org/rest-api/reference/posts/#list-posts
def get_wordpress(blog_url):
    posts_url = blog_url + '/wp-json/wp/v2/posts'
    tags_dict = get_wp_tags(blog_url)
    response = requests.get(posts_url)
    headers = response.headers
    total_articles = headers['X-WP-Total']
    #print('Total articles: ' + str(total_articles))
    total_pages = int(headers['X-WP-TotalPages'])
    #print('Total pages: ' + str(total_pages))
    articles = []
    articles_json = []
    posts_page = int(0)
    while posts_page < total_pages:
        l = posts_page < total_pages
        nextUrl = posts_url + '?page=' +str(posts_page + 1) + '&per_page=10'
        posts = requests.get(nextUrl).text
        articles.extend(json.loads(posts))
        posts_page += 1
    print(len(articles))
    for article in articles:
        article_tags = []
        for tag in article['tags']: article_tags.append(tags_dict[tag])
        #print(article['title']['rendered'])
        #print(article_tags)
        if is_approved(article_tags):
            article_id = article['id']
            date_time = dt_2_e(article['date'])#.encode('utf-8'))
            title = unescape(article['title']['rendered'])
            print('id: ' , article_id, ' title: ', title)
            link = article['link']#.encode('utf-8')
            text = article['content']['rendered']#.encode('utf-8')
            excerpt = strip_tags(article['excerpt']['rendered'])#.encode('utf-8'))
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
    return(articles_json)
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
            date_time = article['publishOn']/1000
            title = unescape(article['title'])
            print(title)
            link = blog_url.split('?')[0] + str(article['fullUrl'])
            text = article['body']
            summary = get_summary(text)
            excerpt = strip_tags(article['excerpt'])
            images = []
            try:
                img = article['assetUrl']
                images.append(img)
            finally:
                imgs = get_images(article['body'])
                images.extend(imgs)
            articles_json.append({'id': article_id, 'datetime': date_time, 'images': images, 'link': link, 'excerpt': excerpt, 'summary': summary, 'title': title, 'type': 'sp-blog'})
    return articles_json
    #return(json.dumps(articles_json, indent=2, sort_keys=True))
#print get_squarespace('https://blog.popitup.com')

def get_featured_article(platform):
    if platform == 'piu':
        featured_title = 'Rename and delete attribues and their values' #'All the things you need to know about PopItUp'
        featured_text = 'The much awaited attribute editor is finished!  You can now rename and delete attributes and their values from the settings attributes page!'
        featured_image = 'https://wyattgrantham.com/marketing/Images/attribute_editor.png'
        featured_subject = None #'All the things you need to know about PopItUp'
        featured_link = 'https://support.popitup.com/support/solutions/articles/16000096818-how-to-delete-or-rename-attributes-and-their-values'
        featured_ids = None #'ffaa5,fe8d5,f3d66'
    if platform == 'str':
        featured_title = 'The Sonlet Retailer App is Here!' #'All the things you need to know about PopItUp'
        featured_text = 'We\'re so excited to announce the new Sonlet Retailer apps is now available for your iPhone or Android device. Download it today.' #'The much awaited attribute editor is finished!  You can now rename and delete attributes and their values from the settings attributes page!'
        featured_image = None #'https://wyattgrantham.com/marketing/Images/attribute_editor.png'
        featured_subject = 'The Sonlet Retailer App is Here!' #'All the things you need to know about PopItUp'
        featured_link = 'https://apps.apple.com/us/app/sonlet-retailer/id1530627124'
        featured_ids = None #'113977,115364,113979,115357,113983,114782,217,122' #'ffaa5,fe8d5,f3d66'
    
    featured_article = {
      'title': featured_title,
      'text': featured_text,
      'image': featured_image,
      'subject': featured_subject,
      'link': featured_link,
      'featured_ids': featured_ids
    }
    
    if not any(featured_article.values()):
        return None
    else:
        return featured_article

#print(get_featured_article())

# This sorts the article IDs in date order as follows: 
# 1: ascending order --> oldest article to newest article
# 2: descending order --> newest article to oldest article
# 3: random order --> shuffles the articles in random date order
# The default setting is 2 (descending order)
def sort_article_ids(articles_json, sort_type=2):
    tuples_to_sort = []
    for article in articles_json:
        tuples_to_sort.append((article, articles_json[article]['datetime']))
    sorted_ids = []
    if sort_type == 1: #ascending order
        sorted_tuples = sorted(tuples_to_sort, key=itemgetter(1))
        for i in sorted_tuples: sorted_ids.append(i[0])
    if sort_type == 2: #descending order
        sorted_tuples = sorted(tuples_to_sort, key=itemgetter(1), reverse=True)
        for i in sorted_tuples: sorted_ids.append(i[0])
    if sort_type == 3: #random order
        sorted_ids = random.sample(articles_json, len(articles_json))

    return(sorted_ids)
#print(sort_article_ids(['99176', 755, '87686', '87666', 742, 737, '87693', 718, 716, '79726', 701, 650, 612, '73090', 684, 595, 682, '70114', '69978', '69622', '63441', 585, 543, 533, 509, 505, 501, 492, 487, 475, 471, 462, 422, 397, 384, 355, 348, 337, 311, 301, 287, 260, 240, 230, 217, 211, 200, 187, 176, 164, 135, 131, 122, 111, 95, 89],1))

def get_payload(articles_json, platform, sort_type=2):
    root = {}
    data = {}
    root['data'] = data
    data['featured_article'] = get_featured_article(platform)
    data['articles'] = articles_json
    data['articles_count'] = len(articles_json)
    data['article_ids'] = sort_article_ids(articles_json, sort_type)
    
    #print(json.dumps(data, indent=2, sort_keys=True))
    return(root)

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
    b = get_articles_dict(a)
    c = get_payload(b,'piu',2)
    #print(json.dumps(c, sort_keys=True, indent=2))
    send_event_to_cio('0dfefb1081f03692b8ce', '9d368b1ddbe561236ab0', 9, c)

def send_sonlet_newsletter():
    a = get_wordpress('https://blog.sonlet.com')
    b = get_headway('https://headwayapp.co/sonlet-updates')
    c = a.extend(b)
    d = get_articles_dict(a)
    e = get_payload(d,'str',2)
    #print(json.dumps(e, indent=2))
    send_event_to_cio('6d30b69c3d9afe45835b', 'd3951fc08db29107a260', 31, e)
    
def filter_articles(articles_dict, last_newsletter_date=None):
    filtered_articles = {}
    #print articles_dict
    for article in articles_dict:
        #print(f'{datetime} >= {last_newsletter_date} => {datetime >= last_newsletter_date}')
        if articles_dict[article]['datetime'] >= last_newsletter_date:
            filtered_articles.update({article: articles_dict[article]})
    #print(json.dumps(filtered_articles, indent=2, sort_keys=True))
    return filtered_articles

#def write_html_email(template_filename, payload):
    #print(articles_dict['108491'])
    
    #print articles
    #env = Environment(
    #    loader=PackageLoader('send_newsletter', 'templates'),
    #    autoescape=select_autoescape(['html', 'xml'])
    #)
    #template = env.get_template(template_filename)
    #email = template.render(articles=articles)
    #print(email)
    
    
def create_sonlet_preview(last_newsletter_date):
    a = get_wordpress('https://blog.sonlet.com')
    b = get_headway('https://headwayapp.co/sonlet-updates')
    c = a.extend(b)
    d = get_articles_dict(a)
    e = get_payload(d,'str',2)
    featured_article = e['data']['featured_article']
    articles = filter_articles(e['data']['articles'],last_newsletter_date)
    wp_articles = []
    hw_articles = []
    if featured_article['featured_ids']:
        featured_article_ids = featured_article['featured_ids'].split(',')
        print('There are featured_article_ids: ', featured_article_ids)
        for a_id in e['data']['article_ids']:
            try:
                if str(a_id) in featured_article_ids:
                    if e['data']['articles'][a_id]['type'] == 'wp-blog':
                        wp_articles.append(e['data']['articles'][a_id])
                        print(f'Article {a_id} is featured from headway')
                    else:
                        hw_articles.append(e['data']['articles'][a_id])
                        print(f'Article {a_id} is featured from the blog')
            except:
                pass
        print_hw_articles = hw_articles
        print_wp_articles = wp_articles
    else:
        for a_id in e['data']['article_ids']:
            try:
                if articles[a_id]:
                    if articles[a_id]['type'] == 'wp-blog':
                        wp_articles.append(articles[a_id])
                    else:
                        hw_articles.append(articles[a_id])
            except:
                pass
        print_hw_articles = hw_articles[:3]
        print_wp_articles = wp_articles[:3]
    print('hw_articles: ', json.dumps(hw_articles, indent=2), 'wp_articles: ', json.dumps(wp_articles, indent=2))
    env = Environment(
        loader=PackageLoader('write_emails', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template_sonlet_newsletter.html')
    email_html = transform(template.render(wp_articles=print_wp_articles, hw_articles=print_hw_articles, featured_article=featured_article)).replace('\n', ' ').replace('\r', '')
    #print(email_html)
    subject = "Test: " + featured_article['title'] if featured_article else hw_articles[0]['title']
    send_email(['wdgrantham@yahoo.com', 'elderwdg@hotmail.com', 'wyatt@directangular.com'], subject, [email_html])
    
def create_piu_preview(last_newsletter_date):
    a = get_squarespace('https://blog.popitup.com')
    b = get_articles_dict(a)
    c = get_payload(b,'piu',2)
    #print(json.dumps(c, sort_keys=True, indent=2))
    featured_article = c['data']['featured_article']
    articles = list(filter_articles(c['data']['articles'],last_newsletter_date).values())
    #print(list(articles.keys())[:3])
    #for article in articles: 
    #    print(articles[article]['title'])
    #print(articles)
    #print(articles[0]['title'])
    env = Environment(
        loader=PackageLoader('write_emails', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template_piu_newsletter.html')
    email_html = transform(template.render(articles=articles, featured_article=featured_article)).replace('\n', ' ').replace('\r', '')
    #print(email_html)
    subject = "Test: " + featured_article['title'] if featured_article else "Test: " + articles[0]['title']
    #print(subject)
    send_email(['wdgrantham@yahoo.com', 'elderwdg@hotmail.com', 'wyatt@directangular.com'], subject, [email_html])
    
#send_email('wdgrantham@yahoo.com', 'Test from python send newsletter script', '<p>Here is some sample html for the html version.</p><img src="https://via.placeholder.com/100x100.png">', 'Here is some sample text for the text email version')


#get_headway('https://headwayapp.co/sonlet-updates') #complete
#get_wordpress('https://blog.sonlet.com')#complete
#get_squarespace('https://blog.popitup.com/') #complete --> Doesnt currently use a JSON Dictionary, but given that it's more simple, it may not be needed at the moment.
#get_payload() #complete
#send_event_to_cio() #complete
#create_sonlet_preview(1564470000) #1548057600
#create_piu_preview(1561100400)
#send_piu_newsletter() #complete Recipients: Have a subscription OR Have an active free trial
send_sonlet_newsletter() #complete Recipients: Have an active subscription OR Have an active free trial
