# Tema: el caso de uso conoce una herramienta concreta de correo.
class EmailClient:
    def deliver_email(self, text: str) -> str:
        return f"Email: {text}"

def confirm_order(order_id: str) -> str:
    return EmailClient().deliver_email(f"Confirmed {order_id}")

if __name__ == "__main__":
    print(confirm_order("order-1"))
