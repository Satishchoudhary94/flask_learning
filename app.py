from flask import Flask 
from flask import render_template
from flask import request


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    my_name = "Satish"
    age = 20
    skills = ["Python", "Flask", "HTML", "CSS"]
    location  = "India"
    return render_template('about.html', name=my_name, age=age, skills=skills, location=location)


@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])

def submit():
    username =  request.form['username']
    email  = request.form['email']
    password = request.form['password']
    location = request.form['location']
    age = request.form['age']
    
    return render_template('submit.html', username=username, email=email, password=password)



if __name__ == '__main__':
    app.run(debug=True)