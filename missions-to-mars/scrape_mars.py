from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

def init_browser():
    executable_path = {"executable path":"/usr/local/bin/chromedriver"}
    return Browser("chrome",executable_path, headless=False)

def scrape():
    mars = {}

    # Scrape Mars News
    browser = init_browser()
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = bs(html,"html.parser")

    mars["news_title"] = soup.find_all("div",class_="content_title")[1].text
    mars["news_p"] = soup.find("div",class_="article_teaser_body").text

    # Scrape Featured Image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    browser.links.find_by_partial_text("FULL IMAGE").click()
    time.sleep(2)
    html = browser.html
    soup = bs(html,"html.parser")

    mars["featured_image_url"] = "https://www.jpl.nasa.gov" + soup.find("img",class_="fancybox-image")["src"]

    # Scrape Mars Facts Table 
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    mars_facts_df = tables[0]
    table = mars_facts_df.to_html()
    
    mars["table"] = table


    # Scrape Hemispheres
    clicks = ["Cerberus Hemisphere Enhanced","Schiaparelli Hemisphere Enhanced","Syrtis Major Hemisphere Enhanced",
         "Valles Marineris Hemisphere Enhanced"]
    hemispheres = []

    for click in clicks:
        hemisphere = {}
        
        url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(url)
        time.sleep(1)
        
        browser.links.find_by_partial_text(click).click()
        html = browser.html
        
        soup = bs(html,"html.parser")
        hemisphere["title"] = soup.find("h2",class_="title").text
        hemisphere["img_url"] = "https://astrogeology.usgs.gov" + soup.find("img",class_="wide-image")["src"]
        hemispheres.append(hemisphere)

    mars["hemispheres"] = hemispheres
    
    browser.quit()
    return mars