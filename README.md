# <img src="https://upload.wikimedia.org/wikipedia/commons/4/45/Notion_app_logo.png" width="50" height="50"> Notion_API

As I took on more projects using Notion, it only made sense to create a bridge that would allow me and other potential users to use the API easier and faster. Although Notion unofficial API packages already exist for public usage, relying more on the REST API, our open source provides lighter data movement. Also, with more broad input parameters, it offers a faster and wider range of actions within databases.

<br>

## Instantiate the API Call

```python
token_key = "<Token Key>"
Notion_API = NotionAPI(token_key)
```

<br>  

## Call Designated Database

```python
database_id = "<database_id>"
data = Notion_API.get_database(database_id)
```

The default return type for `get_database()` is pandas data frame, but it can also return the original json format by passing in additional parameter, `return_type = "json"`.

<br>

## Update an Element in the Database

```python
# pageId can be found in the data
pageId = data['pageId'].iloc[0] # Example
content = {"Quantity": {"number": 12345}} # Example

Notion_API.update_element_db(content, pageId)
```

Pleaes checkout the [Reference Guide](https://developers.notion.com/reference/property-value-object) to learn how to correctly input `content` parameter.