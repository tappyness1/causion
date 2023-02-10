import requests 
from bs4 import BeautifulSoup as bs 
from src.util import open_yaml_file

def process_text(text):
    text = text.replace("(", "")
    text = text.replace(")", "")
    text = text.replace(" ", "_")
    return text

def get_data():

    #open cfg file
    cfg_obj = open_yaml_file(fname = "config/config.yml")
    print (cfg_obj['data_source'])
    
    # request data source website
    r = requests.get(cfg_obj['data_source']) 

    # convert to beautiful soup 
    soup = bs(r.content)

    # cards is the class of the div that stores the image url
    cards = soup.find_all("div", class_= "card")

    # for each card in cards, extract the img link
    # download the image using the img link 
    # process the text of the img text to be used as the img file name
    for card in cards:
        img_link = card.find("img").get("src")
        img_url =  f"http:{img_link}"
        text = process_text(card.find("img").get("alt"))
        img_data = requests.get(img_url).content 
        with open(f'data/{text}.jpg', 'wb') as handler: 
            handler.write(img_data) 

if __name__=='__main__':
    get_data()