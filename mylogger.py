import logging
import time
import os

current_date = time.strftime('%d_%m_%Y')
log_file_name = 'logs/ytgrabber.log'
logs_path_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')

if not os.path.isdir(logs_path_dir):
    os.makedirs(logs_path_dir)

logging.basicConfig(filename=log_file_name, filemode='w', format='%(asctime)s | %(levelname)s - %(message)s', level=logging.INFO)

if __name__ == '__main__':
    logging.info("YTGrabber logger working.")
