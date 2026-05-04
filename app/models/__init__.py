"""
資料庫模型初始化與共用例外定義。

提供 get_db、init_db 以及 ModelError 類別供各模型使用。
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional

class ModelError(RuntimeError):
    """Raised when a database operation fails."""


# 資料庫檔案路徑（位於 instance/ 資料夾）
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'database', 'schema.sql')


def get_db():
    """
    取得資料庫連線。
    - 啟用外鍵約束
    - 回傳的 row 可以用欄位名稱存取（dict-like）
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 讓查詢結果可以用欄位名稱存取
    conn.execute("PRAGMA foreign_keys = ON")  # 啟用外鍵約束
    return conn


def init_db():
    """
    初始化資料庫：讀取 schema.sql 並建立所有資料表。
    若 instance/ 資料夾不存在會自動建立。
    """
    # 確保 instance 資料夾存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = get_db()
    try:
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
"""
資料庫模型初始化與共用例外定義。

提供 get_db、init_db 以及 ModelError 類別供各模型使用。
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional

class ModelError(RuntimeError):
    """Raised when a database operation fails."""


# 資料庫檔案路徑（位於 instance/ 資料夾）
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'database', 'schema.sql')


def get_db():
    """
    取得資料庫連線。
    - 啟用外鍵約束
    - 回傳的 row 可以用欄位名稱存取（dict-like）
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 讓查詢結果可以用欄位名稱存取
    conn.execute("PRAGMA foreign_keys = ON")  # 啟用外鍵約束
    return conn


def init_db():
    """
    初始化資料庫：讀取 schema.sql 並建立所有資料表。
    若 instance/ 資料夾不存在會自動建立。
    """
    # 確保 instance 資料夾存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = get_db()
    try:
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
    finally:
        conn.close()
