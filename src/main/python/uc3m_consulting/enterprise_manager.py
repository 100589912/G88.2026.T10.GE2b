"""Module """
import json
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.project_document import ProjectDocument
class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_cif(cif: str):
        """RETURNs TRUE IF THE IBAN RECEIVED IS VALID SPANISH IBAN,
        OR FALSE IN OTHER CASE"""

        return True

    @staticmethod
    def register_document(input_file: str):

        def is_hex(val):
                try:
                    int(val, 16)
                    return True
                except ValueError:
                    return False
        
        try:
            with open(input_file, encoding="utf-8") as json_file:
                document_data = json.load(json_file)
        except FileNotFoundError as exc:
            raise EnterpriseManagementException(f"The input file does not exist") 
        
        except json.JSONDecodeError as exc:
            raise EnterpriseManagementException(f"The file is not JSON formatted")
        
        if "PROJECT_ID" not in document_data or "FILENAME" not in document_data:
            raise EnterpriseManagementException("JSON does not have the expected structure")
        
        filename = document_data["FILENAME"]
        project_id = document_data["PROJECT_ID"]
        valid_extensions = ('.pdf', '.docx', '.xlsx')

        #checks following params:
        # project_id is a hex string
        # project_id is 32 chars
        # filename is 8 characters and are nums or letters
        # filename ends with valid extension
        if not (is_hex(project_id) and len(project_id) == 32 and filename[:8].isalnum() and filename.endswith(valid_extensions) and filename[8] == "."):
            raise EnterpriseManagementException("JSON data has no valid values") 
        
        project = ProjectDocument(project_id, filename)
        try:
            signature = project.document_signature
        except: # This is a catch-all for any unexpected exceptions during signature generation
            raise EnterpriseManagementException("Internal processing error when getting the file_signature")
        with open(filename, "w", encoding="utf-8") as json_file: #output as filename
            json_file.write(filename + " , " + project_id + " , " + signature)

        return signature, filename
        
