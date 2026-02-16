#!/usr/bin/env python3
"""
COMP2090SEF User GUI - Complete User Interface
Integrates with main.py LibrarySession
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import scrolledtext
from datetime import datetime

class UserGUI:
    def __init__(self, session, library):
        self.session = session
        self.library = library
        self.root = tk.Tk()
        self.root.title("COMP2090SEF Library Management System")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Demo books (replace with your models.Book instances)
        self.setup_demo_data()
        
        self.show_login_screen()
    
    def setup_demo_data(self):
        """Initialize demo library data."""
        self.library.books = [
            {"id": 1, "title": "Python Crash Course", "author": "Eric Matthes", "available": True},
            {"id": 2, "title": "Clean Code", "author": "Robert C. Martin", "available": False},
            {"id": 3, "title": "Fluent Python", "author": "Luciano Ramalho", "available": True},
            {"id": 4, "title": "Design Patterns", "author": "Gang of Four", "available": True}
        ]
        self.library.loans = []
    
    def show_login_screen(self):
        """Display login interface."""
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
        ttk.Button(login_frame, text="Demo (admin/admin123)", command=lambda: self.demo_login()).pack()
    
    def demo_login(self):
        """Quick demo login."""
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, "admin")
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, "admin123")
        self.login()
    
    def login(self):
        """Process login."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if self.session.login(username, password):
            self.show_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials!\nDemo: admin/admin123")
    
    def show_main_menu(self):
        """Display authenticated main menu."""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill="x", padx=20, pady=10)
        ttk.Label(header_frame, text=f"Welcome, {self.session.current_user.name}!", 
                 font=("Arial", 16, "bold")).pack(side="left")
        ttk.Button(header_frame, text="Logout", command=self.logout).pack(side="right")
        
        # Buttons frame
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(expand=True, padx=20, pady=10)
        
        # Main action buttons
        ttk.Button(btn_frame, text="📖 Borrow Book", command=self.borrow_book_screen,
                  style="Accent.TButton").pack(fill="x", pady=10)
        ttk.Button(btn_frame, text="📚 Return Book", command=self.return_book_screen).pack(fill="x", pady=10)
        ttk.Button(btn_frame, text="📋 Check Borrow Record", command=self.borrow_record_screen).pack(fill="x", pady=10)
    
    def borrow_book_screen(self):
        """Borrow book interface."""
        self.clear_window()
        ttk.Label(self.root, text="Borrow Book", font=("Arial", 20, "bold")).pack(pady=20)
        
        # Book list
        ttk.Label(self.root, text="Available Books:", font=("Arial", 14)).pack(pady=10)
        book_listbox = tk.Listbox(self.root, height=8, width=60)
        for book in self.library.books:
            if book["available"]:
                book_listbox.insert(tk.END, f"ID:{book['id']} - {book['title']} by {book['author']}")
        book_listbox.pack(pady=10)
        
        ttk.Button(self.root, text="Borrow Selected Book", 
                  command=lambda: self.process_borrow(book_listbox)).pack(pady=20)
        ttk.Button(self.root, text="← Back", command=self.show_main_menu).pack()
    
    def process_borrow(self, listbox):
        """Process book borrowing."""
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a book!")
            return
        
        book_id = int(listbox.get(selection[0]).split("ID:")[1].split(" -")[0])
        book = next((b for b in self.library.books if b["id"] == book_id), None)
        
        if book and book["available"]:
            book["available"] = False
            self.library.loans.append({
                "user": self.session.current_user.user_id,
                "book_id": book_id,
                "title": book["title"],
                "borrow_date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            messagebox.showinfo("Success", f"✓ Borrowed: {book['title']}")
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Book not available!")
    
    def return_book_screen(self):
        """Return book interface."""
        self.clear_window()
        ttk.Label(self.root, text="Return Book", font=("Arial", 20, "bold")).pack(pady=20)
        
        # Active loans list
        ttk.Label(self.root, text="Your Active Loans:", font=("Arial", 14)).pack(pady=10)
        loan_listbox = tk.Listbox(self.root, height=8, width=60)
        
        active_loans = [l for l in self.library.loans 
                       if l["user"] == self.session.current_user.user_id]
        for loan in active_loans:
            book = next(b for b in self.library.books if b["id"] == loan["book_id"])
            loan_listbox.insert(tk.END, f"ID:{loan['book_id']} - {book['title']}")
        
        loan_listbox.pack(pady=10)
        ttk.Button(self.root, text="Return Selected Book", 
                  command=lambda: self.process_return(loan_listbox)).pack(pady=20)
        ttk.Button(self.root, text="← Back", command=self.show_main_menu).pack()
    
    def process_return(self, listbox):
        """Process book return."""
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a loan to return!")
            return
        
        book_id = int(listbox.get(selection[0]).split("ID:")[1].split(" -")[0])
        for loan in self.library.loans:
            if (loan["user"] == self.session.current_user.user_id and 
                loan["book_id"] == book_id):
                loan["return_date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                book = next(b for b in self.library.books if b["id"] == book_id)
                book["available"] = True
                messagebox.showinfo("Success", f"✓ Returned: {book['title']}")
                self.show_main_menu()
                return
        messagebox.showerror("Error", "Return failed!")
    
    def borrow_record_screen(self):
        """Show borrow history."""
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
                book = next(b for b in self.library.books if b["id"] == loan["book_id"])
                status = "✅ Returned" if loan.get("return_date") else "📖 Borrowed"
                history_text.insert(tk.END, 
                    f"{i}. {book['title']} by {book['author']}\n"
                    f"   Borrowed: {loan['borrow_date']}\n"
                    f"   Status: {status}\n\n")
        
        history_text.config(state="disabled")
        ttk.Button(self.root, text="← Back", command=self.show_main_menu).pack(pady=10)
    
    def logout(self):
        """Process logout."""
        self.session.logout()
        self.show_login_screen()
    
    def clear_window(self):
        """Clear all widgets except root."""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def launch(self):
        """Start the GUI."""
        self.root.mainloop()

def launch_gui(session):
    """Entry point from main.py."""
    library = LibraryManager()  # From main.py
    app = UserGUI(session, library)
    app.launch()

