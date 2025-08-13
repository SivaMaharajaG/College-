from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required
from ..models import User
from ..extensions import db, mail
import pyotp
from flask_mail import Message
from .forms import LoginForm, OTPForm

auth_bp = Blueprint("auth", __name__, template_folder="../templates/auth")

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            if user.twofa_secret:
                session["pre_2fa_user_id"] = user.id
                totp = pyotp.TOTP(user.twofa_secret)
                otp = totp.now()
                if user.email:
                    try:
                        msg = Message("Your OTP", recipients=[user.email], body=f"Your OTP: {otp}")
                        mail.send(msg)
                    except Exception:
                        pass
                return redirect(url_for(".twofa"))
            login_user(user)
            return redirect(url_for("index"))
        flash("Invalid credentials", "danger")
    return render_template("auth/login.html", form=form)

@auth_bp.route("/twofa", methods=["GET","POST"])
def twofa():
    uid = session.get("pre_2fa_user_id")
    if not uid:
        return redirect(url_for(".login"))
    user = User.query.get(uid)
    form = OTPForm()
    if form.validate_on_submit():
        totp = pyotp.TOTP(user.twofa_secret)
        if totp.verify(form.token.data):
            login_user(user)
            session.pop("pre_2fa_user_id", None)
            return redirect(url_for("index"))
        flash("Invalid or expired OTP", "danger")
    return render_template("auth/twofa.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for(".login"))
