# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome',**executable_path,headless=False)


# ## Visit the NASA Mars News Site

url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text',wait_time=1)


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html,'html.parser')
slide_elem = news_soup.select_one('div.list_text')


slide_elem.find('div',class_='content_title')


# Use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div',class_='content_title').get_text()
news_title


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div',class_='article_teaser_body').get_text()
news_p

# ### JPL Space Images Featured Image

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html,'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img',class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# ### Mars Facts

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description','Mars','Earth']
df.set_index('description',inplace=True)
df

df.to_html()

# ## D1: Scrape High-Resolution Mars' Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

html = browser.html
bs = soup(html,'html.parser')

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
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
hemisphere_image_urls

# 5. Quit the browser
browser.quit()
