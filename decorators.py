import time
from datetime import datetime


def runtime(func):
    """
    This decorator prints out the runtime of a function.
    Example:
        @runtime
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time() - start
        print(f"'{func.__name__}' function runtime was {end} seconds")
        return result
    return wrapper


def retry(max_retries: int = 5, timeout: int = 0):
    """
    This decorator tries to run the same command if it raises an exception for several times with timeout.
    Parameters:
        max_retries: int = 5    (Number of tries)
        timeout: int = 0        (Timeout between tries in seconds)
    Example:
        @retry(max_retries = 3, timeout = 3)
        @retry()
    """
    def decorator_function(func):
        def wrapper(*args, **kwargs):
            retry_count = 0

            while retry_count <= max_retries:
                try:
                    result = func(*args, **kwargs)
                    break
                except Exception as e:
                    retry_count += 1
                    if retry_count <= max_retries:
                        print(f"Retry attempt {retry_count} due to error: {e}")
                        time.sleep(timeout)
                    else:
                        raise
            return result
        return wrapper
    return decorator_function


def log(func):
    """
    This decorator creates a log.txt file and prints out the arguments, results and the exceptions with timestamp.
    It is recommended to use this decorator as the innermost decorator.
    Example:
        @log
    """
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("log.txt", "a") as file:
                file.write(f"[{timestamp}] Function {func.__name__} called with arguments: {args} {kwargs}\n")
                file.write(f"[{timestamp}] Result: {result}\n")
            return result
        except Exception as e:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("log.txt", "a") as file:
                file.write(f"[{timestamp}] Function {func.__name__} called with arguments: {args} {kwargs}\n")
                file.write(f"[{timestamp}] Function {func.__name__} raised an exception: {str(e)}\n")
            raise
    return wrapper
