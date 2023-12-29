import requests
import numpy as np
import pandas as pd
import json

""" ConnectNotion

__init__:
            Basic setup using database_id & token_key


query_database:
            Sends request to Notion database using the provided information
                - The retrieved data is in JSON format, which will need cleaning


get_all_pages:
            Notion has a retrieval limit of 100 elements for each request.
            Thus, this method reads values from all pages.


get_projects_titles:
            Collects title names of the given database.


clean_data & extract_nested_elements:
            Organizes JSON data into a cleaner dictionary.
            However, each variable has varying number of nested objects.
            In other words, we need different line of code to access different types of elements.
            So extract_nested_elements function generates different codes to help complete the
            cleaning process.


retrieve_data:
            Runs all methods in the script in order and returns a clean dataframe.


"""


class ConnectNotion:
    def __init__(self, token_key: str, database_id: str = None, filters: dict = None, user_db: bool = False):
        """
        Initial Setup
        Args:
            database_id (str): database id can be found in the database url
            token_key (str): token key can be found in Notion page (Under Inspect).
            filters (dict): filters used when calling Notion API
        """
        self.database_id = database_id
        self.token_key = token_key
        self.user_db = user_db
        self.headers = {
            "Accept": "application/json",
            "Notion-Version": "2021-05-13",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token_key
        }
        self.user_headers = {
            "Authorization": f"Bearer {self.token_key}",
            "Notion-Version": "2021-05-13"  # Specify the Notion API version
        }

        if filters is not None:
            self.filters = {"filter": filters}
        else:
            self.filters = None

    def query_user_database(self):
        user_url = "https://api.notion.com/v1/users"
        response = requests.get(user_url, json=self.filters, headers=self.user_headers)

        if response.status_code != 200:
            raise ValueError(f"Response Status: {response.status_code}")
        else:
            self.json = response.json()

    def query_databases(self):
        """
        Requests Notion for an access to the designated database.
        Raises:
            ValueError: ValueError raised with incorrect input.
        Returns:
            JSON data
        """
        database_url = "https://api.notion.com/v1/databases/" + self.database_id + "/query"
        response = requests.post(database_url, json=self.filters, headers=self.headers)

        if response.status_code != 200:
            raise ValueError(f"Response Status: {response.status_code}")
        else:
            self.json = response.json()

    def get_all_pages(self):
        """
        Scrolls through all pages in the database.
            - Only applies when there are more than 100 elements in the database.
        Returns:
            List of all results.
        """
        if self.user_db:
            read_url = "https://api.notion.com/v1/users"
        else:
            read_url = f"https://api.notion.com/v1/databases/{self.database_id}/query"

        all_results = []  # Accumulate results from all pages

        try:
            # Initial request to get the first set of results
            data_hidden = json.dumps(self.json)
            data_hidden = requests.post(
                read_url, json=self.filters, headers=self.headers, data=data_hidden
            ).json()

            # Accumulate the initial set of results
            all_results += data_hidden["results"]

            # Check if there are more pages to retrieve
            while data_hidden.get("has_more"):
                print(f"Reading database row {len(all_results) + 1}...")

                # Set the starting cursor for the next page
                self.json["start_cursor"] = data_hidden.get("next_cursor")

                # Send the request for the next page
                data_hidden = json.dumps(self.json)
                data_hidden = requests.post(
                    read_url, json=self.filters, headers=self.headers, data=data_hidden
                ).json()

                # Accumulate the results from the current page
                all_results += data_hidden["results"]

        except (KeyError, IndexError, TypeError):
            pass

        self.json = {"results": all_results}
        return self.json

    def get_projects_titles(self):
        """
        Collects the titles from the row with maximum number of title names
            - when there is empty input(s) in Notion DB, the title name does not appear
            in the retrieved JSON data. Therefore, by finding the maximum number of
            "non-empty" row provides the maximum number of titles names.
            - page_id tag is also added, which will allow users to modify their Notion
            page using code.
        Returns:
            list: title or column names of the database
        """

        most_properties = [len(self.json["results"][i]["properties"])
                           for i in range(len(self.json["results"]))]

        # Find the index with the maximum length
        try:
            self.max_ind = np.argmax(most_properties)
            self.titles = list(self.json["results"][self.max_ind]["properties"].keys())
        except ValueError:
            error_msg = "No data found in the database. Please check your database."
            raise ValueError(error_msg)

    def clean_data(self):
        """
        Cleans JSON data using title_type
            - Types include created_time, number, checkbox, last_edited_time, multi_select
            select, rich_text, select, title, etc.
        Returns:
            dictionary: organized data
        """
        self.data = {}
        for title in self.titles:
            # Get the type of the variable and use it as a filtering tool
            title_type = self.json["results"][self.max_ind]["properties"][title]["type"]
            temp = []
            page_id = []
            for i in range(len(self.json["results"])):
                try:
                    val = self.json["results"][i]["properties"][title][title_type]
                    val = np.nan if val == [] else val
                    temp.append(val)
                    page_id.append(self.json["results"][i]["id"])
                except (KeyError, IndexError, TypeError):
                    temp.append(np.nan)
            self.data[title] = temp
            self.data["pageId"] = page_id

        # get in-depth json
        for key in self.data.keys():
            row_num = len(self.data[key])

            self.data[key] = [ConnectNotion.extract_nested_elements(self.data, key, ind)
                              for ind in range(row_num)]

        return self.data

    def get_users_data(self):
        results = self.json["results"]
        data = pd.DataFrame(results)
        self.data = pd.concat([data.drop(['person'], axis=1), data['person'].apply(pd.Series)], axis=1)

        return self.data

    def extract_nested_elements(data, key, ind):
        """
        Even after cleaning the data, JSON type elements will still exist.
           Thus, this function provides nested_type, which will allow complete access to all elements.
        Args:
            data (dictionary): cleaned data
            key (str): title name
            ind (int): index of the passed element
        Returns:
            nested_type: provides the nested_type
        """

        try:
            nested_type = data[key][ind][0]["name"]
            # In the case for type external url
            if data[key][ind][0]['type'] == 'external' and 'http' in data[key][ind][0]['external']['url']:
                return data[key][ind][0]['external']['url']
            else:
                return nested_type
        except (KeyError, IndexError, TypeError):
            pass

        # Multi-select
        try:
            if isinstance(data[key][ind], dict):
                nested_type = data[key][ind]["name"]
            elif isinstance(data[key][ind], list):
                nested_type = [data[key][ind][i]["name"] for i in range(len(data[key][ind]))]
            else:
                nested_type = data[key][ind]["name"]
            return nested_type
        except (KeyError, IndexError, TypeError):
            pass

        try:
            nested_type = data[key][ind][0]["text"]["content"]
            return nested_type
        except (KeyError, IndexError, TypeError):
            pass

        try:
            nested_type = data[key][ind]["number"]
            return nested_type
        except (KeyError, IndexError, TypeError):
            pass

        try:
            nested_type = data[key][ind]["start"]
            return nested_type
        except (KeyError, IndexError, TypeError):
            pass

        try:
            nested_type = data[key][ind]
            return nested_type
        except (KeyError, IndexError, TypeError):
            pass

    def get_meta_data(self):

        for key in self.data.keys():
            self.meta_data[key] = {"type": self.json["results"][self.max_ind]["properties"][key]["type"],
                                   "length": len(self.data[key])}

    def retrieve_data(self, return_type: str = "dataframe"):
        """
        retrieve_data(): Retrieves data from the designated database in Notion by running all methods above.
        Args:
            return_type (str): define in which format data is outputted
            - "dataframe"
            - "json"
        Returns:
            data in specified type(format)
        """

        if self.user_db:
            self.query_user_database()
        else:
            self.query_databases()

        jsn_all = self.get_all_pages()
        if return_type == "json":
            return jsn_all

        if return_type == "dataframe":
            if self.user_db:
                df = self.get_users_data()
            else:
                self.get_projects_titles()
                df = pd.DataFrame(self.clean_data())
                df["Index"] = range(0, len(df))
            return df
