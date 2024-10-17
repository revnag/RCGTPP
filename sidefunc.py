# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 09:26:04 2024

@author: HP
"""
import plotly.express as px
def label_pram(dropdown_value: str):
    value=['MP1','MP2','MP5','OSMP1','OSMP2','OSMP5','OSGF','OSMW','OSIOD' ,
           'S1','S2','S5X']  
    label=['Multipath12','Multipath21','Multipath15','Obs per Slip:MP12',
    'Obs per Slip:MP21','Obs per Slip:MP15','Obs per Slip:GF','Obs per Slip:MW',
    'Obs per Slip:IOD','Signal to Noise Ration on L1',
    'Signal to Noise Ration on L2',
    'Signal to Noise Ration on L5']
    for i in range(len(value)):
       if dropdown_value==value[i]:
           return label[i]
def label_site(dropdown_value: str):
    value=['IITK','BOMB','MANI','ROPA','TRIV','DHAN']
    label=['IIT Kanpur','IIT Bombay','MANIT','IIT Ropar','IIST','IIT(IISM]']
    for i in range(len(value)):
       if dropdown_value==value[i]:
           return label[i]

def SetColor(value):
    if(value==2):
        return " red"
    elif(value ==3 ):
        return "blue"
    elif(value == 4):
        return "green"
    elif(value==1):
        return 
      

    