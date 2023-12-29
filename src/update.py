import requests
import json

def update_notion(content: dict, pageId: str, headers):
    """_summary_
    Args:
        name (str): name of the column
        content (json): specified details in json format
            - Reference: https://developers.notion.com/reference/property-value-object
            - ex)
                - For date -> {"date": {"start": "2022-09-02"}}
                - For number -> {"number": 100}
        pageId (str): record pageId
        headers (dictionary): headers with the token_key
    """
    update_url = f"https://api.notion.com/v1/pages/{pageId}"

    update_properties = {
        "properties": content
        }

    response = requests.request("PATCH", update_url,
                                headers=headers, data=json.dumps(update_properties))
    print(response, "\n")

def add_new_row_to_notion_database(content: dict, databaseId: str, headers):
    """Adds a new row to a specified Notion database.

    Args:
        content (dict): Property values for the new row in JSON format.
        databaseId (str): The ID of the Notion database where the new row will be added.
        headers (dict): Headers including the authentication token.
    """
    create_url = "https://api.notion.com/v1/pages"

    new_page_data = {
        "parent": {"database_id": databaseId},
        "properties": content
    }

    response = requests.post(create_url, headers=headers, data=json.dumps(new_page_data))
    
    if response.status_code == 200:
        print("New row added successfully.")
    else:
        print(f"Failed to add new row. Status code: {response.status_code}\nResponse: {response.text}")
    return response
