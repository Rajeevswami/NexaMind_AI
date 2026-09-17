import logging
import sys

def configure_logging() -> None:
    logging.basicConfig(level=logging.DEBUG if __import__('app.core.config', fromlist=['settings']).settings.debug else logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s", stream=sys.stdout)

