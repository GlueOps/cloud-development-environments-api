from pydantic import BaseModel, Field
from typing import Dict
import re
import random
import string

class Message(BaseModel):
    message: str = Field(...,example = 'Success')


class CloudDevelopmentEnvironmentRequest(BaseModel):
    student_name: str = Field(..., example='Nicholas Archuletta')
    class_name: str = Field(..., example='COSC 1010')

    @property
    def dns_name(self) -> str:
        """
        Generate a DNS-friendly name using student_name and class_name.
        """
        # Convert to lowercase
        student_name = self.student_name.lower()
        class_name = self.class_name.lower()

        # Replace spaces and special characters with hyphens
        student_name = re.sub(r'[^a-z0-9]', '-', student_name)
        class_name = re.sub(r'[^a-z0-9]', '-', class_name)

        # Combine the two with a hyphen
        dns_name = f"{class_name}-{student_name}"

        # Ensure it doesn't start or end with a hyphen
        return dns_name.strip('-')

    @staticmethod
    def generate_password(length: int = 12) -> str:
        """
        Generate a secure random password using only uppercase letters and digits.

        Args:
            length (int): Length of the password. Default is 12.

        Returns:
            str: A secure random password.
        """
        characters = string.ascii_uppercase + string.digits
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    def dict(self, *args, **kwargs):
        """
        Override the default dict() method to include the dns_name and password.
        """
        original_dict = super().dict(*args, **kwargs)
        original_dict['dns_name'] = self.dns_name  # Add the dns_name property
        original_dict['password'] = self.generate_password()  # Add a generated password
        return original_dict