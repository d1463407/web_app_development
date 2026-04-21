"""
食譜管理系統 - Ingredient Model

負責食材 (ingredient) 資料表的 CRUD 操作。
注意：食材通常隨食譜一起新增/更新（透過 Recipe Model），
此模組提供獨立的操作方法以備彈性使用。
"""

from app.models import get_db


class Ingredient:
    """食材資料模型，提供對 ingredient 資料表的 CRUD 操作。"""

    # ──────────────────────────────
    #  Create
    # ──────────────────────────────
    @staticmethod
    def create(recipe_id, name, quantity=''):
        """
        新增一筆食材。

        Args:
            recipe_id (int): 所屬食譜的 ID
            name (str): 食材名稱
            quantity (str): 用量描述

        Returns:
            int: 新建食材的 ID
        """
        conn = get_db()
        try:
            cursor = conn.execute(
                "INSERT INTO ingredient (recipe_id, name, quantity) VALUES (?, ?, ?)",
                (recipe_id, name, quantity)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    # ──────────────────────────────
    #  Read - 取得全部
    # ──────────────────────────────
    @staticmethod
    def get_all():
        """
        取得所有食材紀錄。

        Returns:
            list[dict]: 所有食材列表
        """
        conn = get_db()
        try:
            rows = conn.execute(
                "SELECT * FROM ingredient ORDER BY id"
            ).fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    # ──────────────────────────────
    #  Read - 取得單筆
    # ──────────────────────────────
    @staticmethod
    def get_by_id(ingredient_id):
        """
        透過 ID 取得單筆食材。

        Args:
            ingredient_id (int): 食材 ID

        Returns:
            dict | None: 食材 dict，找不到則回傳 None
        """
        conn = get_db()
        try:
            row = conn.execute(
                "SELECT * FROM ingredient WHERE id = ?", (ingredient_id,)
            ).fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    # ──────────────────────────────
    #  Read - 依食譜 ID 取得
    # ──────────────────────────────
    @staticmethod
    def get_by_recipe_id(recipe_id):
        """
        取得指定食譜的所有食材。

        Args:
            recipe_id (int): 食譜 ID

        Returns:
            list[dict]: 該食譜的食材列表
        """
        conn = get_db()
        try:
            rows = conn.execute(
                "SELECT * FROM ingredient WHERE recipe_id = ? ORDER BY id",
                (recipe_id,)
            ).fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    # ──────────────────────────────
    #  Update
    # ──────────────────────────────
    @staticmethod
    def update(ingredient_id, name, quantity=''):
        """
        更新指定食材的名稱與用量。

        Args:
            ingredient_id (int): 食材 ID
            name (str): 新的食材名稱
            quantity (str): 新的用量描述

        Returns:
            bool: 更新是否成功
        """
        conn = get_db()
        try:
            result = conn.execute(
                "UPDATE ingredient SET name = ?, quantity = ? WHERE id = ?",
                (name, quantity, ingredient_id)
            )
            conn.commit()
            return result.rowcount > 0
        finally:
            conn.close()

    # ──────────────────────────────
    #  Delete
    # ──────────────────────────────
    @staticmethod
    def delete(ingredient_id):
        """
        刪除指定食材。

        Args:
            ingredient_id (int): 食材 ID

        Returns:
            bool: 刪除是否成功
        """
        conn = get_db()
        try:
            result = conn.execute(
                "DELETE FROM ingredient WHERE id = ?", (ingredient_id,)
            )
            conn.commit()
            return result.rowcount > 0
        finally:
            conn.close()

    # ──────────────────────────────
    #  Delete - 依食譜 ID 全部刪除
    # ──────────────────────────────
    @staticmethod
    def delete_by_recipe_id(recipe_id):
        """
        刪除指定食譜的所有食材。

        Args:
            recipe_id (int): 食譜 ID

        Returns:
            int: 被刪除的食材數量
        """
        conn = get_db()
        try:
            result = conn.execute(
                "DELETE FROM ingredient WHERE recipe_id = ?", (recipe_id,)
            )
            conn.commit()
            return result.rowcount
        finally:
            conn.close()
