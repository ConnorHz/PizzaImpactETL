#Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from config import chromedriverpath, pw
from sqlalchemy import create_engine, inspect, func
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


###START OF OBESITY DATA
#Path for splinter
executable_path = {'executable_path': chromedriverpath}
browser = Browser('chrome', **executable_path, headless=False)

#Grab HTML data
url = 'https://stateofchildhoodobesity.org/adult-obesity/'
browser.visit(url)
html = browser.html
soup = bs(html, 'html.parser')
browser.quit()

States=soup.find_all('td', class_='state-column')
Rates=soup.find_all('td', class_='rate-column')

#format data to be usable
State_Names=[]
State_Abs=[]
State_Rates=[]
for state in States:
    Span_Length=len(state.span.text)
    State_Names.append(state.text.strip()[Span_Length:])
    State_Abs.append(state['data-state-ab'].upper())

for rate in Rates:
    State_Rates.append(float(rate.text.replace('\n','').replace('%','')))

df = pd.DataFrame({
    "State_Name": State_Names,
    "State_Ab": State_Abs,
    "State_Rate": State_Rates
})
###END OF OBESITY DATA

###START OF PIZZA DATA
## path to the pizza
path="pizza_file.csv"

##creating the raw dataframe
raw_pizza_df=pd.read_csv(path)

##removing cells we don't need and making a clean df
clean_pizza=raw_pizza_df[['country','province','menus.amountMax','menus.currency','menus.name', 'name']]

# making sure all the entries we're looking at are in USD and pizza in america

clean_pizza=clean_pizza[(clean_pizza["menus.currency"]=="USD") & (clean_pizza["country"]=="US")][['province','menus.amountMax','menus.name', 'name']]

#renaming columns
clean_pizza.rename(columns={
    "province":"state",
    "menus.amountMax":"price",
    "menus.name":"menu_item",
    "name":"store_name"
},inplace=True)
###END OF PIZZA DATA

###START OF POSTGRESQL TABLE CREATION

###END OF POSTGRESQL TABLE CREATION
###START OF POSTGRESQL DATE IMPORTING

###END OF POSTGRESQL DATE IMPORTING