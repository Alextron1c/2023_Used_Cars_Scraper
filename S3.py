import requests
import time
from bs4 import BeautifulSoup
import io
import sys
import csv

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
name_list=[]
brand_list=[]
price_list=[]
holder_list=[]
start=1

parsing_list=["https://kuruma-ex.jp/usedcar/search/result/year_max/2022/year_min/2022/odd_max/5000/page/",
            ]


for url in parsing_list:
    website = requests.get(url+"1", headers=HEADERS) 
    website.encoding = 'UTF-8'
    time.sleep(1)  
    doc0 = BeautifulSoup(website.content, 'html.parser')

    pagelist = doc0.find("div", class_="right stockCount mt15 mr10 ajax_stock_count")

    if pagelist:
        span_element = pagelist.find("span")
        if span_element:
            span_text = span_element.text.strip().replace(",", "")
            
            try:
                fullpage_list = ((int(span_text)) + 49) // 50  
               
                for y in range(1, fullpage_list+ 1): 
                    holder_list.append(url + f"{y}/per_page/50")  
                
            except ValueError:
                print("Item count does not exit")




with open('Used-Cars.csv', 'w', encoding="utf-8", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Brand","Name",'Price'])

    for items in holder_list:
        website = requests.get(items, headers=HEADERS)
        website.encoding = 'UTF-8'
        time.sleep(1)
        doc = BeautifulSoup(website.content, 'html.parser')

        table_element=doc.find_all("table",class_="usedResultList usedResultList_item")    

        for tables in table_element:
            price_list_elements = tables.find("span", class_="total_price")    
            
            if not price_list_elements:  
                price_list.append(" ")
                name_list.append(" ")
                brand_list.append(" ")
                continue

            price_text = price_list_elements.text.strip().replace("総額", "")  
            price=price_list.append(price_text) 

            brand_name_elements=tables.find("li", class_="maker_name newer left")         
            brand_list.append(brand_name_elements.text.strip())

            name_list_elements = tables.find("h3", class_="car_name mb10") 
            name_list.append(name_list_elements.text.strip())

    
    for i in range(len(price_list)):
        if brand_list[i].strip():
            writer.writerow([brand_list[i], name_list[i], price_list[i]])

        
        