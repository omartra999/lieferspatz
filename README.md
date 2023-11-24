# lieferspatz
# app.py 
is the main app where everything is connected, this is our flask app, it routes the different web pages, defines where buttons should bring the user, 
and connect the logic from backend classses like RegistrationManager, etc... to the frontend and the routings

# templates
this folder is used to save our html templates, so that our flask app can read the templates directly from this folder and render them to the browser

# RegistrationManager.py
this class handels the customer registration process, it connects to the customer table in Lieferspatz database, adds a new customer if it still not exists

# CustomerLogin.py
this class handels the login logic, I'm still trying to figuer out how to keep the user authenticated after the login...
