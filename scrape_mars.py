import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time


def init_browser():
    executable_path = {'executable_path': '/Applications/chromedriver'}
    return Browser("chrome", executable_path)
    #^^ it doesn't seem to like this line? I don't really know what's wrong 

def scrape():
    browser = init_browser()
    
    browser.visit('https://mars.nasa.gov/news/')
    time.sleep(5)
    html=browser.html
    soup=bs(html, 'html.parser')

    article=soup.find("div", class_='list_text')
    title=article.find("div", class_="content_title")

    news_title=title.find("a").text
    news_body=article.find("div", class_ ="article_teaser_body").text


        
    url_image='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_image)
    time.sleep(5)
    html_image=browser.html
    soup_image=bs(html_image, 'html.parser')

    containers=soup_image.find_all("div",class_="img")
    for container in containers:
        img=container.find('img')["src"]
        img2=img.split('/')[4]
        img3=img2.split('-')[0]
    #splice together image url
    featured_image_url='https://www.jpl.nasa.gov/spaceimages/images/largesize/' + img3 +'_hires.jpg'




    # URL of page to be scraped
    url_tweet='https://twitter.com/marswxreport'
    browser.visit(url_tweet)
    time.sleep(5)
    html_tweet=browser.html
    soup_tweet=bs(html_tweet, 'html.parser')

    # Find weather info tweets
    tweet_container=soup_tweet.find_all('span',class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')
    for tweet in tweet_container: 
        mars_weather=tweet.text
        print(mars_weather)
        #this seems to fetch all of the text on the page, EXCEPT the tweet content body, despite my class being the most
        #specific container for the tweet text. Not sure what is wrong here. Tried a few different classes with no result 
        #normally if we captured the correct weather text, could use some logic to pick it out of all the results




    #mars facts 
    url_facts='https://space-facts.com/mars/'
    tables=pd.read_html(url_facts)
    profile=pd.DataFrame(tables[0])
    profile=profile.rename(columns={0:"Facts", 1:"Results"}).set_index('Facts')
    #profile #df object
    html_profile=profile.to_html()





        
    url_hem='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hem)
    time.sleep(1)
    hem=browser.html
    soup_hem=bs(hem, 'html.parser')
    #declare list to store our jawns 
    image_urls=[]
    results=soup_hem.find_all('div', class_='item')
    #store results in dict. title, img_url ::  
    for result in results:
        description=result.find('div', class_='description')
        title_text=description.find('a')
        imgName=title_text['href'].split('/')[5]
        #splice together url
        img_link='http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/' + imgName + '.tif/full.jpg'
        title=title_text.find('h3').text
        dict={'Title': title, 'img_url': img_link}
        image_urls.append(dict)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #summary table 
    data = {"news_title": news_title,
        "news_body": news_body,
        "featured_image_url":featured_image_url,
        "mars_weather":mars_weather,
        "html_table": html_profile,
        }
    browser.quit()
    return data