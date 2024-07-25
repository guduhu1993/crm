import reflex as rx

config = rx.Config(
    app_name="reflex_crm",
    frontend_port="3000",
    api_url = "http://localhost:8000",
    db_url = "postgresql://postgres:123456@localhost:5432/crm"
)