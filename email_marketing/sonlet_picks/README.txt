DIRECTIONS FOR SENDING SONLET'S PICKS EMAIL
===========================================
1. Create a shop with the week's Sonlet's Picks
2. Create .JSON File with the information for the email
2a. Use the get_picks function in send_picks_email.py to grab the products quickly
3. Send the API triggered broadcast to Customer io using the send_event_to_cio(campaign_id, json_filename) function in send_picks_email.py
4. Send drafts in Customer.IO at https://fly.customer.io/env/65348/campaigns/30/overview


PYTHON SCRIPT
=============
The python script contains several basic functions to reduce manual and repetive effort required to send the Sonlet's Picks weekly emails.  It's intended to be used by a marketer (nothing super complicated here). There are really only three functions:

Function 1: get_picks(shop_url)
This function takes a Sonlet Shop url and returns the product images and urls to be used for the Sonlet Picks email. Usually just run this function and then paste the products object into the .json file.

Function 2: get_json_payload(json_filename)
This function massages the .json file so it can be sent to customer.io correctly.  It's really only needed because the .json file is meant to be coded by hand.

Function 3: send_event_to_cio(campaign_id, json_filename)
This function sends the JSON object to Customer.IO as an API triggered broadcast. 


HTML TEMPLATE
=============
The html file is the template used in the API triggered broadcast for the Sonlet's Picks API Triggered Broadcast set upon Customer.IO. It is HTML mixed with liquid code that allows the JSON object to populate the template. The liquid code contains some defaults so that the template can be populated by more or few items from attributes in teh JSON file.


JSON OBJECT
===========

The python script contains a function called 'send_event_to_cio(campaign_id, json_filename)'takes a JSON object from .json file in the JSON directory and sends it to Customer.io as an API triggered broadcast.

This is a sample JSON Object. The JSON object contains several data attributes that are used to modify the content (not the design) of the email.  Reference this sample object and note that each object indicates in the comment next to it whether it is a Required or Optional attribute.  The email template file template_shops_email.html is written to include default attributes such that the only required attibutes are the 'products' and 'browse_shortlink' attributes.

NOTE: If you copy and paste this sample object, then make sure to remove the comments. JSON objects don't handle comments very well.

```
{'data': {
  "subject":"", //OPTIONAL. Default: This week's Sonlet's picks
  "hero_img":"https://wyattgrantham.com/marketing/Images/190314_ss_hero_2.png", //OPTIONAL. Default image:  'https://wyattgrantham.com/marketing/Images/ss_hero_2_nd.png'
  "ltr_date":"April 12", //Optional. Default does not include an LTR date section
  "browse_shortlink":"https://sonlet.com/shops/b/T5zksuFf/", //Required.  TODO: Add a default link to  the browse page (Once the it supporst a better browse experience)
  "name_promo":"Buy or Sell one and Get one FREE",//Optional. Default: 'Open an online boutique'
  "promo_html":'Use our \"<i>Sell</i> One Get One\" promo to offer your shoppers a prize for free!<br><br>We want to help you promote your Sonlet Shop boutique! When your account logs any sale between now and March 21st, you\'re eligible for a free item to give away. (We\'ll immediately email you when you get a sale.)  Your free item can be anything of equal or lesser value to the highest priced item purchased. <i>Pro tip:</i> giveaway contests cannot require a purchase to enter, but purchasing can increase the odds of winning. Need help deciding on a great promo...? Have questions...? <a href=\"mailto:support@sonlet.com?subject=Run%20a%20shops%20promo&body=Can%20you%20please%20help%20me%20run%20a%20giveaway%20contest%3f\">Talk to our team!</a>',//Optional. Default: 'Earn up to 35% commissions.  NO tracking inventory, NO tracking orders, NO invoicing, NO shipping... Sonlet collects and distributes payment and suppliers dropship directly to your customers!'
  "img_training":"https://wyattgrantham.com/marketing/Images/ss_training.png",//Optional. Default: 'https://wyattgrantham.com/marketing/Images/ss_training.png'
  "training_url":"https://support.sonlet.com/support/solutions/articles/16000089177-how-to-shop-on-a-sonlet-shop-",//Optional. Default: 
  "img_training_video":"https://wyattgrantham.com/marketing/Images/how_to_ss.png",//Optional. Default: "https://wyattgrantham.com/marketing/Images/how_to_ss.png"
  "name_training_video":"HOW TO SHOP ON A SONLET SHOP",//Optional. Default: 'HOW TO SETUP SONLET SHOPS (6:29)'
  "products": [
    {"name": "3751 Natasha Bombshell Dress", "img": "https://cdn.shopify.com/s/files/1/0015/8534/8681/products/IMG_6338_400x.jpg?v=1542066516"}, 
    {"name": "Navy Short Sleeve Button Down Midi Dress", "img": "https://cdn.shopify.com/s/files/1/0015/8534/8681/products/maitaiwholesale-preorder-navy-short-sleeve-button-down-midi-dress-4293062983746_400x.jpg?v=1544479983"}, 
    {"name": "Plum Floral Surplice Wrap Dress Plus Size", "img": "https://cdn.shopify.com/s/files/1/0015/8534/8681/products/maitaiwholesale-plus-dresses-plum-floral-surplice-wrap-dress-plus-size-4127179472962_400x.jpg?v=1544480035"}, 
    {"name": "Dusty Rose Ruffle High Low Lace Maxi Dress", "img": "https://cdn.shopify.com/s/files/1/0015/8534/8681/products/maitaiwholesale-dresses-blush-ruffle-high-low-lace-maxi-dress-25086771277_400x.jpg?v=1544479501"}, 
    {"name": "Pine Linen Blend Kimono Sleeve Wrap Midi Dress", "img": "https://cdn.shopify.com/s/files/1/0015/8534/8681/products/maitaiwholesale-dresses-pine-linen-blend-kimono-sleeve-wrap-midi-dress-4112613146690_400x.jpg?v=1544480019"}, 
    {"name": "Navy Floral Ruffle Midi Wrap Dress", "img": "https://cdn.shopify.com/s/files/1/0015/8534/8681/products/maitaiwholesale-preorder-navy-floral-ruffle-midi-wrap-dress-3602468143170_1024x1024_227edbe9-5d1f-4f25-b6a0-b78a93a8ed44_400x.jpg?v=1544479964"}],//REQUIRED
}}
```