from flask import Flask, render_template, request
import joblib
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///predictions.db'
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    experience = db.Column(db.Float, nullable=False)
    salary = db.Column(db.Float, nullable=False)

model = joblib.load("model.joblib")

@app.before_request
def create_tables():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    salary = None

    if request.method == "POST":
        experience = float(request.form["experience"])
        salary = round(model.predict([[experience]])[0], 2)

        record = Prediction(experience=experience, salary=salary)
        db.session.add(record)
        db.session.commit()

    all_predictions = Prediction.query.all()
    return render_template("index.html", salary=salary, data=all_predictions)

if __name__ == "__main__":
    app.run(debug=True)