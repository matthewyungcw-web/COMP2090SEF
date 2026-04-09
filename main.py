#!/usr/bin/env python3
"""
COMP2090SEF Library Management System - Complete Entry Point
Supports login/logout, borrow history, borrow/return operations
"""

import sys
import os
import traceback
import subprocess
from pathlib import Path
from datetime import datetime
import json

sys.path.insert(0, str(Path(__file__).parent / "functions"))

from functions.models import Book, User, LibraryManager

def can_launch_tkinter():
    """Check if tkinter can create a root window in this environment."""
    cmd = [sys.executable, "-c",
           "import tkinter as tk;\n"
           "r = None\n"
           "try:\n"
           "    r = tk.Tk(); r.withdraw(); r.destroy();\n"
           "    print('OK')\n"
           "except Exception as e:\n"
           "    import sys; sys.stderr.write(str(e)); sys.exit(1)\n"
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except Exception as e:
        print("tkinter availability check failed:", e)
        return False

class LibrarySession:
    """Manages user authentication and session state."""
    def __init__(self):
        self.current_user = None
        self.is_authenticated = False

        
    def login(self, username, password):
        """Authenticate user - replace with MySQL check."""
        # Demo users
        users_db = {
            "admin": "admin123",
            "librarian": "lib123", 
            "student1": "pass123",
            "a": "a",
            "b":"b"
        }
        
        if username in users_db and users_db[username] == password:
            role = "admin" if username == "admin" else "member"
            self.current_user = User(name=username, user_id=username, role=role)
            self.is_authenticated = True
            print(f"Login successful: {username}")
            return True
        return False
    
    def logout(self):
        """Clear session."""
        self.current_user = None
        self.is_authenticated = False
        print("Logged out successfully")












def cli_mode(session, library,username):
    """Authenticated CLI interface."""
    while session.is_authenticated:
        print("\n=== Library Menu ===")
        print("1. View borrow History")
        print("2. Borrow Book") 
        print("3. Return Book")
        print("4. Add Book(admin account required)")
        print("5. Show all books")
        print("6. Logout")

        choice = input("Choose (1-6): ").strip()
        
        if choice == "1":
            library.view_borrow_history(session.current_user)
        elif choice == "2":
            library.borrow_book(session.current_user)
        elif choice == "3":
            library.return_book(session.current_user)
        elif choice == "4":
            book_title = input("Book title: ").strip()
            book_id = input("Book id: ").strip()
            library.add_book(session.current_user, book_title, book_id)
        elif choice == "5":
            library.show_all_books()
        elif choice == "6":
            session.logout()
            break
        else:
            print("Invalid choice")

def main():
    session = LibrarySession()
    library = LibraryManager()

    # Demo data
    library.books = [####################################################### might not be working  quite right
        Book(title="book 1", id="123", available=True),
        Book(title="book 2", id="223", available=True),
        Book(title="book 3", id="323", available=True),
        Book(title="book 4", id="423", available=True)
    ]
    
    mode = sys.argv[1] if len(sys.argv) > 1 else "gui"

    if mode == "gui":
        if not can_launch_tkinter():
            print("GUI is unavailable (Tk startup check failed). Switching to CLI.")
            mode = "cli"
        else:
            try:
                from functions.ui.user_gui import launch_gui
                launch_gui(session, library)
                return
            except Exception as e:
                print("ERROR: GUI initialization failed:", e)
                traceback.print_exc()
                print("Falling back to CLI mode.")
                mode = "cli"

    if mode != "gui":
        # CLI login flow        print("Library Login")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        if session.login(username, password):
            cli_mode(session, library,username)
        else:
            print("Login failed")

if __name__ == "__main__": 
    main()
 