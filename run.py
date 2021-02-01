#We need to import the main app
from flaskblog import create_app

#DELETE PYCACHE WHEN RUNNING ON A DIFFERENT PC

app = create_app()

#Runs Flask even when not in virenv
if __name__ == '__main__':
	app.run(debug=True)