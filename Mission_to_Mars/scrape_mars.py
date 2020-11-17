from splinter import Browser
from bs4 import BeautifulSoup as bs
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

   
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # find content titles
    soup.find_all(class_="content_title")[1]
    news_title =soup.find_all("div",class_='content_title')[1].get_text().strip()
    news_paragrah=soup.find_all("div", class_='rollover_description_inner')[0].get_text()


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
    mars_table = mars_df.to_html()






    # Store data in a dictionary
    # costa_data = {
    #     "sloth_img": sloth_img,
    #     "min_temp": min_temp,
    #     "max_temp": max_temp
    # }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return costa_data
