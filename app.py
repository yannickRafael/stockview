from document_processor import DocumentProcessor
from config import Config as c


if __name__=='__main__':
    dp = DocumentProcessor(auto_process=True, file_path=c.FILE_PATH)
    dp.save_blocks("blocos.xlsx")
    dp.save_blocks("blocos.json")

    dp.save_tables(output_dir="tabelas", format="xlsx")