# Liquidity Watch

Liquidity Watch is a web application that will allow you to select from over 600 commodity contracts and plot price, volume and volatility graphs. There are additional metrics that can be added to these graphs which currently includes Volume Weighted Average Price and Average Daily Volume, which can be useful for traders who want to analyse price and volume action. 

### Deployment

Currently having issues with Docker (and Postgres Image), therefore you will need to install Python and PostgresSQL.


From Command Line:
```
psql postgres
```

From within Postgres Shell:
```
CREATE ROLE lw_user WITH LOGIN PASSWORD '1234';
ALTER ROLE lw_user CREATEDB
```

From command line:
```
createdb referencedb
```

To test it was created (from command line):
```
psql referencedb
```

Once you have your Python environment setup you need to install the dependencies (from within application root).
```
pip install -r requirements.txt
```

Finally run (within the app folder):
```
python loader.py
```

Once this has been completed you should be able to simply run (within the app folder):

```
python app.py
```

Please navigate to `localhost:80` where the app should be running.

### Technologies

 - [pandas (Python)](http://pandas.pydata.org/):  Used for data manipulation and calculations. 
 - [Bokeh (Python)](http://bokeh.pydata.org/en/latest/): Charting library that integrates well into flask while displaying results in JS.
 - [Flask (Python)](http://flask.pocoo.org/): Lightweight Python web framework. 
 - [Quandl](https://www.quandl.com/): Main datasource with an easy to use API.
 - [PostgreSQL](https://www.postgresql.org/): Database used to store reference data. 
 - [Bootstrap](http://getbootstrap.com/): A front end CSS package with easy to use components.
 - [Github](https://github.com/): A Git repository with many open sourced projects.
 - [PyCharm](https://www.jetbrains.com/pycharm/): Primary IDE used for development.
 
### Considerations
 - Redis or a temporal database (e.g. KDB)
 - React (Front End)
 - Docker (Deployment)


![Annotation 2019-06-22 172908](https://user-images.githubusercontent.com/6753044/59966343-5a18c200-9513-11e9-951d-a9d5afae8d73.png)
![64848676_461545794419313_2096851893455159296_n](https://user-images.githubusercontent.com/6753044/59965478-72ceab00-9506-11e9-8eee-26adf1a3a0c2.png)
