# Mission-to-Mars
This project involves web-scraping to put together Mars data using Splinter to automate a web browser, BeautifulSoup to parse and extract the data, MongoDB to hold the data gathered, Flask and Python to write the scripts.

## Overview of Project

For this project, a web app has been created to show the latest Mars news, featured image, facts, and the Mars hemispheres. There is a button on the page that will scrape the web for the newest data on Mars. To add the images of Mars' hemispheres, we use BeautifulSoup and Splinter to scrape the full-resolution images of Mars' hemispheres and the titles of those images and store the scraped data on a Mongo database. Finally, we use a web application to display this data and alter the design of the web app to accommodate to the new added images. The last part of this project was to add Bootstrap 3 components to update the web app including making it mobile-responsive and updating the style of the images, facts, and button.

Files used:
- .py (for scraping and app scripts)
- .ipynb (to test the Python code for scraping the data)
- .html (to access the Mongo database and display the data)
