## Why

目前分帳 API 只能透過 Swagger UI 或 curl 操作，一般使用者無法直接使用。新增一個簡單的網頁前端，讓任何人都能在瀏覽器中輸入分帳資料並立即看到結算結果。

## What Changes

- 新增靜態前端頁面（HTML + CSS + JavaScript），由 FastAPI 提供服務
- 使用者可動態新增／刪除參與者列
- 填入名稱與金額後送出，頁面顯示每人淨額與建議轉帳清單
- 不引入任何前端框架，保持簡單

## Capabilities

### New Capabilities
- `split-bill-ui`: 分帳前端介面，提供表單輸入與結果顯示

### Modified Capabilities
（無）

## Impact

- 新增 `static/index.html`（前端頁面）
- FastAPI 加掛 `StaticFiles`，提供靜態檔案服務
- 後端 API 需加入 CORS 設定（允許同源請求）
- 無資料庫、無新依賴
