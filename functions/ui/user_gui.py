#!/usr/bin/env python3
"""
COMP2090SEF User GUI
Integrates with main.py LibrarySession
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import scrolledtext
import traceback
from datetime import datetime
from functions.models import LibraryManager, Book

class UserGUI:
    def __init__(self, session, library):
        self.session = session
        self.library = library
        self.root = tk.Tk()
        self.root.title("COMP2090SEF Library Management System")
        self.root.geometry("900x700")
        
        # books demo function
        self.books_demo_data()
        
        self.show_login_screen()
    
    # === Following methods are for matrix and shell sort ===

    def books_to_matrix(self, available_only=False):
        """Convert Book objects to matrix data structure"""
        matrix = []
        for book in self.library.books:
            if not available_only or book.available:
                matrix.append([book.id, book.title, book.author, book.available])
        return matrix

    def shell_sort_books(self, matrix, column_index=1, ascending=True):
        """Shell sort for 2D book matrix"""
        n = len(matrix)
        gap = n // 2
        while gap > 0:
            for i in range(gap, n):
                temp = matrix[i]
                j = i
                while j >= gap:
                    left = str(matrix[j - gap][column_index]).lower()
                    right = str(temp[column_index]).lower()
                    if ascending:
                        if left > right:
                            matrix[j] = matrix[j - gap]
                            j -= gap
                        else:
                            break
                    else:
                        if left < right:
                            matrix[j] = matrix[j - gap]
                            j -= gap
                        else:
                            break
                matrix[j] = temp
            gap //= 2
        return matrix

    def load_books_to_listbox(self, listbox, matrix):
        """Reload listbox from sorted matrix"""
        listbox.delete(0, tk.END)
        for row in matrix:
            book_id, title, author, available = row
            if available:
                listbox.insert(tk.END, f"id: {book_id} | {title} by {author}")

    def sort_books_action(self, listbox, ascending=True):
        """Sort books by title using Shell sort and refresh listbox"""
        book_matrix = self.books_to_matrix(available_only=True)
        sorted_matrix = self.shell_sort_books(book_matrix, column_index=1, ascending=ascending)
        self.load_books_to_listbox(listbox, sorted_matrix)

    def books_demo_data(self):
        """Initialize demo library data."""
        self.library.books = [
            Book(title="computers", id="101", author="py", available=True),
            Book(title="python for beginners", id="102", author="pi", available=True),
            Book(title="stuff", id="103", author="dol", available=True),
            Book(title="pool", id="104", author="kim", available=True),
            Book(title="broke", id="105", author="car", available=False),
            Book(title="hello world", id="421", author="sam", available=True),
            Book(title="a name", id="735", author="sim", available=True),
            Book(title="this is a book", id="843", author="som", available=True),
            Book(title="mac", id="910", author="mak", available=True),
            Book(title="internet", id="933", author="dude", available=True),
            Book(title="map", id="989", author="kol", available=True)


        ]
        self.library.loans = []
    
    def show_login_screen(self):
        """Display login interface"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Login frame
        login_frame = ttk.Frame(self.root, padding="20")
        login_frame.pack(expand=True)
        
        ttk.Label(login_frame, text="Library Login", font=("Arial", 24, "bold")).pack(pady=20)
        
        ttk.Label(login_frame, text="Username:").pack()
        self.username_entry = ttk.Entry(login_frame, width=20, font=("Arial", 12))
        self.username_entry.pack(pady=5)
        self.username_entry.focus()
        
        ttk.Label(login_frame, text="Password:").pack()
        self.password_entry = ttk.Entry(login_frame, width=20, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=5)
        
        ttk.Button(login_frame, text="Login", command=self.login, style="Accent.TButton").pack(pady=20)
        """ttk.Button(login_frame, text="Demo (admin/admin123)", command=lambda: self.demo_login()).pack()"""
    
    def demo_login(self):
        """Quick demo login, disabled"""
        self.username_entry.delete(0, tk.END)
        """self.username_entry.insert(0, "admin")"""
        self.password_entry.delete(0, tk.END)
        """self.password_entry.insert(0, "admin123")"""
        self.login()
    
    def login(self):
        """Process login"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.session.login(username, password):
            if self.session.current_user.role == "admin":
                self.root.destroy()
                AdminGUI(self.session, self.library)
            else:
                self.show_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")
    
    def show_main_menu(self):
        """Display authenticated main menu"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill="x", padx=20, pady=10)
        ttk.Label(header_frame, text=f"Loged in on: [{self.session.current_user.name}]", 
                 font=("Arial", 16, "bold")).pack(side="left")
        ttk.Button(header_frame, text="Logout", command=self.logout).pack(side="right")
        
        # Buttons frame
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(expand=True, padx=20, pady=10)
        
        # Main action buttons
        ttk.Button(btn_frame, text="Borrow Book", command=self.borrow_book_screen,
                  style="Accent.TButton").pack(fill="x", pady=10)
        ttk.Button(btn_frame, text="Return Book", command=self.return_book_screen).pack(fill="x", pady=10)
        ttk.Button(btn_frame, text="Check Borrow Record", command=self.borrow_record_screen).pack(fill="x", pady=10)
        """if self.session.current_user.role == "admin":
            ttk.Button(btn_frame, text="Add Book", command=self.add_book_screen).pack(fill="x", pady=10)
    """
    # === BEFORE ===
    """def borrow_book_screen(self):
        "Borrow book interface"
        self.clear_window()
        ttk.Label(self.root, text="Borrow Book", font=("Arial", 20, "bold")).pack(pady=20)
        
        # Book list
        ttk.Label(self.root, text="Available Books:", font=("Arial", 14)).pack(pady=10)
        book_listbox = tk.Listbox(self.root, height=8, width=80)
        for book in self.library.books:
            if book.available:
                book_listbox.insert(tk.END, f"id: {book.id} | {book.title} by {book.author}")
        book_listbox.pack(pady=10)
        
        ttk.Button(self.root, text="Borrow Selected Book", 
                command=lambda: self.process_borrow(book_listbox)).pack(pady=20)
        ttk.Button(self.root, text="Back", command=self.show_main_menu).pack()"""

    # === AFTER (New version with matrix + Shell sort buttons) ===
    def borrow_book_screen(self):
        """Borrow book interface"""
        self.clear_window()
        ttk.Label(self.root, text="Borrow Book", font=("Arial", 20, "bold")).pack(pady=20)

        ttk.Label(self.root, text="Available Books:", font=("Arial", 14)).pack(pady=10)
        book_listbox = tk.Listbox(self.root, height=8, width=80)
        book_listbox.pack(pady=10)

        # initial load - CHANGED from direct Book loop to matrix
        self.load_books_to_listbox(book_listbox, self.books_to_matrix(available_only=True))

        # NEW sort buttons frame - ADDED
        sort_frame = ttk.Frame(self.root)
        sort_frame.pack(pady=10)

        ttk.Button(
            sort_frame,
            text="Sort Title in Ascending Order",
            command=lambda: self.sort_books_action(book_listbox, True)
        ).pack(side="left", padx=5)

        ttk.Button(
            sort_frame,
            text="Sort Title in Descending Order",
            command=lambda: self.sort_books_action(book_listbox, False)
        ).pack(side="left", padx=5)

        ttk.Button(
            self.root,
            text="Borrow Selected Book",
            command=lambda: self.process_borrow(book_listbox)
        ).pack(pady=20)

        ttk.Button(self.root, text="Back", command=self.show_main_menu).pack()

    def process_borrow(self, listbox):
        """Process book borrowing"""
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a book!")
            return
        
        selected_text = listbox.get(selection[0])
        id = selected_text.split("id:")[1].split("|")[0].strip()
        book = next((b for b in self.library.books if b.id == id), None)
        
        if book and book.available:
            book.available = False
            self.library.loans.append({
                "user": self.session.current_user.user_id,
                "id": id,
                "title": book.title,
                "borrow_date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            messagebox.showinfo("Success", f"Borrowed: {book.title}")
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Book not available!")
    
    def return_book_screen(self):
        """Return book interface"""
        self.clear_window()
        ttk.Label(self.root, text="Return Book", font=("Arial", 20, "bold")).pack(pady=20)
        
        # Active loans list
        ttk.Label(self.root, text="Your Active Loans:", font=("Arial", 14)).pack(pady=10)
        loan_listbox = tk.Listbox(self.root, height=8, width=80)
        
        active_loans = [l for l in self.library.loans 
                       if l["user"] == self.session.current_user.user_id and not l.get("return_date")]
        for loan in active_loans:
            book = next((b for b in self.library.books if b.id == loan["id"]), None)
            if book:
                loan_listbox.insert(tk.END, f"id:{loan['id']} | {book.title}")
        
        loan_listbox.pack(pady=10)
        ttk.Button(self.root, text="Return Selected Book", 
                  command=lambda: self.process_return(loan_listbox)).pack(pady=20)
        ttk.Button(self.root, text="Back", command=self.show_main_menu).pack()
    
    def process_return(self, listbox):
        """Process book return"""
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a loan to return!")
            return
        
        selected_text = listbox.get(selection[0])
        id = selected_text.split("id:")[1].split("|")[0].strip()
        for loan in self.library.loans:
            if (loan["user"] == self.session.current_user.user_id and 
                loan["id"] == id and not loan.get("return_date")):
                loan["return_date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                book = next((b for b in self.library.books if b.id == id), None)
                if book:
                    book.available = True
                messagebox.showinfo("Success", f"Returned: {book.title if book else id}")
                self.show_main_menu()
                return
        messagebox.showerror("Error", "Return failed!")
    
    def borrow_record_screen(self):
        """Show borrow history"""
        self.clear_window()
        ttk.Label(self.root, text="Your Borrow Record", font=("Arial", 20, "bold")).pack(pady=20)
        
        # History text area
        history_text = scrolledtext.ScrolledText(self.root, width=70, height=15, wrap=tk.WORD)
        history_text.pack(pady=20, padx=20, fill="both", expand=True)
        
        user_loans = [l for l in self.library.loans if l["user"] == self.session.current_user.user_id]
        if not user_loans:
            history_text.insert(tk.END, "No borrow records found.")
        else:
            for i, loan in enumerate(user_loans, 1):
                book = next((b for b in self.library.books if b.id == loan.get("id")), None)
                status = "Returned" if loan.get("return_date") else "Borrowed"
                title = book.title if book else loan.get('title', 'Unknown Title')
                author = book.author if book else 'Unknown Author'
                history_text.insert(tk.END, 
                    f"{i}. {title} by {author}\n"
                    f"   Borrowed: {loan['borrow_date']}\n"
                    f"   Status: {status}\n\n")
        
        history_text.config(state="disabled")
        ttk.Button(self.root, text="Back", command=self.show_main_menu).pack(pady=10)
    
    def add_book_screen(self):
        """Add book interface (admin only)"""
        self.clear_window()
        ttk.Label(self.root, text="Add Book", font=("Arial", 20, "bold")).pack(pady=20)
        
        ttk.Label(self.root, text="Book Title:").pack(pady=5)
        title_entry = ttk.Entry(self.root, width=40)
        title_entry.pack(pady=5)
        
        ttk.Label(self.root, text="Book id:").pack(pady=5)
        id_entry = ttk.Entry(self.root, width=40)
        id_entry.pack(pady=5)
        
        ttk.Label(self.root, text="Author:").pack(pady=5)
        author_entry = ttk.Entry(self.root, width=40)
        author_entry.pack(pady=5)

        ttk.Button(self.root, text="Add Book", command=lambda: self.process_add_book(title_entry, id_entry, author_entry)).pack(pady=20)
        ttk.Button(self.root, text="Back", command=self.show_main_menu).pack()
    
    """def process_add_book(self, title_entry, id_entry, author_entry):
        Process adding a book, original version outside of admingui
        title = title_entry.get().strip()
        id = id_entry.get().strip()
        author = author_entry.get().strip()

        
        if not title or not id or not author:
            messagebox.showerror("Error", "Please enter both title and id!")
            return
        
        self.library.add_book(self.session.current_user, title, id, author)
        messagebox.showinfo("Success", f"Book '{title' added successfully!")
        self.show_main_menu()"""
    
    def logout(self):
        """Process logout"""
        self.session.logout()
        self.show_login_screen()
    
    def clear_window(self):
        """Clear all widgets except root"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def launch(self):
        """Start the GUI"""
        self.root.mainloop()

class AdminGUI(UserGUI):
    """Admin GUI inherit from UserGUI"""

    def __init__(self, session, library):
        super().__init__(session, library)
        self.show_admin_menu()

    def show_admin_menu(self):
        self.clear_window()
        ttk.Label(self.root, text="Admin page", font=("Arial", 20, "bold")).pack(pady=20)
        ttk.Button(self.root, text="Add a New Book", command=self.add_book_screen).pack(pady=5)
        ttk.Button(self.root, text="current available books", command=self.show_books).pack(pady=5)
        ttk.Button(self.root, text="Logout", command=self.logout).pack(pady=5)

    def add_book_screen(self):
        """admin ver add book"""
        self.clear_window()
        ttk.Label(self.root, text="Add Book", font=("Arial", 20, "bold")).pack(pady=20)

        ttk.Label(self.root, text="Title:").pack()
        title_entry = ttk.Entry(self.root, width=40)
        title_entry.pack()

        ttk.Label(self.root, text="ID:").pack()
        id_entry = ttk.Entry(self.root, width=40)
        id_entry.pack()

        ttk.Label(self.root, text="Author:").pack()
        author_entry = ttk.Entry(self.root, width=40)
        author_entry.pack()

        ttk.Button(
            self.root, 
            text="Add Book", 
            command=lambda: self.process_add_book(title_entry, id_entry, author_entry)
        ).pack(pady=20)

        ttk.Button(self.root, text="Back", command=self.show_admin_menu).pack()

    def process_add_book(self, title_entry, id_entry, author_entry):
        """process add book"""
        title = title_entry.get().strip()
        book_id = id_entry.get().strip()
        author = author_entry.get().strip()

        if not title or not book_id or not author:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        self.library.add_book(self.session.current_user, title, book_id, author)
        messagebox.showinfo("Success", f"Book '{title}' added.")
        self.show_admin_menu()

    def show_books(self):
        """admin-show current available book"""
        self.clear_window()

        ttk.Label(self.root, text="current books in library:", font=("Arial", 14)).pack(pady=10)
        book_listbox = tk.Listbox(self.root, height=8, width=80)
        book_listbox.pack(pady=10)

        # initial load - CHANGED from direct Book loop to matrix
        """currently only shows available ones instead of all"""
        self.load_books_to_listbox(book_listbox, self.books_to_matrix(available_only=True))

        sort_frame = ttk.Frame(self.root)
        sort_frame.pack(pady=10)

        ttk.Button(
            sort_frame,
            text="Sort Title in Ascending Order",
            command=lambda: self.sort_books_action(book_listbox, True)
        ).pack(side="left", padx=5)

        ttk.Button(
            sort_frame,
            text="Sort Title in Descending Order",
            command=lambda: self.sort_books_action(book_listbox, False)
        ).pack(side="left", padx=5)

        ttk.Button(self.root, text="Back", command=self.show_admin_menu).pack()


def launch_gui(session, library=None):
    """Entry point from main.py."""
    try:
        if library is None:
            library = LibraryManager()
        app = UserGUI(session, library)
        app.launch()
    except Exception as e:
        print("ERROR: Unable to start Tkinter GUI:", e)
        traceback.print_exc()
        raise

