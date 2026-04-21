"""
食譜管理系統 - Tag Model

負責標籤 (tag) 資料表與食譜-標籤關聯表 (recipe_tag) 的 CRUD 操作。
"""

from app.models import get_db


class Tag:
    """標籤資料模型，提供對 tag 與 recipe_tag 資料表的操作。"""

    # ──────────────────────────────
    #  Create
    # ──────────────────────────────
    @staticmethod
    def create(name):
        """
        新增一個標籤。若標籤名稱已存在則忽略。

        Args:
            name (str): 標籤名稱

        Returns:
            int: 新建或已存在標籤的 ID
        """
        conn = get_db()
        try:
            # INSERT OR IGNORE 避免重複
            conn.execute(
                "INSERT OR IGNORE INTO tag (name) VALUES (?)", (name,)
            )
            conn.commit()

            # 取得該名稱的 ID（不管是新建還是已存在）
            row = conn.execute(
                "SELECT id FROM tag WHERE name = ?", (name,)
            ).fetchone()
            return row['id'] if row else None
        finally:
            conn.close()

    # ──────────────────────────────
    #  Read - 取得全部
    # ──────────────────────────────
    @staticmethod
    def get_all():
        """
        取得所有標籤（依名稱排序）。

        Returns:
            list[dict]: 標籤列表
        """
        conn = get_db()
        try:
            rows = conn.execute(
                "SELECT * FROM tag ORDER BY name"
            ).fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    # ──────────────────────────────
    #  Read - 取得單筆
    # ──────────────────────────────
    @staticmethod
    def get_by_id(tag_id):
        """
        透過 ID 取得單一標籤。

        Args:
            tag_id (int): 標籤 ID

        Returns:
            dict | None: 標籤 dict，找不到則回傳 None
        """
        conn = get_db()
        try:
            row = conn.execute(
                "SELECT * FROM tag WHERE id = ?", (tag_id,)
            ).fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    # ──────────────────────────────
    #  Read - 依食譜 ID 取得標籤
    # ──────────────────────────────
    @staticmethod
    def get_by_recipe_id(recipe_id):
        """
        取得指定食譜的所有標籤。

        Args:
            recipe_id (int): 食譜 ID

        Returns:
            list[dict]: 該食譜所擁有的標籤列表
        """
        conn = get_db()
        try:
            rows = conn.execute(
                """
                SELECT t.id, t.name
                FROM tag t
                JOIN recipe_tag rt ON t.id = rt.tag_id
                WHERE rt.recipe_id = ?
                ORDER BY t.name
                """,
                (recipe_id,)
            ).fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    # ──────────────────────────────
    #  Update
    # ──────────────────────────────
    @staticmethod
    def update(tag_id, name):
        """
        更新指定標籤的名稱。

        Args:
            tag_id (int): 標籤 ID
            name (str): 新的標籤名稱

        Returns:
            bool: 更新是否成功
        """
        conn = get_db()
        try:
            result = conn.execute(
                "UPDATE tag SET name = ? WHERE id = ?",
                (name, tag_id)
            )
            conn.commit()
            return result.rowcount > 0
        finally:
            conn.close()

    # ──────────────────────────────
    #  Delete
    # ──────────────────────────────
    @staticmethod
    def delete(tag_id):
        """
        刪除指定標籤（由 CASCADE 自動移除 recipe_tag 中的關聯紀錄）。

        Args:
            tag_id (int): 標籤 ID

        Returns:
            bool: 刪除是否成功
        """
        conn = get_db()
        try:
            result = conn.execute(
                "DELETE FROM tag WHERE id = ?", (tag_id,)
            )
            conn.commit()
            return result.rowcount > 0
        finally:
            conn.close()

    # ──────────────────────────────
    #  關聯操作 - 為食譜加上標籤
    # ──────────────────────────────
    @staticmethod
    def add_to_recipe(recipe_id, tag_id):
        """
        在 recipe_tag 中新增一筆關聯（若已存在則忽略）。

        Args:
            recipe_id (int): 食譜 ID
            tag_id (int): 標籤 ID

        Returns:
            bool: 是否成功新增（已存在會回傳 False）
        """
        conn = get_db()
        try:
            cursor = conn.execute(
                "INSERT OR IGNORE INTO recipe_tag (recipe_id, tag_id) VALUES (?, ?)",
                (recipe_id, tag_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    # ──────────────────────────────
    #  關聯操作 - 從食譜移除標籤
    # ──────────────────────────────
    @staticmethod
    def remove_from_recipe(recipe_id, tag_id):
        """
        從 recipe_tag 中移除一筆關聯。

        Args:
            recipe_id (int): 食譜 ID
            tag_id (int): 標籤 ID

        Returns:
            bool: 是否成功移除
        """
        conn = get_db()
        try:
            result = conn.execute(
                "DELETE FROM recipe_tag WHERE recipe_id = ? AND tag_id = ?",
                (recipe_id, tag_id)
            )
            conn.commit()
            return result.rowcount > 0
        finally:
            conn.close()
