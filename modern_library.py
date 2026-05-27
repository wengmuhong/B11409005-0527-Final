import json
import os
from dataclasses import dataclass, asdict
from typing import List, Optional, Tuple

DATA_FILE = "books.json"


@dataclass
class Book:
    title: str
    isbn: str
    status: str

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        if not isinstance(data, dict):
            raise ValueError("Book record must be a dictionary")

        try:
            return cls(
                title=str(data["title"]),
                isbn=str(data["isbn"]),
                status=str(data["status"]),
            )
        except KeyError as exc:
            raise ValueError(f"Missing book field: {exc}") from exc


class Library:
    def __init__(self, storage_file: str = DATA_FILE) -> None:
        self.storage_file = storage_file
        self.books: List[Book] = []
        self.load()

    def load(self) -> None:
        if not os.path.exists(self.storage_file):
            self.books = []
            return

        try:
            with open(self.storage_file, "r", encoding="utf-8") as f:
                raw_data = json.load(f)

            if not isinstance(raw_data, list):
                raise ValueError("Library data must be a JSON list")

            self.books = [Book.from_dict(item) for item in raw_data]
        except (OSError, json.JSONDecodeError, ValueError) as error:
            print(f"讀取資料失敗：{error}")
            self.books = []

    def save(self) -> bool:
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump([asdict(book) for book in self.books], f, ensure_ascii=False, indent=2)
            return True
        except OSError as error:
            print(f"儲存資料失敗：{error}")
            return False

    def find_book(self, isbn: str) -> Optional[Book]:
        return next((book for book in self.books if book.isbn == isbn), None)

    def add_book(self, title: str, isbn: str, status: str) -> bool:
        if self.find_book(isbn) is not None:
            return False

        self.books.append(Book(title=title, isbn=isbn, status=status))
        return True

    def borrow_book(self, isbn: str) -> str:
        book = self.find_book(isbn)
        if book is None:
            return "not_found"

        if book.status == "borrowed":
            return "already_borrowed"

        book.status = "borrowed"
        return "updated"

    def show_books(self) -> None:
        if not self.books:
            print("No books available")
            return

        for book in self.books:
            print(f"書名: {book.title}, ISBN: {book.isbn}, 狀態: {book.status}")

    @staticmethod
    def parse_add_command(raw_text: str) -> Optional[Tuple[str, str, str]]:
        parts = raw_text.split("/", 2)
        if len(parts) != 3:
            return None

        title, isbn, status = (part.strip() for part in parts)
        if not title or not isbn or not status:
            return None

        return title, isbn, status


def main() -> None:
    library = Library()
    print("=== 圖書管理系統 v0.1 (Modern) ===")

    while True:
        try:
            op = input("> ").strip()
        except EOFError:
            print("\n輸入結束，關閉程式。")
            if library.save():
                print("系統關閉，資料已儲存。")
            else:
                print("系統關閉，但儲存資料失敗。")
            break

        if op == "exit":
            if library.save():
                print("系統關閉，資料已儲存。")
            else:
                print("系統關閉，但儲存資料失敗。")
            break

        if op == "show":
            library.show_books()
            continue

        if op.startswith("add "):
            parsed = Library.parse_add_command(op[4:].strip())
            if parsed is None:
                print("Format Error: add 指令格式為 add 書名/ISBN/狀態")
                continue

            title, isbn, status = parsed
            if library.add_book(title, isbn, status):
                print("Success")
            else:
                print("ISBN Exist")
            continue

        if op.startswith("borrow "):
            isbn = op[7:].strip()
            if not isbn:
                print("Format Error: borrow 指令格式為 borrow ISBN")
                continue

            result = library.borrow_book(isbn)
            if result == "updated":
                print("Updated")
            elif result == "already_borrowed":
                print("Already Borrowed")
            else:
                print("ISBN Not Found")
            continue

        print("Unknown Command")


if __name__ == "__main__":
    main()
