import logging
from typing import Optional

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Email, To, Content, Mail, HtmlContent

from app.core.config import settings

logger = logging.getLogger(__name__)


def send_verification_email(email: str, verification_token: str) -> bool:
    verify_url = f"{settings.APP_URL}/auth/verify-email?token={verification_token}"

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2>Verify Your Email</h2>
        <p>Thank you for registering! Please click the button below to verify your email address:</p>
        <a href="{verify_url}" style="background-color: #4CAF50; color: white; padding: 12px 24px; 
           text-decoration: none; border-radius: 4px; display: inline-block; margin: 16px 0;">
            Verify Email
        </a>
        <p>Or copy and paste this link: {verify_url}</p>
        <p>This link expires in 1 hour.</p>
        <hr>
        <p style="color: #666; font-size: 12px;">If you didn't create an account, please ignore this email.</p>
    </body>
    </html>
    """

    plain_content = f"""
    Verify Your Email
    
    Thank you for registering! Please click the link below to verify your email address:
    {verify_url}
    
    This link expires in 1 hour.
    
    If you didn't create an account, please ignore this email.
    """

    return _send_email(email, "Verify Your Email", html_content, plain_content)


def send_password_reset_email(email: str, reset_token: str) -> bool:
    reset_url = f"{settings.APP_URL}/auth/reset-password?token={reset_token}"

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2>Reset Your Password</h2>
        <p>You requested a password reset. Click the button below to reset your password:</p>
        <a href="{reset_url}" style="background-color: #f44336; color: white; padding: 12px 24px; 
           text-decoration: none; border-radius: 4px; display: inline-block; margin: 16px 0;">
            Reset Password
        </a>
        <p>Or copy and paste this link: {reset_url}</p>
        <p>This link expires in 1 hour.</p>
        <hr>
        <p style="color: #666; font-size: 12px;">If you didn't request a password reset, please ignore this email.</p>
    </body>
    </html>
    """

    plain_content = f"""
    Reset Your Password
    
    You requested a password reset. Click the link below to reset your password:
    {reset_url}
    
    This link expires in 1 hour.
    
    If you didn't request a password reset, please ignore this email.
    """

    return _send_email(email, "Reset Your Password", html_content, plain_content)


def _send_email(
    to_email: str, subject: str, html_content: str, plain_content: str
) -> bool:
    if not settings.SENDGRID_API_KEY or not settings.SENDGRID_API_KEY.startswith("SG."):
        logger.info(
            f"Email delivery disabled. Recipient: {to_email}, Subject: {subject}"
        )
        return True

    try:
        message = Mail(
            from_email=Email(settings.SENDGRID_FROM_EMAIL),
            to_emails=To(to_email),
            subject=subject,
            html_content=HtmlContent(html_content),
            content=Content("text/plain", plain_content),
        )

        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)

        logger.info(f"Email sent to {to_email}. Status code: {response.status_code}")
        return response.status_code in [200, 201, 202]

    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return False
