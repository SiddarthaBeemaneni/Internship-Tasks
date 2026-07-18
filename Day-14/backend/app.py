"""
app.py
TicketSense - AI-assisted support ticket triage.
Flask application entry point: page routes + JSON API.
"""
import os
import re
import random
import string
import secrets
from functools import wraps

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

import database
import ml_predictor

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
database.init_db()

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MAX_TEXT_LEN = 5000
MAX_NAME_LEN = 120


def generate_ticket_ref():
    return "TS-" + "".join(random.choices(string.digits, k=6))


def is_valid_email(value):
    return bool(value) and bool(EMAIL_RE.match(value))


# ------------------------------------------------------------------ auth ----

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if session.get("user_id"):
        return redirect(url_for("home"))

    if request.method == "GET":
        return render_template("signup.html")

    try:
        data = request.get_json(silent=True) or request.form
        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""
        confirm = data.get("confirm_password") or ""

        errors = {}
        if not name or len(name) < 2:
            errors["name"] = "Please enter your full name."
        elif len(name) > MAX_NAME_LEN:
            errors["name"] = "Name is too long."

        if not is_valid_email(email):
            errors["email"] = "Enter a valid email address."

        if not password or len(password) < 8:
            errors["password"] = "Password must be at least 8 characters."

        if password != confirm:
            errors["confirm_password"] = "Passwords do not match."

        if not errors and database.get_user_by_email(email):
            errors["email"] = "An account with this email already exists."

        if errors:
            return jsonify({"error": "Please fix the highlighted fields.", "fields": errors}), 400

        password_hash = generate_password_hash(password)
        user_id = database.create_user(name, email, password_hash)
        session["user_id"] = user_id
        session["user_name"] = name
        return jsonify({"ok": True, "redirect": url_for("home")}), 201

    except Exception:
        app.logger.exception("Signup failed")
        return jsonify({"error": "Something went wrong creating your account. Please try again."}), 500


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("home"))

    if request.method == "GET":
        return render_template("login.html")

    try:
        data = request.get_json(silent=True) or request.form
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""

        if not is_valid_email(email) or not password:
            return jsonify({"error": "Enter a valid email and password."}), 400

        user = database.get_user_by_email(email)
        if not user or not check_password_hash(user["password_hash"], password):
            return jsonify({"error": "Incorrect email or password."}), 401

        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        return jsonify({"ok": True, "redirect": url_for("home")}), 200

    except Exception:
        app.logger.exception("Login failed")
        return jsonify({"error": "Something went wrong signing you in. Please try again."}), 500


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------------------------------------------------------- pages ----

@app.route("/")
@login_required
def home():
    return render_template("index.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


# ------------------------------------------------------------------ API ----

@app.route("/api/tickets", methods=["POST"])
@login_required
def create_ticket():
    try:
        data = request.get_json(silent=True) or request.form
        subject = (data.get("subject") or "").strip()
        body = (data.get("body") or "").strip()
        name = (data.get("name") or "").strip()[:MAX_NAME_LEN]
        email = (data.get("email") or "").strip()

        if not name or len(name) < 2:
            return jsonify({"error": "Please enter your name."}), 400
        if not email or not is_valid_email(email):
            return jsonify({"error": "Please enter a valid email address."}), 400
        if not subject:
            return jsonify({"error": "Subject is required."}), 400
        if not body:
            return jsonify({"error": "Please describe the issue."}), 400
        if len(body) < 10:
            return jsonify({"error": "Please describe the issue in a bit more detail (at least 10 characters)."}), 400
        if len(subject) > MAX_TEXT_LEN or len(body) > MAX_TEXT_LEN:
            return jsonify({"error": f"Please keep each field under {MAX_TEXT_LEN} characters."}), 400

        try:
            prediction = ml_predictor.predict(subject, body)
        except ValueError as ve:
            app.logger.warning("Prediction ValueError: %s", ve)
            return jsonify({"error": "Couldn't analyze that input. Please rephrase and try again."}), 422
        except Exception:
            app.logger.exception("Prediction failed")
            return jsonify({"error": "The prediction model is temporarily unavailable. Please try again shortly."}), 503

        ticket_ref = generate_ticket_ref()

        try:
            database.insert_ticket(
                ticket_ref=ticket_ref,
                user_id=session["user_id"],
                customer_name=name,
                customer_email=email,
                subject=subject,
                body=body,
                language=prediction.get("language"),
                predicted_queue=prediction.get("queue"),
                predicted_priority=prediction.get("priority"),
                predicted_type=prediction.get("type"),
            )
        except Exception:
            app.logger.exception("Failed to save ticket")
            return jsonify({"error": "Your ticket was analyzed but couldn't be saved. Please try again."}), 500

        return jsonify({
            "ticket_ref": ticket_ref,
            "prediction": prediction,
        }), 201

    except Exception:
        app.logger.exception("Unexpected error creating ticket")
        return jsonify({"error": "Something unexpected went wrong. Please try again."}), 500


@app.route("/api/tickets", methods=["GET"])
@login_required
def list_tickets():
    try:
        tickets = database.get_all_tickets(
            user_id=session["user_id"],
            status=request.args.get("status"),
            queue=request.args.get("queue"),
            priority=request.args.get("priority"),
            search=request.args.get("q"),
        )
        return jsonify(tickets)
    except Exception:
        app.logger.exception("Failed to list tickets")
        return jsonify({"error": "Couldn't load tickets right now. Please try again."}), 500


@app.route("/api/tickets/<ticket_ref>/status", methods=["PATCH"])
@login_required
def change_status(ticket_ref):
    try:
        data = request.get_json(silent=True) or {}
        status = data.get("status")
        if status not in ("open", "in_progress", "resolved"):
            return jsonify({"error": "Invalid status."}), 400
        ok = database.update_ticket_status(ticket_ref, session["user_id"], status)
        if not ok:
            return jsonify({"error": "Ticket not found."}), 404
        return jsonify({"ok": True})
    except Exception:
        app.logger.exception("Failed to update ticket status")
        return jsonify({"error": "Couldn't update the ticket status. Please try again."}), 500


@app.route("/api/stats", methods=["GET"])
@login_required
def stats():
    try:
        return jsonify(database.get_stats(session["user_id"]))
    except Exception:
        app.logger.exception("Failed to load stats")
        return jsonify({"error": "Couldn't load stats right now."}), 500


@app.route("/api/contact", methods=["POST"])
@login_required
def contact():
    try:
        data = request.get_json(silent=True) or request.form
        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip()
        message = (data.get("message") or "").strip()
        if not name or not email or not message:
            return jsonify({"error": "All fields are required."}), 400
        if not is_valid_email(email):
            return jsonify({"error": "That email address doesn't look right."}), 400
        if len(message) > MAX_TEXT_LEN:
            return jsonify({"error": f"Message must be under {MAX_TEXT_LEN} characters."}), 400
        database.insert_contact_message(name, email, message)
        return jsonify({"ok": True})
    except Exception:
        app.logger.exception("Failed to save contact message")
        return jsonify({"error": "Couldn't send your message. Please try again."}), 500


# --------------------------------------------------------- error handlers ----

@app.errorhandler(404)
def not_found(e):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Not found."}), 404
    return render_template("error.html", code=404,
                            message="We couldn't find that page."), 404


@app.errorhandler(500)
def server_error(e):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Internal server error. Please try again."}), 500
    return render_template("error.html", code=500,
                            message="Something went wrong on our end."), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
