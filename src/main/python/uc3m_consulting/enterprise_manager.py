"""Module """
import json
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

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
        try:
            with open(input_file, encoding="utf-8") as json_file:
                document_data = json.load(json_file)
        except FileNotFoundError as exc:
            raise EnterpriseManagementException(f"The input file does not exist") from exc
        
        except json.JSONDecodeError as exc:
            raise EnterpriseManagementException(f"The file is not JSON formatted") from exc
        
        if "PROJECT_ID" not in document_data or "FILENAME" not in document_data:
            raise EnterpriseManagementException("JSON does not have the expected structure") from exc
        
        filename = document_data["FILENAME"]
        valid_extensions = ('.pdf', '.docx', '.xlsx')
        if not (len(filename) == 12 and filename[:8].isalnum() and filename.endswith(valid_extensions)):
            raise EnterpriseManagementException("JSON data has no valid values") from exc
        
        return 
        
