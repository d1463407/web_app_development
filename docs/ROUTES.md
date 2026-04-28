# Route Design Documentation

## Route Overview Table

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|----------|----------|------|
| 任務列表 | GET | /tasks | templates/tasks/index.html | 顯示所有任務 |
| 新增任務頁面 | GET | /tasks/new | templates/tasks/new.html | 顯示建立任務表單 |
| 建立任務 | POST | /tasks | — | 接收表單資料，寫入資料庫，完成後重導向到任務列表 |
| 任務詳情 | GET | /tasks/<id> | templates/tasks/detail.html | 顯示單筆任務 |
| 編輯任務頁面 | GET | /tasks/<id>/edit | templates/tasks/edit.html | 顯示編輯表單 |
| 更新任務 | POST | /tasks/<id>/update | — | 接收表單資料，更新資料庫，完成後重導向到任務詳情 |
| 刪除任務 | POST | /tasks/<id>/delete | — | 刪除資料庫中的任務，完成後重導向到任務列表 |

## Detailed Route Descriptions

### 任務列表
- **輸入**：無
- **處理邏輯**：呼叫 `TaskModel.get_all()` 取得所有任務
- **輸出**：渲染 `templates/tasks/index.html`，傳入任務清單
- **錯誤處理**：若資料庫存取失敗，返回 500 錯誤頁面

### 新增任務頁面
- **輸入**：無
- **處理邏輯**：僅返回建立表單頁面
- **輸出**：渲染 `templates/tasks/new.html`
- **錯誤處理**：無特別錯誤處理

### 建立任務
- **輸入**：HTML 表單欄位（如 `title`, `description`）
- **處理邏輯**：呼叫 `TaskModel.create(data)` 寫入資料庫
- **輸出**：成功後 `redirect(url_for('tasks.list'))`
- **錯誤處理**：表單驗證失敗時重新渲染表單並顯示錯誤訊息

### 任務詳情
- **輸入**：URL 參數 `<id>`（整數）
- **處理邏輯**：呼叫 `TaskModel.get(id)` 取得單筆任務
- **輸出**：渲染 `templates/tasks/detail.html`，傳入任務資料
- **錯誤處理**：若找不到任務返回 404

### 編輯任務頁面
- **輸入**：URL 參數 `<id>`
- **處理邏輯**：取得任務資料，渲染編輯表單
- **輸出**：渲染 `templates/tasks/edit.html`
- **錯誤處理**：任務不存在返回 404

### 更新任務
- **輸入**：URL 參數 `<id>`、表單欄位
- **處理邏輯**：呼叫 `TaskModel.update(id, data)` 更新資料庫
- **輸出**：成功後 `redirect(url_for('tasks.detail', id=id))`
- **錯誤處理**：驗證失敗重新渲染編輯表單，資料庫錯誤返回 500

### 刪除任務
- **輸入**：URL 參數 `<id>`
- **處理邏輯**：呼叫 `TaskModel.delete(id)` 刪除資料
- **輸出**：成功後 `redirect(url_for('tasks.list'))`
- **錯誤處理**：若刪除失敗返回 500

---

*以上路由設計遵循 RESTful 原則，使用名詞作為資源路徑，透過 HTTP 方法區分操作。表單提交均使用 POST，以兼容 HTML 表單的限制。*
