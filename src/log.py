import logging

open("hist.log", "w").close()
logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("hist.log")
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.ERROR)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

def historical(func):
    def wrapper(*args, **kwargs):
        logger.debug(f"PC: {args[0].program_counter} A: {args[0].register_a} X: {args[0].register_x} Y: {args[0].register_y} P: {args[0].status}")
        logger.debug(f"Calling: {func.__name__}")
        func(*args, **kwargs)
        logger.debug(f"PC: {args[0].program_counter} A: {args[0].register_a} X: {args[0].register_x} Y: {args[0].register_y} P: {args[0].status}")
    return wrapper
