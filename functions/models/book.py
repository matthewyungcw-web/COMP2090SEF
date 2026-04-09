#Book info
class Book:
    def __init__(self, title, id, author="", available=True):
        self.title = title
        self.id = id
        self.author = author
        self.available = available
    
    def __str__(self):
        return f"{self.title} by {self.author} (ID: {self.id})"

