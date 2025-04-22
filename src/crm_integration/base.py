"""
Base CRM integration module
Defines the interface for CRM integrations
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseCRMIntegration(ABC):
    """Base class for CRM integrations"""
    
    def __init__(self, api_endpoint: str, username: str, password: str):
        """Initialize the CRM integration with credentials"""
        self.api_endpoint = api_endpoint
        self.username = username
        self.password = password
        self.authenticated = False
    
    @abstractmethod
    def authenticate(self) -> bool:
        """
        Authenticate with the CRM
        
        Returns:
            Boolean indicating if authentication was successful
        """
        pass
    
    @abstractmethod
    def get_patient(self, patient_id: str) -> Dict[str, Any]:
        """
        Retrieve patient information from the CRM
        
        Args:
            patient_id: Patient identifier in the CRM
            
        Returns:
            Dictionary containing patient information
        """
        pass
    
    @abstractmethod
    def save_report(self, patient_id: str, report_data: Dict[str, Any]) -> bool:
        """
        Save a report to the CRM
        
        Args:
            patient_id: Patient identifier in the CRM
            report_data: Dictionary containing report data
            
        Returns:
            Boolean indicating if save was successful
        """
        pass
    
    @abstractmethod
    def list_patients(self, query: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List patients from the CRM
        
        Args:
            query: Optional search query
            
        Returns:
            List of dictionaries containing patient information
        """
        pass
    
    @abstractmethod
    def upload_attachment(self, patient_id: str, file_data: bytes, file_name: str, file_type: str) -> bool:
        """
        Upload an attachment to the CRM
        
        Args:
            patient_id: Patient identifier in the CRM
            file_data: File content as bytes
            file_name: Name of the file
            file_type: MIME type of the file
            
        Returns:
            Boolean indicating if upload was successful
        """
        pass


class CRMIntegrationError(Exception):
    """Exception raised for errors in CRM integration."""
    pass


def get_crm_integration(crm_type: str, api_endpoint: str, username: str, password: str) -> BaseCRMIntegration:
    """
    Factory function to get the appropriate CRM integration
    
    Args:
        crm_type: Type of CRM (e.g., 'dentrix', 'eaglesoft', 'open_dental')
        api_endpoint: API endpoint for the CRM
        username: Username for CRM authentication
        password: Password for CRM authentication
        
    Returns:
        CRM integration instance
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
