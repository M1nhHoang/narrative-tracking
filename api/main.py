from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import os
from datetime import datetime

app = FastAPI(title="Chainslab Analytics API")

# Cấu hình CORS để frontend có thể gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong môi trường production nên hạn chế origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đường dẫn đến thư mục dữ liệu
DATA_DIR = "api/data"

# Đảm bảo thư mục dữ liệu tồn tại
def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

# Sao chép file markdown mẫu nếu không tồn tại
def initialize_data():
    ensure_data_dir()

# Khởi tạo dữ liệu khi ứng dụng khởi động
initialize_data()

# API endpoints
@app.get("/")
def read_root():
    return {"message": "Welcome to Chainslab Analytics API"}

# Endpoint trả về toàn bộ nội dung markdown cho một dự án
@app.get("/api/projects/{project_id}/markdown")
def get_project_markdown(project_id: str):
    project_id = project_id.lower()
    
    # Xác định đường dẫn file markdown
    if project_id == "neo":
        markdown_file = os.path.join(DATA_DIR, "sample_1.md")
    else:
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
    
    # Kiểm tra file tồn tại
    if not os.path.exists(markdown_file):
        raise HTTPException(status_code=404, detail=f"Markdown file for project {project_id} not found")
    
    # Đọc nội dung markdown
    with open(markdown_file, "r", encoding="utf-8") as f:
        markdown_content = f.read()
    
    return {"content": markdown_content}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 