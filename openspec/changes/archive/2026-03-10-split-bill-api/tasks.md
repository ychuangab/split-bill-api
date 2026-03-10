## 1. 專案初始化

- [x] 1.1 建立專案目錄結構（src/、tests/）
- [x] 1.2 建立 requirements.txt，加入 fastapi、uvicorn、pydantic
- [x] 1.3 建立 main.py 作為應用程式入口

## 2. 資料模型

- [x] 2.1 定義 Participant Pydantic model（name: str, paid: float >= 0）
- [x] 2.2 定義 SplitRequest Pydantic model（currency: str optional, participants: list 非空）
- [x] 2.3 定義 SplitResponse Pydantic model（total, per_person_share, balances, settlements）

## 3. 核心計算邏輯

- [x] 3.1 實作 calculate_balances()：計算 total、per_person_share、每人 balance
- [x] 3.2 實作 calculate_settlements()：greedy two-pointer 演算法，產生最少筆數轉帳清單
- [x] 3.3 處理浮點數精度，統一四捨五入至小數點後兩位

## 4. API 端點

- [x] 4.1 實作 POST /split 路由，呼叫計算邏輯並回傳結果
- [x] 4.2 加入輸入驗證（participants 非空、paid >= 0）
- [x] 4.3 確認錯誤回傳 HTTP 422

## 5. 測試

- [x] 5.1 測試三人分帳範例（Alice/Bob/Carol）
- [x] 5.2 測試有人未付款範例（阿明/小美/大華）
- [x] 5.3 測試所有人金額相同（settlements 為空）
- [x] 5.4 測試非法輸入（缺 participants、空陣列、負數金額）
