from flask import render_template, request, redirect, url_for, flash
from app.routes import recipe_bp
from app.models import Recipe, Tag

@recipe_bp.route('/recipes')
def index():
    keyword = request.args.get('keyword', '').strip()
    ingredient_names = request.args.get('ingredients', '').strip()

    if ingredient_names:
        # Search by ingredients (comma separated)
        ing_list = [i.strip() for i in ingredient_names.split(',') if i.strip()]
        recipes = Recipe.search_by_ingredients(ing_list)
    elif keyword:
        # Search by keyword
        recipes = Recipe.search(keyword)
    else:
        # Get all
        recipes = Recipe.get_all()
        
    return render_template('recipes/index.html', recipes=recipes, keyword=keyword, ingredients=ingredient_names)

@recipe_bp.route('/recipes/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        steps = request.form.get('steps', '').strip()
        image_url = request.form.get('image_url', '').strip()
        
        ingredient_names = request.form.getlist('ingredient_name[]')
        ingredient_qtys = request.form.getlist('ingredient_qty[]')
        ingredients = []
        for name, qty in zip(ingredient_names, ingredient_qtys):
            if name.strip():
                ingredients.append({'name': name.strip(), 'quantity': qty.strip()})
                
        tag_ids_str = request.form.getlist('tag_ids[]')
        tag_ids = []
        for tid in tag_ids_str:
            try:
                tag_ids.append(int(tid))
            except ValueError:
                pass
                
        if not title or not steps:
            flash('標題與烹飪步驟為必填欄位', 'danger')
            tags = Tag.get_all()
            return render_template('recipes/form.html', tags=tags, form_title='新增食譜')
            
        try:
            Recipe.create(title, steps, description, image_url, ingredients, tag_ids)
            flash('食譜新增成功！', 'success')
            return redirect(url_for('recipe.index'))
        except Exception as e:
            flash(f'發生錯誤：{str(e)}', 'danger')
            tags = Tag.get_all()
            return render_template('recipes/form.html', tags=tags, form_title='新增食譜')

    # GET request
    tags = Tag.get_all()
    return render_template('recipes/form.html', tags=tags, form_title='新增食譜')

@recipe_bp.route('/recipes/<int:recipe_id>')
def detail(recipe_id):
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        flash('找不到該食譜', 'danger')
        return redirect(url_for('recipe.index'))
    return render_template('recipes/show.html', recipe=recipe)

@recipe_bp.route('/recipes/<int:recipe_id>/edit', methods=['GET', 'POST'])
def edit(recipe_id):
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        flash('找不到該食譜', 'danger')
        return redirect(url_for('recipe.index'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        steps = request.form.get('steps', '').strip()
        image_url = request.form.get('image_url', '').strip()
        
        ingredient_names = request.form.getlist('ingredient_name[]')
        ingredient_qtys = request.form.getlist('ingredient_qty[]')
        ingredients = []
        for name, qty in zip(ingredient_names, ingredient_qtys):
            if name.strip():
                ingredients.append({'name': name.strip(), 'quantity': qty.strip()})
                
        tag_ids_str = request.form.getlist('tag_ids[]')
        tag_ids = []
        for tid in tag_ids_str:
            try:
                tag_ids.append(int(tid))
            except ValueError:
                pass
                
        if not title or not steps:
            flash('標題與烹飪步驟為必填欄位', 'danger')
            tags = Tag.get_all()
            return render_template('recipes/form.html', recipe=recipe, tags=tags, form_title='編輯食譜')
            
        try:
            Recipe.update(recipe_id, title, steps, description, image_url, ingredients, tag_ids)
            flash('食譜更新成功！', 'success')
            return redirect(url_for('recipe.detail', recipe_id=recipe_id))
        except Exception as e:
            flash(f'發生錯誤：{str(e)}', 'danger')
            tags = Tag.get_all()
            return render_template('recipes/form.html', recipe=recipe, tags=tags, form_title='編輯食譜')

    tags = Tag.get_all()
    return render_template('recipes/form.html', recipe=recipe, tags=tags, form_title='編輯食譜')

@recipe_bp.route('/recipes/<int:recipe_id>/delete', methods=['POST'])
def delete(recipe_id):
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        flash('找不到該食譜', 'danger')
        return redirect(url_for('recipe.index'))
        
    try:
        Recipe.delete(recipe_id)
        flash('食譜已刪除', 'success')
    except Exception as e:
        flash(f'刪除失敗：{str(e)}', 'danger')
        
    return redirect(url_for('recipe.index'))
