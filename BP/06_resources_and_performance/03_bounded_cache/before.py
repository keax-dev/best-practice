# Tema: una caché sin límite puede crecer con todas las claves recibidas.
if __name__ == "__main__":
    cache = {}
    for index in range(5):
        cache[index] = f"Product {index}"
    print(f"Items retained: {len(cache)}")
