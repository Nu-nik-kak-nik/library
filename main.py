import json
import uuid
from typing import Dict, Any, List

DATA_FILE = "library.json"


class Library:
    """Класс для управления библиотекой книг."""

    def __init__(self) -> None:
        """Инициализация библиотеки. Загружает данные из файла."""
        self.data: Dict[str, Dict[str, Any]] = self.load_data()

    @staticmethod
    def load_data() -> Dict[str, Dict[str, Any]]:
        """Загружает данные из файла library.json. Если файла нет, то создает пустой словарь."""
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            print("Ошибка: файл поврежден или содержит некорректные данные.")
            return {}

    def save_data(self) -> None:
        """Сохраняет данные в файл library.json."""
        json_string = json.dumps(self.data, indent=4)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            f.write(json_string)

    def add_book(self) -> None:
        """Добавляет книгу в библиотеку."""
        title = input("Введите название книги: ")
        author = input("Введите автора книги: ")

        while True:
            try:
                year = int(input("Введите год издания: "))
                break
            except ValueError:
                print("Некорректный год. Попробуйте еще раз.")

        book_id = str(uuid.uuid4())
        new_book = {
            "id": book_id,
            "title": title,
            "author": author,
            "year": year,
            "status": "в наличии",
        }
        self.data[book_id] = new_book
        self.save_data()
        print(f"Книга '{title}' добавлена.")

    def delete_book(self) -> None:
        """Удаляет книгу из библиотеки."""
        book_id = input("Введите ID книги для удаления: ")
        if book_id in self.data:
            del self.data[book_id]
            self.save_data()
            print(f"Книга с ID '{book_id}' удалена.")
        else:
            print(f"Книга с ID '{book_id}' не найдена.")

    @staticmethod
    def _matches_search_term(book: Dict[str, Any], search_term: str) -> bool:
        """Проверяет, содержит ли книга поисковый запрос в заголовке, авторе или годе."""
        return (search_term.lower() in book["title"].lower() or
                search_term.lower() in book["author"].lower() or
                search_term in str(book["year"]))

    def search_book(self) -> None:
        """Ищет книги по названию, автору или году."""
        search_term = input("Введите поисковый запрос (название, автор или год): ")
        results: List[Dict[str, Any]] = [book for book in self.data.values() if
                                         self._matches_search_term(book, search_term)]
        if results:
            print("Найденные книги:")
            for book in results:
                self.print_book(book)
        else:
            print("Книги не найдены.")

    def show_all_books(self) -> None:
        """Отображает все книги."""
        if self.data:
            print("Все книги:")
            for book in self.data.values():
                self.print_book(book)
        else:
            print("Библиотека пуста.")

    def change_book_status(self) -> None:
        """Изменяет статус книги."""
        book_id = input("Введите ID книги для изменения статуса: ")
        if book_id not in self.data:
            print(f"Книга с ID '{book_id}' не найдена.")
            return
        current_status = self.data[book_id]["status"]
        print(f"Текущий статус книги: '{current_status}'")
        new_status = input("Введите новый статус ('в наличии' или 'выдана'): ").lower()
        if new_status in ["в наличии", "выдана"]:
            self.data[book_id]["status"] = new_status
            self.save_data()
            print(f"Статус книги с ID '{book_id}' изменен на '{new_status}'.")
        else:
            print("Некорректный статус. Статус не изменен.")

    @staticmethod
    def print_book(book: Dict[str, Any]) -> None:
        """Выводит информацию о книге в удобном формате."""
        print(f"ID: {book['id']}")
        print(f"Название: {book['title']}")
        print(f"Автор: {book['author']}")
        print(f"Год: {book['year']}")
        print(f"Статус: {book['status']}")
        print("-" * 20)

    def main_menu(self) -> None:
        """Главное меню для управления библиотекой."""
        while True:
            print("\nМеню:"
                  "\n1. Добавить книгу"
                  "\n2. Удалить книгу"
                  "\n3. Найти книгу"
                  "\n4. Показать все книги"
                  "\n5. Изменить статус книги"
                  "\n6. Выход")

            choice = input("Выберите пункт меню: ")

            match choice:
                case "1":
                    self.add_book()
                case "2":
                    self.delete_book()
                case "3":
                    self.search_book()
                case "4":
                    self.show_all_books()
                case "5":
                    self.change_book_status()
                case "6":
                    break
                case _:
                    print("Некорректный выбор. Попробуйте еще раз.")


if __name__ == "__main__":
    library = Library()
    library.main_menu()