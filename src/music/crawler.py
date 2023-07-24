import requests
from bs4 import BeautifulSoup

def get_soup(date='2020-10-20'):
  """Retrieves the soup from https://www.billboard.com/charts/hot-100/ on the date passed
  """
  url = 'https://www.billboard.com/charts/hot-100/'
  response = requests.get(url+date)
  # print(response.content)
  return BeautifulSoup(response.content, "html.parser")
  # print(soup.title)

if __name__ == '__main__':
  date = '2005-05-13'
  print(get_soup(date))