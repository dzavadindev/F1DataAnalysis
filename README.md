# ADM Exam 2

## Introduction 

This preload has been created as an alternative to the dev.container. It uses poetry as its package manager, to help ensure compatibility on different machines.

You can create your python scripts in the base of the project. Please ensure, that you name logically.

## Install poetry    

1. Install poetry on your computer: [link](https://python-poetry.org/docs/#installation)
   1. *Poetry is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on* [Taken from [python-poetry.org)](https://python-poetry.org/docs/)]
   2. Poetry has been setup for this project, and to run libraries you will first call `poetry run` i.e. if you need to run `duckbd` you should run `poetry run duckdb`
2. **Step 1** The configuration file has setup the correct pachackes etc... please fun the following command in this project after poetry installed on your computer.
   1. `poetry install`
3. If you change the name of your project folder, also change the name in the pyproject.toml file to the name you renamed the folder.
   
## Source data

The `raw` folder has got the `API` folder containing the API with some of your source data. Please copy the aditional source files into this folder to load from.

Inside the `API` folder is instructions on running the API.

## Evidence

### To start Evidence

`poetry run npm install;poetry run npm run sources; poetry run npm exec evidence dev -- --open /`

#### Terminal commands while evidence is running

  press r + enter to restart the server
  press u + enter to show server url   
  press o + enter to open in browser   
  press c + enter to clear console     
  press q + enter to quit

### Learning More

- [Docs](https://docs.evidence.dev/)
- [Github](https://github.com/evidence-dev/evidence)
- [Slack Community](https://slack.evidence.dev/)
- [Evidence Home Page](https://www.evidence.dev)

## DBT

Modify profiles.yml to point to your database.

### Usefull commands

- `poetry run dbt build` 
  - This will build and check queries etc...
- `poetry run dbt test`
  - This will run the tests
- `poetry run dbt run`
  - This will run dbt
- `poetry run dbt docs generate`
  - This will generate your documentation

### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices

## Python
*Please note, <name> should be replaced with the name of your file.*

Create your python file(s)
to run:
- `poetry run python <name>.py`

## duckdb
*Please note, <name> should be replaced with the name of your file.*

To create a duckdb file
- Option 1: Create it using your python script
- Option 2: `poetry run duckdb <name>.duckdb`

To open a duckdb file
- `duckdb <name>.ddb`