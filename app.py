from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta,datetime
import re
from email_validator import validate_email, EmailNotValidError
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "c33b3033f61952a6a5a900fcef4d8f8333ee89a0fb7dd7eeb61294b0f2983ee5" 

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Auricdefence.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=7)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# 1. User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    # mobileNumber = db.Column(db.String(15), unique=True, nullable=False)
    role = db.Column(db.String(50), default='user')  # e.g., admin/user
    reports = db.relationship('ReportSubmission', backref='user', lazy=True)
    settings = db.relationship('UserSettings', backref='user', uselist=False)
    plan = db.Column(db.String(50), default="Free")
    signup_date = db.Column(db.DateTime, default=datetime.utcnow)
    has_active_subscription = db.Column(db.Boolean, default=False)

# 2. User Settings Model
class UserSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(20), default='light')
    notifications_enabled = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# 3. Blockchain Ledger Model
class BlockchainLedger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(100), unique=True, nullable=False)
    data_hash = db.Column(db.String(256), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.Text)



# 5. Compliance Report Model
class ComplianceReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    submitted_by = db.Column(db.String(100), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Pending')  # Pending, Reviewed, Approved

# 6. Report Submission Model
class ReportSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(50), default='Submitted')

# 7. Pricing Plan Model (if pricing is dynamic)
class PricingPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    features = db.Column(db.Text)





@app.route('/')
def landing():
    return render_template('landing.html')


# Signup route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        # mobileNumber=request.form.get("mobileNumber")
        password = request.form.get("password")

        # Validate email format
        try:
            valid = validate_email(email)
            email = valid.email
        except EmailNotValidError:
            flash("Invalid email format", "danger")
            return render_template("signup.html")

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash("Email is already registered", "warning")
            return render_template("signup.html")

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Signup successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password", "danger")

    return render_template("login.html")




@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    # Calculate trial period end date
    trial_end = user.signup_date + timedelta(days=7)

    # Check if trial expired and user has no active subscription
    if not user.has_active_subscription and datetime.utcnow() > trial_end:
        return render_template('limit.html', user=user)  # limit.html shows plan expired message

    # If still in trial or subscribed, show dashboard
    return render_template("dashboard.html", username=user.username)


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))


@app.route('/features')
def features():
    return render_template('Features.html')


@app.route('/pricing')
def pricing():
    return render_template('pricing.html')


@app.route('/blockchain-ledger')
def blockchain_ledger():
    return render_template('blockchain-ledger.html')


@app.route('/compliancereport')
def compliancereport():
    return render_template('compliancereport.html')


@app.route('/reportsubmit')
def reportsubmit():
    return render_template('reportsubmit.html')

@app.route('/settings', methods=['GET'])
def settings():
    return render_template('settings.html')

@app.route('/settings/profile', methods=['POST'])
def save_profile_settings():
    # Process profile settings form
    print("Saved Profile:", request.form)
    return redirect(url_for('settings') + "#profile-settings")

@app.route('/settings/security', methods=['POST'])
def save_security_settings():
    # Process security settings form
    print("Saved Security:", request.form)
    return redirect(url_for('settings') + "#security-settings")

@app.route('/settings/notifications', methods=['POST'])
def save_notifications_settings():
    # Process notifications form
    print("Saved Notifications:", request.form)
    return redirect(url_for('settings') + "#notifications-settings")

@app.route('/settings/download', methods=['POST'])
def download_data():
    # Trigger data download
    print("Download data requested")
    return redirect(url_for('settings') + "#data-privacy-settings")

@app.route('/settings/delete', methods=['POST'])
def delete_account():
    # Handle account deletion
    print("Account deletion requested")
    return redirect(url_for('settings'))

@app.route('/settings/support', methods=['GET'])
def contact_support():
    # Optionally show support info, or just go back to settings
    return redirect(url_for('settings') + "#help-support")

@app.route('/settings/faqs', methods=['GET'])
def view_faqs():
    # Optionally show FAQs, or just go back to settings
    return redirect(url_for('settings') + "#help-support")



@app.route('/blog')
def blog():
    return render_template('blog.html')



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)