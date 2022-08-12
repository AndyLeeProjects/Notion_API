# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 14:02:35 2022

@author: anddy
"""

import requests
import sys
import numpy as np
from datetime import datetime
sys.path.append('C:\\NotionUpdate\progress')
from secret import secret
import pandas as pd
import os
import mysql.connector as MC




class connect_NotionDB:
    def __init__(self, database_id, token_key):
        self.database_id = database_id
        self.token_key = token_key

    def query_databases(self):
        database_url = 'https://api.notion.com/v1/databases/' + self.database_id + "/query"
        response = requests.post(database_url, headers={"Authorization": self.token_key, "Notion-Version":'2021-05-13'})
        if response.status_code != 200:
            raise ValueError(f'Response Status: {response.status_code}')
        else:
            self.json = response.json()
        return self.json
            
    def get_projects_titles(self):
        most_properties = [len(self.json['results'][i]['properties'])
                                for i in range(len(self.json["results"]))]
        
        # Find the index with the maximum length
        self.max_ind = np.argmax(most_properties)
        self.titles = list(self.json["results"][self.max_ind]["properties"].keys())
        return self.titles
    
    def clean_data(self):
        
        data = {}
        for title in self.titles:
            
            # Get type of the variable and use it as a filtering tool
            title_type = self.json['results'][self.max_ind]['properties'][title]['type']
                        
            data[title] = [self.json['results'][i]['properties'][title][title_type]
                           for i in range(len(self.json['results']))]
        
        for key in data.keys():
            row_num = len(data[key])
            try:
                data[key] = [data[key][i][0]['name'] for i in range(row_num)]
            except:
                pass
            
            try:
                data[key] = [data[key][i][0]['text']['content'] for i in range(row_num)]
            except:
                pass
            
            try:
                data[key] = [data[key][i]['number'] for i in range(row_num)]
            except:
                pass
            
            #try:
            #    data[key] = [[data[key][i][j]['name']] for i in range(row_num) for j in range(data[key][i])]
            #except:
            #    pass
            
        self.data = data
        return data
    
    def retrieve_data(self):
        Notion = connect_NotionDB(self.database_id, self.token_key)
        db = Notion.query_databases()
        titles = Notion.get_projects_titles()
        data = pd.DataFrame(Notion.clean_data())
        
        return data
    
    
database_id = "b8844373ea4240929bac6e3d6044cb89"
token_key = secret.notion_API("token")

Notion = connect_NotionDB(database_id, token_key)
data = Notion.query_databases()
sample = data['results'][0]['properties']
titles = Notion.get_projects_titles()
dat = Notion.clean_data()
data = Notion.retrieve_data()

types = []
for k in sample.keys():
    if sample[k]['type'] not in types:    
        types.append(sample[k]['type'])

