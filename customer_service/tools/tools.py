# In customer_service/tools.py

import docx

def generate_document(document_content: str, file_name: str = "meeting_summary.docx") -> str:
    """
    Generates a .docx Word document with the given content.
    
    Args:
        document_content: The text to be placed in the document.
        file_name: The name of the file to be saved (e.g., 'summary.docx').
    
    Returns:
        A confirmation message with the name of the file created.
    """
    try:
        document = docx.Document()
        document.add_heading('Meeting Summary', level=1)
        
        # Add the content as a paragraph
        document.add_paragraph(document_content)
        
        document.save(file_name)
        
        return f"Successfully created the document: {file_name}"
    except Exception as e:
        return f"Error creating document: {e}"
