-- ============================================
-- 食譜管理系統 - SQLite 資料庫建表語法
-- ============================================

-- 啟用外鍵約束（SQLite 預設關閉）
PRAGMA foreign_keys = ON;

-- -------------------------------------------
-- 1. RECIPE（食譜）
-- -------------------------------------------
CREATE TABLE IF NOT EXISTS recipe (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    description TEXT    DEFAULT '',
    steps       TEXT    NOT NULL,
    image_url   TEXT    DEFAULT '',
    created_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- 建立標題索引以加速搜尋
CREATE INDEX IF NOT EXISTS idx_recipe_title ON recipe(title);

-- -------------------------------------------
-- 2. INGREDIENT（食材）
-- -------------------------------------------
CREATE TABLE IF NOT EXISTS ingredient (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id   INTEGER NOT NULL,
    name        TEXT    NOT NULL,
    quantity    TEXT    DEFAULT '',
    FOREIGN KEY (recipe_id) REFERENCES recipe(id) ON DELETE CASCADE
);

-- 建立食材名稱索引以加速「用食材推薦食譜」功能
CREATE INDEX IF NOT EXISTS idx_ingredient_name ON ingredient(name);
CREATE INDEX IF NOT EXISTS idx_ingredient_recipe_id ON ingredient(recipe_id);

-- -------------------------------------------
-- 3. TAG（標籤）
-- -------------------------------------------
CREATE TABLE IF NOT EXISTS tag (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT    NOT NULL UNIQUE
);

-- -------------------------------------------
-- 4. RECIPE_TAG（食譜-標籤 關聯表）
-- -------------------------------------------
CREATE TABLE IF NOT EXISTS recipe_tag (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id   INTEGER NOT NULL,
    tag_id      INTEGER NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipe(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id)    REFERENCES tag(id)    ON DELETE CASCADE,
    UNIQUE (recipe_id, tag_id)
);

CREATE INDEX IF NOT EXISTS idx_recipe_tag_recipe_id ON recipe_tag(recipe_id);
CREATE INDEX IF NOT EXISTS idx_recipe_tag_tag_id    ON recipe_tag(tag_id);
