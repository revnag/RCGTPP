# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 14:08:04 2024

@author: HP
"""

import pandas as pd
import plotly.io as pio
from dash import Dash,html,dcc,Input,Output,callback
import plotly.express as px
import dash_bootstrap_components as dbc
import sidefunc as s

pio.renderers.default='browser'

# Plotly and Dash Reading RINGO output 
tppW = pd.read_csv('tppW.csv')
tppPos = pd.read_csv('tppPos.csv')
tppTec = pd.read_csv('tppTec.csv')

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP],
                            meta_tags=[{'name': 'viewport',
                            'content': "width=device-width, initial-scale=1"}] )

server = app.server


SIDEBAR_STYLE = {
    "margin": "1rem 0rem 2rem ",
    "padding": "1rem 1rem 4rem ","background-color": "#f8f9fa"}
GRAPH_STYLE = {
    "margin": "1rem 0rem 2rem ",
    "padding": "2rem 1rem ",
    "background-color": "#f8f9fa"}
sidebar = html.Div([
  html.H3("Select Site to View Graphs",style={'font-size':'18px','color':'green','text-decoration': 'underline','justify':'left'}),
  dbc.Col([dcc.Dropdown(id='site-dropdown',options={'IITK':'IIT Kanpur','BOMB':'IIT Bombay',
                      'MANI':'MANIT','ROPA':'IIT Ropar','TRIV':'IIST','DHAN':'IIT(ISM)'},value='IITK') 
          ],style={"width": "75%"},),
  html.Br(),
  html.H3("Mean Positions (IITK fixed).Select station other than IITK",style={'font-size':'15px','color':'red','justify':'center'}),
  dcc.Checklist(
      id="pos",options={'mean_dN':'dN','mean_dE':'dE','mean_dH':'dH'},
        value=[ ],style={'accent-color':'#A6192E'},inline=True,inputStyle={"margin-right": "10px","margin-left": "10px"},),
  html.Br(),
  html.H3("Atmosphere Module",style={'font-size':'15px','color':'red','justify':'center'}),
  dcc.Checklist(
      id="atm",options={'mean_IPWV':'IPWV','mean_ZTD':'ZTD','mean_ZWD':'ZWD'},
      value=[ ],style={'accent-color':'#A6192E'},inline=True,inputStyle={"margin-right": "10px","margin-left": "10px"},),
  html.Br(),
  html.H3("Ionosphere Module",style={'font-size':'15px','color':'red','justify':'center'}),
  dcc.Checklist(
    id="iono",options={'GPS':'GPS'},
    value= [],style={'accent-color':'#A6192E'},inline=True,inputStyle={"margin-right": "10px","margin-left": "10px"},),
  html.Br(),
  html.H3("Site Map",style={'font-size':'20px','color':'red','justify':'center'}),
  dcc.Checklist(
    id="rcgloc",options=[{"label":"Site Map","value":"loc"}],
    value= ['loc'],style={'accent-color':'#A6192E'},inline=True,inputStyle={"margin-right": "10px","margin-left": "10px"},),  
  
    ],style=SIDEBAR_STYLE,)


# Layout section : Bootstrap               
app.layout = dbc.Container([
# First Row
dbc.Row([
  dbc.Col([dbc.Card([
    dbc.CardImg(src="assets/NCG.png",className = 'align-self-right',top=True)
      ],style = {'width':"6rem",'border':0}),],className="g0",align='center'),
  dbc.Col([html.H1("Trimble Pivot Platform Outputs (RCG)",style={'font-size':'35px'},className='text-success')],
        width={'size':7,'offset':0},className="p-1" "g0",align='center'),
  dbc.Col([dbc.Card([
    dbc.CardImg(src="assets/bluelog.jpg",className = 'align-self-left',top=True)
      ],style = {'width':"6rem",'border':0})],className="go" ,align='center'),
       ],justify='around',style={'marginTop': 20,"height": "6vh"}),
html.Br(),
#First Row A
html.Div([dcc.Markdown(''' 
   **The Trimble® Progressive Infrastructure Via Overlaid Technology (Pivot) Platform is a comprehensive GNSS CORS
   network software designed for managing GNSS reference stations. It offers various applications that can be tailored 
   to meet specific requirements. One key component is the Trimble Integrity Manager App, which features the Post Processing 
   Engine module. This module processes stored raw receiver data, to automatically estimate 
   positions using baseline combinations with overlapping time sequences. It relies on dual-frequency GNSS observations from 
   satellites above a specified elevation and utilizes predicted orbits for accurate positioning. The Trimble Integrity Monitoring
   module, which is connected to the Post Processing Engine, performs a least squares adjustment of the processed baselines. For 
   effective position adjustment, it requires at least one station to be fixed (IITK). Another useful app is the Atmosphere App 
   which is a scientific tool that leverages data from weather stations and GNSS to estimate atmospheric conditions. It employs the 
   Modified Hopfield &#8212 Niell model (for both dry and wet components) and utilizes DCB files to enhance its calculations of total 
   electron content (TEC), thereby improving the accuracy of atmospheric estimations. The platform’s capabilities are further illustrated 
   by the range of graphs presented, enabling users to analyze and study the results effectively.**
            
     '''),],style={'textAlign':'justify','marginBottom': 20,'marginTop': 30,'font-size':'12px',"height": "12vh"}),
    
html.Br(),
html.Br(),


#Third Row        
dbc.Row([
  dbc.Col([sidebar],width=3),
  dbc.Col([dcc.Graph(id='quality-graph',responsive=True)],width='9'),
       ],style={"height": "80vh"}),
],class_name='m-auto' 'p-auto')
html.Br()  
# End Container
@callback(
    Output('quality-graph','figure'),
    Input('site-dropdown','value'),
    Input('pos','value'),
    Input('atm','value'),
    Input('iono','value'),
    Input('rcgloc','value')
    
    )

def graph(site_sel,pos,atm,iono,loc):
       seltppW=tppW[tppW['StationCode']==site_sel]
       seltppPos=tppPos[tppPos['Station']==site_sel]
       seltppTec=tppTec[tppTec['StationCode']==site_sel]
       fig=mymap('rcgloc.csv')

# Creating Graph conditions 
       if loc!= []:
          fig=mymap('rcgloc.csv')
       elif len(pos) > 0:
         if 'mean_dN' in pos:
           yax='mean_dN'
           mycolorVal='red'
           pram='Mean Position '
           sitel=s.label_site(site_sel)
           legend=True
           rangey=[-0.05,0.05]
           fig=pos_graph(seltppPos,yax,rangey,pram,sitel,legend,mycolorVal)   
         elif 'mean_dE' in pos:
            yax='mean_dE'
            mycolorVal='yellow'
            pram='Mean Position '
            sitel=s.label_site(site_sel)
            legend=True
            rangey=[-0.05,0.05]
            fig=pos_graph(seltppPos,yax,rangey,pram,sitel,legend,mycolorVal)   
         else:
            yax='mean_dH'
            mycolorVal='deepskyblue'
            pram='Mean Position '
            sitel=s.label_site(site_sel)
            legend=True
            rangey=[-0.05,0.05]
            fig=pos_graph(seltppPos,yax,rangey,pram,sitel,legend,mycolorVal)   
       elif len(atm) > 0:
         if 'mean_IPWV' in atm:
           yax='mean_IPWV'
           mycolorVal='red'
           pram="IPWV"
           sitel=s.label_site(site_sel)
           legend=True
           fig=atm_graph(seltppW,yax,pram,sitel,legend,mycolorVal) 
         elif 'mean_ZTD' in atm:
           yax='mean_ZTD'
           pram="ZTD"
           sitel=s.label_site(site_sel)
           legend=True
           mycolorVal='blue'
           fig=atm_graph(seltppW,yax,pram,sitel,legend,mycolorVal) 
         elif 'mean_ZWD' in atm:
           yax='mean_ZWD'
           pram="ZWD"
           sitel=s.label_site(site_sel)
           legend=True
           mycolorVal='green'
           fig=atm_graph(seltppW,yax,pram,sitel,legend,mycolorVal) 
       elif len(iono) > 0:
           yax='mean_tec'
           pram="TEC"
           sitel=s.label_site(site_sel)
           legend=True
           mycolorVal='green'
           fig=atm_graph(seltppTec,yax,pram,sitel,legend,mycolorVal) 
       return fig  


def mymap(file):
# Creating Location map
  df = pd.read_csv(file)
  rcgloc = px.scatter_mapbox(df, lat="Lat", lon="Lon",zoom=1.5, mapbox_style='open-street-map',text= df['SName'],hover_data=["Type"],
                             color='Type',color_discrete_map={"IGS": "#FF6347", "RCG": "forestgreen","NCG":"darkviolet"})
  rcgloc.update_traces(hovertemplate="%{text}<br>Site Type: %{customdata[0]}<br>Lat: %{lat}<br>Lon:%{lon}<br>")
  rcgloc.update_layout(hoverlabel=dict(bgcolor="white",font_size=10,font_family="Rockwell"))
  rcgloc.update_traces(marker=dict(size=8))
  rcgloc.update_traces(textposition='top right',textfont=dict(color='blue',size=11),
                  mode='markers+text')
  rcgloc.update_mapboxes(center_lat=21.9,center_lon=80.3)
  rcgloc.update_layout(margin=dict(l=20, r=20, t=20, b=20))
  rcgloc.update_layout(legend_title='Site Type')
                       
  return rcgloc  

def pos_graph(possel,yax,rangey,pram,sitel,legend,mycolorVal):
  fig = px.scatter(possel,template="plotly_dark",y=yax, x="DOY",
        labels={"DOY": 'Day of year 2024'},title=f'{pram}  of {sitel}',)
  fig.update_layout(yaxis_title='Component in mm',legend_title=f' {yax}')
  fig.update_traces(error_y=dict(color='#00FFFF',thickness=0.4))
  fig.update_traces(showlegend=legend)
  fig.update_traces(marker=dict(size=5,color=mycolorVal))
  fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='LightPink')
  fig.update_layout(hoverlabel=dict(bgcolor="white",font_size=16,font_family="Rockwell"))
  fig.update(layout=dict(title=dict(x=0.5,y=0.9,))) 
  fig.update_layout(legend=dict(orientation='h',bordercolor="White",y=1,x=1,borderwidth=1))
  fig.update_layout(yaxis_range=rangey)
  return fig       


def atm_graph(df,yax,pram,sitel,legend,mycolorVal):   
# Constellation independent Information
  line_fig1=px.line(df,template="ggplot2",color_discrete_sequence=[mycolorVal],
      x='DOY',y=yax,labels={"DOY": 'Day of year 2024','mean_ZWD':'ZWD (m)',
      'mean_ZTD':'ZTD (m)','mean_IPWV':'IPWV (m)','mean_tec':'TEC (mm)'},
      title=f'{pram} values {sitel}',)
  line_fig1.update_layout(showlegend=legend,)
  line_fig1.update_traces(mode="markers+lines",marker=dict(size=3))
  line_fig1.update_layout(hoverlabel=dict(bgcolor="white",font_size=16,font_family="Rockwell"))
  line_fig1.update(layout=dict(title=dict(x=0.5,y=0.9, )))
  return line_fig1    


if __name__=='__main__':
    app.run_server(debug=True)
    
