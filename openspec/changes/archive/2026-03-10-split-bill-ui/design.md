## Context

後端 API 已完成，前端以純 HTML/CSS/JS 實作，由 FastAPI 的 StaticFiles 提供服務，避免跨來源問題。頁面在 `http://localhost:8000/` 提供。

## Goals / Non-Goals

**Goals:**
- 單一 HTML 檔案，零依賴、零建置步驟
- 動態新增／刪除參與者列
- 呼叫 `POST /split`，顯示結算結果

**Non-Goals:**
- 多語系、RWD 優化
- 歷史記錄、分享連結
- 前端框架（React、Vue 等）

## Decisions

**單一 HTML 檔案（`static/index.html`）**
- 無建置工具，維護最簡單
- 替代方案：Vite + Vue → 過重，與「臨時前端」定位不符

**FastAPI StaticFiles + 根路由 redirect**
- `app.mount("/static", StaticFiles(...))` 提供靜態資源
- `GET /` redirect 到 `/static/index.html`
- 替代方案：Nginx → 不必要的額外服務

**fetch API 直接呼叫 `/split`**
- 同源請求，不需 CORS 設定
- 錯誤以 alert 簡單提示

## Risks / Trade-offs

- **瀏覽器相容性** → 使用現代 fetch/ES6，不支援 IE（可接受）
- **無輸入 debounce** → 使用者點送出才觸發，無即時驗證風險
