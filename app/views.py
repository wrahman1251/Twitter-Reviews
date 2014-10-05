from flask import Flask
from flask import render_template, flash, redirect, session, url_for, request, g
from app import app


@app.route('/')
@app.route('/index')
def my_form():
	return render_template("my-form.html", name='Home')

@app.route('/', methods=['POST'])
def my_form_post():

	text = request.form['text']
	processed_text = text.upper()
	return processed_text

if __name__=='__main__':
	app.run()

