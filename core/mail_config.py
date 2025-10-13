from fastapi_mail import ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="55ed41e16d27f5",
    MAIL_PASSWORD="9e00a5ffb301e4",
    MAIL_FROM="noreply@example.com",
    MAIL_PORT=2525,
    MAIL_SERVER="sandbox.smtp.mailtrap.io",
    MAIL_STARTTLS=True,   # en lugar de MAIL_TLS
    MAIL_SSL_TLS=False,   # en lugar de MAIL_SSL
    USE_CREDENTIALS=True
)