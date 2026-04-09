"""Library management operations."""

from datetime import datetime
from .book import Book


class LibraryManager:
    """Core library operations."""
    def __init__(self):
        self.books = []  # Replace with Book model/DB
        self.borrow = []  # borrow history
        self.loans = []  # GUI loan records
    
    def view_borrow_history(self, user):
        """Display user's borrow history."""
        user_borrow = [borrow for borrow in self.borrow if borrow['user'] == user.user_id]
        print(f"\n {user.name}'s borrow History ({len(user_borrow)} records):")
        for i, borrow in enumerate(user_borrow, 1):
            status = " Returned" if borrow.get('returned') else " Borrowed"
            print(f"{i}. {borrow['book_title']} | {borrow['borrow_date']} | {status}")
    
    def borrow_book(self, user):
        book_title = input("Book title: ").strip()
        """Process book borrowing."""
        book = next((b for b in self.books if b.title == book_title), None)
        if not book:
            print("Book not found")
            return
        
        if book.available:
            book.available = False
            self.borrow.append({
                'user': user.user_id,
                'book_title': book.title,
                'borrow_date': datetime.now().strftime("%Y-%m-%d"),
                'returned': None
            })
            print(f"{book.title} borrowed by {user.name}")
        else:
            print("Book not available")
    
    def return_book(self, user):
        for borrow in self.borrow:
            if (borrow['user'] == user.user_id and not borrow.get('returned')):
                print("Currently borrowed:",borrow["book_title"])
        book_title = input("Book title: ").strip()
        """Process book return."""
        for borrow in self.borrow:
            if (borrow['user'] == user.user_id and 
                borrow['book_title'] == book_title and 
                not borrow.get('returned')):
                borrow['returned'] = datetime.now().strftime("%Y-%m-%d")
                book = next(b for b in self.books if b.title == book_title)
                book.available = True
                print(f"{book_title} returned")
                return
        print(f"{book_title} not found")

    def add_book(self, user, title, id, author=""):
        if user.role != "admin":
            print("Admin access required for this function")
            return
        self.books.append(Book(title=title, id=id, author=author, available=True))
        print("Book added")

    def show_all_books(self):
        for books in self.books:
            if books.available == True:
                bavai = "Yes"
            else:
                bavai = "No"
            print("Title: ", books.title, ", id: ", books.id, ", available: ", bavai)
