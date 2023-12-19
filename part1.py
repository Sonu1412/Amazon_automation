import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from msedge.selenium_tools import Edge,EdgeOptions
from selenium.webdriver.edge.options import Options
import csv
import pandas as pd

def new_csv():
    fields = ['URL','Name','Price','Rating','Review']
    filename = 'assignment_part1.csv'
    with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
            
        # writing the fields 
        csvwriter.writerow(fields) 

def input_csv(data):
    
    data1 = {
        'URL': [data[0]],
        'Name': [data[1]],
        'price(INR)': [data[2]],
        'rating': [data[3]],
        'reviews':[data[4]]
    }
     
    # Make data frame of above data
    df = pd.DataFrame(data1)
     
    # append data frame to CSV file
    df.to_csv("assignment_part1.csv", mode='a', index=False, header=False)
    
        
    

def extract(item):
    atag = item.h2.a
    dec = atag.text.strip()
   
    link = 'https://www.amazon.in'+atag.get('href')
    
    try:
        price_parent = item.find('span','a-price')
        price = price_parent.find('span','a-offscreen').text
        price = price[1:]
    except AttributeError:
        return
    
    try:
        
        rating =item.i.text
        
        review_count = item.find('span',{'class':'a-size-base s-underline-text'}).text
    except AttributeError:
        rating = ''
        review_count = ''
    if '(' in review_count:
        review_count=review_count[1:-1]
            
    data = [link,dec,price,rating,review_count]
    print(data[2:])
    input_csv(data)
    

if __name__ == '__main__'  :
    new_csv()
    options = EdgeOptions()
    options.use_chromium = True
    #driver = Edge(options = options)
    url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'
    for i in range(20):
        if(i!=0):
            url='https://www.amazon.in/s?k=bags&page='+str(i+1)+'&crid=2M096C61O4MLT&qid=1675330632&sprefix=ba%2Caps%2C283&ref=sr_pg_'+str(i+1)

        headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
        driver = requests.get(url,headers =headers)
        soup1 = BeautifulSoup(driver.content,'html.parser')
        #soup2 = BeautifulSoup(soup1.prettify(),'html.parser')
        results = soup1.find_all('div',{'data-component-type':'s-search-result'})

        
        for item in results:
            extract(item)


    


