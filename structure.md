Real‑Time Chat Backend + API Gateway
The Complete Project Bible using FastAPI & React
Version: 1.0 | Target: 2nd‑year CS students | Completion: 3 weekends

Table of Contents
Introduction & Why This Project

Core Concepts (The “Why” Behind Every Feature)

System Architecture Overview

Technology Stack

Project Checklist – Track Your Progress

Phase 1 – Chat Backend with FastAPI (Week 1)

6.1 Folder Structure

6.2 Database Schema (PostgreSQL + SQLAlchemy)

6.3 Redis Data Structures for Presence

6.4 WebSocket Endpoint & Connection Manager

6.5 Message Persistence

6.6 Online / Offline & Last Seen

6.7 Typing Indicators

Phase 2 – API Gateway with FastAPI (Week 2)

7.1 Folder Structure

7.2 JWT Authentication (Login / Register)

7.3 Rate Limiting Middleware

7.4 Request Logging & Correlation IDs

7.5 Service Routing (Proxy to Chat Service)

Phase 3 – React Frontend (Week 3)

8.1 Folder Structure

8.2 Authentication Flow

8.3 WebSocket Connection & Real‑Time Messaging

8.4 Typing Indicators & Online Status

Phase 4 – Docker Compose Integration

Deadlines & Milestone Calendar

How to Present This Project to Recruiters

Common Pitfalls & Solutions

Conclusion & Next Steps

1. Introduction & Why This Project
Most students build simple REST APIs or basic chat apps. You will build a system that demonstrates both real‑time engineering (WebSockets) and microservice infrastructure (API Gateway).

Chat backend (FastAPI) → shows you understand WebSockets, presence tracking, message persistence, typing indicators.

API Gateway (FastAPI) → shows you understand authentication, rate limiting, logging, service routing – exactly what backend recruiters look for.

React frontend → proves you can integrate full‑stack, making your demo visually impressive.

By combining them, your resume speaks two languages:

“Built a real‑time chat platform with WebSockets, online presence, message persistence – fronted by an API Gateway with JWT auth, rate limiting, and service routing – plus a React UI.”

That single sentence will put you ahead of 90% of applicants.

What You Will Build
text
React App (port 3000) → API Gateway (port 8000) → Chat Service (port 8001) → PostgreSQL + Redis
Users authenticate via Gateway and receive a JWT.

Chat Service handles WebSocket connections, stores messages, manages presence.

All chat features (typing, online status) work in real time.

Messages survive logouts because they are persisted in PostgreSQL.

2. Core Concepts (The “Why” Behind Every Feature)
2.1 HTTP vs WebSockets
HTTP	WebSockets
Request‑response, half‑duplex	Full‑duplex, persistent
Server cannot push messages	Either side can send anytime
Stateless	Stateful connection
Good for APIs, file uploads	Good for chat, gaming, live feeds
Why WebSockets for chat?
If you used HTTP, User B would have to constantly poll the server to check for new messages (wasteful and laggy). With WebSockets, the server pushes the message instantly the moment User A sends it.

2.2 Presence Tracking (Online/Offline/Last Seen)
Stored in Redis because it’s in‑memory and ultra‑fast.

When a user connects via WebSocket → set user:{id}:status = online, add to online_users set.

When they disconnect → set status = offline, update user:{id}:last_seen = now().

Redis also allows TTL: if a connection drops without a clean disconnect (e.g., network failure), you can set an auto‑expiry (10 seconds) to mark them offline.

2.3 Typing Indicators
A lightweight WebSocket event:

json
{ "type": "typing", "from": "alice", "to": "bob", "isTyping": true }
The server simply forwards it to the recipient. No storage needed.

2.4 Message Persistence
SQL database (PostgreSQL) – because you need ACID, relationships, and queries like “fetch last 50 messages between two users”.

2.5 API Gateway Responsibilities
Authentication – verify JWT before requests reach the chat service.

Rate Limiting – prevent abuse (e.g., 100 requests per minute per IP).

Logging – every request logged with correlation ID for debugging.

Routing – forward requests to the correct internal service (using httpx or aiohttp).

3. System Architecture Overview
text
         (HTTP)            WebSocket (ws://)
      ┌──────────┐      ┌──────────┐
      │          │      │          │
   ┌──▼──┐    ┌──▼──┐   ┌▼─────────▼──┐
   │React│    │React│   │   API       │
   │ A   │    │ B   │   │  Gateway    │
   └──┬──┘    └──┬──┘   └──┬───────┬──┘
      │          │         │       │
      │ POST     │ POST    │JWT    │
      │ /login   │ /msg    │rate   │
      │          │ (REST)  │limit  │
      │          │         │       │
      └──────────┼─────────┘       │
                 │                 │
                 │ WebSocket       │ Internal
                 │ (port 8001)     │ HTTP
                 │                 │
              ┌──▼─────────────────▼──┐
              │    Chat Service        │
              │  - WebSocket handler   │
              │  - msg persistence     │
              └──┬───────────────┬─────┘
                 │               │
           ┌─────▼─────┐    ┌─────▼─────┐
           │PostgreSQL │    │   Redis   │
           │(messages, │    │(presence, │
           │ users)    │    │ sessions) │
           └───────────┘    └───────────┘
Communication flow for a message:

User A sends WebSocket message to Chat Service (already connected via Gateway upgrade).

Chat Service stores message in PostgreSQL.

Chat Service looks up User B’s WebSocket connection (in‑memory map) and forwards the message.

User B receives it instantly.

4. Technology Stack
Component	Technology	Why
Backend	FastAPI (Python)	Native async/await, automatic OpenAPI docs, excellent WebSocket support.
Chat Service	FastAPI + websockets (built‑in)	Lightweight, no extra dependencies.
API Gateway	FastAPI + httpx (async proxy)	Same framework as chat service, easier to maintain.
Database	PostgreSQL (or SQLite for local dev)	Reliable, ACID, good for message history.
Cache/Presence	Redis (v7+)	In‑memory, perfect for ephemeral presence data.
Auth	JWT (python-jose or PyJWT)	Stateless, easy to verify across services.
Rate Limiting	slowapi (FastAPI extension)	Production‑grade for gateway.
Frontend	React + Vite + react-use-websocket	Modern, fast, easy WebSocket integration.
Container	Docker + Docker Compose	Package everything for demo/deployment.
5. Project Checklist – Track Your Progress
Use this checklist to mark off each feature. Recruiters will glance at these.

Core Chat Backend (FastAPI)
WebSocket endpoint /ws accepts connections and verifies JWT

Store messages in PostgreSQL (sender, receiver, content, timestamp)

REST endpoint GET /api/messages/{user_id} to retrieve last 50 messages

Broadcast “online” status when user connects

Broadcast “offline” status and update last_seen on disconnect

Typing indicator – forward { isTyping: true/false } to recipient

Message persistence survives server restart

API Gateway (FastAPI)
JWT login endpoint POST /auth/login returns signed token

Register endpoint POST /auth/register

Gateway verifies JWT on every protected route (including WebSocket upgrade)

Rate limiting – max 100 requests/minute per IP, returns 429

Request logging with timestamp, method, path, status, duration, correlation ID

Proxy all /api/* requests to Chat Service (using httpx.AsyncClient)

WebSocket connections are proxied correctly (with token validation)

React Frontend
Login / Register forms with JWT storage (localStorage)

WebSocket connection using react-use-websocket with token

Display list of online users in real time

Send and display messages instantly

Typing indicator shows “User is typing...”

Scrollable message history

Integration & Polish
Docker Compose file with services: gateway, chat, postgres, redis

Environment variables for secrets (JWT secret, DB passwords)

Demo video / live deployment on Render or Railway

README with setup instructions

6. Phase 1 – Chat Backend with FastAPI (Week 1)
Goal: A working chat service with WebSockets, persistence, presence, and typing indicators.

6.1 Folder Structure for Chat Service
text
chat-service/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app, lifespan, WebSocket endpoint
│   ├── database.py             # SQLAlchemy setup, engine, session
│   ├── models.py               # SQLAlchemy ORM models (User, Message)
│   ├── schemas.py              # Pydantic schemas
│   ├── redis_client.py         # Redis connection
│   ├── connection_manager.py   # WebSocket connection manager
│   ├── handlers/
│   │   ├── message.py
│   │   ├── typing.py
│   │   └── presence.py
│   ├── crud/
│   │   ├── messages.py
│   │   └── users.py
│   └── utils/
│       └── jwt.py              # JWT verify (shared secret)
├── migrations/                 # Alembic migrations
├── requirements.txt
├── Dockerfile
└── .env
6.2 Database Schema (PostgreSQL + SQLAlchemy)
app/models.py:

python
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    last_seen = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Message(Base):
    __tablename__ = "messages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    receiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    content = Column(Text, nullable=False)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())

    # Indexes for performance
    __table_args__ = (
        Index("idx_messages_conversation", "sender_id", "receiver_id", "sent_at"),
        Index("idx_messages_receiver", "receiver_id", "sent_at"),
    )
Migrations – use Alembic:
alembic init migrations then edit env.py to point to your database URL.

6.3 Redis Data Structures for Presence
Key	Type	Value	Expiry
user:{userId}:status	String	"online" / "offline"	None
user:{userId}:last_seen	String	ISO timestamp	None
online_users	Set	userId strings (only online)	N/A
app/redis_client.py:

python
import redis.asyncio as redis
import os

redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
Presence helper functions:

python
async def set_user_online(user_id: str):
    await redis_client.sadd("online_users", str(user_id))
    await redis_client.set(f"user:{user_id}:status", "online")

async def set_user_offline(user_id: str):
    await redis_client.srem("online_users", str(user_id))
    await redis_client.set(f"user:{user_id}:status", "offline")
    await redis_client.set(f"user:{user_id}:last_seen", datetime.utcnow().isoformat())

async def get_online_users():
    return await redis_client.smembers("online_users")
6.4 WebSocket Endpoint & Connection Manager
app/connection_manager.py:

python
from fastapi import WebSocket
from typing import Dict

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        self.active_connections.pop(user_id, None)

    async def send_personal_message(self, message: dict, user_id: str):
        ws = self.active_connections.get(user_id)
        if ws:
            await ws.send_json(message)

    async def broadcast_presence(self, user_id: str, status: str):
        for other_id, ws in self.active_connections.items():
            if other_id != user_id:
                await ws.send_json({
                    "type": "presence",
                    "user_id": user_id,
                    "status": status
                })

manager = ConnectionManager()
app/main.py (WebSocket endpoint):

python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from app.connection_manager import manager
from app.redis_client import set_user_online, set_user_offline
from app.utils.jwt import verify_token_ws
from app.handlers import message_handler, typing_handler

app = FastAPI(title="Chat Service")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Extract and verify JWT from query param
    token = websocket.query_params.get("token")
    user_id = verify_token_ws(token)  # returns user_id or raises
    if not user_id:
        await websocket.close(code=1008)
        return

    await manager.connect(str(user_id), websocket)
    await set_user_online(user_id)
    await manager.broadcast_presence(user_id, "online")

    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type")
            if msg_type == "message":
                await message_handler.handle(data, user_id, manager)
            elif msg_type == "typing":
                await typing_handler.handle(data, user_id, manager)
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        await set_user_offline(user_id)
        await manager.broadcast_presence(user_id, "offline")
6.5 Message Persistence
app/crud/messages.py:

python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models import Message

async def save_message(db: AsyncSession, sender_id, receiver_id, content):
    msg = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg

async def get_conversation(db: AsyncSession, user1_id, user2_id, limit=50):
    stmt = select(Message).where(
        ((Message.sender_id == user1_id) & (Message.receiver_id == user2_id)) |
        ((Message.sender_id == user2_id) & (Message.receiver_id == user1_id))
    ).order_by(Message.sent_at.desc()).limit(limit)
    result = await db.execute(stmt)
    messages = result.scalars().all()
    return list(reversed(messages))  # oldest first
app/handlers/message.py:

python
from app.crud.messages import save_message
from app.database import async_session

async def handle(data, sender_id, manager):
    receiver_id = data.get("to")
    content = data.get("content")
    async with async_session() as db:
        saved = await save_message(db, sender_id, receiver_id, content)
    # Forward to receiver if online
    await manager.send_personal_message({
        "type": "message",
        "from": sender_id,
        "content": content,
        "sent_at": saved.sent_at.isoformat()
    }, receiver_id)
6.6 Online / Offline & Last Seen
Presence logic is already integrated into the WebSocket lifecycle (see set_user_online / set_user_offline). Additionally, provide a REST endpoint to fetch last seen:

app/main.py:

python
@app.get("/api/users/{user_id}/last_seen")
async def get_last_seen(user_id: str):
    last_seen = await redis_client.get(f"user:{user_id}:last_seen")
    if not last_seen:
        # fallback to DB
        async with async_session() as db:
            user = await db.get(User, user_id)
            last_seen = user.last_seen if user else None
    return {"last_seen": last_seen}
6.7 Typing Indicators
app/handlers/typing.py:

python
async def handle(data, sender_id, manager):
    receiver_id = data.get("to")
    is_typing = data.get("isTyping", False)
    await manager.send_personal_message({
        "type": "typing",
        "from": sender_id,
        "isTyping": is_typing
    }, receiver_id)
7. Phase 2 – API Gateway with FastAPI (Week 2)
Goal: A gateway that authenticates, rate‑limits, logs, and proxies requests to the chat service.

7.1 Folder Structure for Gateway
text
gateway/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app
│   ├── middleware/
│   │   ├── auth.py              # JWT verification
│   │   ├── rate_limit.py        # slowapi integration
│   │   └── logging.py           # correlation ID + request logging
│   ├── routes/
│   │   └── auth.py              # login / register
│   ├── proxy.py                 # httpx async proxy client
│   └── utils/
│       └── jwt.py               # JWT sign/verify
├── requirements.txt
├── Dockerfile
└── .env
7.2 JWT Authentication (Login / Register)
app/utils/jwt.py:

python
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
EXPIRY = 24 * 60 * 60

def create_token(user_id: str, username: str) -> str:
    payload = {
        "sub": user_id,
        "username": username,
        "exp": datetime.utcnow() + timedelta(seconds=EXPIRY)
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
app/routes/auth.py:

python
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from app.utils.jwt import create_token
from app.database import get_db  # shared DB or separate user service
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User  # reuse User model

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    # fetch user, verify password, return token
    ...

@router.post("/register")
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    # hash password, create user, return token
    ...
7.3 Rate Limiting Middleware
Using slowapi:

python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Then on endpoints:
@router.get("/protected")
@limiter.limit("50/minute")
async def protected(request: Request):
    ...
Apply globally to all routes except WebSocket.

7.4 Request Logging & Correlation IDs
app/middleware/logging.py:

python
from starlette.middleware.base import BaseHTTPMiddleware
from uuid import uuid4
import time
import logging

logger = logging.getLogger("gateway")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = request.headers.get("X-Request-Id", str(uuid4()))
        request.state.request_id = request_id
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start
        logger.info(f"{request_id} {request.method} {request.url.path} {response.status_code} {duration:.3f}s")
        response.headers["X-Request-Id"] = request_id
        return response
Add to main.py: app.add_middleware(LoggingMiddleware)

7.5 Service Routing (Proxy to Chat Service)
app/proxy.py:

python
import httpx
from fastapi import Request, Response
from fastapi.responses import StreamingResponse

async def proxy_to_chat(request: Request):
    """Forward request to chat service (http://chat-service:8001)"""
    async with httpx.AsyncClient() as client:
        url = f"http://chat-service:8001{request.url.path}"
        if request.query_params:
            url += f"?{request.query_params}"
        headers = dict(request.headers)
        # Remove host header to avoid conflict
        headers.pop("host", None)
        # Forward correlation ID
        if hasattr(request.state, "request_id"):
            headers["X-Request-Id"] = request.state.request_id

        response = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=await request.body()
        )
        return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))
WebSocket proxying: FastAPI does not natively proxy WebSockets. Instead, have the React frontend connect directly to the chat service's WebSocket endpoint (or use a reverse proxy like Nginx). For simplicity, expose chat service's WebSocket on a different public port (e.g., 8001) or use an additional proxy like nginx in Docker. We'll document both approaches.

Simplest approach: In production, put a reverse proxy (Nginx) in front that routes /ws to chat service and /api via gateway. But for the project, you can just have React connect directly to ws://localhost:8001/ws after authentication. The gateway still handles REST APIs.

8. Phase 3 – React Frontend (Week 3)
8.1 Folder Structure
text
frontend/
├── src/
│   ├── components/
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── Chat.jsx
│   │   ├── MessageList.jsx
│   │   ├── MessageInput.jsx
│   │   └── OnlineUsers.jsx
│   ├── hooks/
│   │   └── useWebSocket.js
│   ├── utils/
│   │   └── auth.js
│   ├── App.jsx
│   └── main.jsx
├── package.json
├── vite.config.js
└── .env
8.2 Authentication Flow
Login form sends POST to http://localhost:8000/auth/login (gateway).

Store returned JWT in localStorage.

Include token in WebSocket connection: ws://localhost:8001/ws?token={jwt}.

utils/auth.js:

javascript
export const login = async (username, password) => {
  const res = await fetch('http://localhost:8000/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  if (!res.ok) throw new Error('Login failed');
  const data = await res.json();
  localStorage.setItem('token', data.token);
  localStorage.setItem('userId', data.userId);
  return data;
};
8.3 WebSocket Connection & Real‑Time Messaging
Using react-use-websocket:

bash
npm install react-use-websocket
hooks/useWebSocket.js:

javascript
import useWebSocket from 'react-use-websocket';

export const useChatWebSocket = (token, userId) => {
  const socketUrl = token ? `ws://localhost:8001/ws?token=${token}` : null;
  const { sendJsonMessage, lastJsonMessage, readyState } = useWebSocket(socketUrl, {
    shouldReconnect: () => true,
    reconnectAttempts: 10,
    reconnectInterval: 3000,
  });

  const sendMessage = (to, content) => {
    sendJsonMessage({ type: 'message', to, content });
  };

  const sendTyping = (to, isTyping) => {
    sendJsonMessage({ type: 'typing', to, isTyping });
  };

  return { lastJsonMessage, sendMessage, sendTyping, readyState };
};
8.4 Typing Indicators & Online Status
components/Chat.jsx (excerpt):

javascript
const { lastJsonMessage, sendMessage, sendTyping } = useChatWebSocket(token, userId);
const [typingFrom, setTypingFrom] = useState(null);
const [onlineUsers, setOnlineUsers] = useState([]);

useEffect(() => {
  if (lastJsonMessage) {
    switch (lastJsonMessage.type) {
      case 'message':
        // add to messages list
        break;
      case 'typing':
        setTypingFrom(lastJsonMessage.from);
        setTimeout(() => setTypingFrom(null), 1000);
        break;
      case 'presence':
        if (lastJsonMessage.status === 'online')
          setOnlineUsers(prev => [...prev, lastJsonMessage.userId]);
        else
          setOnlineUsers(prev => prev.filter(id => id !== lastJsonMessage.userId));
        break;
    }
  }
}, [lastJsonMessage]);

// Input handler for typing
const handleTyping = (e) => {
  sendTyping(selectedUser, true);
  setTimeout(() => sendTyping(selectedUser, false), 1000);
};
9. Phase 4 – Docker Compose Integration
Create docker-compose.yml at project root:

yaml
version: '3.8'

services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_USER: chatuser
      POSTGRES_PASSWORD: chatpass
      POSTGRES_DB: chatdb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - chatnet

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - chatnet

  chat-service:
    build: ./chat-service
    environment:
      DATABASE_URL: postgresql://chatuser:chatpass@postgres:5432/chatdb
      REDIS_URL: redis://redis:6379
      JWT_SECRET: your-secret-key-change-in-prod
    depends_on:
      - postgres
      - redis
    ports:
      - "8001:8001"
    networks:
      - chatnet

  gateway:
    build: ./gateway
    environment:
      CHAT_SERVICE_URL: http://chat-service:8001
      JWT_SECRET: your-secret-key-change-in-prod
    depends_on:
      - chat-service
    ports:
      - "8000:8000"
    networks:
      - chatnet

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    networks:
      - chatnet

volumes:
  postgres_data:

networks:
  chatnet:
Frontend Dockerfile (using nginx for production or vite preview for dev):

dockerfile
FROM node:18 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
But for local development, you can just run npm run dev outside Docker.

10. Deadlines & Milestone Calendar
Day	Focus Area	Deliverable	Checkbox
Week 1 – Chat Backend			
Day 1	Setup FastAPI + PostgreSQL + SQLAlchemy	Database models, migrations	☐
Day 2	Redis integration & presence helpers	Set/get online, offline	☐
Day 3	WebSocket connection manager	Accept connections, store in dict	☐
Day 4	Message persistence & retrieval	Save to DB, fetch conversation	☐
Day 5	Typing indicators & broadcast	Forward typing events	☐
Day 6	Online status broadcasting	Notify all when user connects/disconnects	☐
Day 7	REST endpoints for history & last_seen	/api/messages, /api/last_seen	☐
Week 2 – API Gateway			
Day 8	JWT auth endpoints	Login, register, token creation	☐
Day 9	Auth middleware & WebSocket token verify	Protect routes	☐
Day 10	Rate limiting with slowapi	Global & per‑route limits	☐
Day 11	Logging middleware & correlation IDs	Request logging	☐
Day 12	HTTP proxy to chat service (httpx)	Forward /api/*	☐
Day 13	Integration testing (gateway + chat)	curl scripts	☐
Day 14	Documentation & environment setup	README, .env.example	☐
Week 3 – React Frontend			
Day 15	Login/Register UI	Forms, JWT storage	☐
Day 16	WebSocket hook & connection	useWebSocket with token	☐
Day 17	Message list & send message UI	Chat window	☐
Day 18	Online users list & presence updates	Real‑time status	☐
Day 19	Typing indicator UI	Show “User is typing...”	☐
Day 20	Polish & error handling	Reconnect logic, error toasts	☐
Day 21	Docker Compose & demo recording	Full system runs in containers	☐
11. How to Present This Project to Recruiters
On Your Resume (Bullet Points)
Real‑Time Chat Platform – Built a WebSocket‑based chat backend (FastAPI) supporting instant messaging, online/offline presence (Redis), typing indicators, and persistent message history (PostgreSQL).

API Gateway – Designed a gateway service with JWT authentication, rate limiting (100 req/min), request logging (correlation IDs), and transparent HTTP proxying to the chat service – demonstrating microservice patterns.

Full‑Stack Integration – Developed a React frontend that consumes the gateway APIs and maintains a persistent WebSocket connection for real‑time updates, including online user lists and typing notifications.

Containerization – Packaged all three services (gateway, chat, database, cache) with Docker Compose, enabling one‑command local deployment.

In an Interview (Talking Points)
Why WebSockets over HTTP? – “HTTP polling would cause high latency and wasted requests. WebSockets maintain a persistent full‑duplex connection, so the server can push messages the instant they arrive.”

How do you handle offline messages? – “All messages are persisted in PostgreSQL. When a user comes online, we don’t automatically push old messages – instead the client fetches the last 50 messages via a REST call to /api/messages. This keeps the WebSocket lightweight.”

How does presence work? – “Redis stores an online_users set. On WebSocket connect, we add the user to the set and broadcast to others. On disconnect, we remove them and update last_seen. Redis is fast and perfect for ephemeral data.”

What challenges did you face? – “Proxying WebSockets through FastAPI was non‑trivial, so I simplified by having the frontend connect directly to the chat service’s WebSocket endpoint while all REST traffic goes through the gateway. This trade‑off kept the architecture clean.”

Demo Video (2‑3 minutes)
Show:

Two browser windows (User A and User B).

Login/register flow.

User A sends “Hello” – appears instantly on User B.

User A starts typing – User B sees “User A is typing...”.

User A closes tab – User B sees “User A went offline”.

Refresh User B – messages still there.

(Optional) Show Docker Compose running: docker-compose up.

12. Common Pitfalls & Solutions
Pitfall	Solution
WebSocket closes immediately	Verify JWT is correctly extracted from query string and not expired. Use ws.on('error') to log.
Messages not persisting	Check database commit – use await db.commit() after db.add().
Redis not connecting inside Docker	Use service name (redis) not localhost in REDIS_URL.
Rate limiting blocks WebSocket handshake	Apply rate limiter only to HTTP routes, not to the WebSocket upgrade path.
Typing indicator shows indefinitely	Send isTyping: false after a debounce (1 second of no input).
Frontend CORS errors	Add allow_origins=["*"] in FastAPI CORS middleware for development.
JWT secret mismatch between gateway and chat service	Use same environment variable for both services.
13. Conclusion & Next Steps
You have now built a production‑ready real‑time system that impresses recruiters because it combines:

Low‑level networking (WebSockets)

Distributed state management (Redis presence)

Data persistence (PostgreSQL)

Microservice patterns (API Gateway with auth, rate limiting, logging)

Full‑stack integration (React)

Next Features to Add (If You Have Time)
Group chats – extend message schema with room_id.

Message delivery receipts – add delivered_at and read_at.

Media sharing – upload images to S3, send URLs over WebSocket.

End‑to‑end encryption – encrypt messages client‑side before sending.

Kafka / RabbitMQ – replace direct forwarding with a message broker for better scalability.

Deploy to cloud – Render, Railway, or AWS ECS.

Final Checklist Before Showing Recruiters
All checkboxes from Section 5 are ticked.

Docker Compose runs without errors.

You have a 2‑minute demo video (Loom or OBS).

GitHub repository has a detailed README with setup steps.

You can explain every line of code in an interview.

