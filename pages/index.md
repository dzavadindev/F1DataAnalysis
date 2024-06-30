# How to run the data processing 'pipeline' 

First ensure that you have python version 3.11 or above and poetry installed
Then enter your terminal (suggest running everything via WSL) and run the following commands:

``` bash
python --version
./run.sh init
npm run dev
```

Subsequential runs to update data, rerun models and resource evidence can be run with 

``` bash
./run.sh
```

# Introduction

This page will detail the data processing journey, what steps it took to make it look like this, logic behind the calculations and reasoning for why certain data is relevant to answer the question.  

To see the answers to the questions, follow to [Constructor Predictions]("/constructor_predictions") or [Drivers Incidents]("/drivers_incidents") pages using those links or the side bar.

# Process 

First, lets run thought the process of getting all the different data sources like api, csv and txt files into one DuckDB database. 

## Loading 

Starting off with loading the data, `assignment-data.zip` contains csv and txt files, detailing things like race control logs, constructor earned points, race information, weather details, lap times etc.. Loading csv files using pandas and duckdb is pretty easy, as csv files have a table-like structure, which is easily conversable into dataframes, which in turn can easily be made into a database table.

txt files (being race control logs) need some formatting, like determining patterns within the line, and using regular expressions to filter out the relevant information. I decided to only take the incident logs from the race control, as there is no elegant way to structure a table to contain all the different things race control keeps track of. Even the file format begin txt instead of csv proves it.

Lastly, the `requests` library is used to retrieve the drivers and teams from API. If the resource is not available, the script will fail.  

## Transformations

After all the raw data is in the database, we can start the transformation part. I decided to split this phase into 4 stages: staging - initial cleaning, type casting, column renaming etc., intermediate - if something needs to be done before defining dims and fcts, in my case table joining, star - creating tables according to STAR schema and finally report - where all actual calculations and aggregates happen. 

All models are tested using `data_tests` definitions inside of the `schema.yml` files.

### Staging

As mentioned before, this stage consists mainly of type casing and renaming columns. Additionally, the `stg_` models are materialized as `incremental`, and have incremental conditions. This enables to not insert duplicates with every data load, and most of conditions are time based, as in "only accept new records, date is later than the current latest date in the database". If its not that, it would be "if its something that already exists, don't add it".

### Intermediate

Nothing much to say about it, the only one intermediate model is the `int_races`, allowing to join the number of races in the championship and points given for finishing first (as those differ over the years). 

### STAR

This step defines the dimension and fact tables, the former describing object/entities and the latter describing events, and practically being a "junction" between dimension tables. Other than than, pretty straight forward, those tables contain pretty general information about the entities or event, not dependent on anything besides the initial `stg_` tables.

### Reports

Finally, `rpt_` tables contain all my calculations and aggregates

For incidents, its as simple as counting all occurrences where the drivers code appears in `driver_one_code` column, then counting all occurrences where the drivers code appears in `driver_two_code` column, when using union operation with combine flag to join to tables with summing of incident number for every driver

For predictions, its also quite simple. We are defining two point stats - potential and perdition. Potential refers to how much points a constructor team CAN earn if then just go on a winning streak and prediction is their likely score by the end of the season. Both are done using a similar formula - we get the number of races left, and multiply it by wither average score (for prediction) or points for first place (potential) and adding the current number of points they have.

To not make predictions that are impossible (having more points than its physically possible to earn in a championship), the predicted score is being normalized, using the common 0 to 1 normalization formula, and then multiplied by the maximum possible to achieve points (for year 2023 being 575) 

## Automation

Lastly, the process of loading, transformation and source updating is also runnable via a Bash script, that is why I recommend using a WSL if you are running the project on Windows. THe script takes care of spinning up and disposing of a docker container running the API, execution of the loading script, running and testing dbt models and updating the evidence source. After that the evidence server can be started, and the new changes reviewed on the pages.

The only two things you would need to do manually is the raw data sources into the `./raw/` directory and run the evidence server.

# Remarks 

Some remarks about data and calculations...

## API

The initial `api.json` node server was serving from contained many entries that had null driver codes and driver numbers. I am not sure if that was intentional, so I can filter out the null values using dbt, or were they accidental.  

I have redacted the `api.json` in the server to contain actual complete information about F1 drivers competing 2020-2023, with most recently used number and 3 letter code.

## Constructors results

What I have noticed is that in our constructors results csv (and all dataset who inherit from it) we have only got 3 races of the 2023 season. My idea was to count how much races are left, get the average of what a team has earned so far as the score they are likely to get for next races and compare and rank final scores (races left * average points). Then its normalized to be in reasonable bounds of maximum available points.

Technically, this is a decent solution, but the fact that the information is only 3 races make a big impact on the quality of prediction.

## Races updates

I have added a .csv file containing number of races for each year of F1 championships, starting from 2000 and the score you would get for getting first place in the race.
