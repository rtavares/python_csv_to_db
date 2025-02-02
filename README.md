# Python - Getting data from a CSV file to a DB

### A Proof of Concept (P.O.C.) to show how to import data from a CVS file to a database and show it to others.

This is an early version and a Work In Progress (W.I.P).

### Dataset used to test: [Books Dataset from Kaggle](https://www.kaggle.com/datasets/saurabhbagchi/books-dataset).
- The dataset is not included in the repository, once it is 

## Tech stack / requirements
- A container manager like Docker installed and running.
- The project is running in the local OS
  - Virtual Env and package management is done with [uv](https://docs.astral.sh/uv/getting-started/installation/).
- We are using Python 3.13.1

## Project setup
- Download the Books Dataset and extract books.csv to [source/books_data](source/books_data) project folder.
- If you want to use `uv` , it is only required to do `uv sync` 
  - Otherwise, please do your own virtual environment and package management configuration and do the necessary adjustments.
  - We are supplying ` requirements.txt` and ` dev-requirements.txt` for convenience.

## Get the project running
- Start PostGeSql and PgAdmin: 
  - `docker compose up -d`
- Load the Books CSV to the database:
  - `python source/import_books_dataset.py`
- Start the UI:
  - `streamlit run source/app.py`

Access the frontend in [http://localhost:8501](http://localhost:8501)
- Or other port you may have specified in the .env file.   

Access `pgadmin` in [http://localhost:8001](http://localhost:8001)
- Or other port you may have specified in the .env file.
- Login with the credentials defined in `.env` file
- Configure the `servers` access (TBD) 

## TO-DO:
- Move the app to a container
- Write better documentation
----

