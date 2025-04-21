"""
Security manager for handling sensitive information
Provides secure storage and access for API keys and credentials
"""
import os
import json
import base64
from typing import Dict, Any, Optional
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SecurityManager:
    """Manages secure storage and access of sensitive information"""
    
    def __init__(self, config_dir: str = None):
        """
        Initialize the security manager
        
        Args:
            config_dir: Directory to store encrypted configuration
        """
        self.config_dir = config_dir or os.path.join(os.path.expanduser("~"), ".dental_ai")
        self.config_file = os.path.join(self.config_dir, "config.encrypted")
        self.key_file = os.path.join(self.config_dir, "key.salt")
        self._ensure_config_dir()
    
    def _ensure_config_dir(self):
        """Ensure the configuration directory exists"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir, exist_ok=True)
    
    def _derive_key(self, password: str, salt: Optional[bytes] = None) -> tuple:
        """
        Derive encryption key from password
        
        Args:
            password: User password for encryption
            salt: Optional salt value
            
        Returns:
            Tuple of (key, salt)
        """
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    def save_api_key(self, api_key: str, password: str) -> bool:
        """
        Securely save the API key
        
        Args:
            api_key: The API key to save
            password: Password for encryption
            
        Returns:
            Boolean indicating success
        """
        try:
            # Create encryption key
            key, salt = self._derive_key(password)
            
            # Save salt for later decryption
            with open(self.key_file, 'wb') as f:
                f.write(salt)
            
            # Encrypt the API key
            cipher = Fernet(key)
            encrypted_data = cipher.encrypt(api_key.encode())
            
            # Save the encrypted data
            with open(self.config_file, 'wb') as f:
                f.write(encrypted_data)
            
            return True
        
        except Exception as e:
            print(f"Error saving API key: {str(e)}")
            return False
    
    def get_api_key(self, password: str) -> Optional[str]:
        """
        Retrieve the API key securely
        
        Args:
            password: Password for decryption
            
        Returns:
            API key if successful, None otherwise
        """
        if not os.path.exists(self.config_file) or not os.path.exists(self.key_file):
            return None
        
        try:
            # Read salt
            with open(self.key_file, 'rb') as f:
                salt = f.read()
            
            # Derive key
            key, _ = self._derive_key(password, salt)
            
            # Read encrypted data
            with open(self.config_file, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt
            cipher = Fernet(key)
            decrypted_data = cipher.decrypt(encrypted_data)
            
            return decrypted_data.decode()
        
        except Exception as e:
            print(f"Error retrieving API key: {str(e)}")
            return None
    
    def save_credentials(self, credentials: Dict[str, Any], password: str) -> bool:
        """
        Securely save credential information
        
        Args:
            credentials: Dictionary of credentials
            password: Password for encryption
            
        Returns:
            Boolean indicating success
        """
        try:
            # Create encryption key
            key, salt = self._derive_key(password)
            
            # Save salt for later decryption
            with open(self.key_file, 'wb') as f:
                f.write(salt)
            
            # Convert credentials to JSON
            json_data = json.dumps(credentials).encode()
            
            # Encrypt the data
            cipher = Fernet(key)
            encrypted_data = cipher.encrypt(json_data)
            
            # Save the encrypted data
            with open(self.config_file, 'wb') as f:
                f.write(encrypted_data)
            
            return True
        
        except Exception as e:
            print(f"Error saving credentials: {str(e)}")
            return False
    
    def get_credentials(self, password: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve credentials securely
        
        Args:
            password: Password for decryption
            
        Returns:
            Dictionary of credentials if successful, None otherwise
        """
        if not os.path.exists(self.config_file) or not os.path.exists(self.key_file):
            return None
        
        try:
            # Read salt
            with open(self.key_file, 'rb') as f:
                salt = f.read()
            
            # Derive key
            key, _ = self._derive_key(password, salt)
            
            # Read encrypted data
            with open(self.config_file, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt
            cipher = Fernet(key)
            decrypted_data = cipher.decrypt(encrypted_data)
            
            # Parse JSON
            return json.loads(decrypted_data.decode())
        
        except Exception as e:
            print(f"Error retrieving credentials: {str(e)}")
            return None
    
    def clear_all_data(self) -> bool:
        """
        Clear all stored data
        
        Returns:
            Boolean indicating success
        """
        try:
            if os.path.exists(self.config_file):
                os.remove(self.config_file)
            
            if os.path.exists(self.key_file):
                os.remove(self.key_file)
            
            return True
        
        except Exception as e:
            print(f"Error clearing data: {str(e)}")
            return False
