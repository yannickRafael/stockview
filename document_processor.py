from google.cloud import documentai_v1 as documentai
from config import Config as c
import pandas as pd
import json
from pathlib import Path


class DocumentProcessor:
    def __init__(self, file_path=None):
        self.file_path = file_path or c.FILE_PATH
        self.client = documentai.DocumentProcessorServiceClient(
            client_options={"api_endpoint": f"{c.LOCATION}-documentai.googleapis.com"}
        )
        self.name = f"projects/{c.PROJECT_ID}/locations/{c.LOCATION}/processors/{c.PROCESSOR_ID}"
        self.document = None

    def load_file(self):
        with open(self.file_path, "rb") as file:
            return file.read()

    def process_document(self):
        raw_document = documentai.RawDocument(
            content=self.load_file(),
            mime_type=c.MIME_TYPE
        )
        request = documentai.ProcessRequest(
            name=self.name,
            raw_document=raw_document
        )
        result = self.client.process_document(request=request)
        self.document = result.document
        return self.document

    def extract_blocks(self):
        if not self.document:
            raise ValueError("Documento não processado. Use `.process_document()` primeiro.")
        blocks = []
        for page in self.document.pages:
            for block in page.blocks:
                for segment in block.layout.text_anchor.text_segments:
                    text = self.document.text[segment.start_index:segment.end_index]
                    blocks.append(text.strip())
        return blocks

    def save_blocks(self, output_path="blocos.json"):
        blocks = self.extract_blocks()
        if output_path.endswith(".json"):
            with open(output_path, "w") as f:
                json.dump(blocks, f, indent=2, ensure_ascii=False)
        elif output_path.endswith(".xlsx"):
            df = pd.DataFrame(blocks, columns=["Bloco"])
            df.to_excel(output_path, index=False)
        else:
            raise ValueError("Formato não suportado. Use .json ou .xlsx")

    def extract_tables(self):
        if not self.document:
            raise ValueError("Documento não processado. Use `.process_document()` primeiro.")
        tables = []

        for page in self.document.pages:
            for table in page.tables:
                rows = []
                for row in table.header_rows + table.body_rows:
                    row_data = []
                    for cell in row.cells:
                        segments = cell.layout.text_anchor.text_segments
                        cell_text = "".join([
                            self.document.text[seg.start_index:seg.end_index] for seg in segments
                        ]).strip()
                        row_data.append(cell_text)
                    rows.append(row_data)
                tables.append(rows)

        return tables

    def save_tables(self, output_dir="tabelas", format="xlsx"):
        tables = self.extract_tables()
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        for i, table in enumerate(tables):
            df = pd.DataFrame(table)
            path = Path(output_dir) / f"tabela_{i+1}.{format}"
            if format == "xlsx":
                df.to_excel(path, index=False, header=False)
            elif format == "json":
                df.to_json(path, orient="records", indent=2, force_ascii=False)
            else:
                raise ValueError("Formato não suportado. Use 'xlsx' ou 'json'.")

        return f"{len(tables)} tabelas salvas em {output_dir}/"
