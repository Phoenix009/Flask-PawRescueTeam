from flask import Flask, render_template, abort, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, SignUpForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PawsRescue.db'

db = SQLAlchemy(app)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable= False)
    age = db.Column(db.String, nullable = False)
    bio = db.Column(db.Text, nullable = False)
    adopted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fName = db.Column(db.String, nullable = False)
    email = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    pets = db.relationship('Pet', backref='owner', lazy=True) 

db.drop_all()
db.create_all()

user1 = User(fName="Pet Rescue Team", email="team@pawsrescue.co", password="adminpass")
user2 = User(fName="Jaideep More", email="jaideepmore@rocketmail.com", password="root")
db.session.add(user1)
db.session.add(user2)

try:
    db.session.commit()
except Exception as e:
    db.session.rollback()
finally:
    db.session.close()

nelly = Pet(name = "Nelly", age = "5 weeks", bio = "I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles.")
yuki = Pet(name = "Yuki", age = "8 months", bio = "I am a handsome gentle-cat. I like to dress up in bow ties.")
basker = Pet(name = "Basker", age = "1 year", bio = "I love barking. But, I love my friends more.")
mrfurrkins = Pet(name = "Mr. Furrkins", age = "5 years", bio = "Probably napping.")

db.session.add(nelly)
db.session.add(yuki)
db.session.add(basker)
db.session.add(mrfurrkins)

try:
    db.session.commit()
except Exception as e: 
    db.session.rollback()
finally:
    db.session.close()


@app.route("/")
def home():
    data = Pet.query.all()
    return render_template("home.html", data=data)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/details/<int:petId>")
def details(petId):
    data = Pet.query.get(petId)
    if not data:
        return abort(404, description="Pet Not Found")
    else:
        return render_template("details.html", data = data)


@app.route("/login", methods=['GET', 'POST'])
def login():
    msg=None
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user:
            msg = "User Not Found !"
        else:
            if user.password == password:
                session['login'] = True
                msg="Login Successful"
                return redirect("/")
            else:
                msg="Incorrect Password"
    elif form.errors:
        msg="Invalid Input"
    return render_template("login.html", form=form, msg=msg)


@app.route("/logout")
def logout():
    if session['login']:
        session['login'] = False
        return redirect("/")
    else:
        return redirect("login")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    msg = None
    form = SignUpForm()
    if form.validate_on_submit():
        fName = form.fName.data
        email = form.email.data
        password = form.password.data
        newUser = User(fName=fName, email=email, password=password)
        db.session.add(newUser)
        try:
            db.session.commit()
            msg = "Account Made Successfully"
        except Exception as e:
            print(e)
            db.session.rollback()
            msg="Account with that email already exists !!"
        finally:
            db.session.close()
    return render_template("signup.html", form = form, msg=msg)


if __name__ == "__main__":
    app.run(debug =True)
