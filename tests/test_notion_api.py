import pytest
from unittest.mock import patch
import sys
sys.path.append('src')
from main import NotionAPI

@pytest.fixture
def notion_api():
    return NotionAPI(token_key="fake_token")

@patch('main.ConnectNotion')
def test_get_database(mock_connect, notion_api):
    # Setup the mock
    mock_instance = mock_connect.return_value
    mock_instance.retrieve_data.return_value = "mocked data"

    # Execute the method under test
    result = notion_api.get_database(database_id="fake_id")

    # Assertions
    mock_connect.assert_called_with(database_id="fake_id", token_key="fake_token", filters=None)
    mock_instance.retrieve_data.assert_called_with("dataframe")
    assert result == "mocked data"

@patch('main.update_notion')
def test_update_element_db(mock_update, notion_api):
    # Prepare test data
    content = {"some": "data"}
    pageId = "fake_pageId"

    # Execute the method under test
    notion_api.update_element_db(content, pageId)

    # Assert that the mock was called correctly
    mock_update.assert_called_once_with(content, pageId, notion_api.headers)

@patch('main.add_new_row_to_notion_database')
def test_add_element_db(mock_add_new, notion_api):
    # Set up test data
    content = {"other": "data"}
    databaseId = "fake_databaseId"

    # Call the method
    notion_api.add_element_db(content, databaseId)

    # Assertions
    mock_add_new.assert_called_once_with(content, databaseId, notion_api.headers)
