import asyncio
from typing import Tuple
import files.decorators as decorators
import functools
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from urllib.request import urlopen
import asyncio
import time
from websites import ElementFilterer, Etsy, AliExpress
from urllib import parse
import logging

# init logging
logging.basicConfig(level=logging.NOTSET)


def create_driver(headless: bool = True):
  # Get Service
  firefox_service = webdriver.FirefoxService(executable_path="./geckodriver")

  # Set Prefs
  options = webdriver.FirefoxOptions()

  if headless: options.add_argument("-headless")
  options.set_preference('intl.accept_languages', 'en-US')

  # Create Driver
  driver = webdriver.Firefox(options=options, service=firefox_service)
  return driver

class Scraper:
  def __init__(
      self,
      url: str,
      max_pages: int,
      element_filterer: ElementFilterer,
  ):

    self.driver = create_driver()     # Create Driver

    self.url = url
    self.max_pages = max_pages

    self.element_filterer = element_filterer
    self.items_found: list[Tuple(str, str)] = [] #Tuple(Title, Image)

  def scroll_to_bottom(self, delay: float):
    doc_height = self.driver.execute_script("return document.body.scrollHeight")
    win_height = self.driver.execute_script("return window.innerHeight")
    num_pages = int(doc_height / win_height)
    print(f'doc height=>{doc_height}\tpages =>{num_pages}')
    # scroll through the document

    for page in range(num_pages):
      self.driver.execute_script("window.scrollTo(0, arguments[0]);", win_height * (page+1))
      print(f'scrolling to=>{win_height * (page+1)}')
      time.sleep(delay)

  def scrape_page(self, page_number):
    params = {"page_number": page_number}
    url_formatted = self.url.format(**params)

    self.driver.get(url_formatted)

    self.scroll_to_bottom(0.1)

    items = self.driver.find_elements(By.CLASS_NAME, self.element_filterer.item_class_name)
    if len(items) < 1: raise exceptions.NoSuchElementException # raise error if no elements have been found

    for item in items:
      title = item.find_element(By.CLASS_NAME, self.element_filterer.item_class_name).text
      image = item.find_element(By.TAG_NAME, 'img').get_attribute('src')

      self.items_found.append((title, image))
    
  def run(self):
    for page_number in self.max_pages:
      try:
        self.scrape_page(page_number)
      except exceptions.NoSuchElementException:
        break
    
    logging.info(f"Total # of Items Found: {len(self.items_found)}")

  def end(self) -> list[Tuple(str, str)]:
    self.driver.quit()
    return self.items_found


def scraper(item_name):
  # Prep url:
  pass



