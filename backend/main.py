from fastapi import FastAPI,UploadFile,File,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import shutil
from typing import List,Dict,Any
from rag_system import RAGSystem
from test_case_generator import TestCaseGenerator
from script_generator import ScriptGenerator

app = FastAPI(title="Autonomous QA Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_system = None
test_case_generator = None
script_generator = None
html_content = None  # Store HTML content separately

UPLOAD_DIR = "uploads"
HTML_DIR = "html_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(HTML_DIR, exist_ok=True)

@app.post("/upload-documents")
async def upload_documents(files: List[UploadFile] = File(...)):
    saved_files = []
    for file in files:
        # Skip HTML
        if file.filename.endswith('.html'):
            continue
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            saved_files.append(file_path)
            
    return JSONResponse({
            "status": "success",
            "message": f"Uploaded {len(saved_files)} files",
            "files": saved_files
        })


@app.post("/upload-html")
async def upload_html(file: UploadFile = File(...)):
    global html_content
    if not file.filename.endswith('.html'):
        raise HTTPException(status_code=400, detail="Only HTML files allowed")

    html_path = os.path.join(HTML_DIR, file.filename)
    with open(html_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return JSONResponse({
        "status": "success",
        "message": "HTML file uploaded successfully",
        "file": html_path
    })

@app.post("/build-knowledge-base")
async def build_knowledge_base():
    global rag_system, test_case_generator, script_generator
    if not os.listdir(UPLOAD_DIR):
        raise HTTPException(status_code=400, detail="No documents uploaded. Please upload documents first.")
    rag_system = RAGSystem(UPLOAD_DIR)
    rag_system.build_knowledge_base()
    test_case_generator = TestCaseGenerator(rag_system)
    script_generator = ScriptGenerator(rag_system)
    return JSONResponse({
        "status": "success",
        "message": "Knowledge base built successfully"
    })


@app.post("/generate-test-cases")
async def generate_test_cases(query: str):
    if not test_case_generator:
        raise HTTPException(status_code=400, detail="Knowledge base not built. Please build knowledge base first.")
    test_cases = test_case_generator.generate_test_cases(query)
    return JSONResponse({
        "status": "success",
        "test_cases": test_cases
        })


@app.post("/generate-script")
async def generate_selenium_script(test_case: Dict[str, Any]):
    global html_content
    if not script_generator:
        raise HTTPException(status_code=400, detail="Knowledge base not built")
    if not html_content:
        raise HTTPException(status_code=400, detail="HTML file not uploaded. Please upload HTML file first.")
    script = script_generator.generate_script_with_html(test_case, html_content) 
    return JSONResponse({
        "status": "success",
        "script": script
    })


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "rag_system": rag_system is not None,
        "html_uploaded": html_content is not None
    }

@app.get("/status")
async def get_status():
    return JSONResponse({
        "knowledge_base_built": rag_system is not None,
        "html_uploaded": html_content is not None,
        "documents_count": len(os.listdir(UPLOAD_DIR)) if os.path.exists(UPLOAD_DIR) else 0
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)