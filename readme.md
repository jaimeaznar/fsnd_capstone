# Full Stack Nanodegree Capstone Project


## Intro

This is the final project for the Udacity Full Stack Nanodegree. This project consists of an API with a Python backend, and stores data in a Postgresql database. This project will also incorporate third-party authentication with Role Based Access Control using Auth0.

Currently there is no frontend besides the html templates

## Motivation

As part of my journey of becoming a SWE and FullStack developer I have taken it upon myself to improve our family business infrastructure and digital/online presence. This is part of a personal project to develop a website for our family business. It is time we increase our online presence!!



## Installing Dependencies

### Python 3.7

Follow instructions to install the correct version of Python for your platform in the python docs.

### Virtual Environment (venv)

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the python docs.

### PIP Dependecies

Once you have your venv setup and running, install dependencies by navigating to the root directory and running:

pip install -r requirements.txt
This will install all of the required packages included in the requirements.txt file.

### Local Database Setup

before running the project make sure to execute createdb capstone


### Environment Variables

All variables are stored locally in the `.env` file. Please ensure the `DATABASE_URL` is accurate for your system if running this project locally.

### Local Testing

To test your local installation, run the following command from the root folder:

python test_api.py
If all tests pass, your local installation is set up correctly.

### Running the server

From within the root directory, first ensure you're working with your created venv. To run the server, execute the following:

export FLASK_APP=app
export FLASK_ENV=development
flask run
Setting the `FLASK_ENV` variable to development will detect file changes and restart the server automatically.
Setting the `FLASK_APP` variable to `app` directs Flask to use the `capstone` directory and the `__init__.py` file to find and load the application.

Please see the documentation on API usage at `readme_api.md`.