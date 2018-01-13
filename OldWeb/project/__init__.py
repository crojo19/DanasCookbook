from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Smokey19!@localhost/website'
 
db = SQLAlchemy(app)
class students(db.Model):
   id = db.Column('student_id', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   city = db.Column(db.String(50))  
   addr = db.Column(db.String(200))
   pin = db.Column(db.String(10))

def __init__(self, name, city, addr,pin):
   self.name = name
   self.city = city
   self.addr = addr
   self.pin = pin
 
db.create_all() 
 
@app.route("/")
def show_all():
   return render_template('show_all.html', students = students.query.all() )
 
if __name__ == "__main__":
    app.run()