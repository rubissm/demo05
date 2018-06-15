from flask import Flask,request, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return "<h2>Welcome</h2>"

# Mapping, decorator(?)
@app.route('/metodito')
def metodito():
    return 'Method used: %s' %request.method

@app.route('/Gianmar')
def Gianmar():
    return '<h3> Pollito uwu</h3>'

@app.route('/profile/<name>')
def profile(name):
    return render_template("profile.html", name=name)
#Por default es string
@app.route('/post/<int:post_id>')
def show_post(post_id):
    return "<h2>Post ID is %s </h2>" % post_id

@app.route("/uwu", methods=['GET', 'POST'])
def uwu():
    if request.method == 'POST':
        return "Estás usando POST we"
    else:
        return "Parece que estás usando GET we"

#Se declara como main uwu

