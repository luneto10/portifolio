# app/utils/logger.py
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a stream handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

# Create a formatter and add it to the handler
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
stream_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(stream_handler)
