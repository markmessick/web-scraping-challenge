import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    # browser = init_browser()
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    mars_dict = {}

    # Step One:
    browser.visit("https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest")
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find_all('div', class_="content_title")[1].text
    description = soup.find('div', class_="article_teaser_body").text
    mars_dict["news_title"] = title
    mars_dict["news_description"] = description

    # Step Two:
    browser.visit("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")
    browser.find_by_id('full_image').click()
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all('img', class_="fancybox-image")
    link = str(results)
    # link = link.split("src=")[1]
    link = link.split("style")[0]
    link = link.replace('"', "")
    link = link.replace(" ", "")
    featured_image_url = f"https://www.jpl.nasa.gov{link}"
    mars_dict["featured_image"] = featured_image_url

    # Step Three:
    browser.visit("https://twitter.com/marswxreport?lang=en")
    browser.find_by_xpath("/html/body/div/div/div/div[2]/main/div/div/div/div/div/div/div/div/div[2]/section/div/div/div/div[1]/div/div/div/article/div/div[2]/div[2]/div[2]/div[1]/div/span").click()
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    weather = soup.find_all('div', class_='css-901oao r-hkyrab r-1qd0xha r-1blvdjr r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')
    weather = str(weather)
    weather = weather.split("r-ad9z0x r-bcqeeo r-qvutc0")[1]
    weather = weather.split("/span")[0]
    weather = weather.replace('>', '')
    weather = weather.replace('<', '')
    current_mars_weather = weather.replace('"', '')
    mars_dict["mars_weather"] = current_mars_weather

    # Step Four:
    url = "https://space-facts.com/mars/"
    mars_table = pd.read_html(url)
    mars_df = mars_table[0]
    mars_html = mars_df.to_html()
    mars_dict["mars_facts"] = mars_html

    # Step Five:
    hemisphere_list = []
    for i in range(0, 4):
        links = []
        browser.visit("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
        browser.find_by_tag('h3')[i].click()
        browser.find_by_id('wide-image-toggle').click()
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find('h2', class_="title").text
        results = soup.find_all('li')
        for result in results:
            link = result.find('a')['href']
            links.append(link)
        hemisphere_dict = {"Title": title, "img_url": links[0]}
        hemisphere_list.append(hemisphere_dict)
        mars_dict["hemispheres"] = hemisphere_list

        return mars_dict

    