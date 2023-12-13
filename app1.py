# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 10:46:28 2023

@author: jozef.hubrechts
"""
import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.graph_objs as go
import pandas as pd
import dash_auth





DATA = pd.read_pickle("sensorDATA.pkl")
USERNAME_PASSWORD_PAIRS = [['JamesBond', '007'],['4stem','isfun']]

app = Dash(__name__)
auth = dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)
server = app.server

#sensorList=['field1', 'field2', 'field3', 'field4', 'field5', 'field6', 'field7', 'field8']
sensorDict = {'field1': 'CO2(ppm)', 'field2': 'PM10(µg/m³)', 'field3': 'PM2.5(µg/m³)', 'field4': 'temperatuur(°C)',
              'field5': 'RH(%)', 'field6': 'R_VOC(ohm)', 'field7': 'eCO2(ppm)', 'field8': 'VOC(PPB)'}
sensor_options = []
for sensor in sensorDict:
    sensor_options.append({'label': sensorDict[sensor], 'value': sensor})
print(sensor_options)

lokaalDict = {1: 'sensor1', 2: 'sensor2', 3: 'sensor3', 4: 'sensor4',
              5: 'sensor5', 6: 'sensor6', 7: 'sensor7'}
lokaal_options = []
for lokaal in lokaalDict:
    lokaal_options.append({'label': lokaalDict[lokaal], 'value': lokaal})
print(lokaal_options)

app.layout = html.Div([
    html.H1('Grafische voorstelling van de meetresultaten'),
    dcc.Graph(id='Overzichtsgrafiek'),
    html.H4('Kies een sensortype'),
    dcc.Dropdown(id='keuzeSensor', options=sensor_options, value='field3',multi=True),
    html.H4('Kies een lokaal'),
    dcc.Dropdown(id='keuzeLokaal', options=lokaal_options, value=list(range(1,8)),multi=True)
])


@app.callback(Output('Overzichtsgrafiek', 'figure'),
              [Input('keuzeSensor', 'value'), Input('keuzeLokaal', 'value')])
def update_figure(sensorType, lokaalnummer):
    print(sensorType, lokaalnummer)
    if isinstance(lokaalnummer, list)==0:
        lokaalnummer=[lokaalnummer]
    if isinstance(sensorType, list)==0:
        sensorType=[sensorType]  
    traces = []
    for n in lokaalnummer:
        for sensorField in list(sensorType):
            trace = go.Scatter({'x': DATA['created_at'][DATA['sensor'] == n],
                            'y': DATA[sensorField][DATA['sensor'] == n],
                           'name':"Sensor"+str(n)+", "+sensorDict[sensorField]})
            traces.append(trace)
        #traces.append(trace)
   
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'tijd'},
            yaxis={'title': 'meetwaarde'},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server()
