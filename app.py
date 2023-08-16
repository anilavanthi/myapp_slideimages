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
    image_path_2 = db.Column(db.String(200))
    image_path_3 = db.Column(db.String(200))
    website_url = db.Column(db.String(200))

    def __repr__(self):
        return f'<College {self.name}>'

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    colleges = College.query.all()
    return render_template('index.html', colleges=colleges)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        college_name = request.form['college_name']
        activities = request.form['activities']
        website_url = request.form['website_url']
        image_1 = request.files['image_1']
        image_2 = request.files['image_2']
        image_3 = request.files['image_3']

        if image_1:
            filename_1 = os.path.join(app.config['UPLOAD_FOLDER'], image_1.filename)
            image_1.save(filename_1)
        if image_2:
            filename_2 = os.path.join(app.config['UPLOAD_FOLDER'], image_2.filename)
            image_2.save(filename_2)
        if image_3:
            filename_3 = os.path.join(app.config['UPLOAD_FOLDER'], image_3.filename)
            image_3.save(filename_3)

        college = College(
            name=college_name,
            activities=activities,
            image_path=image_1.filename,
            image_path_2=image_2.filename,
            image_path_3=image_3.filename,
            website_url=website_url
        )
        db.session.add(college)
        db.session.commit()

        return redirect(url_for('colleges', new_college_id=college.id))

    return render_template('submit.html')
@app.route('/delete/<int:college_id>', methods=['GET', 'POST'])
def delete(college_id):
    college = College.query.get_or_404(college_id)

    if college.image_path:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], college.image_path)
        if os.path.exists(image_path):
            os.remove(image_path)

    if college.image_path_2:
        image_path_2 = os.path.join(app.config['UPLOAD_FOLDER'], college.image_path_2)
        if os.path.exists(image_path_2):
            os.remove(image_path_2)

    if college.image_path_3:
        image_path_3 = os.path.join(app.config['UPLOAD_FOLDER'], college.image_path_3)
        if os.path.exists(image_path_3):
            os.remove(image_path_3)

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
    return 'College information and images uploaded successfully!'

if __name__ == '__main__':
    app.run(port=5000, debug=True)



