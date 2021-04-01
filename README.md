# mag-app
 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Build Status](https://travis-ci.org/AnzeLovse/mag-app.svg?branch=master)](https://travis-ci.org/AnzeLovse/mag-app) [![Updates](https://pyup.io/repos/github/AnzeLovse/mag-app/shield.svg)](https://pyup.io/repos/github/AnzeLovse/mag-app/) [![Python 3](https://pyup.io/repos/github/AnzeLovse/mag-app/python-3-shield.svg)](https://pyup.io/repos/github/AnzeLovse/mag-app/) [![Coverage](https://codecov.io/github/AnzeLovse/mag-app/coverage.svg?branch=master)](https://codecov.io/github/AnzeLovse/mag-app?branch=master) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


Dash app for time course RNAseq visualisation


## Usage
You will need to create an `.env` file where to store your environment variables (SECRET key, plotly credentials, API keys, etc). Do NOT TRACK this `.env` file. See `.env.example`.

Run all tests with a simple:

```
pytest -v
```


## Run your Dash app
Check that the virtual environment is activated, then run:

```shell
cd mag_app
python app.py
```

## Code formatting
To format all python files, run:

```shell
black .
```

## Pin your dependencies

```shell
pip freeze > requirements.txt
```

## Deploy on Heroku
Follow the [Dash deployment guide](https://dash.plot.ly/deployment) or have a look at the [dash-heroku-template](https://github.com/plotly/dash-heroku-template)
