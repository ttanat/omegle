from fastapi import FastAPI, WebSocket, WebSocketDisconnect, WebSocketException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from helpers.chat_manager import ChatManager


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

manager = ChatManager()


@app.get("/")
def read_root():
    return FileResponse("index.html")


@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    # Handle connection
    await manager.connect(websocket)
    await manager.update_num_online(websocket)
    # Handle chat
    try:
        while True:
            data = await websocket.receive_json()
            if data["action"] == "start_chat":
                await manager.start_chat(websocket)
            elif data["action"] == "send_message":
                await manager.send_message(data["message"], websocket)
            elif data["action"] == "end_chat":
                await manager.end_chat(websocket)
            elif data["action"] == "update_num_online":
                await manager.update_num_online(websocket)
            else:
                raise WebSocketException(400, "Invalid action")
    # Handle disconnection
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
