from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=True)


def scrape_info():
    browser = init_browser()

   
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(2)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # find content titles
    soup.find_all(class_="content_title")[1]
    news_title =soup.find_all("div",class_='content_title')[1].get_text().strip()
    news_paragrah=soup.find_all("div", class_='rollover_description_inner')[0].get_text()


#JPL Mars Space Images Scrape
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html=browser.html
    soup = bs(html, 'html.parser')

    # find images
    button=browser.find_by_id('full_image')
    button.click()


    button_image = browser.links.find_by_partial_text('more info')
    button_image.click()

    html=browser.html
    soup = bs(html, 'html.parser')

    image_source= soup.find_all(class_="main_image")[0].get('src')
    image= f"https://www.jpl.nasa.gov/{image_source}"


    #scrape mars table

    mars_df=pd.read_html("https://space-facts.com/mars")[0]
    mars_df.index.names=[None]
    mars_table = mars_df.to_html(index=False, header=False)




   #creating hemispheres' images list
    url1 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url1)
    hemisphere_list = []
        #  list of all of the hemispheres
    links = browser.find_by_css("a.product-item h3")
        # for loop
    for i in range(len(links)):
            hemi_dict = {}
            browser.find_by_css("a.product-item h3")[i].click()
            sample_element = browser.links.find_by_text('Sample').first
            hemi_dict['img_url'] = sample_element['href']
            hemi_dict['title'] = browser.find_by_css("h2.title").text
            hemisphere_list.append(hemi_dict)
            browser.back()

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_paragrah": news_paragrah,
        "image": image,
        "mars_table": mars_table,
        "hemisphere_list": hemisphere_list
        }
    


    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
