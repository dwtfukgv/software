#!/usr/bin/env python
from unittest.mock import patch, MagicMock
from kmAction import (
    query_users, search_history, suggest, latest_edit_list, UnitItem,
    query_dxuid, operation_history, query_limit_operation_history,
    quick_access_list, query_collections, get_space_id_by_mis,
    get_pages_by_space_id, get_child_pages_by_id, get_space_pages
)

class TestKmAction(unittest.TestCase):

    @patch('kmAction.api_request')
    def test_query_users(self, mock_api_request):
        mock_api_request.return_value = {
            "data": {
                "users": [{"name": "John Doe"}, {"name": "Jane Doe"}]
            }
        }
        result = query_users("doe")
        self.assertEqual(result, ["John Doe", "Jane Doe"])

    @patch('kmAction.api_request')
    def test_search_history(self, mock_api_request):
        mock_api_request.return_value = {
            "data": [{"query": "test1"}, {"query": "test2"}]
        }
        result = search_history()
        self.assertEqual(result, [{"query": "test1"}, {"query": "test2"}])

    @patch('kmAction.api_request')
    def test_suggest(self, mock_api_request):
        mock_api_request.return_value = {
            "data": {
                "sugList": [{"sug": "suggestion1"}, {"sug": "suggestion2"}]
            }
        }
        result = suggest("test")
        self.assertEqual(result, ["suggestion1", "suggestion2"])

    @patch('kmAction.api_request')
    def test_last_edit(self, mock_api_request):
        mock_api_request.return_value = {
            "data": {
                "units": [
                    {"page_id": "1", "title": "Page 1", "creator": "User 1", "modify_time": "2023-05-01"},
                    {"page_id": "2", "title": "Page 2", "creator": "User 2", "modify_time": "2023-05-02"}
                ]
            }
        }
        result = latest_edit_list()
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], UnitItem)
        self.assertEqual(result[0].page_id, "1")
        self.assertEqual(result[1].title, "Page 2")

    @patch('kmAction.api_request')
    def test_query_dxuid(self, mock_api_request):
        mock_api_request.return_value = {
            "data": [{"dxuid": "12345", "mis": "user1"}]
        }
        result = query_dxuid("user1")
        self.assertEqual(result, {"dxuid": "12345", "mis": "user1"})

    @patch('kmAction.api_request')
    def test_operation_history(self, mock_api_request):
        mock_api_request.return_value = {
            "data": {
                "units": [
                    {"page_id": "1", "title": "Page 1", "creator": "User 1", "modify_time": "2023-05-01"},
                    {"page_id": "2", "title": "Page 2", "creator": "User 2", "modify_time": "2023-05-02"}
                ]
            }
        }
        result = operation_history()
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], UnitItem)
        self.assertEqual(result[0].page_id, "1")
        self.assertEqual(result[1].title, "Page 2")

    @patch('kmAction.operation_history')
    def test_query_limit_operation_history(self, mock_operation_history):
        mock_operation_history.side_effect = [
            [UnitItem(page_id="1", title="Page 1", creator="User 1", modify_time="2023-05-01")],
            [UnitItem(page_id="2", title="Page 2", creator="User 2", modify_time="2023-05-02")],
            []
        ]
        result = query_limit_operation_history(2)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].page_id, "1")
        self.assertEqual(result[1].title, "Page 2")

    @patch('kmAction.api_request')
    def test_quick_access_list(self, mock_api_request):
        mock_api_request.return_value = {
            "data": {
                "contentVOList": [
                    {"content_key": "1", "content_type": "doc", "title": "Doc 1", "creator": "User 1", "mod_time": "2023-05-01"},
                    {"content_key": "2", "content_type": "doc", "title": "Doc 2", "creator": "User 2", "mod_time": "2023-05-02"}
                ]
            }
        }
        result = quick_access_list(1)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].content_key, "1")
        self.assertEqual(result[1].title, "Doc 2")

    @patch('kmAction.api_request')
    def test_query_collections(self, mock_api_request):
        mock_api_request.side_effect = [
            {
                "data": {
                    "units": [
                        {"page_id": "1", "title": "Page 1", "creator": "User 1", "modify_time": "2023-05-01"},
                        {"page_id": "2", "title": "Page 2", "creator": "User 2", "modify_time": "2023-05-02"}
                    ]
                }
            },
            {"data": {"units": []}}
        ]
        result = query_collections()
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], UnitItem)
        self.assertEqual(result[0].page_id, "1")
        self.assertEqual(result[1].title, "Page 2")

    @patch('kmAction.api_request')
    def test_get_space_id_by_mis(self, mock_api_request):
        mock_api_request.return_value = {
            "data": {"space_id": "space1", "mis": "user1"}
        }
        result = get_space_id_by_mis("user1")
        self.assertEqual(result, {"space_id": "space1", "mis": "user1"})

    @patch('kmAction.api_request')
    def test_get_pages_by_space_id(self, mock_api_request):
        mock_api_request.return_value = {
            "data": {
                "list": [
                    {"content_id": "1", "title": "Page 1", "child_count": 0, "modify_time": "2023-05-01", "modifier": "User 1"},
                    {"content_id": "2", "title": "Page 2", "child_count": 1, "modify_time": "2023-05-02", "modifier": "User 2"}
                ]
            }
        }
        result = get_pages_by_space_id("space1")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].content_id, "1")
        self.assertEqual(result[1].title, "Page 2")

    @patch('kmAction.api_request')
    def test_get_child_pages_by_id(self, mock_api_request):
        mock_api_request.return_value = {
            "data": {
                "list": [
                    {"content_id": "3", "title": "Child Page 1", "child_count": 0, "modify_time": "2023-05-03", "modifier": "User 3"},
                ]
            }
        }
        result = get_child_pages_by_id("space1", "2")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].content_id, "3")
        self.assertEqual(result[0].title, "Child Page 1")

    @patch('kmAction.get_pages_by_space_id')
    @patch('kmAction.get_child_pages_by_id')
    def test_get_space_pages(self, mock_get_child_pages, mock_get_pages):
        mock_get_pages.return_value = [
            MagicMock(content_id="1", title="Page 1", child_count=1, modify_time="2023-05-01", modifier="User 1"),
            MagicMock(content_id="2", title="Page 2", child_count=0, modify_time="2023-05-02", modifier="User 2")
        ]
        mock_get_child_pages.return_value = [
            MagicMock(content_id="3", title="Child Page 1", child_count=0, modify_time="2023-05-03", modifier="User 3")
        ]
        result = get_space_pages("space1")
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].content_id, "1")
        self.assertEqual(result[1].content_id, "3")
        self.assertEqual(result[2].content_id, "2")
        self.assertEqual(result[1].path, "/Page 1")

if __name__ == '__main__':
    unittest.main()
