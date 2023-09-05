from urllib import parse
from enum import Enum
import decorators


class ElementFilterer():
  def __init__(
      self, 
      item_class_name: str, 
      item_title_class_name: str, 
  ):
    self.item_class_name = item_class_name
    self.item_title_class_name = item_title_class_name

    
  

class Website(Enum):
  ETSY="Etsy"
  ALIEXPRESS="AliExpress"

  """
  Etsy
  """

  @property
  @decorators.bind('ETSY')
  def element_filterer(self):
    return ElementFilterer(
      item_class_name="v2-listing-card",
      item_title_class_name="v2-listing-card__title",
    )

  @decorators.bind('ETSY')
  def get_search_url(self, query):
    search_arg = parse.quote(query)

    url = "https://www.etsy.com/search?q="+search_arg+"&ref=pagination&page={page_number}"
    return url
  

  """
  AliExpress
  """

  @property
  @decorators.bind('ALIEXPRESS')
  def element_filterer(self):
    return ElementFilterer(
      item_class_name="",
      item_title_class_name="",
    )

  @decorators.bind('ALIEXPRESS')
  def get_search_url(self, query):
    search_arg = query.replace(" ", "-")

    url = "https://www.aliexpress.com/w/wholesale-"+search_arg+".html?page={page_number}"
    return url
  
