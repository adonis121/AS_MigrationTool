import logging

# Configure the logging module
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def write_log(log_level, log_message):
    if log_level == 'Verbose':
        logging.debug(log_message)
    elif log_level == 'Error':
        logging.error(log_message)
    else:
        logging.info(log_message)

def write_verbose(message):
    write_log('Verbose', message)

def write_error(message):
    write_log('Error', message)

# Example usage
if __name__ == "__main__":
    write_verbose("This is a verbose message")
    write_error("This is an error message")
