from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json, os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "stock_data.json")
templates = Jinja2Templates(directory="templates")


def load_stock_data():
    try:
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return []


@app.get("/", response_class=HTMLResponse)
async def chat_ui(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@app.post("/chat", response_class=JSONResponse)
async def handle_chat(action: str = Form(...), value: str = Form(...)):
    data = load_stock_data()

    if action == "select_exchange":
        exchange = next((ex for ex in data if ex["code"] == value), None)
        if not exchange:
            return {"type": "error", "message": "Exchange not found."}
        return {
            "type": "stock_list",
            "exchange_code": exchange["code"],
            "exchange_name": exchange["stockExchange"],
            "stocks": exchange["topStocks"]
        }

    elif action == "select_stock":
        for ex in data:
            stock = next((s for s in ex["topStocks"] if s["code"] == value), None)
            if stock:
                return {
                    "type": "stock_price",
                    "stock_name": stock["stockName"],
                    "price": stock["price"],
                    "exchange_code": ex["code"]
                }

    return {"type": "error", "message": "Invalid action or value."}
