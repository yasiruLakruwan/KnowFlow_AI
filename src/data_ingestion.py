from utils.embeding_model import *
from config.path_config import *
from logger import get_logger

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self,data_path):
        self.data_path = data_path
        