## Context

本次實作一個無狀態的分帳計算 API，基於 `addition.spec.yaml` 的規格定義。不涉及資料庫，所有計算均在單次請求中完成。

## Goals / Non-Goals

**Goals:**
- 實作 `POST /split` 端點，接受參與者清單與已付金額
- 計算每人平均應分攤金額與淨額
- 以 greedy 演算法產生最少筆數轉帳建議

**Non-Goals:**
- 使用者認證與授權
- 資料持久化（不存儲歷史記錄）
- 支援不等比例分攤
- 多幣別換算

## Decisions

**語言/框架：Python + FastAPI**
- FastAPI 自動產生 OpenAPI 文件，與 spec 驅動開發一致
- 型別提示與 Pydantic validation 符合 spec 定義的 schema
- 替代方案：Node.js/Express（較少內建 validation）

**最少筆數演算法（Two-pointer greedy）**
- 將參與者依淨額排序（負=欠款，正=應收）
- 雙指針從兩端開始匹配，每次配對取較小金額
- 時間複雜度 O(n log n)，對分帳場景已足夠
- 替代方案：min-flow 最佳化（過於複雜，非必要）

**浮點數精度**
- 使用 Python `round(..., 2)` 處理小數，符合金融場景慣例
- 回傳值統一四捨五入至小數點後兩位

## Risks / Trade-offs

- **浮點誤差** → 使用 `round()` 在最終輸出截斷，中間計算保留精度
- **人數極少（1人）** → 需驗證至少 2 人參與，否則回傳 400
- **金額全為 0** → 合法輸入，回傳全為 0 的結算結果（無轉帳）
