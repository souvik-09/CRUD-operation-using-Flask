from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import desc


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Souvikpgadmin@localhost/Flask_todo"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__="data"
    SNo = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), primary_key=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.SNo} - {self.title}"

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template("home.html", allTodo = allTodo)

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/show")
def show():
    allTodo = Todo.query.all()
    print(allTodo)
    
@app.route("/update/<int:SNo>", methods=['GET', 'POST'])
def update(SNo):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(SNo=SNo).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(SNo=SNo).first()    
    return render_template("update.html", todo = todo)
    
    
@app.route("/delete/<int:SNo>")
def delete(SNo):
    todo = Todo.query.filter_by(SNo=SNo).first()
    db.session.delete(todo)
    db.session.commit() 
    return redirect("/")      

if __name__ == "__main__":
    app.run(debug = True)
    
#from app import app, db  # import some bits from app.py
#with app.app_context():  # this line defines the context manager
    #db.create_all()      # this line runs within the context manager    