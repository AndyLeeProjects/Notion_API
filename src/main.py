from utils.notion.retrieve import ConnectNotion
from utils.notion.update import update_notion, add_new_row_to_notion_database


class NotionAPI:
    def __init__(self, token_key: str):
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

    def get_database(self, database_id: str = None, filters: dict = None,
                     return_type: str = "dataframe", user_db: bool = False):
        """
        get_database(): retrieves Notion databases with the specified database, filters, and return type.
        Args:
            database_id (str): database_id found in the Notion database url
            filters (dict, optional): The filtering format can be found here\
                --> https://developers.notion.com/reference/post-database-query-filter. Defaults to None.
            return_type (str, optional): "dataframe" or "json". Defaults to "dataframe".
        Returns:
            data frame or json: returns the results according ot the specified return_type
        """
        if not isinstance(filters, dict) and filters is not None:
            raise KeyError("Please provide a json format content.\
                            Reference: https://developers.notion.com/reference/property-value-object ")

        if database_id is None and not user_db:
            raise KeyError("Please provide a database_id or set user_db to True.")
        elif user_db:
            Notion = ConnectNotion(token_key=self.token_key, filters=filters, user_db=True)
        else:
            Notion = ConnectNotion(database_id=database_id, token_key=self.token_key, filters=filters)

        return Notion.retrieve_data(return_type)

    def update_element_db(self, content: dict, pageId: str):
        """
        update_element_db(): updates a designated element in the database with the provided content & pageId.
        Args:
            content (json): Reference --> https://developers.notion.com/reference/property-value-object
            pageId (str): _description_
        """
        if not isinstance(content, dict):
            raise KeyError("Please provide a json format content.\
                            Reference: https://developers.notion.com/reference/property-value-object")
        elif 'properties' in content.keys():
            raise KeyError("Please include json inside the 'properties' layer.")
        else:
            # Update content
            update_notion(content, pageId, self.headers)
    
    def add_element_db(self, content: dict, databaseId: str):
        """
        add_element_db(): adds a new element in the database with the provided content & databaseId.
        Args:
            content (json): Reference --> https://developers.notion.com/reference/property-value-object
            databaseId (str): _description_
        """
        if not isinstance(content, dict):
            raise KeyError("Please provide a json format content.\
                            Reference: https://developers.notion.com/reference/property-value-object")
        elif 'properties' in content.keys():
            raise KeyError("Please include json inside the 'properties' layer.")
        else:
            # Update content
            add_new_row_to_notion_database(content, databaseId, self.headers)
