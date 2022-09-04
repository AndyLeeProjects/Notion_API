# -*- coding: utf-8 -*-

def update_Notion(name: str, content, pageId: str, headers):
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
        "properties": {
            name: content
        }}

    response = requests.request("PATCH", update_url,
                                headers=headers, data=json.dumps(update_properties))
