import os
import fastapi
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from chat.controller.ChatController import chat_router
from chat.controller.HistoryController import history_router
from user.controller.UserController import user_router
from ai import LoadChromaCon, LoadReRankerModel, LoadIntentRecognitionModel, LoadEmbeddingModel


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    # 启动时预加载模型
    LoadChromaCon.load_chroma_conn()
    print("Chroma 加载完成")
    LoadReRankerModel.load_rerank_model()
    print("ReRanker 加载完成")
    LoadIntentRecognitionModel.load_intent_recognition_model()
    print("IntentRecognition 加载完成")
    LoadEmbeddingModel.load_embedding_model()
    print("Embedding 加载完成")
    yield
    # 关闭时清理（如有需要）

app = fastapi.FastAPI(lifespan=lifespan)

# CORS 配置：从环境变量读取允许的前端地址，默认为允许所有
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
if cors_origins == ["*"]:
    cors_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    router=user_router,
    prefix="/user",
    tags=["user"],
)

app.include_router(
    router=chat_router,
    prefix="/chat",
    tags=["chat"],
)

app.include_router(
    router=history_router,
    prefix="/history",
    tags=["history"],
)
app.mount("/media", StaticFiles(directory="media"), name="media")