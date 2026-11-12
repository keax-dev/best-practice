# Tema: incluso una credencial ficticia muestra el patrón de hardcode que debe evitarse.
DEMO_TOKEN = "demo-only-not-a-real-token"

def connect() -> str:
    return f"Using token: {DEMO_TOKEN}"

if __name__ == "__main__":
    print(connect())
