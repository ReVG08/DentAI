"""
Report generator for dental AI analysis
Generates different types of reports based on AI analysis
"""
from typing import Dict, Any
from datetime import datetime

from openai import OpenAI
import config

class ReportGenerator:
    """Generates dental reports based on AI analysis"""
    
    def __init__(self, api_key: str = None):
        """Initialize the report generator"""
        self.api_key = api_key or config.OPENAI_API_KEY
        self.client = OpenAI(api_key=self.api_key)
    
    def generate_detailed_report(self, analysis: str, patient_info: Dict[str, Any]) -> str:
        """
        Generate a detailed report explaining the reasoning behind the diagnosis
        
        Args:
            analysis: Raw analysis from the vision model
            patient_info: Dictionary containing patient information
            
        Returns:
            Detailed report as a string
        """
        try:
            response = self.client.chat.completions.create(
                model=config.COMPLETION_MODEL,
                messages=[
                    {"role": "system", "content": "You are a dental AI assistant generating reports for dentists. Create detailed, professional reports that explain the reasoning behind potential diagnoses. Include specific observations from the images and relate them to possible dental conditions."},
                    {"role": "user", "content": f"""Based on the following analysis of dental images and patient information, generate a detailed report for the dentist explaining the reasoning behind each potential diagnosis.
                    
                    Patient Information:
                    Name: {patient_info.get('name')}
                    Age: {patient_info.get('age')}
                    Gender: {patient_info.get('gender')}
                    Primary complaint: {patient_info.get('complaint')}
                    Medical history: {patient_info.get('medical_history')}
                    
                    Image Analysis:
                    {analysis}
                    
                    Format the report professionally with sections including:
                    1. Patient Information
                    2. Summary of Findings
                    3. Detailed Analysis by Region
                    4. Potential Diagnoses and Reasoning
                    5. Recommendations for Additional Tests/Imaging
                    """}
                ],
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise ReportGeneratorError(f"Error generating detailed report: {str(e)}")
    
    def generate_summary_report(self, analysis: str, patient_info: Dict[str, Any]) -> str:
        """
        Generate a concise report for the doctor to review and sign. Add the key findings and a single potential and most likely diagnostic. For this one do not suggest a doctor.
        
        Args:
            analysis: Raw analysis from the vision model
            patient_info: Dictionary containing patient information
            
        Returns:
            Summary report as a string
        """
        try:
            response = self.client.chat.completions.create(
                model=config.COMPLETION_MODEL,
                messages=[
                    {"role": "system", "content": "You are a dental AI assistant generating concise reports for dentists to review and sign. Create professional, clinical summaries that highlight key findings and potential diagnoses."},
                    {"role": "user", "content": f"""Based on the following analysis of dental images and patient information, generate a concise report for the dentist to review and sign if correct.
                    
                    Patient Information:
                    Name: {patient_info.get('name')}
                    Age: {patient_info.get('age')}
                    Gender: {patient_info.get('gender')}
                    Primary complaint: {patient_info.get('complaint')}
                    Medical history: {patient_info.get('medical_history')}
                    Date: {datetime.now().strftime('%B %d, %Y')}
                    
                    Image Analysis:
                    {analysis}
                    
                    Format as a professional dental report with:
                    1. Patient Information
                    2. Key Findings
                    3. Potential Diagnoses
                    4. Recommended Treatment Plan
                    5. Signature Line for Doctor's Approval
                    """}
                ],
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise ReportGeneratorError(f"Error generating summary report: {str(e)}")


class ReportGeneratorError(Exception):
    """Exception raised for errors in the Report Generator."""
    pass
