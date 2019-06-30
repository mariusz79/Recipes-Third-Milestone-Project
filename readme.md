##### Third Milestone Project
# Recipes website


> A web application that allows users to store and easily access cooking recipes. Logic is written in Python. Flask, a micro-framework, is used to run the application. The website is data-driven. CRUD operations are carried out using NoSQL - MongoDB.


## Table of Contents
1. [Ux](#ux)
   1. [Users stories](#users-stories)
   1. [Wireframes](#wireframes)
1. [Features](#features)
1. [Technologies used](#technologies-used)
1. [Project difficulties](#project-challenges)
1. [Testing](#testing)
   1. [User stories](#user-stories)
   1. [Different browsers, mobile, desktop](#different-browsers-mobile-desktop)
1. [Deployment](#deployment)
1. [Content](#content)
1. [Acknowledgements](#acknowledgements)

## UX
The website is made to be as responsive as possible. HTML, CSS, and JavaScript are used to enhance the look and feel of the project. The site also makes use of CSS framework named Materializecss.

Target audience of the website are people who want to easily store and access cooking recipes.

#### Users Stories:
1. As a user who is visiting the website I want to be able:
    - to see images and slogans explaining the website's content, 
    - to register, to get access to registered users features,
    - to see info about how many recipes and users the website has,
    - to see latest recipes added to database:
        - each recipe should show miniature image, title, author's name and date of adding
        - if recipe's image wasn't delivered deafault image for recipe shoud by displayed
    - to see most liked recipes
        - each recipe should show miniature image, title, author's name, date of adding and numbers of likes
    - to search for recipes in database by typing a phrase in a searchbar:
        - search in titles
        - search in ingredients 
        - search in keywords
        - search in all above
    - to see statistics of recipes in website's database:
        - divided by cousine, difficulty, preparation time and number of servings.
    - to see all recipes in all categories:
        - sorted by name(ascending and descending) or date(ascending and descending).
    - to browse recipes by category:
        - cousine, difficulty, prep time, servings and main ingredient
        - see how many recipes is there in every category
    - in case when recipes are searched or browsed each recipe should show:
        - miniature image,
        - title,
        - author's name,
        - date of adding,
        - number of views, likes and comments
    - to see all info about a single recipe displayed on single page by clicking on the recipe:
        - title
        - full image,
        - info about prep time, difficulty, servings and cousine,
        - author's name and avatar, date of adding,
        - main ingredient, ingredients and keywords,
        - instructions,
        - views, likes, comments,
        - comments leaved by users.
    - to contact website's owners, by filling in and submitting contact form
    - to read some info about the website
    - to read terms of use of the website
    
2. As a registered user I want to be able:
    - to log in,
    - to add new recipe with image,
    - to access my profile:
        - update my profile avatar,
        - if profile's avatar wasn't delivered deafault avatar for a profile shoud by displayed
        - check recipes liked and commented by me,
    - to edit, delete recipes added by me,
    - update images of recipes added by me,
    - comment recipes,
    - like recipes,
    - to log out.

#### Wireframes
- [Home page](https://github.com/mariusz79/Recipes-Third-Milestone-Project//blob/master/wireframes/Homepage.png)
- [Statistics](https://github.com/mariusz79/Recipes-Third-Milestone-Project//blob/master/wireframes/Statistics.png)
- [All Recipes](https://github.com/mariusz79/Recipes-Third-Milestone-Project//blob/master/wireframes/AllRecipes.png)
- [Single Recipe](https://github.com/mariusz79/Recipes-Third-Milestone-Project//blob/master/wireframes/SingleRecipe.png)
- [Add Recipe](https://github.com/mariusz79/Recipes-Third-Milestone-Project//blob/master/wireframes/AddRecipe.png)
- [Login/Register/Contact](https://github.com/mariusz79/Recipes-Third-Milestone-Project//blob/master/wireframes/LoginRegisterContact.png)
- [Add Image](https://github.com/mariusz79/Recipes-Third-Milestone-Project//blob/master/wireframes/AddImage.png)
- [Dashboard](https://github.com/mariusz79/Recipes-Third-Milestone-Project//blob/master/wireframes/Dashboard.png)


## Features
- __Register__
    - user can register by providing username and password in register form. Password needs to be confirmed in extra field. Both username and password have to be at least two characters long. If user tries to register username that already exists in the database an error is displayed. After successful registering user is redirected to the home page.
- __Log in, log out__
    - registered user can log in by filling in login form. If user was redirected to login page from a page which functionality required user to be authenticated, after successful logging in user will be redirected back to that page. Otherwise user is redirected to the home page. If user provides wrong username and/or wrong password an error is displayed.
- __Add recipe__
    - user can add recipe to database by filling in add-recipe form. The form contains following fields:
        - title (length between 2 and 70 characters)
        - main ingredient, having 7 choices
        - ingredients (length between 2 and 300 characters), ingredients need to be separated by commas
        - servings (an integer between 1 and 6)
        - prep_time (an integer between 1 and 180)
        - difficulty, having 3 choices
        - cousine, having 4 choices
        - keywords (length between 2 and 100 characters), keywords need to be separated by commas
        - body (length minimum 40 characters)
    - all fields are required
    - if user leaves any field empty an error is displayed
    - after filling in all fields user can post recipe to the database by clicking on 'Add Recipe' button
    - anytime user can be redirected to the home page by clicking on 'Cancel' button
    - only registered users can add recipes
- __Edit recipe__
    - user can update recipe by changing data in add-recipe form. Characteristic of 'Add recipe' feature from above is in use
- __Search__
    - user can search for recipes by typing a phrase in a search-bar and pressing  search button or enter on the keyboard,
    - a phrase needs to be at least 2 characters long, otherwise a warning will be displayed;
    - user can choose where to look for his search: in titles, ingredients, keywords or all places together.
- __View all recipes__
    - user has access to all recipes sorted by name(ascending and descending) or date(ascending and descending)
    - pagination is in use
- __Browse recipes by category and subcategory__
    - user can browse recipes (from the home page) in 5 categories:
        - main ingredient, with subcategories:
            - eggs, cheese, pasta, meat, wheat, fruits, vegs.
        - difficulty, with subcategories:
            - easy, medium, difficult.
        - preparation time, with subcategories:
            1-30 minutes, 30-60 minutes, 60-180 minutes. 
        - servings, with subcategories:
            1-2, 3-4, 5-6.
        - cousine, with subcategories:
            - african, american, asian and european.
    - number of recipes is displayed next to each subcategory
    - pagination is in use
- __Contact__
    - user can send message to website's owners by filling in contact form's fields:
        - username, email, subject and message
        - each field is required
        - email needs to be valid email
    - in case of errors an error is diplayed
    - user can post message by clicking on 'Send message' button
    - if success, success message is displayed
    - user can be redirect to the home page without sending message by clicking on 'Cancel' button
- __Summarized information about number of recipes and users__
    - info about number of recipes and users is displayed on the front page
- __Statistics__
    - displays charts for all recipes in 4 categories
- __Latest recipes__
    - displays most recently added recipes on the front page
- __Most liked recipes__
    - displays recipes with most likes on the front page
    - number of likes is highlighted in the upper left corner of the recipes miniatures
- __View single recipe__
    - displays all information about the recipe on a single page
- __Like single recipe__
    - user is able to like single recipe by clicking on 'Like' button on a single recipe's page
    - only registered users can like recipes
    - user can't like his own recipes
- __Comment single recipe__
    - user is able to post comment(s) for single recipe by filling in comment's form and clicking on 'Add comment' button on a single recipe's page
- __Add/update recipes' image__
    - user can upload images for his recipes
    - on upload page user has to choose file to upload
    - if no file is chosen and user clicks on 'Send image' button, an error is displayed
    - if chosen file has wrong extension, an error is displayed
- __Add/update user's avatar__
    - user can upload pictures for his profile
    - on upload page user has to choose file to upload
    - if no file is chosen and user clicks on 'Send avatar' button, an error is displayed
    - if chosen file has wrong extension, an error is displayed
- __Navbar__
    - contains logo and other links, fully responsive
- __Footer__
    - contains linked social icons, terms of use, about and contact form; fully responsive


## Technologies Used
- [Flask](http://flask.pocoo.org/)
    - to build web application
- [Python 3.7.3](https://www.python.org/)
    - to write logic
- [MongoDB](https://www.mongodb.com/)
    - for store and retrieve data
- [HTML5](https://www.w3.org/TR/html52/)
    - to create website
- [CSS3](https://www.w3.org/Style/CSS/Overview.en.html)
    - to style all elements of the website
- [Materializecss ](https://materializecss.com/)
    - used for responsiveness and styling
- [jQuery](https://jquery.com/) v3.3.1
    - used for DOM manipulation
- [Charts.js](https://www.chartjs.org/)
    - used for creation charts
- [Font Awesome](https://fontawesome.com/) v5.5.0
    - for all icons used on website
- [Google fonts](https://fonts.google.com/)
    - for extra fonts used on website
- [Gimp](https://www.gimp.org/)
    - for changing resolution and cutting images
- [Chrome developer tools](https://developers.google.com/web/tools/chrome-devtools/)
    - for editing page on-the-fly, diagnosing problems
- [Visual Studio Code](https://code.visualstudio.com/)
    - code editor
- [Git & GitHub](https://github.com/)
    - for project's version control
- [Heroku](https://www.heroku.com/)
    - for app deployment
- [tinypng.com](https://tinypng.com/) 
    - for images compression
- [Pencil v3.0.4](https://pencil.evolus.vn)
    - for wireframes
- [The W3C Markup Validation Service](https://validator.w3.org/nu/)
    - to check for syntax errors in HTML code
- [The W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/)
    - to check for errors in CSS code

## Project challenges.
This project was very challenging yet rewarding.
I learned important things from this project.
First, I learned how to use Python as a Server Side Language.
Second, I learned about MongoDB and how to use it with Flask.
Third, I learned about Cloud Services(Heroku). 
I also learned about Flask wtforms, how to validate them, pagination, uploading files, registering, logging, sending emails, coding and decoding passwords. I find the time I spend working on the project very beneficial.

## Testing
#### User stories
User stories from the UX section were tested to ensure that they all work as intended, with the project providing an easy and straightforward way for the users to achieve their goals.

1. As a user who is visiting the website I want:
    - to see images and slogans explaining the website's content, 
    > - Carousel of 3 full-width images is presented on the front page. Each image contains standing out slogan, informing about website content.
    - to register, to get access to registered users features,
    > - Click on Register link situated in navbar. For browser's width less than 992px click menu('hamburger' icon) and then click 'Register'.
    - to see info about how many recipes and users the website has,
    > - Numbers of recipes and users are show on three panels containing icons and text on the front page
    - to see latest recipes added to database:
        - each recipe should show miniature image, title, author's name and date of adding
    > - Three miniatures of images of the latest added recipes are presented in section Latest Recipes on the front page. Each miniature also shows title, author's name and date of adding of the recipe. If recipe's image wasn't delivered default image for recipe is displayed
    - to see most liked recipes
        - each recipe should show miniatare image, title, author's name, date of adding and numbers of likes
    > -Three miniatures of images of the most liked recipes are presented in section Most Liked Recipes on the front page. Each miniature also shows title, author's name and date of adding of the recipe. If recipe's image wasn't delivered default image for recipe is displayed. Number of likes for each recipes is presented in upper left corner of the miniature.
    - to search for recipes in database by typing a phrase in a searchbar:
        - search in titles
        - search in ingredients 
        - search in keywords
        - search in all above
    > - A searchbar is provided. User can use it on the front page or by clicking Search link in the navbar. For browser's width less than 992px click menu('hamburger' icon) and then click 'Search'. 
    - to see statistics of recipes in website's database:
        - divided by cousine, difficulty, preparation time and number of servings.
    > - Click on Statistics link situated in navbar. For browser's width less than 992px click menu('hamburger' icon) and then click 'Statistics'. After that user is redirected to 'Statistic' page, where three kinds of charts are displayed.
    - to see all recipes in all categories:
        - sorted by name(ascending and descending) or date(ascending and descending).
    > - Click on All Recipes link situated in navbar. For browser's width less than 992px click menu('hamburger' icon) and then click 'All Recipes'. After that user is redirected to 'All Recipes' page, where pagination is in use and 6 recipes are displayed at once. To see more recipes and travel between user has to use left and right chevrons at the bottom of the page. User can choose how recipes have to be sorted. The options are: date ascending and descending, name ascending and descending.
    - to browse recipes by category:
        - cousine, difficulty, prep time, servings and main ingredient
        - see how many recipes is there in every category
    > - On the bottom of the front page click on one of the categories, then click of the subcategory you want do check.
    - in case when recipes are searched or browsed each recipe should show:
        - miniature image,
        - title,
        - author's name,
        - date of adding,
        - number of views, likes and comments
    - to see all info about a single recipe displayed on single page by clicking on the recipe:
        - title
        - full image,
        - info about prep time, difficulty, servings and cousine,
        - author's name and avatar, date of adding,
        - main ingredient, ingredients and keywords,
        - instructions,
        - views, likes, comments,
        - comments leaved by users.
    - > - Click on the miniature of the recipe's image
    - to contact website's owners, by filling in and submitting contact form
    > - Click on Contact link situated in navbar and in footer. User will be redirected to Contact page and has to fill in contact form. From there user can send message by clicking 'Send message' button or go the front page by clicking 'Cancel' button.
    - to read some info about the website
    > - Click on About link situated in footer. 
    - to read terms of use of the website
    > - Click on Terms of use link situated in footer. 

2. As a registered user I want to:
    - to log in,
    > - Click on Login link situated in navbar. For browser's width less than 992px click menu('hamburger' icon) and then click 'Login'.
    - to add new recipe with image,
    > - Click on Add Recipe link situated in navbar. For browser's width less than 992px click menu('hamburger' icon) and then click 'Add Recipe'. 
    - to access my profile:
    > - Click on Dashboard link situated in navbar. For browser's width less than 992px click menu('hamburger' icon) and then click 'Dashboard'.
    - update my profile avatar
    > - When on Dashboard page click 'Update avatar' button.
        - if profile's avatar wasn't delivered deafault avatar for a profile shoud by displayed
    - check recipes liked and commented by me,
    > - Liked and commented recipes are displayed on Dashboard page
    - to edit, delete recipes, update images of recipes added by me,
    > - When on Dashboard page, check section My Recipes. Edit, Delete and Update Image options are available for all recipes. Clicking on Edit will redirect user to add-recipe form with all fields filled in. User can change the  data and accepts changes. Clicking on Delete will trigger modal asking user if he really wants to delete the recipe. User can delete recipe or cancel his action. Clicking on Image will redirect user to upload page, when he can choose and upload image or go back to Dashboard.    
    - comment recipes,
    > - When on single recipe page, type comment in the comment form and click 'Post comment' button.
    - like recipes,
     > - When on single recipe page, click 'Like' button.
    - to log out.
    > - Click on Logout link situated in navbar. For browser's width less than 992px click menu('hamburger' icon) and then click 'Logout'.


#### Different browsers, mobile, desktop.
According to https://www.w3schools.com/browsers/ statistics, the most popular browsers are:
- Chrome;
- Edge/IE,
- Firefox,
- Opera.

This project website was tested on mentioned above web browsers, desktop/mobile, Android and iOS.
The project looks and works properly on different browsers and screen sizes. 

#### Code validation
HTML and Css code for this website were validated using W3C Validation Service. No errros were found in the code.

## Deployment
#### To push this app to GitHub repository, the following actions were taken:
1. Installing git and creating a GitHub account.
2. Initializing a git repository in the root of the app folder, by running the git init command.
3. Creating a new repository on GitHub:
    - logging in and going to the GitHub home page. Clicking '+ New repository' button,
    - typing name of the repo and providing a brief description,
    - pressing the 'Create repository' button to make new repo,
    - following the '....or push an existing repository from the command line' section.
4. Adding, committing and pushing changes to GitHub repository.

#### Deploying to heroku took following steps:
1. Developing app and pushing it to GitHub.
2. Creating a requirements.txt file. That file contains all required packages to run the application.
```
pip freeze > requirements.txt
```
3. Creating a Procfile. Procfile is a mechanism for declaring what commands are run by application’s dynos on the Heroku platform.
Procfile contains:
```
web: python app.py
```
4. Pushing changes on Github.
5. Creating an App on Heroku(before creating an app make sure your GitHub account is connected with Heroku Account):
    - click on Create new app an Heroku website
    - type app name and choose region
    - click create app button.
6. Creating config variables:
    - on Heroku app go to settings
    - click Reveal Vars
    - set IP to 0.0.0.0
    - set PORT to 5000
    - set MAIL_PASSWORD, MONGO_URI1 and SECRET_KEY
7. Deploying the app on Heroku:
    -  open your Heroku app and go to deploy option 
    -  select the deployment method as  Github,
    -  search your repository with a name and click connect 
    -  app started to deploy on Heroku,  wait for some time 
    -  after the successful message popup, app can be view using URL delivered by Heroku. 
Live version of this app can be found [here](https://recipes-flask.herokuapp.com/).

#### To clone this repository and run the app locally following steps are needed:
1. On GitHub, navigate to the main page of the repository.
2. Under the repository name, click Clone or download.
3. In the Clone with HTTPs section, click an copy icon to copy the clone URL for the repository.
4. Open Git Bash and change the current working directory to the location where you want the cloned directory to be made.
5. Type git clone, and then paste the URL you copied in Step 2.
    ```
    $ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
    ```
6. Press Enter. Your local clone will be created.  
7. Install requirements
```
pip install -r requirements.txt
```
8. Set the environmental variables(FOR ASSESOR):
    - IP = 0.0.0.0 ,
    - PORT = 5000 ,
    - MONGO_URI1 = mongodb+srv://root1:r00tuser1@myfirstcluster-bvngp.mongodb.net/task_manager?retryWrites=true ,
    - SECRET_KEY = secret123
    - For sending mails you would have to set your own variables.
9. Start the app 
```
python app.py
```
and go to http://127.0.0.1:5000/

## Database schema
NoSql MongoDB was used as a database to store data about recipes and users. 
MongoDB works on concept of collection and document. A collection exists within a single database and is a group of MongoDB documents. Typically, all documents in a collection are of similar or related purpose. A document is a set of key-value pairs.
I've created two collection within my database, named recipes and users.
All documents in recipes collection have the following schema:
```
{"_id":{"$oid":"5d0757f9a4c2223724d59eaa"},
"title":"Stuffed eggs",
"main_ingredient":"eggs",
"ingredients":"10 eggs , 1/4 cup mayonnaise, 1 teaspoon Dijon mustard, 2 tablespoons grated Parmesan cheese, salt and ground black pepper, 1 tablespoon ketchup",
"servings":{"$numberInt":"4"},
"prep_time":{"$numberInt":"10"},
"body":"    Place eggs in a large pot and cover with cool water. Bring to a boil and cook, stirring occasionally, for 10 minutes. Transfer eggs to a bowl of cold water using tongs. Peel.\r\n    Cut eggs in half. Slice a small piece off bottoms so halves don't tip over. Place yolks in a mixing bowl. Add mayonnaise, mustard, Parmesan cheese, salt, and pepper. Mix until creamy, 1 or 2 minutes.\r\n    Spoon yolk mixture into egg white halves. Garnish with a dot of ketchup on top. Refrigerate about 20 minutes before serving.\r\n","difficulty":"easy",
"cousine":"asian",
"keywords":"eggs, stuffed",
"author":"Sylvia",
"date_of_adding":"Jun 17, 2019",
"recipe_image_name":"asparagus-1307604_640.jpg",
"views":{"$numberInt":"8"},
"likes":{"$numberInt":"3"},
"comments":[{"author":"qq","comment":"Really nice","date_of_adding":"Jun 18, 2019"}],"comments_number":{"$numberInt":"1"}}
```
All documents in users collection have the following schema:
```
{"_id": {"$oid":"5d08b374a2e599000f911cff"},
"username":"potato",
"password":"$2b$12$BgWGl4oCwEOotAtLbKskueJuQo6auMFrK28MbgRKeUYvW26CVLB7O",
"date_of_registration":"Jun 18, 2019",
"profile_image_name":"ja.jpeg",
"liked":[{"$oid":"5d075f73a4c22227ac6521ac"},{"$oid":"5d075ddea4c22227ac6521a9"},{"$oid":"5d0755a5a4c2223724d59ea4"}],"commented_recipe_id":[{"$oid":"5d075f73a4c22227ac6521ac"},{"$oid":"5d075f73a4c22227ac6521ac"},{"$oid":"5d075ddea4c22227ac6521a9"}]}
```
I've decided to store images uploaded by users in MongoDB. That's why my database contains two extra collections: fs.files and fs.chunks which are used to store binary data of images.
## Content
#### Images 
All images used in the project were downloaded from [pixabay](https://pixabay.com/).

## Acknowledgements
I received inspiration for this project from [Code Institute](https://www.codeinstitute.net/).