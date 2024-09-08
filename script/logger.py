import logging

# Configuração básica do logging
logging.basicConfig(filename='email_checker.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log(message):
    logging.info(message)
