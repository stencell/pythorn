#importing Flask class object from flask library
#import render_template method from flask library
from flask import Flask, render_template

#instantiating Flask object
#__name__ is special and will inherite the name of the python script
application = Flask(__name__)

@application.route('/')
def home():
    #files must live inside a folder called "templates"
    return render_template("home.html")

@application.route('/about/')
def about():
    return render_template("about.html")

if __name__ == "__main__":
    application.run(debug=True)


#when using to create requirements.txt, use pip freeze
#to get list of libraries and versions