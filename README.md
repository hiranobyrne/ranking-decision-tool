# Car Ranking Decision Tool
![Python](https://img.shields.io/badge/python-%23F0F0F0?style=for-the-badge&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAACXBIWXMAAAsTAAALEwEAmpwYAAADGUlEQVR4nO2YPWgUQRTHZ2dzM5dYaCFBAiaFNkZRBMUuiI0fRdBCwSZFolj4kWCSmRMJhyksBJVgI2qhhYIpFEREczPZmUSDSBo%2FkIAERWMnETQmSDRPdm89g4TczCXrXnD%2F8Jpr9vfb92Z25hBKkiRJEoTAQTy3GWcEd7i8i7l4hZkYx0x%2Bx1xMYi4%2BYCaeOlxecrncgbJZXD5vrUNsDIC5BNNyuHiITnor40ZHKHuvCjM5ZgNfKCaHYu%2BEy%2Fp3lgQflpvJ7YpVAHPZHL7NMXRK1COeq8VcvrAYpe54BZhoy4PIa39%2Bk13mAvJiWQgUOtAu6%2Bw6IMtEoMRyEoGYu%2BSEHQBN2kBTmFVToOkzUGTfUhWAoBSdAU0Plf70jLfW4fJy%2BKWdWMi8lySgg%2FoKMl1nze52ykbM5LfFhi5BAEDRs3b0%2Be1w0d%2F4HALnzQTIqBW%2Fw0VP1PBBMXEsEFDk9LwCfnlVq4wFMBNvohcQn1H7o%2Bp8B%2BjtogKK7DGjb%2FVWYC5mIhaY8A%2BCyId%2Fsqw6WKjFBVrNBHhuezTjIn9iJt87TF5FHXLN78eBpreKwufrjNn4ZORBy1EYwVw2oc6%2BmuBmZhgAhEHRC4bw%2Fk50zkyAi6Pmu4i4iY4%2FoKbQhZFRqQOg6LAxfH6EuJkAEy2GW2A%2FynoVAdTjyhrQtAc0eQua%2FrAC06YC6SYjAbdT7DWZZ8T61gXwXsUW0ORTJNB6Vg2mNpn1mMn1BgJDeXiUBk3eRQ6v6CQMo5SZwP5et9hX2OHiSiCgSGPk8DqoO8gmDhPS6AyjyIl%2FAD%2Ftj6mVAGbiiJFAsTPMYsAr2oysw3PL5%2Fu%2FJ2KBKdD0NShy3XzhzhGXid2YiemSBRSN98IehMsGf7%2F%2F%2B16wdASKZMEjpGKW%2FM8EyBgMkHrQ6dWg6POlJ6BI4e9H0KSrTARoi4XAR%2FBSG2AwXQuavgwFuuMVCEZiAWvAo4djFTC%2Bz869gL9YXdQjExhGVaDJDTt4Mgo63YDKKaAqtvrXPlBEh0fsifAsMw6KjoCi90GRLAxUboNe5MbNmyRJElQe%2BQWgfIcmva%2Bj%2BwAAAABJRU5ErkJggg%3D%3D)
![Flask](https://img.shields.io/badge/flask-%232BAED5?style=for-the-badge&logo=flask)
![Pandas](https://img.shields.io/badge/pandas-%23150458?style=for-the-badge&logo=pandas)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

## Table of Contents
 - [About](#about)
 - [Project Setup](#project-setup)
 - [Prerequisites](#prerequisites)
 - [Dependencies](#dependencies)
 - [Execution](#execution)

## About
 A web application that ranks data according to custom multiple-criteria and individual preferences selected by the user. It uses the Analytical Hierachical Process (AHP) algorithm, helping with decision making in a car purchase process.

### Screenshots

1. **Criteria Selection and Preferences View**  
   <img width="500" alt="Criterion Selection" src="https://github.com/hiranobyrne/car-ranking-decision-tool/blob/ed7c37f4526409366a0c3d92d8a99547ac18dd82/assets/alternatives_preferences_screen.png?raw=true">

2. **Final Ranking View**  
   <img width="500" alt="Ranking View" src="https://github.com/hiranobyrne/car-ranking-decision-tool/blob/9cf4f44252b94a0d5de5e0149302929c991820c3/assets/ranking_screen.png?raw=true">


## Project Setup

### General GUI setup
 The app contains 4 views:
 - **First view:** selection of dataset and column for alternatives to be ranked.
 - **Criterion and Alternatives Selection view:** allows selection of criterion to be used in ranking (min 2, max 5), and selection of alternatives for the ranking (min 2, max 5). 
 - **Criterion Weight Preferences view:** ranking with selection of different calculation methods.
 - **Alternatives Weight Preferences view:** ranking with selection of different calculation methods.
 - **Ranking view:** ranking with selection of different calculation methods.

### Directories structure
```bash
.
├── README.md
├── app
│   ├── __init__.py
│   ├── logic
│   │   ├── __init__.py
│   │   └── ahp.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── ahp_routes.py
│   │   ├── dash_routes.py
│   │   └── root_routes.py
│   ├── static
│   │   ├── css
│   │   ├── images
│   │   └── js
│   ├── templates
│   │   ├── ahp
│   │   └── index.html
│   └── utils
│       └── utils.py
├── config.py
├── data
│   ├── cache
│   └── csv_datasets
├── requirements.txt
└── run.py
```
 - **./ :** root directory of the project. Contains the project's metadata files, and configuration files.
 - **./data :** all csv data used.
 - **./app :** the Python application.
 - **./app/routes :** all routes and backend code.
 - **./app/logic :** business logic. In this case, the AHP class. Other classes can be added for different MCDM techniques.
 - **./app/static :** all static assets, such as images, icons, Javascript and CSS files.
 - **./app/templates :** templates for the views using mainly HTML, Jinja and JavaScript.
 - **./app/utils :** shared utilitary functions.

### Techstack
 Made in object oriented Python, it uses Flask microframework as the web server gateway interface (WSGI). It uses Jinja, HTML, JavaScript, and is styled with CSS. The visualization components for the range inputs were developed in JavaScript. For more details, see [Dependencies](#dependencies).
 
 - Python (3.12)
 - Flask
 - Pandas
 - JavaScript

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12 or later**: [Download Python](https://www.python.org/downloads/)
- **Pip**
- **Virtual Environment (optional)**

## About the Dependencies

### Getting Started with Flask
Web framework used was [Flask](https://flask.palletsprojects.com/en/3.0.x/installation/#install-flask). Application uses [Jinja](https://jinja.palletsprojects.com/en/3.1.x/intro/#installation) templating.

### Getting Started with Pandas
Data manipulation uses [Pandas](https://pandas.pydata.org/getting_started.html).

## Running the app
### Install dependencies
```pip install -r requirements.txt```

### Start Flask server
```python run.py```

### Access the app on a browser
```http://127.0.0.1:5000/```

### Explore the routes
+ /
+ /ahp


