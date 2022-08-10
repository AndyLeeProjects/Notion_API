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
        self.notion_url = 'https://api.notion.com/v1/databases/'

    def query_databases(self):
        database_url = self.notion_url + self.database_id + "/query"
        response = requests.post(database_url, headers={"Authorization": self.token_key, "Notion-Version":'2021-05-13'})
        if response.status_code != 200:
            raise ValueError(f'Response Status: {response.status_code}')
        else:
            self.json = response.json()
        return self.json
            
    def get_projects_titles(self):
        most_properties = [len(self.json['results'][i]['properties'])
                                for i in range(len(self.json["results"]))]
        self.titles = list(self.json["results"][np.argmax(most_properties)]["properties"].keys())
        return self.titles
    
    def get_DB_data(self):
        data = {}
        duration_temp = []        
        for p in self.titles:
            if "Related" in p:
                pass
            elif p !="To-do" and p != 'Duration':
                data[p] = [self.json["results"][i]["properties"][p]["checkbox"]
                                    for i in range(len(self.json["results"]))]
            elif p=="To-do":
                names = [self.json['results'][i]['properties']['To-do']['title'][0]['text']['content']
                                    for i in range(len(self.json["results"]))]
            elif p=="Duration":
                for i in range(len(self.json["results"])):
                    try:
                        duration_temp.append(self.json['results'][i]['properties']['Duration']['number'])
                    except:
                        duration_temp.append(None)
                data[p] = duration_temp

        # When everything is NULL, it causes KeyError
        try:
            data['Duration']
        except KeyError:
            data['Duration'] = [None]*len(names)
        
        self.data = data
        return data,names
    
    def retrieve_data(self):
        Notion = connect_NotionDB(self.database_id, self.token_key)
        db = Notion.query_databases()
        titles = Notion.get_projects_titles()
        data = Notion.get_DB_data()
        
        return data
    
    
database_id = "b8844373ea4240929bac6e3d6044cb89"
token_key = secret.notion_API("token")

Notion = connect_NotionDB(database_id, token_key)
data = Notion.query_databases()
titles = Notion.get_projects_titles()
data = Notion.retrieve_data()
sample = data['results'][0]
"""
{'object': 'page',
 'id': '0174e92f-db98-4ac5-8d1b-99888a09f9f0',
 'created_time': '2022-08-10T18:57:00.000Z',
 'last_edited_time': '2022-08-10T19:01:00.000Z',
 'created_by': {'object': 'user',
  'id': '05f9e30a-01f5-4662-87eb-060babc25fbe'},
 'last_edited_by': {'object': 'user',
  'id': '05f9e30a-01f5-4662-87eb-060babc25fbe'},
 'cover': None,
 'icon': None,
 'parent': {'type': 'database_id',
  'database_id': 'b8844373-ea42-4092-9bac-6e3d6044cb89'},
 'archived': False,
 'properties': {'int': {'id': '@F?g', 'type': 'number', 'number': 3},
  'phone': {'id': 'CC]`',
   'type': 'phone_number',
   'phone_number': '234-512-5837'},
  'Property 1': {'id': 'KMe}',
   'type': 'files',
   'files': [{'name': 'https://www.google.com/search?q=sally&oq=sally&aqs=chrome..69i57j46i67i131i199i433i465j46i67j46i67i433l2j46i67j46i67i433j46i67j46i131i433i512j46i512.609j0j7&sourceid=chrome&ie=UTF-8',
     'type': 'external',
     'external': {'url': 'https://www.google.com/search?q=sally&oq=sally&aqs=chrome..69i57j46i67i131i199i433i465j46i67j46i67i433l2j46i67j46i67i433j46i67j46i131i433i512j46i512.609j0j7&sourceid=chrome&ie=UTF-8'}}]},
  'Property': {'id': 'LfeV',
   'type': 'people',
   'people': [{'object': 'user',
     'id': '05f9e30a-01f5-4662-87eb-060babc25fbe',
     'name': 'Andy Lee',
     'avatar_url': 'https://lh3.googleusercontent.com/a-/AAuE7mAEtRZIVFfnVeuEd8Wq2uZ-l2Sew3UjiV2c_XFl=s100',
     'type': 'person',
     'person': {'email': 'jal19@geneseo.edu'}}]},
  'formula': {'id': 'NQ@t',
   'type': 'formula',
   'formula': {'type': 'number', 'number': 303.124125}},
  'Tags': {'id': 'QrZR',
   'type': 'rich_text',
   'rich_text': [{'type': 'text',
     'text': {'content': 'tag3', 'link': None},
     'annotations': {'bold': False,
      'italic': False,
      'strikethrough': False,
      'underline': False,
      'code': False,
      'color': 'default'},
     'plain_text': 'tag3',
     'href': None}]},
  'last_edited_by': {'id': 'Qwvr',
   'type': 'last_edited_by',
   'last_edited_by': {'object': 'user',
    'id': '05f9e30a-01f5-4662-87eb-060babc25fbe',
    'name': 'Andy Lee',
    'avatar_url': 'https://lh3.googleusercontent.com/a-/AAuE7mAEtRZIVFfnVeuEd8Wq2uZ-l2Sew3UjiV2c_XFl=s100',
    'type': 'person',
    'person': {'email': 'jal19@geneseo.edu'}}},
  'select': {'id': 'YdjZ',
   'type': 'select',
   'select': {'id': '162c75a5-04b2-4e2a-9e78-ccffe93bf29b',
    'name': 'select3',
    'color': 'brown'}},
  'status': {'id': 'jxX`',
   'type': 'status',
   'status': {'id': '46af5c46-6a3f-446d-a0ff-75b4e1e1bfa7',
    'name': 'Not started',
    'color': 'default'}},
  'multi_select': {'id': 'vU::',
   'type': 'multi_select',
   'multi_select': [{'id': '3ac34c8d-59b3-4af0-827b-5fe3ea67bfab',
     'name': 'm3',
     'color': 'blue'},
    {'id': 'ff775b50-a198-49f5-82d9-024ad8be003f',
     'name': 'm4',
     'color': 'gray'}]},
  'email': {'id': 'y~{X', 'type': 'email', 'email': 'e3@gmail.com'},
  'Birthday': {'id': '}:f~',
   'type': 'date',
   'date': {'start': '2021-10-27', 'end': None, 'time_zone': None}},
  'Name': {'id': 'title',
   'type': 'title',
   'title': [{'type': 'text',
     'text': {'content': 'Sally', 'link': None},
     'annotations': {'bold': False,
      'italic': False,
      'strikethrough': False,
      'underline': False,
      'code': False,
      'color': 'default'},
     'plain_text': 'Sally',
     'href': None}]}},
 'url': 'https://www.notion.so/Sally-0174e92fdb984ac58d1b99888a09f9f0'}
"""




