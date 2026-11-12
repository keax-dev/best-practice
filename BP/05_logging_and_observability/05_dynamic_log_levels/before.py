# Tema: el nivel queda fijado dentro de la operación.
import logging

def configure(logger: logging.Logger) -> None:
    logger.setLevel(logging.INFO)

if __name__ == "__main__":
    logger = logging.getLogger("fixed")
    configure(logger)
    print(logger.isEnabledFor(logging.DEBUG))
