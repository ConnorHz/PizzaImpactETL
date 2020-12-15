#Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from config import chromedriverpath, pw
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float
from sqlalchemy.orm import Session
import sqlalchemy_utils as utils


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

obesity_df = pd.DataFrame({
    "state_name": State_Names,
    "state": State_Abs,
    "rate": State_Rates
})
###END OF OBESITY DATA

###START OF PIZZA DATA
## path to the pizza
path="pizza_file.csv"

##creating the raw dataframe
raw_pizza_df=pd.read_csv(path)

##removing cells we don't need and making a clean df
pizza_df=raw_pizza_df[['country','province','menus.amountMax','menus.currency','menus.name', 'name']]

# making sure all the entries we're looking at are in USD and pizza in america

pizza_df=pizza_df[(pizza_df["menus.currency"]=="USD") & (pizza_df["country"]=="US")][['province','menus.amountMax','menus.name', 'name']]

#renaming columns
pizza_df.rename(columns={
    "province":"state",
    "menus.amountMax":"price",
    "menus.name":"menu_item",
    "name":"store_name"
},inplace=True)


###END OF PIZZA DATA

###START OF POSTGRESQL TABLE CREATION
connection_string = f'postgresql://postgres:{pw}@localhost'
database_name = "pizza_db"

if utils.database_exists(f'{connection_string}/{database_name}') == False:
    engine = create_engine(connection_string)
    conn = engine.connect()
    conn.execute("commit")
    conn.execute("create database pizza_db")
    conn.close()

engine = create_engine(f'{connection_string}/{database_name}')
conn = engine.connect()

meta = MetaData()

# Create pizza table if it doesn't exist
pizza_table = Table(
   'pizza', meta,
   Column('state', String), 
   Column('price', Float),
   Column('menu_item', String),
   Column('store_name', String),
)
pizza_table.create(engine, checkfirst=True)


# Create obesity table if it doesn't exist
obesity_table = Table(
   'obesity', meta,
   Column('state_name', String), 
   Column('state', String),
   Column('rate', Float)
)
obesity_table.create(engine, checkfirst=True)

conn.close()

###END OF POSTGRESQL TABLE CREATION
###START OF POSTGRESQL DATA IMPORTING
for index, row in pizza_df.iterrows():
    pizza = pizza_table(state=row.state, price=row.price, menu_item=row.menu_item, store_name=row.store_name)
    session.add(pizza)

# Load obesity table
for index, row in obesity_df.iterrows():
    obesity = obesity_table(state=row.state, state_name=row.state_name, rate=row.rate)
    session.add(obesity)

session.commit()
###END OF POSTGRESQL DATA IMPORTING