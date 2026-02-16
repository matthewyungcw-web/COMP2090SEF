class User:
    def __init__(self, name, user_id, role="member"):
        self.name = name
        self.user_id = user_id
        self.role = role
    
    def __str__(self):
        return f"User: {self.name} (ID: {self.user_id}, Role: {self.role})"

