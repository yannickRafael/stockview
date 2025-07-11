import os

class Config():
    PROJECT_ID = os.getenv('PROJECT_ID') 
    LOCATION = os.getenv('LOCATION') 
    PROCESSOR_ID = os.getenv('PROCESSOR_ID') 
    FILE_PATH = os.getenv('FILE_PATH') 
    MIME_TYPE = os.getenv('MIME_TYPE') 