from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__, static_url_path='/static')

# Set an absolute path for the upload folder
upload_path = os.path.join(os.getcwd(), 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = upload_path
app.config['DATABASE'] = 'college_info.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.getcwd(), app.config['DATABASE'])}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

# Create upload folder if it doesn't exist
if not os.path.exists(upload_path):
    os.makedirs(upload_path)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class College(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Expecting unique names
    activities = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(200))
    image_path_2 = db.Column(db.String(200))
    image_path_3 = db.Column(db.String(200))
    image_path_4 = db.Column(db.String(200))
    image_path_5 = db.Column(db.String(200))
    website_url = db.Column(db.String(200))
    contact_number = db.Column(db.String(20))
    contact_number_2 = db.Column(db.String(20))

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
        # Check if a college with this name already exists
        existing_college = College.query.filter_by(name=college_name).first()
        if existing_college:
            return "A college with that name already exists.", 400

        activities = request.form['activities']
        website_url = request.form['website_url']
        contact_number = request.form['contact_number']
        # Convert empty string to None for contact_number_2 if desired
        contact_number_2 = request.form['contact_number_2'] or None

        image_1 = request.files['image_1']
        image_2 = request.files['image_2']
        image_3 = request.files['image_3']
        image_4 = request.files['image_4']
        image_5 = request.files['image_5']

        # Save images if provided, else set to empty string
        if image_1 and image_1.filename != '':
            filename_1 = os.path.join(app.config['UPLOAD_FOLDER'], image_1.filename)
            image_1.save(filename_1)
        else:
            filename_1 = ''

        if image_2 and image_2.filename != '':
            filename_2 = os.path.join(app.config['UPLOAD_FOLDER'], image_2.filename)
            image_2.save(filename_2)
        else:
            filename_2 = ''

        if image_3 and image_3.filename != '':
            filename_3 = os.path.join(app.config['UPLOAD_FOLDER'], image_3.filename)
            image_3.save(filename_3)
        else:
            filename_3 = ''

        if image_4 and image_4.filename != '':
            filename_4 = os.path.join(app.config['UPLOAD_FOLDER'], image_4.filename)
            image_4.save(filename_4)
        else:
            filename_4 = ''

        if image_5 and image_5.filename != '':
            filename_5 = os.path.join(app.config['UPLOAD_FOLDER'], image_5.filename)
            image_5.save(filename_5)
        else:
            filename_5 = ''

        college = College(
            name=college_name,
            activities=activities,
            image_path=filename_1,
            image_path_2=filename_2,
            image_path_3=filename_3,
            image_path_4=filename_4,
            image_path_5=filename_5,
            website_url=website_url,
            contact_number=contact_number,
            contact_number_2=contact_number_2
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
    if college.image_path_4:
        image_path_4 = os.path.join(app.config['UPLOAD_FOLDER'], college.image_path_4)
        if os.path.exists(image_path_4):
            os.remove(image_path_4)
    if college.image_path_5:
        image_path_5 = os.path.join(app.config['UPLOAD_FOLDER'], college.image_path_5)
        if os.path.exists(image_path_5):
            os.remove(image_path_5)
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



