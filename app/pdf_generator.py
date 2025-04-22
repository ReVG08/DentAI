"""
PDF report generator for dental AI analysis results
Creates professionally formatted PDF reports
"""
import io
from typing import Dict, Any, Optional
from datetime import datetime
import os

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image

class PDFGenerator:
    """Generates PDF reports from dental AI analysis results"""
    
    def __init__(self, logo_path: Optional[str] = None):
        """
        Initialize the PDF generator
        
        Args:
            logo_path: Optional path to clinic logo image
        """
        self.logo_path = logo_path
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Set up custom paragraph styles for the reports"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            alignment=1,  # Center
            spaceAfter=12
        ))
        
        # Section heading style
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=12,
            spaceAfter=6
        ))
        
        # Normal text style
        self.styles.add(ParagraphStyle(
            name='ReportText',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceBefore=6,
            spaceAfter=6
        ))
        
        # Patient info style
        self.styles.add(ParagraphStyle(
            name='PatientInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceBefore=0,
            spaceAfter=0
        ))
        
        # Footer style
        self.styles.add(ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.gray
        ))
    
    def _create_header(self, doc, clinic_name: str = "Dental Clinic"):
        """Create the header section of the report with logo and clinic info"""
        elements = []
        
        # Add logo if available
        if self.logo_path and os.path.exists(self.logo_path):
            img = Image(self.logo_path, width=100, height=50)
            elements.append(img)
            elements.append(Spacer(1, 10))
        
        # Add clinic name
        elements.append(Paragraph(clinic_name, self.styles['ReportTitle']))
        elements.append(Spacer(1, 10))
        
        # Add date
        date_text = f"Report Generated: {datetime.now().strftime('%B %d, %Y %H:%M')}"
        elements.append(Paragraph(date_text, self.styles['Normal']))
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_patient_info_section(self, patient_info: Dict[str, Any]):
        """Create the patient information section"""
        elements = []
        
        elements.append(Paragraph("Patient Information", self.styles['SectionHeading']))
        
        # Create patient info table
        data = [
            ["Name:", patient_info.get('name', 'N/A')],
            ["Age:", str(patient_info.get('age', 'N/A'))],
            ["Gender:", patient_info.get('gender', 'N/A')],
            ["Primary Complaint:", patient_info.get('complaint', 'N/A')],
            ["Medical History:", patient_info.get('medical_history', 'N/A')]
        ]
        
        table = Table(data, colWidths=[100, 400])
        table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('VALIGN', (0, 4), (0, 4), 'TOP'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 15))
        
        return elements
    
    def _create_findings_section(self, report_content: str):
        """Create the findings section from the report content"""
        elements = []
        
        # Parse the report content to extract sections
        sections = self._parse_report_sections(report_content)
        
        # Add each section
        for title, content in sections.items():
            elements.append(Paragraph(title, self.styles['SectionHeading']))
            
            # Split content by paragraphs and add each paragraph
            paragraphs = content.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    elements.append(Paragraph(para, self.styles['ReportText']))
            
            elements.append(Spacer(1, 10))
        
        return elements
    
    def _parse_report_sections(self, report_content: str) -> Dict[str, str]:
        """
        Parse the report content into sections
        
        Args:
            report_content: Raw report text
            
        Returns:
            Dictionary with section titles as keys and content as values
        """
        sections = {}
        current_section = "Findings"
        current_content = []
        
        lines = report_content.split('\n')
        
        for line in lines:
            # Check if line is a section header (e.g., "### Section Title" or "## Section Title")
            if line.startswith('#'):
                # If we have content in the current section, save it
                if current_content:
                    sections[current_section] = '\n'.join(current_content)
                    current_content = []
                
                # Extract new section title from markdown heading
                current_section = line.strip('#').strip()
            else:
                current_content.append(line)
        
        # Add the last section
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        
        # If no sections were found, use the entire content as "Findings"
        if not sections:
            sections["Findings"] = report_content
            
        return sections
    
    def _create_signature_section(self):
        """Create the signature section for the doctor"""
        elements = []
        
        elements.append(Paragraph("Approval", self.styles['SectionHeading']))
        
        # Add signature fields
        elements.append(Paragraph("I confirm that I have reviewed this AI-generated report and:", self.styles['ReportText']))
        elements.append(Spacer(1, 20))
        
        data = [
            ["☐", "Approve the findings as presented"],
            ["☐", "Approve with modifications noted below"],
            ["☐", "Reject the findings"]
        ]
        
        table = Table(data, colWidths=[30, 470])
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (0, -1), 14),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        # Add doctor's notes section
        elements.append(Paragraph("Notes:", self.styles['ReportText']))
        elements.append(Spacer(1, 40))
        
        # Add signature line
        elements.append(Paragraph("_" * 50, self.styles['Normal']))
        elements.append(Paragraph("Doctor's Signature", self.styles['Footer']))
        elements.append(Spacer(1, 15))
        
        elements.append(Paragraph("_" * 50, self.styles['Normal']))
        elements.append(Paragraph("Date", self.styles['Footer']))
        
        return elements
    
    def _create_footer(self, canvas, doc):
        """Add footer to each page"""
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.grey)
        
        # Add page number
        page_num = canvas.getPageNumber()
        text = f"Page {page_num}"
        canvas.drawRightString(letter[0]-30, 30, text)
        
        # Add disclaimer
        disclaimer = "AI-GENERATED REPORT: This report was generated with artificial intelligence and should be reviewed by a qualified dental professional before use in diagnosis or treatment."
        canvas.drawString(30, 30, disclaimer)
        
        canvas.restoreState()
    
    def generate_summary_pdf(self, patient_info: Dict[str, Any], report_content: str, clinic_name: str = "Dental Clinic") -> bytes:
        """
        Generate a summary PDF report for dentist approval
        
        Args:
            patient_info: Dictionary containing patient information
            report_content: Generated report content
            clinic_name: Name of the dental clinic
            
        Returns:
            PDF content as bytes
        """
        buffer = io.BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=letter,
            rightMargin=30,
            leftMargin=30,
            topMargin=30,
            bottomMargin=50
        )
        
        # Create elements list
        elements = []
        
        # Add header
        elements.extend(self._create_header(doc, clinic_name))
        
        # Add title
        elements.append(Paragraph("Dental AI Analysis - Summary Report", self.styles['ReportTitle']))
        elements.append(Spacer(1, 10))
        
        # Add patient info section
        elements.extend(self._create_patient_info_section(patient_info))
        
        # Add findings
        elements.extend(self._create_findings_section(report_content))
        
        # Add signature section
        elements.extend(self._create_signature_section())
        
        # Build PDF
        doc.build(elements, onFirstPage=self._create_footer, onLaterPages=self._create_footer)
        
        # Return PDF data
        buffer.seek(0)
        return buffer.getvalue()
    
    def generate_detailed_pdf(self, patient_info: Dict[str, Any], report_content: str, clinic_name: str = "Dental Clinic") -> bytes:
        """
        Generate a detailed PDF report with the AI's reasoning
        
        Args:
            patient_info: Dictionary containing patient information
            report_content: Generated report content
            clinic_name: Name of the dental clinic
            
        Returns:
            PDF content as bytes
        """
        buffer = io.BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=letter,
            rightMargin=30,
            leftMargin=30,
            topMargin=30,
            bottomMargin=50
        )
        
        # Create elements list
        elements = []
        
        # Add header
        elements.extend(self._create_header(doc, clinic_name))
        
        # Add title
        elements.append(Paragraph("Dental AI Analysis - Detailed Report", self.styles['ReportTitle']))
        elements.append(Spacer(1, 10))
        
        # Add patient info section
        elements.extend(self._create_patient_info_section(patient_info))
        
        # Add detailed findings
        elements.extend(self._create_findings_section(report_content))
        
        # Add AI disclaimer
        elements.append(Spacer(1, 20))
        disclaimer = "DISCLAIMER: This detailed report provides the AI system's reasoning and analysis. All findings should be independently verified by a qualified dental professional."
        elements.append(Paragraph(disclaimer, self.styles['Footer']))
        
        # Build PDF
        doc.build(elements, onFirstPage=self._create_footer, onLaterPages=self._create_footer)
        
        # Return PDF data
        buffer.seek(0)
        return buffer.getvalue()