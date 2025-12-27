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

@router.post("/config/trades_per_second")
def set_trades_per_second(numTradesPerSecond: int):
    shared_engine.numTradesPerSecond = numTradesPerSecond
    return {"status": "config updated"}

@router.post("/config/maker_taker_ratio")  
def set_maker_taker_ratio(ratio: float):
    shared_engine.candleBuilder.makerTakerRatio = ratio
    return {"status": "config updated"}

@router.get("/config/taker_params/buysell_ratio")
def get_taker_buy_sell_ratio(ratio: float):
    shared_engine.taker.buySellRatio = ratio
    return {"status": "config updated"}

@router.get("/config/taker_params/min_spread")
def get_taker_min_spread(minSpread: float):
    shared_engine.taker.minSpread = minSpread
    return {"status": "config updated"}

@router.get("/config/taker_params/max_spread")
def get_taker_max_spread(maxSpread: float):
    shared_engine.taker.maxSpread = maxSpread
    return {"status": "config updated"}

@router.get("/config/taker_params/max_qty")
def get_taker_max_qty(maxQty: float):
    shared_engine.taker.maxQty = maxQty
    return {"status": "config updated"}

@router.get("/config/taker_params/lamda_qty")
def get_taker_lamda_qty(lamdaQty: float):
    shared_engine.taker.lamdaQty = lamdaQty
    return {"status": "config updated"}

@router.get("/config/maker_params/buysell_ratio")
def get_maker_buy_sell_ratio(ratio: float):
    shared_engine.maker.buySellRatio = ratio
    return {"status": "config updated"}

@router.get("/config/maker_params/min_spread")
def get_maker_min_spread(minSpread: float):
    shared_engine.maker.minSpread = minSpread
    return {"status": "config updated"}

@router.get("/config/maker_params/max_spread")
def get_maker_max_spread(maxSpread: float):
    shared_engine.maker.maxSpread = maxSpread
    return {"status": "config updated"}

@router.get("/config/maker_params/max_qty")
def get_maker_max_qty(maxQty: float):
    shared_engine.maker.maxQty = maxQty
    return {"status": "config updated"}

@router.get("/config/maker_params/lamda_qty")
def get_maker_lamda_qty(lamdaQty: float):
    shared_engine.maker.lamdaQty = lamdaQty
    return {"status": "config updated"}

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
