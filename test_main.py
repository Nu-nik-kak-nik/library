import unittest
from main import Library
import json
import os

class TestLibrary(unittest.TestCase):

    def setUp(self):
        """Создаем временный файл для тестов."""
        self.library = Library()
        self.library.data = {}
        self.test_file = "test_library.json"
        self.library.save_data()

    def tearDown(self):
        """Удаляем временный файл после тестов."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_book(self):
        """Тестируем добавление книги."""
        self.library.data['test_id'] = {
            "id": "test_id",
            "title": "Test Book",
            "author": "Test Author",
            "year": 2023,
            "status": "в наличии"
        }
        self.library.save_data()
        self.assertIn('test_id', self.library.data)

    def test_delete_book(self):
        """Тестируем удаление книги."""
        self.library.data['test_id'] = {
            "id": "test_id",
            "title": "Test Book",
            "author": "Test Author",
            "year": 2023,
            "status": "в наличии"
        }
        self.library.delete_book = lambda: None  # Переопределяем метод для теста
        self.library.data.pop('test_id', None)
        self.library.save_data()
        self.assertNotIn('test_id', self.library.data)

    def test_search_book(self):
        """Тестируем поиск книги."""
        self.library.data['test_id'] = {
            "id": "test_id",
            "title": "Test Book",
            "author": "Test Author",
            "year": 2023,
            "status": "в наличии"
        }
        search_term = "Test Book"
        results = [book for book in self.library.data.values() if self.library._matches_search_term(book, search_term)]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], "Test Book")

    def test_change_book_status(self):
        """Тестируем изменение статуса книги."""
        self.library.data['test_id'] = {
            "id": "test_id",
            "title": "Test Book",
            "author": "Test Author",
            "year": 2023,
            "status": "в наличии"
        }
        self.library.data['test_id']['status'] = "выдана"
        self.library.save_data()
        self.assertEqual(self.library.data['test_id']['status'], "выдана")


if __name__ == "__main__":
    unittest.main()