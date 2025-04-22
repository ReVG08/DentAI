# ... (imports unchanged)
class PDFGenerator:
    def __init__(
        self,
        logo_path: Optional[str] = None,
        watermark_path: Optional[str] = None,
        footer_note: Optional[str] = None,
        show_signature_block: bool = True,
        show_patient_id: bool = False,
        clinic_email: str = "",
        clinic_phone: str = "",
        clinic_address: str = "",
    ):
        self.logo_path = logo_path
        self.watermark_path = watermark_path
        self.footer_note = footer_note
        self.show_signature_block = show_signature_block
        self.show_patient_id = show_patient_id
        self.clinic_email = clinic_email
        self.clinic_phone = clinic_phone
        self.clinic_address = clinic_address
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    # ... all other methods mostly unchanged except for header/footer adjustments:

    def _create_header(self, doc, clinic_name: str = "Dental Clinic"):
        elements = []
        if self.logo_path and os.path.exists(self.logo_path):
            img = Image(self.logo_path, width=100, height=50)
            elements.append(img)
            elements.append(Spacer(1, 10))
        elements.append(Paragraph(clinic_name, self.styles['ReportTitle']))
        contact_info = " | ".join(
            [x for x in [self.clinic_email, self.clinic_phone] if x]
        )
        if contact_info:
            elements.append(Paragraph(contact_info, self.styles['Normal']))
        if self.clinic_address:
            elements.append(Paragraph(self.clinic_address, self.styles['Normal']))
        elements.append(Spacer(1, 10))
        date_text = f"Report Generated: {datetime.now().strftime('%B %d, %Y %H:%M')}"
        elements.append(Paragraph(date_text, self.styles['Normal']))
        elements.append(Spacer(1, 20))
        return elements

    def _create_patient_info_section(self, patient_info: Dict[str, Any]):
        elements = []
        elements.append(Paragraph("Patient Information", self.styles['SectionHeading']))
        data = [
            ["Name:", patient_info.get('name', 'N/A')],
            ["Age:", str(patient_info.get('age', 'N/A'))],
            ["Gender:", patient_info.get('gender', 'N/A')],
            ["Primary Complaint:", patient_info.get('complaint', 'N/A')],
            ["Medical History:", patient_info.get('medical_history', 'N/A')]
        ]
        if self.show_patient_id and patient_info.get("patient_id"):
            data.insert(1, ["Patient ID:", str(patient_info.get("patient_id"))])
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

    def _create_signature_section(self):
        if not self.show_signature_block:
            return []
        # ... (rest unchanged, see previous message) ...

    def _create_footer(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.grey)
        page