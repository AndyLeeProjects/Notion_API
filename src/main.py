# -*- coding: utf-8 -*-

import requests, os
import numpy as np
import pandas as pd
import json
from retrieve import ConnectNotion
from update import update_notion

class NotionAPI:
    def __init__(self, token_key:str):
        """
        __init__(): Instantiation with the token key and the headers 

        Args:
            token_key (str): token key retrieved from Notion page
        """
        self.token_key = token_key
        self.headers = {
            "Accept": "application/json",
            "Notion-Version": "2021-05-13",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token_key
        }

        
    def get_database(self, database_id:str, filters:dict = None, return_type:str = "dataframe"):
        """
        get_database(): retrieves Notion databases with the specified database, filters, and return type.

        Args:
            database_id (str): database_id found in the Notion database url
            filters (dict, optional): The filtering format can be found here --> https://developers.notion.com/reference/post-database-query-filter. Defaults to None.
            return_type (str, optional): "dataframe" or "json". Defaults to "dataframe".

        Returns:
            data frame or json: returns the results according ot the specified return_type 
        """
        if isinstance(filters, dict) == False and filters != None:
            raise KeyError("Please provide a json format content. Reference: https://developers.notion.com/reference/property-value-object ")
        
        Notion = ConnectNotion(database_id, self.token_key, filters)
        return Notion.retrieve_data(return_type)
    
    
    def update_element_db(self, content:dict, pageId:str):
        """
        update_element_db(): updates a designated element in the database with the provided content & pageId.

        Args:
            content (json): Reference --> https://developers.notion.com/reference/property-value-object 
            pageId (str): _description_
        """
        if isinstance(content, dict) == False:
            raise KeyError("Please provide a json format content. Reference: https://developers.notion.com/reference/property-value-object ")
        elif 'properties' in  content.keys():
            raise KeyError("Please include json inside the 'properties' layer.")
        
        # Update content
        update_notion(content, pageId, self.headers)
        


Notion = NotionAPI("secret_WCXYCVzuU52uLqAdYvJZRtpnd3UD4vR1c85iPFr0n55")
data = Notion.get_database("b550f45159a9473fbe21e570293f11db", return_type="json")
for key in data.keys():
    print(data["results"][0])