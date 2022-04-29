from flask_app import app
from flask import render_template, redirect, request, session, flash

from flask_app.models.user import User
from flask_app.models.recipe import Recipe


@app.route('/new/recipe')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template('new_recipe.html', user=User.get_by_id(data))


@app.route('/create/recipe', methods=['POST'])
def create_recipe():
    # print("request form-", request.form)
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/new/recipe')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under_30_minutes": int(request.form["under_30_minutes"]),
        "date_made": request.form["date_made"],
        "user_id": session["user_id"]
    }
    Recipe.save(data)
    return redirect('/dashboard')


@app.route('/update/recipe/<int:recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    # print('recipe_id - ', recipe_id)
    # print('user_id - ', session['user_id'])
    # print("form - ", request.form)
    if not session['user_id']:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/edit/recipe/{recipe_id}')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under_30_minutes": int(request.form["under_30_minutes"]),
        "date_made": request.form["date_made"],
        "id": recipe_id
    }
    Recipe.update(data)
    return redirect('/dashboard')


@app.route('/recipe/<int:id>')
def show_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template("show_recipe.html", recipe=Recipe.get_one(data), user=User.get_by_id(user_data))


@app.route('/edit/recipe/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    recipe = Recipe.get_one(data)
    yes_checked = "checked" if recipe.under_30_minutes == 1 else ""
    no_checked = "" if recipe.under_30_minutes == 1 else "checked"
    return render_template(
        "edit_recipe.html",
        recipe=recipe,
        user=User.get_by_id(user_data),
        yes_checked=yes_checked,
        no_checked=no_checked,
    )


@app.route('/destroy/recipe/<int:id>')
def destroy_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    Recipe.destroy(data)
    return redirect('/dashboard')
