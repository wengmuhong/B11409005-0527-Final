# 台科大資管 Python 考試作答區

---

## 基本資料

**學號：** B11409005  
**系級：** 資管系大一  
**姓名：** 翁睦閎  

---

## 一、 原始碼分析報告 (Static Analysis) (共8小題，每小題3分，總共24分)

### 1.1 變數與邏輯對照表

| 原始變數名稱 | 代表意義 (Business Logic) | 建議修正名稱 |
|---|---|---|
| Q1 l1 (in load_proc) |代表從檔案 lib_data.txt 讀入的每一行文字，也就是「檔案內容行清單」 |file_lines |
| Q2 d2 (in main) |代表程式中的資料庫清單，儲存所有書籍記錄 |book_records |
| Q3 c_res (in check) |代表「檢查 ISBN 是否已存在」 |isbn_exists |

### 1.2 壞味道 (Code Smells) 診斷

請列出原程式碼中至少 5 個嚴重的設計問題，並說明為什麼不好：

- **Q1：** 
變數命名完全不具可讀性：l1、d2、c_res、以及字典鍵 t、i、s 沒有語意。這是最嚴重的維護問題，會讓程式碼易出錯且難以擴充。
- **Q2：**
檔案操作未使用上下文管理器：open(F_NAME, "r", encoding="utf-8") 和 open(F_NAME, "w", encoding="utf-8") 都沒有 with。
如果程式在讀寫過程中發生例外，檔案可能不會正確關閉，造成資源洩漏或資料遺失。
- **Q3：**
輸入與資料處理混合在 main() 中：main() 同時負責命令解析、資料讀寫、驗證、更新和顯示。這違反單一職責原則，讓函式變得笨重且不易測試。
- **Q4：**
資料格式驗證不足且可能崩潰：load_proc() 假設每行都包含 @@ 和 ##，直接 p = x.strip().split("@@")、p2 = p[1].split("##")。
如果檔案內容格式錯誤，就會丟出 IndexError。
- **Q5：**
 c_res() 搜尋方式效率低且名稱不明：c_res() 每次新增時都遍歷整個 d2，時間複雜度為 O(n)。會在資料量大時變慢，且名稱無法表達「ISBN 是否已存在」。

---

## 二、 Vibe-Coding 協作紀錄 (共6小題，每小題3分，總共18分)

請記錄你如何引導 GitHub Copilot 進行重構。
重構的要求，請根據題目卷以及你發現的 Code Smells 來進行。

### 2.1 關鍵 Prompt 紀錄

請貼出你對 AI 下達過最有效的 3 個 Prompt：

```log
Prompt A： 請幫我解決這些嚴重的設計問題，並優化程式碼

Prompt B： 請幫我把程式碼模組化，將程式碼拆解為類別以及多個函式

Prompt C： 請幫我優化儲存格式，將原本的 txt 改成 json
```

### 2.2 AI 錯誤處理

1. AI 在撰寫過程中是否有出錯？（例如：漏寫了某個功能、語法錯誤）你是如何發現並請它修正的？
我在測試程式碼時，發現程式碼中有漏掉功能以及有邏輯問題。
2. 發現的問題： (範例：AI 漏掉了 exit 時要印出分類統計的功能)
EOFError 發生時，程式會直接 break 離開迴圈，沒有呼叫 library.save()，因此資料有可能沒被存到。
borrow_book 沒有檢查書籍是否已經是 borrowed，所以同一本書借出後仍可再次借書。
3. 修正的對話： (範例：我告訴它「請在結束前迴圈遍歷 JSON 資料並計算分類總額」)
我告訴它：「請在程式偵測到 EOFError時，也要呼叫 library.save()，並提示資料是否已成功儲存。」
我告訴它：「在 borrow 指令執行前，先檢查該書是否存在且目前不是 borrowed，若已借出要顯示 Already Borrowed。」
---

## 三、 成果驗證與測試  (共2小題，每小題10分，總共20分)

確保你的 `modern_library.py` 功能正確。

### 3.1 測試結果驗證 (Terminal)

請貼上執行程式並輸入 show 後，顯示資料清單。(請從呼叫執行程式到結束程式完整的把操作對話複製到下框)

```log
=== 圖書管理系統 v0.1 (Modern) ===
> add 深入淺出Python/978001/available
Success
> add 資料結構理論/978002/available
Success
> add 演算法實作/978003/available
Success
> add 重複測試書/978001/available
ISBN Exist
> borrow 978002
Updated
> show
書名: 深入淺出Python, ISBN: 978001, 狀態: available
書名: 資料結構理論, ISBN: 978002, 狀態: borrowed
書名: 演算法實作, ISBN: 978003, 狀態: available
> exit
系統關閉，資料已儲存。
```

### 3.2 產出的資料檔案格式

請貼上重構後生成的 `books.json` 前幾行內容：

```json
[
  {
    "title": "深入淺出Python",
    "isbn": "978001",
    "status": "available"
  },
  {
    "title": "資料結構理論",
    "isbn": "978002",
    "status": "borrowed"
  },
  {
    "title": "演算法實作",
    "isbn": "978003",
    "status": "available"
  }
]
```

---

## 四、 Git 提交紀錄 (Commit History)  (共2小題，總共13分)

### 4.1. 請執行 `git log --oneline` 並將 Commit 紀錄貼在此處，以證明你的開發流程(此小題6分)


```log
5293c9c (HEAD -> master) v2
066a80c refactor
```

### 4.2. GitHub Repository 連結(此小題7分)

將專案推送到 GitHub (Public) 若提交到 Private 連結不給分。 請設定 Repository 名稱為 `學號-0527-Final` Ex: B11526748-0527-Final **請用 - 不是 _**

```log
https://github.com/wengmuhong/B11409005-0527-Final.git
```

希望這兩份 Markdown 格式能幫你省下不少排版時間！祝你的考試順利舉行！

最後請保留整份專案資料夾歐！
