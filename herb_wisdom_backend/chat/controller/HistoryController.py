from fastapi import APIRouter, Depends
from pydantic import BaseModel

from chat.service import HistoryService
from common.JWTDecode import auth
from user.entity import UserEntity

history_router = APIRouter()


@history_router.get("/getMenu")
def get_menu(d: dict = Depends(auth)):
    return HistoryService.get_menu(d)

@history_router.get("/historyContent/{history_id}")
def get_history_content(history_id: int, d: dict = Depends(auth)):
    return HistoryService.get_history_content(history_id)

@history_router.delete("/deleteHistory/{history_id}")
def delete_history(history_id: int, d: dict = Depends(auth)):
    return HistoryService.delete_history(history_id)
