from fastapi import FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from typing import List
from datetime import datetime
import os
import json
import mimetypes
import bleach
import re
from fastapi import Request
from markupsafe import Markup

# Load configuration from JSON
CONFIG_FILE = "config.json"
if not os.path.exists(CONFIG_FILE):
    raise FileNotFoundError(f"{CONFIG_FILE} not found in the application directory.")

with open(CONFIG_FILE, "r") as config_file:
    config = json.load(config_file)

PIN = config["pin"]
MAX_FILE_SIZE = config["max_file_size"]
ALLOWED_MIME_TYPES = config["allowed_mime_types"]

# Initialize FastAPI application
app = FastAPI()

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],  # Limit to trusted origins
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure the upload directory exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Track connected clients
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.users = {}  # To track users and their nicknames

    async def connect(self, websocket: WebSocket, nickname: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.users[websocket] = nickname
        await self.broadcast_users()
        await self.broadcast(f"{nickname} joined the chat.")

    def disconnect(self, websocket: WebSocket):
        nickname = self.users.pop(websocket, "Unknown")
        self.active_connections.remove(websocket)
        return nickname

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, sender: WebSocket = None):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def broadcast_users(self):
        users_list = list(self.users.values())
        users_message = f"Online Users: {', '.join(users_list)}"
        for connection in self.active_connections:
            await connection.send_text(f"USERS:{users_message}")

manager = ConnectionManager()

# Dependency to check PIN
async def verify_pin(pin: str):
    if pin != PIN:
        raise HTTPException(status_code=401, detail="Invalid PIN")


# Sanitize inputs
def sanitize_input(input_data: str) -> str:
    # Clean user input using bleach to remove dangerous characters
    return bleach.clean(input_data)

# Validate nickname input (only alphanumeric characters and underscores)
def validate_nickname(nickname: str) -> str:
    if not re.match(r'^[a-zA-Z0-9_]+$', nickname):
        raise HTTPException(status_code=400, detail="Invalid nickname. Only alphanumeric characters and underscores are allowed.")
    return nickname


@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket, pin: str, nickname: str):
    await verify_pin(pin)

    # Sanitize and validate the nickname
    sanitized_nickname = sanitize_input(nickname)
    validated_nickname = validate_nickname(sanitized_nickname)

    await manager.connect(websocket, validated_nickname)
    try:
        while True:
            data = await websocket.receive_text()
            sanitized_message = sanitize_input(data)  # Sanitize the message input
            nickname = manager.users.get(websocket, "Unknown")
            timestamp = datetime.now().strftime("%I:%M %p")  # e.g., "12:34 PM"
            message = f"[{timestamp}] {nickname}: {sanitized_message}"
            await manager.broadcast(message, sender=websocket)
    except WebSocketDisconnect:
        nickname = manager.disconnect(websocket)
        await manager.broadcast(f"{nickname} left the chat.")
        await manager.broadcast_users()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return templates.TemplateResponse("index.html", {"request": {}})


@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/upload/")
async def upload_file(file: UploadFile):
    file_content = await file.read()

    # Check file size
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds limit")

    # Validate file type
    mime_type, _ = mimetypes.guess_type(file.filename)
    if mime_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # Save file
    file_path = os.path.join(UPLOAD_DIR, f"{datetime.now().timestamp()}_{file.filename}")
    with open(file_path, "wb") as f:
        f.write(file_content)

    return {"filename": file.filename, "message": "File uploaded successfully"}


@app.get("/images", response_class=HTMLResponse)
async def list_images(request: Request):
    images = os.listdir(UPLOAD_DIR)
    image_list = "".join(
        f'<li><img src="/uploads/{image}" width="200px" /></li>'
        for image in images if image.lower().endswith(("png", "jpg", "jpeg", "gif"))
    )
    # Use Markup to tell Jinja2 this is safe HTML
    image_list = Markup(image_list)

    return templates.TemplateResponse("images.html", {"request": request, "image_list": image_list})


@app.get("/uploads/{image_name}")
async def get_image(image_name: str):
    file_path = os.path.join(UPLOAD_DIR, image_name)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}
