"""
Base CRM integration module.
Defines the interface for CRM integrations.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List

class BaseCRMIntegration(ABC):
    """Abstract base class for CRM integrations."""

    def __init__(self, api_endpoint: str, username: str, password: str):
        self.api_endpoint = api_endpoint
        self.username = username
        self.password = password
        self.authenticated = False

    @abstractmethod
    def authenticate(self) -> bool:
        """Authenticate with the CRM and return True if successful."""
        pass

    @abstractmethod
    def get_patient(self, patient_id: str) -> Dict[str, Any]:
        """Retrieve patient information from the CRM."""
        pass

    @abstractmethod
    def save_report(self, patient_id: str, report_data: Dict[str, Any]) -> bool:
        """Save a report to the CRM."""
        pass

    @abstractmethod
    def list_patients(self, query: Optional[str] = None) -> List[Dict[str, Any]]:
        """List patients from the CRM, optionally filtered by query."""
        pass

    @abstractmethod
    def upload_attachment(self, patient_id: str, file_data: bytes, file_name: str, file_type: str) -> bool:
        """Upload an attachment to the CRM for a patient."""
        pass

class CRMIntegrationError(Exception):
    """Exception for CRM integration errors."""
    pass

def get_crm_integration(crm_type: str, api_endpoint: str, username: str, password: str) -> BaseCRMIntegration:
    """
    Factory to instantiate the correct CRM integration.
    """
    crm_type = crm_type.lower()
    if crm_type == 'dentrix':
        from .dentrix import DentrixCRMIntegration
        return DentrixCRMIntegration(api_endpoint, username, password)
    elif crm_type == 'eaglesoft':
        from .eaglesoft import EaglesoftCRMIntegration
        return EaglesoftCRMIntegration(api_endpoint, username, password)
    elif crm_type == 'open_dental':
        from .open_dental import OpenDentalCRMIntegration
        return OpenDentalCRMIntegration(api_endpoint, username, password)
    else:
        raise ValueError(f"Unsupported CRM type: {crm_type}")