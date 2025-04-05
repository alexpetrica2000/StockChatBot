from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import json, os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "stock_data.json")
templates = Jinja2Templates(directory="templates")


def load_stock_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError("stock_data.json file is missing.")
    try:
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise ValueError("stock_data.json is not a valid JSON file.")


@app.get("/", response_class=HTMLResponse)
async def chat_ui(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@app.post("/chat", response_class=JSONResponse)
async def handle_chat(action: str = Form(...), value: str = Form(...)):
    try:
        data = load_stock_data()

        if action == "select_exchange":
            exchange = next((ex for ex in data if ex["code"] == value), None)
            if not exchange:
                return {"type": "error", "message": f"No exchange found for code '{value}'."}
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
            return {"type": "error", "message": f"Stock with code '{value}' not found."}

        return {"type": "error", "message": f"Invalid action: {action}"}

    except FileNotFoundError as e:
        return {"type": "error", "message": str(e)}
    except ValueError as e:
        return {"type": "error", "message": str(e)}
    except Exception as e:
        return {"type": "error", "message": "Unexpected error occurred.", "detail": str(e)}


# Global exception handler (for request/form validation issues)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"type": "error", "message": "Form data validation failed", "detail": exc.errors()}
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"type": "error", "message": exc.detail}
    )
