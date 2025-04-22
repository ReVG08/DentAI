"""
PDF report generator for dental AI analysis results.
Creates professionally formatted PDF reports.
"""

import io
from typing import Dict, Any, Optional
from datetime import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

class PDFGenerator:
    """Generates PDF reports from dental AI analysis results."""

    def __init__(self, logo_path: Optional[str] = None):
        self.logo_path = logo_path
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Define custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            alignment=1,  # Center
            spaceAfter=12
        ))
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=12,
            spaceAfter=6
        ))
        self.styles.add(ParagraphStyle(
            name='ReportText',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceBefore=6,
            spaceAfter=6
        ))
        self.styles.add(ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.gray
        ))

    def _create_header(self, clinic_name="Dental Clinic"):
        """Create header with logo and clinic info."""
        elements = []
        if self.logo_path and os.path.exists(self.logo_path):
            elements.append(RLImage(self.logo_path, width=100, height=50))
            elements.append(Spacer(1, 10))
        elements.append(Paragraph(clinic_name, self.styles['ReportTitle']))
        elements.append(Spacer(1, 10))
        date_text = f"Report Generated: {datetime.now().strftime('%B %d, %Y %H:%M')}"
        elements.append(Paragraph(date_text, self.styles['Normal']))
        elements.append(Spacer(1, 20))
        return elements

    def _create_patient_info_section(self, patient_info: Dict[str, Any]):
        elements = [Paragraph("Patient Information", self.styles['SectionHeading'])]
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
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 15))
        return elements

    def _parse_report_sections(self, report_content: str) -> Dict[str, str]:
        """Parse report content into sections by markdown headings."""
        sections = {}
        current_section = "Findings"
        current_content = []
        lines = report_content.split('\n')
        for line in lines:
            if line.strip().startswith('#'):
                if current_content:
                    sections[current_section] = '\n'.join(current_content)
                    current_content = []
                current_section = line.lstrip('#').strip()
            else:
                current_content.append(line)
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        if not sections:
            sections["Findings"] = report_content
        return sections

    def _create_findings_section(self, report_content: str):
        elements = []
        sections = self._parse_report_sections(report_content)
        for title, content in sections.items():
            elements.append(Paragraph(title, self.styles['SectionHeading']))
            for para in filter(None, (p.strip() for p in content.split('\n\n'))):
                elements.append(Paragraph(para, self.styles['ReportText']))
            elements.append(Spacer(1, 10))
        return elements

    def _create_signature_section(self):
        elements = [Paragraph("Approval", self.styles['SectionHeading'])]
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
        elements.append(Paragraph("Notes:", self.styles['ReportText']))
        elements.append(Spacer(1, 40))
        elements.append(Paragraph("_" * 50, self.styles['Normal']))
        elements.append(Paragraph("Doctor's Signature", self.styles['Footer']))
        elements.append(Spacer(1, 15))
        elements.append(Paragraph("_" * 50, self.styles['Normal']))
        elements.append(Paragraph("Date", self.styles['Footer']))
        return elements

    def _create_footer(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.grey)
        page_num = canvas.getPageNumber()
        canvas.drawRightString(letter[0]-30, 30, f"Page {page_num}")
        disclaimer = (
            "AI-GENERATED REPORT: This report was generated with artificial intelligence and "
            "should be reviewed by a qualified dental professional before use in diagnosis or treatment."
        )
        canvas.drawString(30, 30, disclaimer)
        canvas.restoreState()

    def generate_summary_pdf(self, patient_info: Dict[str, Any], report_content: str, clinic_name: str = "Dental Clinic") -> bytes:
        """Generate a summary PDF report for dentist approval."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=50
        )
        elements = []
        elements.extend(self._create_header(clinic_name))
        elements.append(Paragraph("Dental AI Analysis - Summary Report", self.styles['ReportTitle']))
        elements.append(Spacer(1, 10))
        elements.extend(self._create_patient_info_section(patient_info))
        elements.extend(self._create_findings_section(report_content))
        elements.extend(self._create_signature_section())
        doc.build(elements, onFirstPage=self._create_footer, onLaterPages=self._create_footer)
        buffer.seek(0)
        return buffer.getvalue()

    def generate_detailed_pdf(self, patient_info: Dict[str, Any], report_content: str, clinic_name: str = "Dental Clinic") -> bytes:
        """Generate a detailed PDF report with AI's reasoning."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=50
        )
        elements = []
        elements.extend(self._create_header(clinic_name))
        elements.append(Paragraph("Dental AI Analysis - Detailed Report", self.styles['ReportTitle']))
        elements.append(Spacer(1, 10))
        elements.extend(self._create_patient_info_section(patient_info))
        elements.extend(self._create_findings_section(report_content))
        elements.append(Spacer(1, 20))
        disclaimer = (
            "DISCLAIMER: This detailed report provides the AI system's reasoning and analysis. "
            "All findings should be independently verified by a qualified dental professional."
        )
        elements.append(Paragraph(disclaimer, self.styles['Footer']))
        doc.build(elements, onFirstPage=self._create_footer, onLaterPages=self._create_footer)
        buffer.seek(0)
        return buffer.getvalue()