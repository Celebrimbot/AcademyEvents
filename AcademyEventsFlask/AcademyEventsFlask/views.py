"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask, render_template, request, session, url_for, redirect

from AcademyEventsFlask import app
#from forms import SelectionForm
import pandas

from flask_wtf import Form
from wtforms.fields import BooleanField

class MyForm(Form):
    yesno = BooleanField('yesno')

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    """Renders the home page."""
       
    print("Get data")

    df = pandas.read_csv('static/data/Academy Events.csv')

    print(df.columns)

    print("Got data")

    
    #form = MyForm(request.form)

    #  REALLY struggling to get forms working here.  So lets just pretend that a user has already selected a company
    user_trust_number = 8452281

        


    #print("Trust form object created")

    #if request.method == 'POST':
    #    print (form.yesno.data)
    #    flash('Thanks for playing')
    #    return redirect(url_for('contact'))


    #form.drop.choices = (
    #    ['test1', 'test2']
    #)

    #print("Test choices added")

    #acad_form = SelectionForm()

    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        #form=form
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Welcome to the contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='What is Academy Events?'
    )
