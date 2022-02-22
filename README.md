# mag-app
 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Build Status](https://travis-ci.org/AnzeLovse/mag-app.svg?branch=master)](https://travis-ci.org/AnzeLovse/mag-app) [![Updates](https://pyup.io/repos/github/AnzeLovse/mag-app/shield.svg)](https://pyup.io/repos/github/AnzeLovse/mag-app/) [![Python 3](https://pyup.io/repos/github/AnzeLovse/mag-app/python-3-shield.svg)](https://pyup.io/repos/github/AnzeLovse/mag-app/) [![Coverage](https://codecov.io/github/AnzeLovse/mag-app/coverage.svg?branch=master)](https://codecov.io/github/AnzeLovse/mag-app?branch=master) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


Dash app for time course RNAseq visualisation.


## Usage
To locally run the app you have to:

- create a python virtual environment and activate it
- install all project dependencies from `requirements.txt` via `pip install -r requirements.txt`

## Run your Dash app
Check that the virtual environment is activated, then run:

```shell
cd mag_app
python app.py
```
The app will be running on http://127.0.0.1:8050/

## Code formatting
To format all python files, run:

```shell
black .
```

## Pin your dependencies

```shell
pip freeze > requirements.txt
```
