# Tema: el nivel configurado decide qué mensajes se publican.
import logging


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    logger = logging.getLogger("orders")
    logger.debug("Inspecting order")
    logger.info("Order created")
    logger.warning("Response is slow")


if __name__ == "__main__":
    main()
