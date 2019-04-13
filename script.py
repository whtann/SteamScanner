from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url ='https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38?Tpk=graphics%20cards'

# opening up connection, grabbing the page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# html parsing
page_soup = soup(page_html, "html.parser")

# grabs each product
containers = page_soup.findAll("div",{"class":"item-container"})

for container in containers:
    brand_container = container.findAll("a",{"class":"item-brand"})
    img = brand_container[0].findAll("img",{"class":"lazy-img"})
    brand = img[0].get("title").strip()
    
    title_container = container.findAll("a",{"class":"item-title"})
    product_name = title_container[0].text.strip()

    shipping_container = container.findAll("li",{"class":"price-ship"})
    shipping = shipping_container[0].text.strip()

    print("brand: " + brand)
    print("product_name: " + product_name)
    print("shipping: " + shipping)

