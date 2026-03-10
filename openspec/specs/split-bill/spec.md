### Requirement: 計算分帳結算
系統 SHALL 接受參與者清單（名稱與已付金額），計算平均應分攤金額、每人淨額，並回傳最少筆數的轉帳建議清單。

#### Scenario: 三人分帳，金額不均
- **WHEN** POST /split 輸入 Alice 付 120、Bob 付 80、Carol 付 100
- **THEN** 回傳 total=300、per_person_share=100，Bob 轉 20 給 Alice，Carol 淨額為 0

#### Scenario: 有人完全未付款
- **WHEN** POST /split 輸入 阿明 付 0、小美 付 250、大華 付 130
- **THEN** 回傳 total=380、per_person_share≈126.67，阿明需分別轉帳給小美與大華

#### Scenario: 所有人金額相同
- **WHEN** POST /split 輸入所有人付款金額相同
- **THEN** 回傳 settlements 為空清單，所有人 balance 為 0

### Requirement: 輸入驗證
系統 SHALL 驗證請求格式，對非法輸入回傳適當錯誤。

#### Scenario: 缺少 participants 欄位
- **WHEN** POST /split 請求 body 缺少 participants
- **THEN** 回傳 HTTP 422 Unprocessable Entity

#### Scenario: participants 為空陣列
- **WHEN** POST /split 請求 participants 為 []
- **THEN** 回傳 HTTP 422 Unprocessable Entity

#### Scenario: paid 為負數
- **WHEN** POST /split 某位參與者的 paid 為負值
- **THEN** 回傳 HTTP 422 Unprocessable Entity
