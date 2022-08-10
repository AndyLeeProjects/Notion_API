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
        self.database_id = secret.notion_API("DATABASE_ID")
        self.token_key = secret.notion_API("token_key")
        self.notion_url = 'https://api.notion.com/v1/databases/'

    def query_databases(self):
        database_url = self.notion_url + self.database_id + "/query"
        response = requests.post(database_url, headers={"Authorization": self.token_key, "Notion-Version":'2021-05-13'})
        if response.status_code != 200:
            raise ValueError(f'Response Status: {response.status_code}')
        else:
            self.data = response.json()
    
    def get_projects_titles(self):
        most_properties = [len(self.data['results'][i]['properties'])
                                for i in range(len(self.data["results"]))]
        self.titles = list(self.data["results"][np.argmax(most_properties)]["properties"].keys())
    
    def get_projects_data(self):
        projects_data = {}
        duration_temp = []        
        for p in self.titles:
            if "Related" in p:
                pass
            elif p !="To-do" and p != 'Duration':
                projects_data[p] = [self.data["results"][i]["properties"][p]["checkbox"]
                                    for i in range(len(self.data["results"]))]
            elif p=="To-do":
                names = [self.data['results'][i]['properties']['To-do']['title'][0]['text']['content']
                                    for i in range(len(self.data["results"]))]
            elif p=="Duration":
                for i in range(len(self.data["results"])):
                    try:
                        duration_temp.append(self.data['results'][i]['properties']['Duration']['number'])
                    except:
                        duration_temp.append(None)
                projects_data[p] = duration_temp

        # When everything is NULL, it causes KeyError
        try:
            projects_data['Duration']
        except KeyError:
            projects_data['Duration'] = [None]*len(names)

        return projects_data,names
    
    def retrieve_data(self):
        Notion = connect_NotionDB(self.database_id, self.token_key)
        db = Notion.query_databases()
        titles = Notion.get_projects_titles()
        data = Notion.get_projects_data()
        
        return data
    
    
database_id = secret.notion_API("DATABASE_ID")
token_key = secret.notion_API("token_key")

Notion = connect_NotionDB(database_id, token_key)
data = Notion.retrieve_data()
