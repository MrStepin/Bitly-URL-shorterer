from dotenv import load_dotenv
import argparse
import requests
import os
from urllib.parse import urlparse
import sys


secret_token = os.getenv("TOKEN")
token = {"Authorization": secret_token }
url = "https://api-ssl.bitly.com/v4/bitlinks"
url_for_sum = "https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary"
period_for_calc_clicks = {"unit":"day", "units":""}

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('urls', nargs='+')
    return parser
    
def create_short_link(url, token, users_link):
    short_link = requests.post(url, json = users_link, headers = token) 
    
    if short_link.status_code == 400:
        return None
    else:  
        response = short_link.json()
        link_bitly = response["link"]
        return link_bitly

def calculating_of_clicks_to_link(url_for_sum, token, users_link): 
    summ_of_clicks = requests.get(url_for_sum.format(users_link["long_url"][7:]), params = period_for_calc_clicks, headers = token) 
    
    if summ_of_clicks.status_code == 404:
        return None
    else:   
        response = summ_of_clicks.json()
        total_clicks = response["total_clicks"]
        return total_clicks

if __name__ == '__main__': 
    load_dotenv()
    users_link = {"long_url": "", "title": "new"}
    entered_links = createParser()
    urls_space = entered_links.parse_args(sys.argv[1:])
    for entered_urls in urls_space.urls:
        users_link.update({"long_url": entered_urls})
        if urlparse(users_link["long_url"]).netloc == "bit.ly":
            total_clicks = calculating_of_clicks_to_link(url_for_sum, token, users_link) 
        
            if total_clicks == None:
                print("Введена некорректная ссылка.")
            else:
                print("Всего кликов: {}".format(total_clicks))
        else:
            link_bitly = create_short_link(url, token, users_link)
        
            if link_bitly == None:
                print("Введена некорректная ссылка.")
            else:
                print("Короткая ссылка: {}".format(link_bitly))
    
    

 
