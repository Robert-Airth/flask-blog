#import certain functions into the global
#namespace
from app import app
from markdown import markdown
from flask import render_template, render_template_string, request, session
from app.blog_helpers import render_markdown

#safe global import (okay to use)
import flask
#OS is being imported for the /all directory to get the
#template-file names to send to the client
import os

#global import (try to avoid)
#from flask import *

#home page
@app.route("/")
def home():
    return render_template('index.html')

@app.route('/all')
def all():
    #TODO: figure out how to find all files 
    #in the app

    #this will correct root directory which the
    #template/webpage files are located on the server
    path = r'C:\Users\robad\Desktop\School HSU\Spring 2020\CS 232 -Python\flask-blog\app\templates'
    
    view_data = {}
    view_data["pages"] = []
    #root=root, d=directories, f=files
    for r,d, f in os.walk(path):
        for file in f:
            view_data["pages"].append(os.path.splitext(file)[0])
   
    return render_template("all.html", data = view_data)

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        
        uname = request.values['user_name']
        pword = request.values['password']

        if (uname == 'rob') and (pword == 'rob'):
            session['user'] = uname
            return render_template('index.html')


       # session['user_name'] = request.values['user_name']
    return render_template("/login.html")

@app.route('/logout', methods=['POST'])
def logout():
    session['user_name'] = ''
    session['password'] = ''
    return render_template('logged_out.html')

@app.route("/favicon.ico")
def favicon():
    return ""

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route("/click_tracker", methods=['GET', 'POST'])
def click_tracker():
    view_data = {}
    view_data["click_count"] = 0
    if request.method == 'POST':
        view_data["click_count"] = request.values["click_count"]
        view_data["click_count"] = int(view_data["click_count"]) + 1
    return render_template('click_tracker.html', data=view_data)


@app.route("/edit/<page_name>", methods=["GET", "POST"])
def edit(page_name):
    if request.method == "GET":
        if session["user_name"] == "rob" :
           output_page = render_template(page_name + '.html')
           return render_template('edit.html', output_page=output_page, page_name = page_name)
        else:
           return render_template('index.html')
    elif request.method == "POST":
        if session["user_name"] == "rob" :
           new_file = open('app/templates/' + page_name + '.html', 'w')
           new_file.write(request.form["content"].strip())
           new_file.close()
           output_page = render_template(page_name + '.html')
           return render_template('edit.html', output_page=output_page, page_name = page_name)
        else:
           return render_template('login.html')

        return render_template('login.html')


#generic page
@app.route("/<request>")
#input parameter name must match route parameter
def render_page(request):
    return render_template(request + '.html')


