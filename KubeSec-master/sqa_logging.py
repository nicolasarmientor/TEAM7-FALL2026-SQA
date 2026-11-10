# Import libraries
import functools
import logging
import time
import uuid
from pathlib import Path


logger = logging.getLogger("sqa.forensics")
logger.setLevel(logging.INFO)
logger.propagate = False


def configure_logging(log_path="evidence/forensics.log"):
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()

    handler = logging.FileHandler(path, encoding="utf-8")
    formatter = logging.Formatter(
        "%(asctime)sZ %(levelname)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S"
    )
    formatter.converter = time.gmtime
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def forensic_log(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        call_id = uuid.uuid4().hex
        started = time.perf_counter()

        logger.info(
            "event=start method=%s call_id=%s",
            function.__name__,
            call_id
        )

        try:
            result = function(*args, **kwargs)
        except Exception as error:
            logger.error(
                "event=error method=%s call_id=%s exception=%s",
                function.__name__,
                call_id,
                type(error).__name__
            )
            raise

        logger.info(
            "event=complete method=%s call_id=%s elapsed_ms=%.3f",
            function.__name__,
            call_id,
            (time.perf_counter() - started) * 1000
        )
        return result

    return wrapper


def forensic_generator_log(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        call_id = uuid.uuid4().hex
        started = time.perf_counter()

        logger.info(
            "event=start method=%s call_id=%s",
            function.__name__,
            call_id
        )

        try:
            yield from function(*args, **kwargs)
        except GeneratorExit:
            logger.info(
                "event=closed method=%s call_id=%s",
                function.__name__,
                call_id
            )
            raise
        except Exception as error:
            logger.error(
                "event=error method=%s call_id=%s exception=%s",
                function.__name__,
                call_id,
                type(error).__name__
            )
            raise
        else:
            logger.info(
                "event=complete method=%s call_id=%s elapsed_ms=%.3f",
                function.__name__,
                call_id,
                (time.perf_counter() - started) * 1000
            )
            
    return wrapper