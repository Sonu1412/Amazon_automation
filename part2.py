import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from msedge.selenium_tools import Edge,EdgeOptions
from selenium.webdriver.edge.options import Options
import csv
import pandas as pd
from pandas import *
def new_csv():
    fields = ['Decription','ASIN','Product Decription','Manufacturer']
    filename = 'assignment_last.csv'
    with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
            
        # writing the fields 
        csvwriter.writerow(fields)


def input_csv(data):
    
    data1 = {
        'Decription': [data[0]],
        'ASIN': [data[1]],
        'Product Decription': [data[2]],
        'Manufacturer': [data[3]]
        
    }
     
    # Make data frame of above data
    df = pd.DataFrame(data1)
     
    # append data frame to CSV file
    df.to_csv("assignment_last.csv", mode='a', index=False, header=False)
    
      
def dec(soup):
    d = 'NaN'
    try:
        m = soup.find('div',{'id':"productDescription"})
        d = str(m.span).strip()
        d = d[6:-7]
        d.remove('>')
       
    except AttributeError:
        pass
    data = [title,asin,d,manu]
    try: 
        m = soup.find_all('div',{'class':'a-section a-spacing-small'})
        for i in m:
            if 'Product description' in str(i):
                d = str(i.span).strip()
                d = s[6:-7]
                d.remove('>')
    except AttributeError:
        pass
    print(d)
    return d

        
new_csv()
data = read_csv('assignment_part1.csv')
l1 = data['URL'].tolist()
options = EdgeOptions()
options.use_chromium = True

for link in l1:
    headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
    driver = requests.get(link,headers =headers)
    soup = BeautifulSoup(driver.content,'html.parser')
    title = ''
    try:
        title = soup.find(id = 'productTitle').get_text().strip()
        
    except AttributeError:
        
        continue
    manu = ''
    asin = ''
    try:
        table =soup.find("table", class_="a-keyvalue prodDetTable")
        rows = table.find_all("tr")
        
        for x in rows:
            if(x.th.get_text().strip() == 'ASIN'):
                asin = x.td.get_text().strip()
               
            if(x.th.get_text().strip() == 'Manufacturer'):
                manu = x.td.get_text().strip()
    except AttributeError:
        my_list = soup.find("ul", class_="a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list")
        item = my_list.find_all('li')
        for x in item:
            if('ASIN' in str(x)):
                a = str(x)
                a = a[:-21]
                i = a[::-1].index('>')
                asin = a[-i:]   
            if('Manufacturer' in str(x)):
                a = str(x)
                a = a[:-21]
                i = a[::-1].index('>')
                manu = a[-i:]
    except :
        continue
    print(asin,manu)
    d= dec(soup)
    data = [title,asin,d,manu]
    
    print(data)
    input_csv(data)


    
    
