# Tema: mezclar salud del proceso y dependencia produce reinicios innecesarios.
def liveness(database_ready: bool) -> bool:
    return database_ready

if __name__ == "__main__":
    print(f"Live while dependency unavailable: {liveness(False)}")
