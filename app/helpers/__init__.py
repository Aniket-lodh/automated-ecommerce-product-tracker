from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import secrets
import time
import traceback
from typing import Any, Optional, Union
from urllib import response
from fastapi import HTTPException, Response
from pydantic import InstanceOf
from sqlalchemy import or_
from sqlalchemy.orm import Session
from crud.users import get_user
import models
import pytz
from crud.schemas import UsersSessionReqModel
import smtplib
import jwt

SECRET_KEY = os.getenv("SECRECT_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")


def generate_secure_otp():
    """Generate cryptographical 4 digit otp"""
    otp = secrets.randbelow(9000) + 1000
    return otp


def is_otp_expired(timestamp, expiry_minutes=10):
    if not isinstance(timestamp, datetime):
        raise ValueError("Timestamp must be a datetime object")

    current_time = datetime.now(timezone.utc)

    if timestamp.tzinfo is None:
        raise ValueError("Timestamp must include timezone information")

    time_diff = current_time - timestamp

    print(f"Expired: {time_diff > timedelta(minutes=expiry_minutes)}")

    return time_diff > timedelta(minutes=expiry_minutes)


def fetch_otp(user_id: int, otp: int, db: Session):
    try:
        matched_otp = (
            db.query(models.UsersSession)
            .filter(
                models.UsersSession.user_id == user_id,
                models.UsersSession.generated_otp == otp,
            )
            .first()
        )
        return matched_otp
    except Exception as e:
        raise Exception(str(e))


def confirm_otp(request_body: UsersSessionReqModel, db: Session):
    try:
        existing_user = get_user(db=db, searchEmail=request_body.user_email)
        if existing_user is None:
            raise Exception("User doesnot exist with the provided email!")

        verified_otp = fetch_otp(existing_user.id, request_body.generated_otp, db)
        if verified_otp is None:
            raise Exception("Invalid otp or user!")
        elif verified_otp.verified_at is not None:
            raise Exception("Otp is no longer valid!")

        otp_expired = is_otp_expired(verified_otp.created_at)
        if otp_expired:
            raise Exception("Otp expired, please try again!")

        verified_otp.verified_at = datetime.now(pytz.utc)
        existing_user.verified_at = datetime.now(pytz.utc)
        existing_user.updated_at = datetime.now(pytz.utc)
        existing_user.logged_in = True
        verified_otp.verified = True

        db.commit()
        db.refresh(verified_otp)
        db.refresh(existing_user)

        token = create_jwt(existing_user, expires_delta=timedelta(hours=1))

        return token
    except Exception as e:
        db.rollback()
        raise Exception(str(e))


def insert_otp(user: models.Users, db: Session):
    try:
        start = time.time()
        inserted_otp = models.UsersSession(
            user_id=user.id, generated_otp=generate_secure_otp()
        )

        email_sent = email_otp(email=user.email, otp=inserted_otp.generated_otp)
        if not email_sent:
            raise Exception("Could not send email otp!")

        db.add(inserted_otp)
        db.commit()
        db.refresh(inserted_otp)
        print(f"time taken {time.time() - start}")
        return inserted_otp
    except Exception as e:
        db.rollback()
        raise Exception(str(e))


def email_otp(email: str, otp: int):
    try:
        otp_expiration_time = (datetime.now() + timedelta(minutes=10)).strftime(
            "%H:%M %p"
        )

        msg = MIMEMultipart()
        msg["From"] = f"{os.getenv('PRODUCT_NAME')} <{os.getenv('SMTP_SENDER_EMAIL')}>"
        msg["To"] = email
        msg["Subject"] = (
            f"{os.getenv('PRODUCT_NAME')}: OTP for Your Login/Signup Request"
        )

        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.5;">
            <div style="max-width: 600px; margin: 0 auto; border: 1px solid #ddd; padding: 20px; border-radius: 8px;">
                <h1 style="color: #007BFF; text-align: center;">{os.getenv('PRODUCT_NAME')}</h1>
                <p>Dear User,</p>
                <p>We received a request to log in to your <strong>{os.getenv('PRODUCT_NAME')}</strong> account. Your One-Time Password (OTP) is:</p>
                <h2 style="text-align: center; color: #007BFF;">{otp}</h2>
                <p>This OTP is valid until <strong>{otp_expiration_time}</strong>. Please use it to complete your login or signup process.</p>
                <p>If you did not request this, please ignore this email.<br>For assistance, you can reach out to me at <a href="mailto:{os.getenv("SMTP_SENDER_EMAIL")}">dev.aniketlodh@gmail.com</a>.</p>
                <br>
                <p>Best regards,<br>Aniket Lodh,<br><strong>Creator of {os.getenv('PRODUCT_NAME')}</strong></p>
                <hr>
                <footer style="font-size: 0.9em; text-align: center; color: #666;">
                    <p>&copy; {datetime.now().year} {os.getenv('PRODUCT_NAME')}. All rights reserved.</p>
                </footer>
            </div>  
        </body>
        </html>
        """

        part = MIMEText(html_content, "html")
        msg.attach(part)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            sender_email = os.getenv("SMTP_SENDER_EMAIL")
            app_password = os.getenv("SMTP_APP_PASSWORD")
            server.login(sender_email, app_password)

            server.sendmail(msg["From"], msg["To"], msg.as_string())

        return True

    except Exception as e:
        print(f"Error sending OTP email: {e}")
        return False


def create_jwt(data: Union[dict, Any], expires_delta: timedelta):
    """Creates a JWT token with an expiration time."""
    if not isinstance(data, dict):
        payload = {
            "user_id": data.id,
            "email": data.email,
            "verified_at": str(data.verified_at),
            "logged_in": data.logged_in,
            "email_verified": data.email_verified,
        }
    else:
        payload = data

    expire = datetime.utcnow() + expires_delta
    payload.update({"exp": expire})
    return jwt.encode(payload=payload, algorithm=ALGORITHM, key=SECRET_KEY)


def set_cookie(
    response: Response, key: str, value: str, max_age: int = 3600, path: str = "/"
):
    """Sets a cookie based on the environment (development or production)."""
    if ENVIRONMENT == "production":
        response.set_cookie(
            key=key,
            value=value,
            httponly=True,
            secure=True,
            samesite="Strict",
            max_age=max_age,
            path=path,
        )
    else:
        response.set_cookie(
            key=key,
            value=value,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=max_age,
            path=path,
        )
