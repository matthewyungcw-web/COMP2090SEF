class Book:
    def __init__(self, title, isbn, author="", available=True):
        self.title = title
        self.isbn = isbn
        self.author = author
        self.available = available
    
    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

