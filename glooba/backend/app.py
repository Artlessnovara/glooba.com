from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def splash():
    return render_template('splash.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/signup')
def signup():
    return render_template('signup_options.html')

if __name__ == '__main__':
    app.run(debug=True)
