from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import bs4
from fake_useragent import UserAgent
import requests
import lxml

def start_selenium(url, geckodriver=None):
    useragent = UserAgent()
    # Settings of webdriver
    options = webdriver.FirefoxOptions()
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference(f"general.useragent.override", useragent.ie)
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    # options.add_argument('--headless')
    if geckodriver:
        driver = webdriver.Firefox(executable_path=geckodriver, options=options)
    else:
        driver = webdriver.Firefox(options=options)
    driver.get(url)
    try:
        driver.current_url
    except:
        print("The incorrect link")
        exit(0)
    return driver



def pars_urls():

    links = []
    page = 1
    url = lambda \
            page: f"https://suchen.mobile.de/fahrzeuge/search.html?damageUnrepaired=NO_DAMAGE_UNREPAIRED&isSearchRequest=true&pageNumber={page}&ref=srpNextPage&scopeId=C&sortOption.sortBy=searchNetGrossPrice&sortOption.sortOrder=DESCENDING&refId=7222fb65-a5a6-7873-9bb4-98256f4d2682"
    driver = start_selenium(url(page), "geckodriver")

    try:
        soup = bs4.BeautifulSoup(driver.page_source, "lxml")
        pages = int(soup.find("div", class_="cBox-body u-text-center u-margin-top-18").find_all('li')[-2].text)
        car_boxes = soup.find_all("div", class_="cBox-body cBox-body--resultitem")

        for box in car_boxes:
            link = box.find('a', class_="link--muted no--text--decoration result-item").get("href")
            links.append(link)
        time.sleep(5)
        for page in range(2, pages + 1):
            driver.get(url(page))
            print(driver.current_url)
            print(driver.page_source)
            soup = bs4.BeautifulSoup(driver.page_source, "lxml")
            car_boxes = soup.find_all("div", class_="cBox-body cBox-body--resultitem")
            print(car_boxes)
            for box in car_boxes:
                link = box.find('a', class_="link--muted no--text--decoration result-item").get("href")
                links.append(link)

            time.sleep(5)
        print(links)
        print(len(links))
    except:
        pass
        # driver.close()

    # driver.close()


pars_urls()