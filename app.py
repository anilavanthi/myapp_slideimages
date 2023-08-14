from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__, static_url_path='/static')

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['DATABASE'] = 'college_info.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.getcwd(), app.config['DATABASE'])}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class College(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    activities = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(200))
    website_url = db.Column(db.String(200))  # New field for the website URL

    def __repr__(self):
        return f'<College {self.name}>'

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    colleges = College.query.all()
    return render_template('index.html', colleges=colleges)

@app.route('/submit', methods=['POST'])
def submit():
    college_name = request.form['college_name']
    activities = request.form['activities']
    website_url = request.form['website_url']  # Get the website URL from the form
    image = request.files['image']

    if image:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(filename)

    college = College(name=college_name, activities=activities, image_path=image.filename, website_url=website_url)
    db.session.add(college)
    db.session.commit()

    return redirect(url_for('colleges', new_college_id=college.id))

@app.route('/delete/<int:college_id>', methods=['GET', 'POST'])
def delete(college_id):
    college = College.query.get_or_404(college_id)

    if college.image_path:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], college.image_path)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(college)
    db.session.commit()

    return redirect(url_for('colleges'))

@app.route('/colleges')
def colleges():
    new_college_id = request.args.get('new_college_id')
    colleges = College.query.all()

    if new_college_id:
        colleges = [college for college in colleges if college.id == int(new_college_id)]

    return render_template('colleges.html', colleges=colleges)

@app.route('/success')
def success():
    return 'College information and image uploaded successfully!'

if __name__ == '__main__':
    app.run(port=5000, debug=True)



