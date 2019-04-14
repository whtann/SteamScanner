from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url ='https://steamcommunity.com/market/'

# opening up connection, grabbing the page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# html parsing
page_soup = soup(page_html, "html.parser")

# grabs each product
containers = page_soup.findAll("div",{"class":"market_listing_row"})

for container in containers:
    item_container = container.findAll("div",{"class":"market_listing_item_name_block"})    
    item = item_container[0].span.text
    game = item_container[0].find("span", class_ ='market_listing_game_name').text
    
    prices_container = container.findAll("div",{"class":"market_listing_right_cell"})
    price = prices_container[1].span.span.text
    
    print("item: " + item)
    print("Game: " + game)
    print("Price: " + price)

