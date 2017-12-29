from flask import Flask, render_template, request, redirect
from dateutil.relativedelta import relativedelta
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.palettes import Spectral11

import requests
import datetime
import json
import pandas

app = Flask(__name__)

@app.route('/index')
@app.route('/')
def index():
    price_type = ['close', 'adj_close', 'open', 'adj_open']
    return render_template('index.html', price_type = price_type)

'''
@app.route('/price', methods = ["GET","POST"])
def price():    
    ticker = request.form['ticker']
    one_yrs_ago = datetime.date.today() - relativedelta(years=1) 
    type_list = request.form.getlist('pricetype')
    p_type = ','.join(type_list)
    
    req = requests.get('https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?date.gte='
                       + str(one_yrs_ago) + '&qopts.columns=ticker,date,' 
                       + p_type + '&api_key=RQvziVWcARiHqhMdCcvt&ticker='
                       + ticker)
    
    #get the column names
    col_names = pandas.read_json(json.dumps(req.json()['datatable']['columns']))['name'].values
    #get the data
    data_df = pandas.read_json(json.dumps(req.json()['datatable']['data']))    
    #combine the column names with data
    data_df.columns = col_names
    
    return render_template('price.html', price = json.loads(req.text)['datatable']['data'])
'''
@app.route('/graph', methods = ["GET","POST"])
def graph():    
    ticker = request.form['ticker']
    one_yrs_ago = datetime.date.today() - relativedelta(years=1) 
    type_list = request.form.getlist('pricetype')
    p_type = ','.join(type_list)
    
    req = requests.get('https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?date.gte='
                       + str(one_yrs_ago) + '&qopts.columns=ticker,date,' 
                       + p_type + '&api_key=RQvziVWcARiHqhMdCcvt&ticker='
                       + ticker)
    if not req.ok:
        return render_template("error.html")
    #get the column names
    col_names = pandas.read_json(json.dumps(req.json()['datatable']['columns']))['name'].values
    #get the data
    data_df = pandas.read_json(json.dumps(req.json()['datatable']['data']))    
    #combine the column names with data
    data_df.columns = col_names
    
    p = figure(title = 'Quandl WIKI EOD Stock Prices', x_axis_label='date', y_axis_label='price', x_axis_type = 'datetime')
    y = []
    for t in type_list:
        y.append(data_df[t])
    x = []
    for j in range(len(y)):
        x.append(pandas.to_datetime(data_df['date']))
    color = ['red', 'green', 'cyan', 'blue']        
    mypalette=color[0:len(y)]
    legend = [ticker + ': ' + t for t in type_list]
    
    for (colr, leg, x, y ) in zip(mypalette, legend, x, y):
        p.line(x, y, color= colr, legend= leg, alpha = 0.5)
    
    # Embed plot into HTML via Flask Render
    script, div = components(p)
    
    return render_template('graph.html', script = script, div = div, ticker = ticker)

if __name__ == '__main__':
  app.run(port=33507)
