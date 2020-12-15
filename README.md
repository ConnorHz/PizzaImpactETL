# Pizza & You

Are your local pizza joints effecting the health of your community? With the data gathered in this project we are able to investigate correlation between the price of a pizza and the adult obesity rate of the state in which the pizza is sold.

# Data Sources

- [Pizza restaurants and Pizzas on their Menus](https://data.world/datafiniti/pizza-restaurants-and-pizzas-on-their-menus)
    - This dataset from Datafiniti is a list of over 3,500 pizzas from multiple restaurants across the US.

- [Adult Obesity Rate by State, 2019](https://stateofchildhoodobesity.org/adult-obesity/)
    - This dataset from [StateofChildhoodObesity.org](https://stateofchildhoodobesity.org/) includes the adult obesity rates of each state from 2019
        - (according to data from the [Behavioral Risk Factor Surveillance System](https://www.cdc.gov/brfss/index.html))

# ETL Process

## **Extract**

To extract the pizza menu data, we first downloaded the csv file from Datafiniti. We then used Pandas to read the CSV into a data frame and begin the Transformation process.

We scraped the obesity data from the stateofchildhooobesity.org using python, splinter, and beautiful soup.

### **Transform**

Once the pizza menu data frame was created, we removed the columns we didn’t need from the data frame. We then reduced the data frame to only include U.S. currency and locations.


Once we imported the obesity data, we used strip to remove unwanted spaces. Since the state names we had included a character from the span, we checked the span length to eliminate the unwanted character. We then pulled the state abbreviation from the tag and made it upper case. For the obesity rates, we removed line breaks and percentages by using the replace function.


### **Load**

To load our data, we first connected to the postgres server. We then used an if statement to create our database if it wasn't already present. Then we created both tables if they didn't already exist. Finally, we iterated through each data frame, loading them into their respective tables.
