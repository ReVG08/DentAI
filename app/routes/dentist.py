from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from app.auth import get_current_user
from app.database import SessionLocal
from app.models import Analysis
from app.ai_engine import DentalAIEngine
from app.image_processor import ImageProcessor
from app.pdf_generator import PDFGenerator
from PIL import Image
import uuid, os, io

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/dentist")
def dentist_dashboard(request: Request):
    user = get_current_user(request)
    if not user or user.user_type != "dentist":
        return RedirectResponse("/", status_code=302)
    db = SessionLocal()
    analyses = db.query(Analysis).filter(Analysis.user_id == user.id).all()
    db.close()
    return templates.TemplateResponse("dentist.html", {"request": request, "analyses": analyses})

@router.post("/dentist/analyze")
async def analyze(
    request: Request,
    patient_name: str = Form(...),
    patient_age: int = Form(...),
    patient_gender: str = Form(...),
    patient_complaint: str = Form(...),
    patient_medical_history: str = Form(...),
    file: UploadFile = File(...)
):
    user = get_current_user(request)
    if not user or user.user_type != "dentist":
        return RedirectResponse("/", status_code=302)

    # Save uploaded file
    filename = f"{uuid.uuid4()}_{file.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(await file.read())

    # Open and process image
    img = Image.open(filepath)
    processor = ImageProcessor()
    processed_images = processor.process_batch([img])

    # Patient info
    patient_info = {
        "name": patient_name,
        "age": patient_age,
        "gender": patient_gender,
        "complaint": patient_complaint,
        "medical_history": patient_medical_history
    }

    # Run AI analysis
    engine = DentalAIEngine(api_key=user.openai_api_key)
    analysis_result = engine.analyze_images(processed_images, patient_info)

    # Save to DB
    db = SessionLocal()
    analysis = Analysis(
        user_id=user.id,
        patient_name=patient_name,
        patient_age=patient_age,
        patient_gender=patient_gender,
        patient_complaint=patient_complaint,
        patient_medical_history=patient_medical_history,
        uploaded_filename=filename,
        analysis_result=analysis_result,
    )
    db.add(analysis)
    db.commit()
    db.close()

    return RedirectResponse("/dentist", status_code=302)

@router.get("/dentist/report/{analysis_id}")
def download_report(request: Request, analysis_id: int):
    user = get_current_user(request)
    if not user or user.user_type != "dentist":
        return RedirectResponse("/", status_code=302)
    db = SessionLocal()
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id, Analysis.user_id == user.id).first()
    db.close()
    if not analysis:
        return RedirectResponse("/dentist", status_code=302)
    patient_info = {
        "name": analysis.patient_name,
        "age": analysis.patient_age,
        "gender": analysis.patient_gender,
        "complaint": analysis.patient_complaint,
        "medical_history": analysis.patient_medical_history
    }
    pdf_gen = PDFGenerator()
    pdf_bytes = pdf_gen.generate_summary_pdf(patient_info, analysis.analysis_result)
    return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf", headers={"Content-Disposition": f"attachment;filename=report_{analysis.id}.pdf"})