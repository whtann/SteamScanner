from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

filename = "SteamGames.csv"
f = open(filename, "w")

headers = "Name, Price, Date, Reviews\n"

f.write(headers)

my_url = 'https://store.steampowered.com/search/?filter=topsellers&ignore_preferences=1'

# open connection, grab page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

#html parsing
page_soup = soup(page_html, features="lxml")

games = page_soup.findAll("a",{"class":"search_result_row"})

for game in games:
    if game.find("span",{"class":"search_review_summary"}):
        link = game["href"]

        gameClient = uReq(link)
        game_html = gameClient.read()
        gameClient.close()

        print("---------------->" + link)

        game_soup = soup(game_html, features="lxml")

        name = game_soup.find("div",{"class":"apphub_AppName"})
        if name == None:
            continue
        name = name.text

        price = game_soup.find("div",{"class":"discount_original_price"})
        if price == None:
            price = game_soup.find("div",{"class":"game_purchase_price price"})
        price = price.text

        goodData = game_soup.find("div",{"class":"glance_ctn"})
        if goodData == None:
            continue
        reviews = goodData.findAll("span",{"class":"responsive_reviewdesc_short"})

        date = goodData.find("div",{"class":"date"}).text

        rev_string = ""
        for review in reviews:
            rev_string += review.text
        f.write(name + "," + price + "," + date + "," + rev_string + "\n")
        
f.close()