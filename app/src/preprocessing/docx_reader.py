from docx import Document


class DocxReader:
    def __init__(self) -> None:
        pass

    def read_docx(self, file_path):
        """Read DOCX file and return the text."""
        try:
            doc = Document(file_path)

            # Read the contents
            content = []
            for paragraph in doc.paragraphs:
                content.append(paragraph.text)

            # Join the paragraphs
            return "\n".join(content)
        except Exception as e:
            raise e
