## Why

分帳是日常生活中常見的需求（聚餐、旅遊、合購等），手動計算容易出錯且耗時。本次實作提供一個 API，讓使用者輸入每人已付金額，自動計算最少筆數的結算轉帳建議。

## What Changes

- 新增 `POST /split` API 端點，接受參與者名稱與已付金額
- 計算平均應分攤金額（total / 人數）
- 回傳每人淨額（paid - share）與最少筆數轉帳建議清單

## Capabilities

### New Capabilities
- `split-bill`: 分帳結算 API，接受參與者清單與已付金額，回傳淨額與建議轉帳清單

### Modified Capabilities
（無）

## Impact

- 新增後端 API server（建議使用 Python/FastAPI 或 Node.js/Express）
- 新增分帳計算邏輯（greedy 演算法，最小化轉帳筆數）
- 無資料庫依賴，純計算型 API
