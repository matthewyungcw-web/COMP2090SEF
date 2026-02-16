#!/usr/bin/env python3
"""
COMP2090SEF Library Management System - Complete Entry Point
Supports login/logout, borrow history, borrow/return operations
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json

# Add functions/ to path
sys.path.insert(0, str(Path(__file__).parent / "functions"))

from models import Book, User
from ui.user_gui import launch_gui  # Your existing GUI

class LibrarySession:
    """Manages user authentication and session state."""
    def __init__(self):
        self.current_user = None
        self.is_authenticated = False
        
    def login(self, username, password):
        """Authenticate user - replace with MySQL check."""
        # Demo users - replace with your User model/DB query
        users_db = {
            "admin": "admin123",
            "librarian": "lib123", 
            "student1": "pass123"
        }
        
        if username in users_db and users_db[username] == password:
            self.current_user = User(name=username, user_id=username)
            self.is_authenticated = True
            print(f"✓ Login successful: {username}")
            return True
        return False
    
    def logout(self):
        """Clear session."""
        self.current_user = None
        self.is_authenticated = False
        print("✓ Logged out successfully")

class LibraryManager:
    """Core library operations."""
    def __init__(self):
        self.books = []  # Replace with Book model/DB
        self.borrow = []  # borrow history
        
    def view_borrow_history(self, user):
        """Display user's borrow history."""
        user_borrow = [borrow for borrow in self.borrow if borrow['user'] == user.user_id]
        print(f"\n {user.name}'s borrow History ({len(user_borrow)} records):")
        for i, borrow in enumerate(user_borrow, 1):
            status = " Returned" if borrow.get('returned') else " Borrowed"
            print(f"{i}. {borrow['book_title']} | {borrow['borrow_date']} | {status}")
    
    def borrow_book(self, user, book_title):
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
            print(f"✓ {book.title} borrowed by {user.name}")
        else:
            print("Book not available")
    
    def return_book(self, user, book_title):
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
        print("No record found")

def cli_mode(session, library):
    """Authenticated CLI interface."""
    while session.is_authenticated:
        print("\n=== Library Menu ===")
        print("1. View borrow History")
        print("2. Borrow Book") 
        print("3. Return Book")
        print("4. Logout")
        
        choice = input("Choose (1-4): ").strip()
        
        if choice == "1":
            library.view_borrow_history(session.current_user)
        elif choice == "2":
            title = input("Book title: ").strip()
            library.borrow_book(session.current_user, title)
        elif choice == "3":
            title = input("Book title: ").strip()
            library.return_book(session.current_user, title)
        elif choice == "4":
            session.logout()
            break
        else:
            print("Invalid choice")

def main():
    session = LibrarySession()
    library = LibraryManager()
    
    # Demo data
    library.books = [
        Book(title="Python Crash Course", isbn="978-1593279288", available=True),
        Book(title="Clean Code", isbn="978-0132350884", available=False)
    ]
    
    mode = sys.argv[1] if len(sys.argv) > 1 else "cli"
    
    if mode == "gui":
        # GUI handles own auth - pass session
        launch_gui(session)
    else:
        # CLI login flow
        print("Library Login")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        if session.login(username, password):
            cli_mode(session, library)
        else:
            print("Login failed")

if __name__ == "__main__":
    main()
