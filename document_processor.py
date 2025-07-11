from google.cloud import documentai_v1 as documentai
from config import Config as c

class Document_Processor():
    # === CLIENTE ===
    client = documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{c.LOCATION}-documentai.googleapis.com"}
    )

    # Caminho completo do processador
    name = f"projects/{c.PROJECT_ID}/locations/{c.LOCATION}/processors/{c.PROCESSOR_ID}"

    # Lê o conteúdo binário do PDF
    with open(c.FILE_PATH, "rb") as file:
        file_content = file.read()

    # Cria um RawDocument
    raw_document = documentai.RawDocument(
        content=file_content,
        mime_type=c.MIME_TYPE
    )

    # Cria o request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document
    )

    # Faz o processamento
    result = client.process_document(request=request)

    # Extrai o documento processado
    document = result.document

    # === EXEMPLO: listar blocos de texto detectados ===
    for page in document.pages:
        for block in page.blocks:
            text = document.text[block.layout.text_anchor.text_segments[0].start_index:
                                block.layout.text_anchor.text_segments[0].end_index]
            print("Bloco:", text.strip())
