from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px
import requests
from pathlib import Path

app = Flask(__name__)

with open('data.json', 'r') as file:
   data = json.load(file)

with open('theme_transportation.json', 'r') as file:
   transport = json.load(file)

@app.route('/metrics')
def notdash():
   df = pd.DataFrame(data)
   keys = list(data.keys())
   
   fig = px.bar(df, x=keys[0], y=keys[1], color=keys[2], barmode='group')
   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

   pi = px.pie(df, names=keys[0],values=keys[1])
   piJSON = json.dumps(pi, cls=plotly.utils.PlotlyJSONEncoder)

   sun = px.sunburst(df, path=[keys[0], keys[1]])
   sunJSON = json.dumps(sun, cls=plotly.utils.PlotlyJSONEncoder)

   box = px.box(df, x=keys[2], y=keys[1], color=keys[0])
   box.update_traces(quartilemethod="inclusive")
   boxJSON = json.dumps(box, cls=plotly.utils.PlotlyJSONEncoder)

   return render_template('notdash.html', graphJSON=graphJSON, piJSON=piJSON, sunJSON=sunJSON, boxJSON=boxJSON)

@app.route('/themes')
def ckanhardcore():
   data = getRequestJson('https://catalog.data.gov/api/action/package_search?facet.field=[%22theme%22]&facet.limit=25&rows=0')
   themes = data['result']['facets']['theme']
   return render_template('taxonomy.html', themes=themes)


@app.route('/themes/<theme>')
def ckanmoretheme(theme):
   data = getRequestJson(('https://catalog.data.gov/api/action/package_search?fq=theme:"{theme}"&facet.field=[%22tags%22]&facet.limit=100&rows=0'.format(theme=theme)))
   tags = data['result']['facets']['tags']
   return render_template('taxonomy.html', tags=tags, theme=theme)


def getRequestJson(url):
   return requests.get(url).json()
