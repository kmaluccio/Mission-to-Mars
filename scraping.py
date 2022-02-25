# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome',**executable_path,headless=True)

    news_title, news_paragraph = mars_news(browser)
    hemisphere_urls_titles = hemisphere_data(browser)

    # Run all scraping functions and store results in dictionary
    data = {"news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "image url":hemisphere_urls_titles[0]['image url'], "image title": hemisphere_urls_titles[0]['title'],
        "image url":hemisphere_urls_titles[1]['image url'], "image title": hemisphere_urls_titles[1]['title'],
        "image url":hemisphere_urls_titles[2]['image url'], "image title": hemisphere_urls_titles[2]['title'],
        "image url":hemisphere_urls_titles[3]['image url'], "image title": hemisphere_urls_titles[3]['title']}
    
    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text',wait_time=1)

    # Convert browser text to a soup object
    html = browser.html
    news_soup = soup(html,'html.parser')
    
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div',class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div',class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html,'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img',class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use read_html to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set the index of the dataframe
    df.columns=['Description','Mars','Earth']
    df.set_index('Description',inplace=True)

    # Convert dataframe into HTML format and return
    return df.to_html(classes="table table-striped")

def hemisphere_data(browser):
    # 1. Visit url using browser
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    
    html = browser.html
    bs = soup(html,'html.parser')

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for i in range(4):
        rel_img_path = bs.find_all('img',class_='thumb')[i]['src']
        rel_img_title = bs.find_all('img')[i]['alt']
        image_dict = {'image url':url+rel_img_path,'title':rel_img_title}
        hemisphere_image_urls.append(image_dict)

    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())