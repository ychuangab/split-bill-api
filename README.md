# 分帳小幫手 (Split Bill Helper)

一個輕量的分帳計算 API，搭配簡單的網頁前端。輸入每位參與者已付的金額，自動計算出最少筆數的結算轉帳建議。

## 功能

- `POST /split` — 計算分帳結算，回傳每人淨額與最少筆數轉帳建議
- 網頁介面 — 直接在瀏覽器輸入資料，即時顯示結果
- 自動產生 API 文件（Swagger UI）

## 快速開始

**安裝依賴**

```bash
pip install -r requirements.txt
```

**啟動 server**

```bash
python3 -m uvicorn src.main:app --host 0.0.0.0 --port 8000
```

| 頁面 | URL |
|------|-----|
| 網頁介面 | http://localhost:8000 |
| API 文件 | http://localhost:8000/docs |

## API 範例

```bash
curl -X POST http://localhost:8000/split \
  -H "Content-Type: application/json" \
  -d '{
    "currency": "TWD",
    "participants": [
      {"name": "Alice", "paid": 120},
      {"name": "Bob",   "paid": 80},
      {"name": "Carol", "paid": 100}
    ]
  }'
```

```json
{
  "total": 300.0,
  "per_person_share": 100.0,
  "balances": [
    {"name": "Alice", "balance": 20.0},
    {"name": "Bob",   "balance": -20.0},
    {"name": "Carol", "balance": 0.0}
  ],
  "settlements": [
    {"from": "Bob", "to": "Alice", "amount": 20.0}
  ]
}
```

## 專案結構

```
├── src/
│   ├── main.py          # FastAPI app
│   ├── models.py        # Pydantic models
│   └── calculator.py    # 分帳計算邏輯
├── static/
│   └── index.html       # 網頁前端
├── tests/
│   └── test_split.py    # 測試
└── requirements.txt
```

## 執行測試

```bash
python3 -m pytest tests/ -v
```
