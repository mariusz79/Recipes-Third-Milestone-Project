import os
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, Form, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange, Email
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
#where to redirect
login_manager.login_view = 'login'
#change message category
login_manager.login_message_category = 'info'

app.config['SECRET_KEY'] = 'secret123'
app.config['MONGO_DBNAME'] = 'task_manager'
app.config['MONGO_URI'] = os.getenv('MONGO_URI1')  # 'MONGO_URI1' is saved in environmental variables, to hide password
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

mongo = PyMongo(app)

now = datetime.now()
users = mongo.db.users


@login_manager.user_loader
def load_user(user_id):
    users = mongo.db.users
    user_json = users.find_one({'_id': ObjectId(user_id)})
    return User(user_json)

#create a custom User class that extends UserMixin
class User(UserMixin):
    #store the json object from MongoDB inside the User class
    def __init__(self, user_json):
        self.user_json = user_json

    # Overriding get_id is required if don't have the id property
    def get_id(self):
        object_id = self.user_json.get('_id')
        return str(object_id)

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=2, max=20)])
    confirm = PasswordField('Confirm Password', validators=[
                            DataRequired(), EqualTo('password')])

    #custom function that validates username
    def validate_username(self, username):
        form = RegisterForm(request.form)
        username = form.username.data
        user = users.find_one({'username': username})
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')


@app.route("/register", methods=["GET", "POST"])
def register():
    #create an instance of RegisterForm
    form = RegisterForm(request.form)
     
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        date_of_registration = now.strftime("%b %d, %Y")
        users.insert_one({'username': username, 'password': password,
                          'date_of_registration': date_of_registration})
        loginuser_json = users.find_one({'username': username})
        loginuser = User(loginuser_json)
        login_user(loginuser)
        flash('You are now registered!', 'success')
        return redirect(url_for('home'))
    return render_template("register.html", form=form, title='Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        loginuser_json = users.find_one({'username': form.username.data})
        if loginuser_json and bcrypt.check_password_hash(loginuser_json['password'], form.password.data):
            # Create a custom user and pass it to login_user:
            loginuser = User(loginuser_json)
            login_user(loginuser, remember=form.remember.data)
            #redirect to a page that user wanted to enter but wasn't logged in
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash('You are now logged out', 'info')
    return redirect(url_for('login'))

def count_document(category, subcategory):
        if category == 'servings' or category == 'prep_time':
            nums = subcategory.split('-')
            recipes = mongo.db.recipes.count_documents({ category : { '$gt' :  int(nums[0]), '$lt' : int(nums[1])}})
        else:
            recipes = mongo.db.recipes.count_documents({category: subcategory})
        return recipes

@app.route("/statistics")
def statistics():
    return render_template('statistics.html', count_document=count_document, title='Statistics')


class RecipeForm(Form):
    title = StringField('Title', validators=[
                        DataRequired(), Length(min=2, max=70)])
    main_ingredient = SelectField('Main Ingredient', choices=[('', 'Choose ingredient'), ('eggs', 'eggs'), (
        'cheese', 'cheese'), ('pasta', 'pasta'), ('wheat', 'wheat'), ('vegs', 'vegs'), ('fruits', 'fruits'), ('meat', 'meat')], validators=[DataRequired()])
    ingredients = StringField('Ingredients, must be separated by commas', validators=[
                              DataRequired(), Length(min=2, max=300)])
    servings = IntegerField('Servings, must be a number', validators=[
                            DataRequired(message='Integer betweeen 1 and 6 needed'), NumberRange(min=1, max=6, message='Integer betweeen 1 and 6 needed')])
    body = TextAreaField('Description', validators=[
                         DataRequired(), Length(min=40)])
    prep_time = IntegerField('Preparation time in minutes', validators=[
        DataRequired(message='Integer betweeen 1 and 180 needed'), NumberRange(min=1, max=180, message='Integer betweeen 1 and 180 needed')])
    difficulty = SelectField('Difficulty', choices=[('', 'Choose difficulty'), ('easy', 'easy'), (
        'medium', 'medium'), ('difficult', 'difficult')], validators=[DataRequired()])
    cousine = SelectField('Cousine', choices=[('', 'Choose cousine'), ('asian', 'asian'), (
        'european', 'european'), ('african', 'african'), ('american', 'american')], validators=[DataRequired()])
    keywords = StringField('Keywords, must be separated by commas', validators=[
                           DataRequired(), Length(min=2, max=100)])

    def validate_ingredients(self, ingredients):
        form = RecipeForm(request.form)
        ingredients = form.ingredients.data
        if ' ' in ingredients and not ',' in ingredients:
            raise ValidationError(
                'Ingredients must be separated by comma.')

    def validate_keywords(self, keywords):
        form = RecipeForm(request.form)
        keywords = form.keywords.data
        if ' ' in keywords and not ',' in keywords:
            raise ValidationError(
                'Keywords must be separated by comma.')


@app.route("/add_recipe", methods=["GET", "POST"])
@login_required
def add_recipe():
    form = RecipeForm(request.form)
    now = datetime.utcnow()
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        main_ingredient = form.main_ingredient.data
        ingredients = form.ingredients.data
        servings = form.servings.data
        prep_time = form.prep_time.data
        difficulty = form.difficulty.data
        cousine = form.cousine.data
        keywords = form.keywords.data
        user_id = current_user.get_id()
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        author = user['username']
        date_of_adding = now.strftime("%b %d, %Y")
        recipes = mongo.db.recipes
        result = recipes.insert_one({'title': title.capitalize(), 'main_ingredient': main_ingredient, 'ingredients': ingredients, 'servings': servings, 'prep_time': prep_time, 'body': body,
                                     'difficulty': difficulty, 'cousine': cousine, 'keywords': keywords, 'author': author, 'date_of_adding': date_of_adding})

        flash('Data saved, You can add image', 'success')
        return redirect(url_for('add_recipe_image', recipe_id=result.inserted_id))
    return render_template("add_recipe.html", form=form, title='Add Recipe')


def allowed_image(filename):
    # We only want files with a . in the filename
    if not "." in filename:
        return False
    # Split the extension from the filename
    ext = filename.rsplit(".", 1)[1]
    # Check if the extension is in ALLOWED_IMAGE_EXTENSIONS
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):
    if int(filesize) <= app.config['MAX_CONTENT_LENGTH']:
        return True
    else:
        return False


@app.route('/add_recipe_image/<recipe_id>')
def add_recipe_image(recipe_id):
    the_recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template('add_recipe_image.html', recipe_id=recipe_id, recipe=the_recipe, title='Add Image')


@app.route('/upload_recipe_image/<recipe_id>', methods=["GET", "POST"])
def upload_recipe_image(recipe_id):
    if 'recipe_image' in request.files:
        recipe_image = request.files['recipe_image']
        if recipe_image.filename == "":
                    flash('No file selected!', 'error')
                    return redirect(url_for('add_recipe_image', recipe_id=recipe_id))
        if not allowed_image(recipe_image.filename):
                    flash('That file extension is not allowed!', 'error')
                    return redirect(url_for('add_recipe_image', recipe_id=recipe_id))
        mongo.save_file(recipe_image.filename, recipe_image)

        mongo.db.recipes.update_one({'_id': ObjectId(recipe_id)}, {
                                    '$set': {'recipe_image_name': recipe_image.filename}})
        flash('Image has been added', 'success')
    return redirect(url_for('dashboard'))


@app.route('/add_image')
def add_image():
    return render_template('add_avatar.html', title='Add Avatar')


@app.route('/upload', methods=["GET", "POST"])
def upload():
    if 'profile_image' in request.files:
        profile_image = request.files['profile_image']
        if profile_image.filename == "":
                    flash('No file selected!', 'error')
                    return redirect(url_for('add_image'))
        if not allowed_image(profile_image.filename):
                    flash('That file extension is not allowed!', 'error')
                    return redirect(url_for('add_image'))
        mongo.save_file(profile_image.filename, profile_image)
        user_id = current_user.get_id()
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        username = user['username']
        mongo.db.users.update_one({'username': username}, {
                                  '$set': {'profile_image_name': profile_image.filename}})
        flash('Your avatar has been added', 'success')
        return redirect(url_for('dashboard'))

@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)


@app.route("/edit_recipe/<string:recipe_id>", methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    form = RecipeForm(request.form)
    now = datetime.utcnow()
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        main_ingredient = form.main_ingredient.data
        ingredients = form.ingredients.data
        servings = form.servings.data
        prep_time = form.prep_time.data
        difficulty = form.difficulty.data
        cousine = form.cousine.data
        keywords = form.keywords.data
        date_of_update = now.strftime("%b %d, %Y")
        recipes = mongo.db.recipes
        recipes.update({'_id': ObjectId(recipe_id)}, {
                       '$set': {'title': title.capitalize(), 'main_ingredient': main_ingredient, 'ingredients': ingredients, 'servings': servings, 'prep_time': prep_time, 'body': body,
                                'difficulty': difficulty, 'cousine': cousine, 'keywords': keywords, 'date_of_update': date_of_update}})
        flash('Your recipe has been updated', 'success')
        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        form.title.data = recipe['title']
        form.body.data = recipe['body']
        form.main_ingredient.data = recipe['main_ingredient']
        form.ingredients.data = recipe['ingredients']
        form.servings.data = recipe['servings']
        form.prep_time.data = recipe['prep_time']
        form.difficulty.data = recipe['difficulty']
        form.cousine.data = recipe['cousine']
        form.keywords.data = recipe['keywords']
    return render_template('edit_recipe.html', title='Edit recipe', recipe=recipe, form=form)


@app.route('/delete_recipe/<string:recipe_id>', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    flash('Recipe Deleted', 'success')
    return redirect(url_for('dashboard'))

def find_user(username):
        user_ = mongo.db.users.find_one({'username': username})
        return user_


class CommentForm(FlaskForm):
    comment = TextAreaField('comment', validators=[
                            DataRequired(), Length(max=200)])

@app.route("/all_recipes/single_recipe/<string:recipe_id>")
@app.route("/single_recipe/<string:recipe_id>", methods=["GET", "POST"])
def single_recipe(recipe_id):
    mongo.db.recipes.update_one(
        {'_id': ObjectId(recipe_id)}, {'$inc': {'views': 1}})
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    ingredients = the_recipe['ingredients'].split(",")
    keywords = the_recipe['keywords'].split(",")
    form = CommentForm(request.form)
    now = datetime.utcnow()
    avatar_default = url_for('static', filename='users_avatars/default.jpg')
    image_default = url_for(
        'static', filename='default_recipe/default_recipe_image.png')
    user_id = current_user.get_id()
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if current_user.is_authenticated:
        author = user['username']
    comment = form.comment.data
    date_of_adding = now.strftime("%b %d, %Y")

    if request.method == "POST" and form.validate:
            return redirect(url_for('add_comment', recipe_id=the_recipe['_id'], comment=comment))

    return render_template('single_recipe.html', title='The Recipe', recipe=the_recipe, user=user, ingredients=ingredients, keywords=keywords, image_default=image_default, find_user=find_user, form=form,  avatar_default=avatar_default)
    

@app.route("/like_recipe/<string:recipe_id>",  methods=["GET", "POST"])
@login_required
def like_recipe(recipe_id):
    user_id = current_user.get_id()
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    if 'liked' in user:
        if the_recipe['_id'] in user['liked']:
            flash('You can like recipe only once', 'info')
            return redirect(url_for('single_recipe', recipe_id=the_recipe['_id']))
        elif user['username'] == the_recipe['author']:
            flash("You can't like your own recipe", 'info')
            return redirect(url_for('single_recipe', recipe_id=the_recipe['_id']))
        else:
            mongo.db.users.update_one({'_id': ObjectId(user_id)}, {'$push': {'liked': the_recipe['_id']}})
            mongo.db.recipes.update_one({'_id': ObjectId(recipe_id)}, {'$inc': {'likes': 1, 'views': -1}})
            return redirect(url_for('single_recipe', recipe_id=the_recipe['_id']))
    else:
            mongo.db.users.update_one({'_id': ObjectId(user_id)}, {'$push': {'liked': the_recipe['_id']}})
            mongo.db.recipes.update_one({'_id': ObjectId(recipe_id)}, {'$inc': {'likes': 1, 'views': -1}})
            return redirect(url_for('single_recipe', recipe_id=the_recipe['_id']))


@app.route("/add_comment/<string:recipe_id>/<string:comment>",  methods=["GET", "POST"])
@login_required
def add_comment(recipe_id, comment):
    now = datetime.utcnow()
    date_of_adding = now.strftime("%b %d, %Y")
    user_id = current_user.get_id()
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    author = user['username']
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    mongo.db.users.update_one({'_id': ObjectId(user_id)}, {
                              '$push': {'commented_recipe_id': the_recipe['_id']}})
    mongo.db.recipes.update_one({'_id': ObjectId(recipe_id)}, {'$push': {'comments': {
                                'author': author, 'comment': comment, 'date_of_adding': date_of_adding}}})
    mongo.db.recipes.update_one({'_id': ObjectId(recipe_id)}, {
                                '$inc': {'views': -2}})
    mongo.db.recipes.update_one({'_id': ObjectId(recipe_id)}, {
                                '$inc': {'comments_number': 1}})
    return redirect(url_for('single_recipe', recipe_id=the_recipe['_id']))


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    user_id = current_user.get_id()
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    avatar_default = url_for('static', filename='users_avatars/default.jpg')
    recipes = mongo.db.recipes.find(
        {'author': user['username']}).sort('_id', pymongo.DESCENDING)
    num_of_recipes = mongo.db.recipes.count_documents(
        {'author': user['username']})
    def find_recipe_name(recipe_id):
            find_recipe = mongo.db.recipes.find_one(
                {"_id": ObjectId(recipe_id)})
            if find_recipe:
                return find_recipe['title']
    return render_template("dashboard.html", find_recipe_name=find_recipe_name, title='Dashboard', user=user, avatar_default=avatar_default, recipes=recipes, num_of_recipes=num_of_recipes)


class SortForm(FlaskForm):
    sort_by = SelectField(u'Sort by', choices=[('_id1', 'Newest first'), ('_id', 'Oldest first'), (
        "title", 'Name A-Z'), ('title1', 'Name Z-A')], validators=[DataRequired()])

@app.route("/all_recipes/<string:name>/<int:page>", methods=["GET", "POST"])
def all_recipes(name, page):
    form = SortForm()
    avatar_default = url_for('static', filename='users_avatars/default.jpg')
    image_default = url_for(
        'static', filename='default_recipe/default_recipe_image.png')
    num_results = mongo.db.recipes.count_documents({})
    sort_by = form.sort_by.data
    form.sort_by.default = name
    form.process()
    if '1' in name:
        name = name[:-1]
        recipes = mongo.db.recipes.find().sort(
            name, pymongo.DESCENDING).limit(6).skip(int(page*6))
    else:
        recipes = mongo.db.recipes.find().sort(name).limit(6).skip(int(page*6))
    if request.method == "POST" and form.validate:
            return redirect(url_for('all_recipes', name=sort_by, page=0))
    return render_template("all_recipes.html", title='All Recipes', page=page, sort_by=sort_by, recipes=recipes, num_results=num_results, 
    form=form,  find_user=find_user, image_default=image_default, avatar_default=avatar_default)


class SearchForm(FlaskForm):
    search = StringField('Search')
    choose = SelectField('Search in', choices=[('everywhere', 'Everywhere'), (
        'title', 'Titles'), ('ingredients', 'Ingredients'), ('keywords', 'Keywords')])

@app.route("/results", methods=["GET", "POST"])
def results():
    form = SearchForm(request.form)
    avatar_default = url_for('static', filename='users_avatars/default.jpg')
    image_default = url_for(
        'static', filename='default_recipe/default_recipe_image.png')
    num_result = 0
    search = form.search.data
    choose = form.choose.data
    if request.method == 'POST' and len(search) > 1:
            if choose == 'title':
                recipes = mongo.db.recipes.find(
                    {'title': {'$regex': search, '$options': 'i'}})
                num_result = recipes.count()
                return render_template('results.html', form=form, recipes=recipes, find_user=find_user, num_result=num_result, avatar_default=avatar_default, image_default=image_default)
            if choose == 'ingredients':
                recipes = mongo.db.recipes.find(
                    {
                        "$or": [
                            {"main_ingredient": {"$regex": search, "$options": "i"}},
                            {"ingredients": {"$regex": search, "$options": "i"}},
                        ]
                    })
                num_result = recipes.count()
                return render_template('results.html', form=form,  recipes=recipes, find_user=find_user, num_result=num_result, avatar_default=avatar_default, image_default=image_default)
            if choose == 'keywords':
                recipes = mongo.db.recipes.find(
                    {'keywords': {'$regex': search, '$options': 'i'}})
                num_result = recipes.count()
                return render_template('results.html', form=form, recipes=recipes, find_user=find_user, num_result=num_result, avatar_default=avatar_default, image_default=image_default)
            if choose == 'everywhere':
                recipes = mongo.db.recipes.find(
                    {
                        "$or": [
                            {"title": {"$regex": search, "$options": "i"}},
                            {"keywords":   {"$regex": search, "$options": "i"}},
                            {"ingredients":           {
                                "$regex": search, "$options": "i"}},
                            {"main_ingredient":           {
                                "$regex": search, "$options": "i"}},
                        ]
                    })
                num_result = recipes.count()
                return render_template('results.html', form=form, recipes=recipes, find_user=find_user, num_result=num_result, avatar_default=avatar_default, image_default=image_default)
    else:
            flash('Type an expression to search', 'warning')
    return render_template('results.html', title='Results', form=form, find_user=find_user, num_result=num_result, avatar_default=avatar_default, image_default=image_default)


@app.route("/")
@app.route("/home", methods=["GET", "POST"])
def home():
    avatar_default = url_for('static', filename='users_avatars/default.jpg')
    image_default = url_for(
        'static', filename='default_recipe/default_recipe_image.png')
    num_of_recipes = mongo.db.recipes.count_documents({})
    num_of_users = mongo.db.users.count_documents({})
    latest_recipes = mongo.db.recipes.find().sort(
        '_id', pymongo.DESCENDING).limit(3)
    most_liked_recipes = mongo.db.recipes.find(
        {'likes': {'$exists': True}}, sort=[('likes', -1)], limit=3)
    form = SearchForm(request.form)
    return render_template("home.html", title='Recipes', form=form, find_user=find_user, count_document=count_document, avatar_default=avatar_default, image_default=image_default, num_of_recipes=num_of_recipes, num_of_users=num_of_users, latest_recipes=latest_recipes, most_liked_recipes=most_liked_recipes)

@app.route("/browse/<string:category>/<string:subcategory>/<int:page>")
def browse(category, subcategory, page):
    avatar_default = url_for('static', filename='users_avatars/default.jpg')
    image_default = url_for('static', filename='default_recipe/default_recipe_image.png')
    if category == 'servings' or category == 'prep_time':
        nums = subcategory.split('-')
        recipes = mongo.db.recipes.find({ category : { '$gt' :  int(nums[0]), '$lt' : int(nums[1])}}).limit(6).skip(int(page*6))
    else:
        recipes = mongo.db.recipes.find({category: subcategory}).limit(6).skip(int(page*6))
    num_results = recipes.count()
    nums = subcategory.split('-')
    return render_template('browse.html', title='Browse', page=page, category =category, subcategory=subcategory, nums=nums, recipes=recipes, num_results=num_results, avatar_default=avatar_default, image_default=image_default, find_user=find_user)

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)
