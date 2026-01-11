from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from app.services.pdf_extractor import PDFExtractor
from app.services.cv_parser import CVParser
from app.services.job_parser import JobParser
from app.services.scoring_engine import ScoringEngine
from app.services.recommendations import RecommendationsEngine

router = APIRouter()
pdf_extractor = PDFExtractor()
cv_parser = CVParser()
job_parser = JobParser()
scoring_engine = ScoringEngine()
recommendations_engine = RecommendationsEngine()

@router.post("/analyze")
async def analyze_cv(
    cv_file: UploadFile = File(...),
    job_offer: str = Form(...)
):
    
    if cv_file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="El archivo debe ser un PDF"
        )
    
    file_content = await cv_file.read()
    file_size = len(file_content)
    
    max_size = 5 * 1024 * 1024
    if file_size > max_size:
        raise HTTPException(
            status_code=400,
            detail="El archivo es demasiado grande. Máximo 5MB"
        )
    
    extraction_result = pdf_extractor.extract_text(file_content)
    
    if not extraction_result["success"]:
        raise HTTPException(
            status_code=500,
            detail=f"Error al extraer texto del PDF: {extraction_result.get('error', 'Error desconocido')}"
        )
    
    cv_analysis = cv_parser.parse(extraction_result["text"])
    
    job_analysis = job_parser.parse(job_offer)
    
    match_result = scoring_engine.calculate_match(cv_analysis, job_analysis)
    
    recommendations = recommendations_engine.generate(
        cv_analysis,
        job_analysis,
        match_result
    )
    
    return {
        "status": "success",
        "message": "Análisis completado correctamente",
        "data": {
            "cv_info": {
                "filename": cv_file.filename,
                "size_bytes": file_size,
                "num_pages": extraction_result["num_pages"],
                "num_characters": extraction_result["num_characters"]
            },
            "cv_analysis": cv_analysis,
            "job_analysis": job_analysis,
            "match_result": match_result,
            "recommendations": recommendations
        }
    }