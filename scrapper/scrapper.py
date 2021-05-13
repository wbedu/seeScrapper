#!env python3
import os
import errno
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor

from requests import get  # to make GET request
PAGE_XPATH="//img[contains(@class,'img-fluid') and contains(@src,'https')]"
NEXT_PAGE="/html/body/nav/div/div[3]/ul[2]/li[3]/a"

def scrape_chapter():
    urls = []
    try:
        pages = WebDriverWait(browser, 15).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, PAGE_XPATH)
            )
        )
        # pagespages = driver.find_elements_by_xpath(PAGE_XPATH)
        urls = [page.get_attribute("src") for page in pages]

    except:
        pass
    return browser.find_elements_by_xpath(NEXT_PAGE), urls


def make_dir(dir):
    try:
        os.makedirs(dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def download(url, dir):
    # open in binary mode
    dest_path = os.path.join(dir,url.split("/")[-1])
    with open(dest_path, "wb") as file:
        # get request
        print(f"Downloading {url}\r")
        response = get(url)
        # write to file
        file.write(response.content)

browser = webdriver.Firefox()

SeriesTitle = "Solo Leveling"
# url_title=SeriesTitle.replace(" ", "%%20")
browser.get(f"https://mangasee123.com/search/?name={SeriesTitle}")
browser.add_cookie({"name" : "FullPage", "value" : "yes"})
Series = browser.find_element_by_class_name('SeriesName')

Series.click()

chapters = browser.find_elements_by_xpath("//a[contains(@class,'ChapterLink')]")

chapters[-1].click()
next_chapter, urls = scrape_chapter()

series_dir= os.path.join(".","data",SeriesTitle)
make_dir(SeriesTitle)

while len(next_chapter) >0:
    chapter_num = urls[0].split("/")[-1].split("-")[0]
    chapter_dir = os.path.join(series_dir, chapter_num)
    make_dir(chapter_dir)

    with ThreadPoolExecutor(max_workers=5) as exe:
        for url in urls:
        exe.submit(download, url, chapter_dir)

    download(url, chapter_dir)
    next_chapter[0].click()
    next_chapter, urls = scrape_chapter()

browser.close()


# if __name__ == __main__ :