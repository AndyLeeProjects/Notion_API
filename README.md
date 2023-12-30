# <img src="https://upload.wikimedia.org/wikipedia/commons/4/45/Notion_app_logo.png" width="50" height="50"> Notion_API - Python SDK

As my involvement with Notion-based projects increased, the need for an efficient bridge to interact with Notion's API became evident. While there are existing unofficial API packages for Notion, predominantly relying on the REST API, our open-source solution stands out by facilitating lighter data movement. It offers expanded input parameters, enabling a swift and extensive range of actions within Notion databases with minimal code.


<br>

## Instructions

### 1. Instantiate the API Call

```python
token_key = "<Your_Token_Key>"
Notion_API = NotionAPI(token_key)  # The NotionAPI class is defined in src/main.py
```

<br>  

### 2. Call Designated Database

```python
database_id = "<Your_Database_ID>"
data = Notion_API.get_database(database_id)
```
By default, `get_database()` returns data as a pandas DataFrame. To receive the original JSON format, pass the additional parameter: `return_type="dataframe"` or `return_type="json"`.

<br>

### 3. Update an Element in the Database

```python
# Retrieve the pageId from the data
pageId = data['pageId'].iloc[0]  # Example

# Example: Update the "Quantity" column with the value 12345
content = {"Quantity": {"number": 12345}}

# Update a row with the specified pageId in the "Quantity" column
Notion_API.update_element_db(content, pageId)
```
Refer to the [Notion API Reference Guide](https://developers.notion.com/reference/property-value-object) for correct formatting of the `content` parameter.

<br>

### 4. Add an Element in the Database

```python
database_id = "<Your_Database_ID>"  # Example

# Example: Add a new date-time value to the "Recorded At" column
content = {"Recorded At": {"date": {"start": date_time}}}

# Add a new row to the specified database with the value in the "Recorded At" column
Notion_API.add_element_db(content, database_id)
```