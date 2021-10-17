import time
from selenium import webdriver
from selenium.webdriver.common import service
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import xlsxwriter

edge_options = Options()
edge_service = Service("C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe")
edge_options.add_argument("headless")
driver = webdriver.Edge(service=edge_service)
driver.get("https://store.steampowered.com/search/?sort_by=_ASC&ignore_preferences=1&filter=topsellers")
time.sleep(2)
scroll_pause_time = 1
screen_height = driver.execute_script("return window.screen.height;")
i = 1

workbook = xlsxwriter.Workbook('SteamGames.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold':True})

worksheet.write('A1', 'Name', bold)
worksheet.write('B1', 'Price', bold)
worksheet.write('C1', 'Release Date', bold)
worksheet.write('D1', 'Publisher', bold)
worksheet.write('E1', 'Developer', bold)
worksheet.write('F1', '% Positive Reviews (30 days)', bold)
worksheet.write('G1', 'Total Number Reviews (30 days)', bold)
worksheet.write('H1', '% Positive Reviews (All Time)', bold)
worksheet.write('I1', 'Total Number Reviews (All Time)', bold)
worksheet.write('J1', 'Genere(s)', bold)
worksheet.write('K1', 'Storage Capacity', bold)
worksheet.write('L1', 'Mac?', bold)
worksheet.write('M1', 'Windows?', bold)
worksheet.write('N1', 'Steam OS + Linux?', bold)

while True:
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)
    if screen_height * i > 600000:
        break

names = {
    'Valve Index VR Kit':1,
    'Valve Index® Controllers':1,
    'Valve Index Headset + Controllers':1,
    'Oops, sorry!':1,
    'Face Gasket for Valve Index Headset – 2 Pack':1
}

soup = BeautifulSoup(driver.page_source, features="lxml")
row = 1
col = 0
for game in soup.find_all("a",{"class":"search_result_row"}):
    driver.get(game["href"])
    if (row == 1):
        time.sleep(20)
    else:
        time.sleep(1)
    gsoup = BeautifulSoup(driver.page_source, features="lxml")

    name = gsoup.find("div",{"class":"apphub_AppName"})
    if (not name):
        name = gsoup.find("h2",{"class":"pageheader"})
    if (name):
        name = name.text
    else:
        name = None
    
    if (name):
        if (name in names):
            continue
        else:
            names[name] = 1
    
    if not name:
        continue

    dlc = gsoup.find("div",{"class":"game_area_bubble game_area_dlc_bubble"})

    if dlc:
        continue

    #price
    price = gsoup.find("div",{"class":"discount_original_price"})
    if not price:
        price = gsoup.find("div",{"class":"game_purchase_price price"})
    if not price:
        price = gsoup.find("div",{"class":"discount_final_price"})
    if not price:
        price = gsoup.find("div",{"class":"your_price_label"})
        if price:
            price = price.find_next_sibling()

    if price:
        price = price.text
    else:
        price = "N/A"

    #date
    date = gsoup.find("div",{"class":"date"})
    if not date:
        date = gsoup.find("b",text="Release Date:")
        if date:
            date = date.next_sibling

    if date:
        date = date.text
    else:
        date = "N/A"

    #developers & publishers
    devs = gsoup.find("div",{"class":"dev_row"})
    if (not devs):
        developer_tag = gsoup.find("b",text="Developer:")
        developers = []
        if developer_tag:
            for sibling in developer_tag.next_siblings:
                if sibling.name == "a":
                    developers.append(sibling.text)
                else:
                    break
        publisher_tag = gsoup.find("b",text="Publisher:")
        publishers = []
        if publisher_tag:
            for sibling in publisher_tag.next_siblings:
                if sibling.name == "a":
                    publishers.append(sibling.text)
                else:
                    break 
    else:
        developers = gsoup.find("div",{"class":"dev_row"})
        publishers = gsoup.find("div",{"class":"dev_row"})
        if publishers:
            publishers = publishers.find_next_sibling()
            if publishers:
                publishers = publishers.find_all("a", href=True)
        if developers:
            developers = developers.find_all("a", href=True)
    developer_string = ""
    publisher_string = ""
    if developers:
        for developer in developers:
            developer_string += developer.text + ", "
    else:
        developer_string = "N/A"
    if publishers:
        for publisher in publishers:
            publisher_string += publisher.text + ", "
    else:
        publisher_string = "N/A"

    #reviews
    reviews = gsoup.findAll("span",{"class":"responsive_reviewdesc_short"})
    if not reviews:
        per30 = "N/A"
        tot30 = "N/A"
        perAll = "N/A"
        totAll = "N/A"
    else:
        per30 = "N/A"
        tot30 = "N/A"
        perAll = "N/A"
        totAll = "N/A"
        for review in reviews:
            review_string = ""
            tframe = review.find("span",{"class":"desc_short"})
            if not tframe:
                continue
            elif (tframe.text == "All Time"):
                review_string = review.text.lstrip()
                perAll = review_string[1:3]
                perAll = perAll.replace(" ","")
                totAll = review_string[7:]
                totAll = totAll.replace(" ","")
                totAll = totAll.replace(")","")
            elif (tframe.text == "Recent"):
                review_string = review.text.lstrip()
                per30 = review_string[1:3]
                per30 = per30.replace(" ","")
                tot30 = review_string[7:]
                tot30 = tot30.replace(" ","")
                tot30 = tot30.replace(")","")
    
    #generes
    generes = gsoup.find("div",{"class":"glance_tags popular_tags"})
    if not generes:
        genere_string = "N/A"
    else:
        genere_subs = generes.findAll("a", href=True)
        genere_string = ""
        for genere in genere_subs:
            genere_string += genere.text + ", "
    
    #storage
    storage = gsoup.find("strong", text="Storage:")
    if not storage:
        storage_cap = "N/A"
    else:
        storage_cap = storage.next_sibling

    #platforms
    iswin = gsoup.find("div",{"data-os":"win"})
    if iswin:
        win = 1
    else:
        win = 0
    ismac = gsoup.find("div",{"data-os":"mac"})
    if ismac:
        mac = 1
    else:
        mac = 0
    islin = gsoup.find("div",{"data-os":"linux"})
    if islin:
        stmandlin = 1
    else:
        stmandlin = 0

    worksheet.write(row, col, name)
    worksheet.write(row, col+1, price)
    worksheet.write(row, col+2, date)
    worksheet.write(row, col+3, publisher_string)
    worksheet.write(row, col+4, developer_string)
    worksheet.write(row, col+5, per30)
    worksheet.write(row, col+6, tot30)
    worksheet.write(row, col+7, perAll)
    worksheet.write(row, col+8, totAll)
    worksheet.write(row, col+9, genere_string)
    worksheet.write(row, col+10, storage_cap)
    worksheet.write(row, col+11, mac)
    worksheet.write(row, col+12, win)
    worksheet.write(row, col+13, stmandlin)
    
    row += 1

driver.quit()
workbook.close()