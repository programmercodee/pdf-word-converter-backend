from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os
from pdf2docx import Converter
import uuid
from fastapi.middleware.cors import CORSMiddleware
import subprocess
from fastapi import HTTPException
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173" , "https://pdf-word-convertor-frontend.vercel.app" ],  # or ["*"] for all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.post("/pdf-to-word/")
async def pdf_to_word(file: UploadFile = File(...)):
    input_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.pdf")
    output_path = input_path.replace(".pdf", ".docx")

    with open(input_path, "wb") as f:
        f.write(await file.read())

    cv = Converter(input_path)
    cv.convert(output_path)
    cv.close()

    return FileResponse(output_path, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", filename="converted.docx")


# @app.post("/word-to-pdf/")
# async def word_to_pdf(file: UploadFile = File(...)):
#     input_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.docx")
#     output_path = input_path.replace(".docx", ".pdf")

#     with open(input_path, "wb") as f:
#         f.write(await file.read())

#     # Convert .docx to .pdf
#     docx_to_pdf_convert(input_path, output_path)

#     return FileResponse(output_path, media_type="application/pdf", filename="converted.pdf")


@app.post("/word-to-pdf/")
async def word_to_pdf(file: UploadFile = File(...)):
    input_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.docx")
    output_dir = TEMP_DIR

    with open(input_path, "wb") as f:
        f.write(await file.read())

    try:
        subprocess.run([
            "libreoffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", output_dir,
            input_path
        ], check=True)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"LibreOffice conversion failed: {e}")

    output_path = input_path.replace(".docx", ".pdf")

    return FileResponse(output_path, media_type="application/pdf", filename="converted.pdf")