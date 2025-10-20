from fastapi_mail import ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="a61e0fb05fe903",
    MAIL_PASSWORD="2cfaa939562a58",
    MAIL_FROM="noreply@example.com",
    MAIL_PORT=2525,
    MAIL_SERVER="sandbox.smtp.mailtrap.io",
    MAIL_STARTTLS=True,   # en lugar de MAIL_TLS
    MAIL_SSL_TLS=False,   # en lugar de MAIL_SSL
    USE_CREDENTIALS=True
)