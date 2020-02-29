import pymongo
from flask import Flask,render_template,redirect,url_for,session
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

uri = 'mongodb://127.0.0.1:8000'

client = pymongo.MongoClient(uri)

database = client['fullstack']

collections = database['students']

for student in collections.find({}):
    print(student)

app = Flask(__name__)

class InfoForm(FlaskForm):

    author = StringField("Enter your name", validators=[DataRequired()])
    title = StringField("Enter your article",validators=[DataRequired()])
    content = TextAreaField("Enter the article",validators=[DataRequired()])
    submit = SubmitField("Submit")

    def __repr__(self):
        print(f"This a blog by {self.author} on {self.title}")


app.config['SECRET_KEY'] = 'secretKey'

@app.route('/',methods=['GET','POST'])
def index():
    form = InfoForm()
    if form.validate_on_submit():
        author = form.author.data
        title = form.title.data
        content = form.content.data
        collections.insert({'name': author, 'title': title, 'content': content})
        session['author'] = form.author.data
        return redirect(url_for('thankyou'))
    return render_template('basic.html', form=form)


@app.route('/thankyou')
def thankyou():
    articles = [student for student in collections.find({}) if student['name'] == session['author']]
    return render_template('thankyou.html',articles = articles)

if __name__ == '__main__':

    app.run(port = 5000, debug = True)
