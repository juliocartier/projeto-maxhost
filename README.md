# Zombie Apocalypse
## Dev: Julio Cartier M. Gomes


[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

You need to develop a RESTful API that stores survivors from a zombie apocalypse and allow
them to find the closest survivor from their location.

## Features

- Create new survivors - name, gender and current location (latitude/ longitude).
- Retrieve a survivor - survivor id required.
- Update Survivors
- Retrieve closest survivor from a survivor - survivor id required, you can use
only latitude or longitude to calculate it. This is to help a survivor to identify who is
closer.
- Mark survivor as infected - A survivor is marked infected when at least 3 others
survivors report that it is infected.
. Documentation + Setup - We need to run your code based on README and
use the API based on the documentation.

## Technologies

Technologies used for API development.
- Python
- Flask
- Sqlite



## Install and Run

Executar a partir da [Python] v3.7+ (https://www.python.org/).

Clone the repository

Install dependencies and run.

```sh
cd projeto-maxhost
```

#### Install

1. Create a virtual environment:
```sh
cd projeto-maxhost
```
2. Activate a virtual environment MacOS or Linux:
```sh
source env/bin/activate
```
3. Activate a virtual environment Windows

```sh
.\env\Scripts\activate
```

4. Install dependencies:

```sh
pip install -r requirements.txt
```

5. Run Application:
```sh
python app.py
```

6. Run Application at browser:
```sh
http://127.0.0.1:5009/apidocs/
```
7.  Run Application at postman:
```sh
http://127.0.0.1:5009/
```

## License

**Free Software!**