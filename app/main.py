from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from starlette.requests import Request
import os
from .model import process_image

app = FastAPI()

# 挂载静态文件
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# 创建上传目录
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(400, detail="Only PNG and JPEG files are allowed")
    
    # 保存上传的图片
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # 处理图片生成3D模型
    output_path = os.path.join(OUTPUT_DIR, f"{file.filename.split('.')[0]}.ply")
    try:
        await process_image(file_path, output_path)
        return {"filename": os.path.basename(output_path)}
    except Exception as e:
        raise HTTPException(500, detail=str(e))

@app.get("/model/{filename}")
async def get_model(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(404, detail="Model not found")
    return FileResponse(file_path)