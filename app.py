from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError
from flask_bcrypt import Bcrypt
import requests

load_dotenv()

app = Flask(__name__)
app.secret_key = "c33b3033f61952a6a5a900fcef4d8f8333ee89a0fb7dd7eeb61294b0f2983ee5"

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Auricdefence.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=7)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# --------------------- MODELS ---------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phoneNumber = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(50), default='user')  # e.g., admin/user
    reports = db.relationship('ReportSubmission', backref='user', lazy=True)
    settings = db.relationship("UserSettings", backref="user", uselist=False, cascade="all, delete-orphan")
    plan = db.Column(db.String(50), default="Free")
    signup_date = db.Column(db.DateTime, default=datetime.utcnow)
    has_active_subscription = db.Column(db.Boolean, default=False)


class UserSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(150))
    twofa = db.Column(db.String(20))
    email_alerts = db.Column(db.String(10))
    sms_alerts = db.Column(db.String(10))
    frequency = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)  # ✅ One-to-One link


class BlockchainLedger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(100), unique=True, nullable=False)
    data_hash = db.Column(db.String(256), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.Text)


class ComplianceReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    submitted_by = db.Column(db.String(100), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Pending')  # Pending, Reviewed, Approved


class ReportSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(50), default='Submitted')


class PricingPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    features = db.Column(db.Text)


# --------------------- ROUTES ---------------------
@app.route('/')
def landing():
    return render_template('landing.html')

def send_n8n_event(event_type, username, email, ip):
    webhook_url = "https://rithuvaishnav.app.n8n.cloud/webhook-test/auricdefence/user-event"
    payload = {
        "event": event_type,   # "login" or "signup"
        "username": username,
        "email": email,
        "ip_address": ip,
        "timestamp": datetime.utcnow().isoformat()
    }

    try:
        res = requests.post(webhook_url, json=payload, timeout=5)
        res.raise_for_status()
        print("[n8n SUCCESS]", res.text)
    except requests.exceptions.RequestException as e:
        print("[n8n ERROR]", e)
        if e.response is not None:
            print("Response content:", e.response.text)



def send_incident_report(incident_type, severity, description, date_time, reporter_name, reporter_email):
    # Your actual n8n webhook URL (make sure no extra space)
    webhook_url = "https://rithuvaishnav.app.n8n.cloud/webhook-test/Auricdefence-report"

    payload = {
        "incident_type": incident_type,
        "severity": severity,
        "description": description,
        "date_time": date_time if date_time else datetime.utcnow().isoformat(),
        "reporter_name": reporter_name,
        "reporter_email": reporter_email,
        "timestamp": datetime.utcnow().isoformat()
    }

    try:
        res = requests.post(webhook_url, json=payload, timeout=10)
        res.raise_for_status()
        print("[n8n SUCCESS]", res.text)
        return res.json() if res.headers.get("Content-Type") == "application/json" else res.text
    except requests.exceptions.RequestException as e:
        print("[n8n ERROR]", e)
        if hasattr(e, "response") and e.response is not None:
            print("Response content:", e.response.text)
        return None


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username

            # Send event to n8n
            send_n8n_event("login", user.username, user.email, request.remote_addr)

            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password", "danger")

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        phoneNumber = request.form.get("phoneNumber")

        try:
            valid = validate_email(email)
            email = valid.email
        except EmailNotValidError:
            flash("Invalid email format", "danger")
            return render_template("signup.html")

        if User.query.filter_by(email=email).first():
            flash("Email is already registered", "warning")
            return render_template("signup.html")

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(username=username, email=email, password=hashed_password, phoneNumber=phoneNumber)
        db.session.add(new_user)
        db.session.commit()

        # Send event to n8n
        send_n8n_event("signup", username, email, request.remote_addr)

        flash("Signup successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please log in first", "warning")
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session.get("username"))


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))


@app.route('/features')
def features():
    return render_template('features.html')



@app.route('/pricing')
def pricing():
    return render_template('pricing.html')



@app.route('/blockchain-ledger')
def blockchain_ledger():
    return render_template('blockchain-ledger.html')


@app.route('/compliancereport')
def compliancereport():
    return render_template('compliancereport.html')

@app.route('/reportsubmit', methods=['GET', 'POST'])
def reportsubmit():
    if request.method == 'POST':
        # Handle submitted data
        data = request.form.to_dict() if request.form else request.get_json()
        
        incident_type = data.get("incident_type")
        severity = data.get("severity")
        description = data.get("description")
        date_time = data.get("date_time")
        reporter_name = data.get("reporter_name")
        reporter_email = data.get("reporter_email")

        send_incident_report(
            incident_type, severity, description, date_time, reporter_name, reporter_email
        )

        return render_template("reportsubmit.html", success=True)

    # If GET request → show the form
    return render_template("reportsubmit.html")



@app.route('/settings', methods=['GET'])
def settings():
    return render_template('settings.html')


@app.route('/settings/profile', methods=['POST'])
def save_profile_settings():
    username = request.form.get("username")
    email = request.form.get("email")
    phone = request.form.get("phone")

    user = UserSettings.query.filter_by(email=email).first()
    if user:
        user.username = username
        user.phone = phone
    else:
        user = UserSettings(username=username, email=email, phone=phone, user_id=session.get("user_id"))
        db.session.add(user)

    db.session.commit()
    return redirect(url_for('settings') + "#profile-settings")


@app.route('/settings/security', methods=['POST'])
def save_security_settings():
    email = request.form.get("email")   # identify user
    password = request.form.get("password")
    twofa = request.form.get("twofa")

    user = UserSettings.query.filter_by(email=email).first()
    if user:
        user.password = bcrypt.generate_password_hash(password).decode("utf-8") if password else user.password
        user.twofa = twofa
        db.session.commit()

    return redirect(url_for('settings') + "#security-settings")


@app.route('/settings/notifications', methods=['POST'])
def save_notifications_settings():
    email = request.form.get("email")  # identify user
    email_alerts = request.form.get("email_alerts")
    sms_alerts = request.form.get("sms_alerts")
    frequency = request.form.get("frequency")

    user = UserSettings.query.filter_by(email=email).first()
    if user:
        user.email_alerts = email_alerts
        user.sms_alerts = sms_alerts
        user.frequency = frequency
        db.session.commit()

    return redirect(url_for('settings') + "#notifications-settings")


@app.route('/settings/download', methods=['POST'])
def download_data():
    print("Download data requested")
    return redirect(url_for('settings') + "#data-privacy-settings")


@app.route('/settings/delete', methods=['POST'])
def delete_account():
    email = request.form.get("email")  # Identify user
    
    user = UserSettings.query.filter_by(email=email).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        print("Account deleted:", email)
    
    return redirect(url_for('settings'))


@app.route('/settings/support', methods=['GET'])
def contact_support():
    return redirect(url_for('settings') + "#help-support")


@app.route('/settings/faqs', methods=['GET'])
def view_faqs():
    return redirect(url_for('settings') + "#help-support")


@app.route('/blog')
def blog():
    return render_template('blog.html')


# --------------------- MAIN ---------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
