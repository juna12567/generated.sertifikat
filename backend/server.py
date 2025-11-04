from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import qrcode
import io
import zipfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape
from reportlab.lib.utils import ImageReader
import shutil
import locale
import calendar

# Set locale for Indonesian month names
try:
    locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
except:
    pass

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Paths
UPLOADS_DIR = ROOT_DIR / "uploads"
OUTPUT_DIR = ROOT_DIR / "output"
FONTS_DIR = ROOT_DIR / "fonts"

# Ensure directories exist
UPLOADS_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
FONTS_DIR.mkdir(exist_ok=True)

# Font paths
FONT_REGULAR = str(FONTS_DIR / "DejaVuSerif.ttf")
FONT_ITALIC = str(FONTS_DIR / "DejaVuSerif-Italic.ttf")
FONT_BOLD = str(FONTS_DIR / "DejaVuSerif-Bold.ttf")

# Indonesian month names
INDONESIAN_MONTHS = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
    5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
    9: "September", 10: "Oktober", 11: "November", 12: "Desember"
}

# Define Models
class Certificate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    participant_count: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "completed"

class CertificateCreate(BaseModel):
    filename: str
    participant_count: int

# Helper functions
def format_date_indonesian(date_str):
    """Format date to Indonesian: '5 Agustus 2025'"""
    try:
        date_obj = pd.to_datetime(date_str)
        day = date_obj.day
        month = INDONESIAN_MONTHS[date_obj.month]
        year = date_obj.year
        return f"{day} {month} {year}"
    except:
        return date_str

def format_date_english(date_str):
    """Format date to English: 'August 5, 2025'"""
    try:
        date_obj = pd.to_datetime(date_str)
        return date_obj.strftime("%B %d, %Y").replace(" 0", " ")
    except:
        return date_str

def draw_centered_text(draw, text, y, font, img_width, color=(0, 0, 0)):
    """Draw text centered horizontally"""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (img_width - text_width) // 2
    draw.text((x, y), text, font=font, fill=color)
    return x, text_width

def draw_underline(draw, x, y, width, thickness=2):
    """Draw underline below text"""
    draw.rectangle([x, y, x + width, y + thickness], fill=(0, 0, 0))

def generate_qr_code(data, size=150):
    """Generate QR code and return as PIL Image"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=0,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img = qr_img.resize((size, size))
    return qr_img

def create_png_to_pdf(png_path, pdf_path):
    """Convert PNG to PDF with landscape orientation"""
    img = Image.open(png_path)
    img_width, img_height = img.size
    
    # Create PDF with custom size matching image
    c = canvas.Canvas(str(pdf_path), pagesize=(img_width, img_height))
    c.drawImage(ImageReader(img), 0, 0, width=img_width, height=img_height)
    c.save()

def generate_certificate(template_path, name, course, date_str, output_name):
    """
    Generate certificate with auto-scaling layout based on template size
    Returns tuple: (png_path, pdf_path)
    """
    # Open template
    img = Image.open(template_path)
    draw = ImageDraw.Draw(img)
    img_width, img_height = img.size
    
    # Calculate scale factor based on reference size (3000x2000)
    scale_w = img_width / 3000
    scale_h = img_height / 2000
    scale = min(scale_w, scale_h)  # Use smaller scale to fit
    
    # Helper function to scale font size
    def sf(size):
        return int(size * scale)
    
    # Helper function to scale Y position
    def sy(y):
        return int(y * scale_h)
    
    # Load fonts with scaled sizes
    font_title = ImageFont.truetype(FONT_ITALIC, sf(110))
    font_desc_id = ImageFont.truetype(FONT_REGULAR, sf(44))
    font_desc_en = ImageFont.truetype(FONT_ITALIC, sf(36))
    font_name = ImageFont.truetype(FONT_BOLD, sf(100))
    font_attended_id = ImageFont.truetype(FONT_REGULAR, sf(48))
    font_attended_en = ImageFont.truetype(FONT_ITALIC, sf(36))
    font_course = ImageFont.truetype(FONT_REGULAR, sf(58))
    font_course_en = ImageFont.truetype(FONT_ITALIC, sf(34))
    font_para_id = ImageFont.truetype(FONT_REGULAR, sf(44))
    font_para_en = ImageFont.truetype(FONT_ITALIC, sf(34))
    font_date_id = ImageFont.truetype(FONT_REGULAR, sf(44))
    font_date_en = ImageFont.truetype(FONT_ITALIC, sf(34))
    font_location = ImageFont.truetype(FONT_REGULAR, sf(36))
    font_signature_name = ImageFont.truetype(FONT_REGULAR, sf(44))
    font_signature_title = ImageFont.truetype(FONT_REGULAR, sf(34))
    
    # Format dates
    date_id = format_date_indonesian(date_str)
    date_en = format_date_english(date_str)
    
    # Draw texts with scaled positions
    # Title "Training Certificate"
    draw_centered_text(draw, "Training Certificate", sy(330), font_title, img_width, color=(45, 75, 30))
    
    # Description lines
    draw_centered_text(draw, "Sertifikat ini untuk menerangkan bahwa peserta berikut ini :", sy(460), font_desc_id, img_width)
    draw_centered_text(draw, "This is to certify that the following participant :", sy(505), font_desc_en, img_width)
    
    # Participant name (bold with underline)
    x, w = draw_centered_text(draw, name, sy(630), font_name, img_width)
    draw_underline(draw, x, sy(730), w, thickness=int(3 * scale))
    
    # "Has attended" bilingual
    draw_centered_text(draw, "Telah mengikuti", sy(770), font_attended_id, img_width)
    draw_centered_text(draw, "Has attended", sy(810), font_attended_en, img_width)
    
    # Course name
    draw_centered_text(draw, course, sy(885), font_course, img_width)
    draw_centered_text(draw, f"Training of {course}", sy(935), font_course_en, img_width)
    
    # Organizer paragraph
    draw_centered_text(draw, "Yang diselenggarakan oleh PT Aerofood Indonesia", sy(1005), font_para_id, img_width)
    draw_centered_text(draw, f"Pada tanggal {date_id}", sy(1045), font_para_id, img_width)
    draw_centered_text(draw, "Which was conducted by PT Aerofood Indonesia", sy(1085), font_para_en, img_width)
    draw_centered_text(draw, f"on {date_en}", sy(1120), font_para_en, img_width)
    
    # Location and date
    draw_centered_text(draw, f"Tangerang, {date_id}", sy(1200), font_location, img_width)
    
    # Generate and paste QR code
    qr_data = f"{name} | {course} | {date_id}"
    qr_size = int(150 * scale)
    qr_img = generate_qr_code(qr_data, size=qr_size)
    qr_x = (img_width - qr_size) // 2
    qr_y = sy(1270)
    img.paste(qr_img, (qr_x, qr_y))
    
    # Signature name and title
    x, w = draw_centered_text(draw, "Rakhmat Syarifudin", sy(1450), font_signature_name, img_width)
    draw_underline(draw, x, sy(1495), w, thickness=int(2 * scale))
    draw_centered_text(draw, "VP Human Capital Management", sy(1505), font_signature_title, img_width)
    
    # Save PNG
    png_path = OUTPUT_DIR / f"{output_name}.png"
    img.save(png_path, "PNG")
    
    # Create PDF
    pdf_path = OUTPUT_DIR / f"{output_name}.pdf"
    create_png_to_pdf(png_path, pdf_path)
    
    return str(png_path), str(pdf_path)

# API Routes
@api_router.get("/")
async def root():
    return {"message": "Generator Sertifikat Otomatis API"}

@api_router.post("/upload-template")
async def upload_template(file: UploadFile = File(...)):
    """Upload certificate template"""
    try:
        template_path = UPLOADS_DIR / "template.png"
        with open(template_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"message": "Template uploaded successfully", "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/generate")
async def generate_certificates(file: UploadFile = File(...)):
    """Generate certificates from Excel/CSV file"""
    try:
        # Check if template exists
        template_path = UPLOADS_DIR / "template.png"
        if not template_path.exists():
            raise HTTPException(status_code=400, detail="Template not found. Please upload template first.")
        
        # Read uploaded file
        contents = await file.read()
        
        # Determine file type and read with pandas
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="File must be CSV or Excel")
        
        # Validate columns
        required_cols = ['name', 'course', 'date']
        if not all(col in df.columns for col in required_cols):
            raise HTTPException(status_code=400, detail=f"Excel must have columns: {', '.join(required_cols)}")
        
        # Generate unique batch ID
        batch_id = str(uuid.uuid4())[:8]
        
        # Create ZIP file in memory
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Generate certificate for each participant
            for idx, row in df.iterrows():
                name = str(row['name']).strip()
                course = str(row['course']).strip()
                date = str(row['date']).strip()
                
                # Clean filename
                clean_name = name.replace(' ', '_').replace('/', '_')
                output_name = f"{batch_id}_{clean_name}"
                
                # Generate certificate
                png_path, pdf_path = generate_certificate(
                    str(template_path), name, course, date, output_name
                )
                
                # Add to ZIP
                zip_file.write(png_path, f"certificates/{clean_name}.png")
                zip_file.write(pdf_path, f"certificates/{clean_name}.pdf")
        
        # Save to MongoDB
        cert_data = {
            "id": batch_id,
            "filename": file.filename,
            "participant_count": len(df),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "status": "completed"
        }
        await db.certificates.insert_one(cert_data)
        
        # Return ZIP file
        zip_buffer.seek(0)
        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename=certificates_{batch_id}.zip"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating certificates: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/certificates", response_model=List[Certificate])
async def get_certificates():
    """Get list of generated certificates"""
    certificates = await db.certificates.find({}, {"_id": 0}).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for cert in certificates:
        if isinstance(cert['created_at'], str):
            cert['created_at'] = datetime.fromisoformat(cert['created_at'])
    
    return certificates

@api_router.get("/download-sample")
async def download_sample():
    """Download sample Excel file"""
    sample_path = UPLOADS_DIR / "sample_data.xlsx"
    if not sample_path.exists():
        raise HTTPException(status_code=404, detail="Sample file not found")
    
    return FileResponse(
        path=str(sample_path),
        filename="sample_participants.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()