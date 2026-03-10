from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .models import SplitRequest, SplitResponse, Balance
from .calculator import calculate_balances, calculate_settlements

app = FastAPI(title="分帳小幫手", version="1.0.0")

static_dir = Path(__file__).parent.parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def index():
    return RedirectResponse(url="/static/index.html")


@app.post("/split", response_model=SplitResponse)
def split(request: SplitRequest):
    total, share, balances = calculate_balances(request.participants)
    settlements = calculate_settlements(balances)

    # 四捨五入 balance 輸出
    rounded_balances = [Balance(name=b.name, balance=round(b.balance, 2)) for b in balances]

    response = SplitResponse(
        total=total,
        per_person_share=share,
        balances=rounded_balances,
        settlements=settlements,
    )
    # 手動處理 from_ → from 的序列化
    data = response.model_dump()
    data["settlements"] = [s.model_dump() for s in settlements]
    return JSONResponse(content=data)
