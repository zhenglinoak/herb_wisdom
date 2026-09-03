import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from chat.service import ChatService
from chat.entity.SaveChatEntity import SaveChatEntity
from common.JWTDecode import auth

chat_router = APIRouter()


@chat_router.post("/chat")
def chat(q, id, d: dict = Depends(auth)):
    def generator():
        for item in ChatService.chat(q, int(id)):
            if isinstance(item, dict):
                yield f"data: {json.dumps(item, ensure_ascii=False)}\n\n"
            elif isinstance(item, str) and item:
                yield f"data: {json.dumps({'content': item}, ensure_ascii=False)}\n\n"
        yield f"data: {json.dumps({'content': '[DONE]'}, ensure_ascii=False)}\n\n"
    return StreamingResponse(
        generator(),
        media_type="text/event-stream; charset=utf-8"
    )


@chat_router.post("/saveChat")
def save_chat(save_chat_entity: SaveChatEntity, d: dict = Depends(auth)):
    return ChatService.save_chat(save_chat_entity)