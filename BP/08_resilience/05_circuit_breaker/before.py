# Tema: sin protección se insiste en una dependencia que ya está fallando.
def unavailable() -> str:
    raise ConnectionError("Unavailable")

if __name__ == "__main__":
    for attempt in range(4):
        try:
            unavailable()
        except ConnectionError:
            print(f"Remote call failed: {attempt + 1}")
