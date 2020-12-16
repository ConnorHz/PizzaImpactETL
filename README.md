# Pizza & You

Are your local pizza joints affecting the health of your community? 
With the data gathered in this project we are able to investigate the correlation between adult obesity rates and the cost of a pizza in each U.S. state.

# Data Sources

- [Pizza Restaurants and their Pizzas](https://data.world/datafiniti/pizza-restaurants-and-pizzas-on-their-menus)
    - This dataset from Datafiniti is a list of 10,00 pizzas from a wide variety of restaurants across the United States.

- [Adult Obesity Rate by State, 2019](https://stateofchildhoodobesity.org/adult-obesity/)
    - This dataset from [stateofchildhoodobesity.org](https://stateofchildhoodobesity.org/) includes the adult obesity rates of each state from 2019
        - (according to data from the [Behavioral Risk Factor Surveillance System](https://www.cdc.gov/brfss/index.html))

# ETL Process

## **Extract**

To extract the pizza menu data, we first downloaded the csv file from [Datafiniti](https://data.world/datafiniti/pizza-restaurants-and-pizzas-on-their-menus). We then used Pandas to read the [csv file](pizza_file.csv) into a data frame and begin the transformation process.

We scraped the obesity data from [stateofchildhooobesity.org](https://stateofchildhoodobesity.org/) using Python, Splinter, and Beautiful Soup.

### **Transform**

Once the pizza menu data frame was created, we removed the columns that were nonessential to our project from the data frame. Next, we reduced the data frame to exclude any pizza prices not listed in U.S. dollars and any foreign locations.


To transform the obesity data, we used strip to remove unwanted spaces. The state names in the data included a character icon, so we inspected the span length to eliminate the character, leaving just the desired state name. We also pulled the state abbreviation from the tag and converted it uppercase lettering. For the obesity rates, we removed line breaks and percentages by utilizing the replace function.


### **Load**

To load our data, we first connected to the postgres server in pgAdmin. Our next step was to use an if statement to create our database if it wasn't already present. Then we created both tables if they didn't already exist. Lastly, we iterated through each data frame, loading the data into its respective tables.
