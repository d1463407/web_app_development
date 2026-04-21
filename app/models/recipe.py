"""
食譜管理系統 - Recipe Model

負責食譜 (recipe) 資料表的 CRUD 操作，
以及與食材 (ingredient)、標籤 (tag) 的關聯查詢。
"""

from datetime import datetime
from app.models import get_db


class Recipe:
    """食譜資料模型，提供對 recipe 資料表的完整 CRUD 操作。"""

    # ──────────────────────────────
    #  Create
    # ──────────────────────────────
    @staticmethod
    def create(title, steps, description='', image_url='', ingredients=None, tag_ids=None):
        """
        新增一筆食譜，同時寫入食材與標籤關聯。

        Args:
            title (str): 食譜名稱（必填）
            steps (str): 烹飪步驟（必填）
            description (str): 食譜簡介
            image_url (str): 圖片路徑
            ingredients (list[dict]): 食材清單，每個元素為 {'name': str, 'quantity': str}
            tag_ids (list[int]): 要關聯的標籤 ID 清單

        Returns:
            int: 新建食譜的 ID
        """
        now = datetime.now().isoformat(timespec='seconds')
        conn = get_db()
        try:
            cursor = conn.execute(
                """
                INSERT INTO recipe (title, description, steps, image_url, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (title, description, steps, image_url, now, now)
            )
            recipe_id = cursor.lastrowid

            # 寫入食材
            if ingredients:
                for ing in ingredients:
                    conn.execute(
                        "INSERT INTO ingredient (recipe_id, name, quantity) VALUES (?, ?, ?)",
                        (recipe_id, ing.get('name', ''), ing.get('quantity', ''))
                    )

            # 寫入標籤關聯
            if tag_ids:
                for tag_id in tag_ids:
                    conn.execute(
                        "INSERT OR IGNORE INTO recipe_tag (recipe_id, tag_id) VALUES (?, ?)",
                        (recipe_id, tag_id)
                    )

            conn.commit()
            return recipe_id
        finally:
            conn.close()

    # ──────────────────────────────
    #  Read - 取得全部
    # ──────────────────────────────
    @staticmethod
    def get_all():
        """
        取得所有食譜（依建立時間倒序排列）。

        Returns:
            list[dict]: 食譜列表，每筆包含基本欄位
        """
        conn = get_db()
        try:
            rows = conn.execute(
                "SELECT * FROM recipe ORDER BY created_at DESC"
            ).fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    # ──────────────────────────────
    #  Read - 取得單筆（含食材與標籤）
    # ──────────────────────────────
    @staticmethod
    def get_by_id(recipe_id):
        """
        透過 ID 取得單筆食譜，並附帶其所有食材與標籤。

        Args:
            recipe_id (int): 食譜 ID

        Returns:
            dict | None: 含有 'ingredients' 和 'tags' 子列表的食譜 dict，找不到則回傳 None
        """
        conn = get_db()
        try:
            row = conn.execute(
                "SELECT * FROM recipe WHERE id = ?", (recipe_id,)
            ).fetchone()

            if row is None:
                return None

            recipe = dict(row)

            # 附帶食材
            ingredients = conn.execute(
                "SELECT * FROM ingredient WHERE recipe_id = ? ORDER BY id",
                (recipe_id,)
            ).fetchall()
            recipe['ingredients'] = [dict(ing) for ing in ingredients]

            # 附帶標籤
            tags = conn.execute(
                """
                SELECT t.id, t.name
                FROM tag t
                JOIN recipe_tag rt ON t.id = rt.tag_id
                WHERE rt.recipe_id = ?
                ORDER BY t.name
                """,
                (recipe_id,)
            ).fetchall()
            recipe['tags'] = [dict(tag) for tag in tags]

            return recipe
        finally:
            conn.close()

    # ──────────────────────────────
    #  Update
    # ──────────────────────────────
    @staticmethod
    def update(recipe_id, title, steps, description='', image_url='', ingredients=None, tag_ids=None):
        """
        更新指定食譜的資料，同時重建食材與標籤關聯。

        Args:
            recipe_id (int): 要更新的食譜 ID
            title (str): 食譜名稱
            steps (str): 烹飪步驟
            description (str): 食譜簡介
            image_url (str): 圖片路徑
            ingredients (list[dict]): 新的食材清單
            tag_ids (list[int]): 新的標籤 ID 清單

        Returns:
            bool: 更新是否成功
        """
        now = datetime.now().isoformat(timespec='seconds')
        conn = get_db()
        try:
            result = conn.execute(
                """
                UPDATE recipe
                SET title = ?, description = ?, steps = ?, image_url = ?, updated_at = ?
                WHERE id = ?
                """,
                (title, description, steps, image_url, now, recipe_id)
            )

            if result.rowcount == 0:
                return False

            # 重建食材：先刪再建
            conn.execute("DELETE FROM ingredient WHERE recipe_id = ?", (recipe_id,))
            if ingredients:
                for ing in ingredients:
                    conn.execute(
                        "INSERT INTO ingredient (recipe_id, name, quantity) VALUES (?, ?, ?)",
                        (recipe_id, ing.get('name', ''), ing.get('quantity', ''))
                    )

            # 重建標籤關聯：先刪再建
            conn.execute("DELETE FROM recipe_tag WHERE recipe_id = ?", (recipe_id,))
            if tag_ids:
                for tag_id in tag_ids:
                    conn.execute(
                        "INSERT OR IGNORE INTO recipe_tag (recipe_id, tag_id) VALUES (?, ?)",
                        (recipe_id, tag_id)
                    )

            conn.commit()
            return True
        finally:
            conn.close()

    # ──────────────────────────────
    #  Delete
    # ──────────────────────────────
    @staticmethod
    def delete(recipe_id):
        """
        刪除指定食譜（由 CASCADE 自動移除相關食材與標籤關聯）。

        Args:
            recipe_id (int): 要刪除的食譜 ID

        Returns:
            bool: 刪除是否成功
        """
        conn = get_db()
        try:
            result = conn.execute("DELETE FROM recipe WHERE id = ?", (recipe_id,))
            conn.commit()
            return result.rowcount > 0
        finally:
            conn.close()

    # ──────────────────────────────
    #  搜尋 - 關鍵字搜尋
    # ──────────────────────────────
    @staticmethod
    def search(keyword):
        """
        透過關鍵字搜尋食譜（模糊比對標題與描述）。

        Args:
            keyword (str): 搜尋關鍵字

        Returns:
            list[dict]: 符合條件的食譜列表
        """
        conn = get_db()
        try:
            pattern = f"%{keyword}%"
            rows = conn.execute(
                """
                SELECT * FROM recipe
                WHERE title LIKE ? OR description LIKE ?
                ORDER BY created_at DESC
                """,
                (pattern, pattern)
            ).fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    # ──────────────────────────────
    #  搜尋 - 用食材推薦食譜
    # ──────────────────────────────
    @staticmethod
    def search_by_ingredients(ingredient_names):
        """
        根據提供的食材名稱清單，找出包含這些食材的食譜，
        並依符合的食材數量由多到少排序。

        Args:
            ingredient_names (list[str]): 食材名稱清單

        Returns:
            list[dict]: 食譜列表，每筆額外包含 'match_count' 欄位
        """
        if not ingredient_names:
            return []

        conn = get_db()
        try:
            # 建立動態 LIKE 條件
            conditions = " OR ".join(["i.name LIKE ?" for _ in ingredient_names])
            params = [f"%{name.strip()}%" for name in ingredient_names]

            rows = conn.execute(
                f"""
                SELECT r.*, COUNT(DISTINCT i.name) AS match_count
                FROM recipe r
                JOIN ingredient i ON r.id = i.recipe_id
                WHERE {conditions}
                GROUP BY r.id
                ORDER BY match_count DESC, r.created_at DESC
                """,
                params
            ).fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()
