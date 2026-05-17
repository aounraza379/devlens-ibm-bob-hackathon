"""
Example Python code for testing the Code Summarizer
This demonstrates a simple user management system
"""

import hashlib
import json
from datetime import datetime
from typing import List, Dict, Optional


class User:
    """Represents a user in the system"""
    
    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password_hash = self._hash_password(password)
        self.created_at = datetime.now()
        self.is_active = True
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str) -> bool:
        """Verify if provided password matches"""
        return self._hash_password(password) == self.password_hash
    
    def to_dict(self) -> Dict:
        """Convert user to dictionary"""
        return {
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active
        }


class UserManager:
    """Manages user operations"""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
    
    def create_user(self, username: str, email: str, password: str) -> Optional[User]:
        """Create a new user"""
        if username in self.users:
            return None
        
        user = User(username, email, password)
        self.users[username] = user
        return user
    
    def get_user(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.users.get(username)
    
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate user credentials"""
        user = self.get_user(username)
        if user and user.is_active:
            return user.verify_password(password)
        return False
    
    def deactivate_user(self, username: str) -> bool:
        """Deactivate a user account"""
        user = self.get_user(username)
        if user:
            user.is_active = False
            return True
        return False
    
    def list_active_users(self) -> List[User]:
        """Get all active users"""
        return [user for user in self.users.values() if user.is_active]
    
    def export_users(self, filename: str):
        """Export users to JSON file"""
        data = [user.to_dict() for user in self.users.values()]
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)


def main():
    """Main function demonstrating usage"""
    manager = UserManager()
    
    # Create users
    manager.create_user('alice', 'alice@example.com', 'password123')
    manager.create_user('bob', 'bob@example.com', 'securepass')
    
    # Authenticate
    if manager.authenticate('alice', 'password123'):
        print("Alice authenticated successfully")
    
    # List active users
    active_users = manager.list_active_users()
    print(f"Active users: {len(active_users)}")
    
    # Export data
    manager.export_users('users.json')


if __name__ == '__main__':
    main()

# Made with Bob
