import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

shared_engine = None 

def set_engine(engine_instance):
    global shared_engine
    shared_engine = engine_instance

@router.post("/start")
def start():
    shared_engine.start()
    return {"status": "started"}

@router.post("/stop")
def stop():
    shared_engine.stop()
    return {"status": "stopped"}

@router.get("/latest")
def latest():
    if not shared_engine.candles:
        return {}
    return shared_engine.candles.tail(-1)

@router.get("/history")
def history(limit: int = 1):
    return shared_engine.candles.tail(limit).to_dict(orient="records")

@router.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    last_sent_time = None
    try:
        while True:
            if len(shared_engine.candles):
                candle = shared_engine.candles.tail(1).to_dict(orient="records")[0]
                if candle.get("time") != last_sent_time:
                    await websocket.send_json(candle)
                    last_sent_time = candle.get("time")
            await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        print("WebSocket client disconnected")
        pass
