# Tema: un cambio explícito y validado controla el nivel en ejecución.
import logging


def set_log_level(logger: logging.Logger, name: str) -> None:
    levels = {"DEBUG": logging.DEBUG, "INFO": logging.INFO, "WARNING": logging.WARNING, "ERROR": logging.ERROR}
    if name not in levels:
        raise ValueError("Unsupported log level")
    logger.setLevel(levels[name])


if __name__ == "__main__":
    logger = logging.getLogger("dynamic")
    set_log_level(logger, "INFO")
    print(logger.isEnabledFor(logging.DEBUG))
    set_log_level(logger, "DEBUG")
    print(logger.isEnabledFor(logging.DEBUG))
