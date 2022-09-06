# -*- coding: utf-8 -*-

import requests, os
import numpy as np
import pandas as pd
import json
from src.retrieve import ConnectNotionDB
from src.update import update_Notion

class NotionAPI:
    def __init__(self, token_key:str):
        self.token_key = token_key
        self.headers = {
            "Accept": "application/json",
            "Notion-Version": "2021-05-13",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token_key
        }

        
    def get_database(self, database_id:str, filters:dict = None, return_type:str = "dataframe"):
        Notion = ConnectNotionDB(database_id, self.token_key, filters)
        return Notion.retrieve_data(return_type)
    
    def update_element_db(self, content:dict, pageId:str):
        update_Notion(content, pageId, self.headers)
        