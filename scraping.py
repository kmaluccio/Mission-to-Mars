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
    hemispheres = hemisphere_data(browser)

    # Run all scraping functions and store results in dictionary
    data = {"news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres,
        # "img_url":[hemispheres[0]['img_url'],hemispheres[1]['img_url'],hemispheres[2]['img_url'], hemispheres[3]['img_url']],
        # "title":[hemispheres[0]['title'],hemispheres[1]['title'],hemispheres[2]['title'],hemispheres[3]['title']],
        "last_modified": dt.datetime.now()}
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
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    html = browser.html
    bs = soup(html,'html.parser')

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # in for loop we should use range(len(bs.find('div',class_='item'))) instead of range(4)
    # but could not fix error
    for i in range(4):
        # Create empty dictionary to store urls and titles for full images
        hemispheres = {}
        # click on hemisphere link
        browser.links.find_by_partial_text('Enhanced')[i].click()
        # navigate to full-resolution image page
        html = browser.html
        bs = soup(html,'html.parser')
        rel_img_path = bs.find('ul').find('li').find('a')['href']
        title = bs.find('div',class_='cover').find('h2').text
        # retrieve the full resolution image URL string and title
        hemispheres['img_url'] = url + rel_img_path
        hemispheres['title'] = title
        #navigate back to beginning to get the next hemisphere image
        browser.back()
        hemisphere_image_urls.append(hemispheres)

    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())