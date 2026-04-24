"""class for testing the regsiter_order method"""
import json
import os
import tempfile
import unittest
import hashlib
from uc3m_consulting import EnterpriseManager, EnterpriseManagementException

class MyTestCase(unittest.TestCase):
    """class for testing the register_order method"""

    def test_TC_SYN_01_valid_json_pdf(self):
        """TC_SYN_01: valid JSON - pdf"""
        data = {"PROJECT_ID": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4", "FILENAME": "myFile01.pdf"}
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test01.json")
            with open(file_path, "w", encoding="utf-8") as fp:
                json.dump(data, fp)

            signature, filename = EnterpriseManager.register_document(file_path)

        self.assertEqual(filename, "myFile01.pdf")
        self.assertIsInstance(signature, str)
        self.assertGreater(len(signature), 0)

    def test_TC_SYN_02_valid_json_docx(self):
        """TC_SYN_02: valid JSON - docx"""
        data = {"PROJECT_ID": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4", "FILENAME": "myFile01.docx"}
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test02.json")
            with open(file_path, "w", encoding="utf-8") as fp:
                json.dump(data, fp)

            signature, filename = EnterpriseManager.register_document(file_path)

        self.assertEqual(filename, "myFile01.docx")
        self.assertIsInstance(signature, str)

    def test_TC_SYN_03_valid_json_xlsx(self):
        """TC_SYN_03: valid JSON - xlsx"""
        data = {"PROJECT_ID": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4", "FILENAME": "myFile01.xlsx"}
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test03.json")
            with open(file_path, "w", encoding="utf-8") as fp:
                json.dump(data, fp)

            signature, filename = EnterpriseManager.register_document(file_path)

        self.assertEqual(filename, "myFile01.xlsx")
        self.assertIsInstance(signature, str)

    def test_TC_SYN_04_missing_opening_brace(self):
        """TC_SYN_04: Missing opening {"""
        content = '"PROJECT_ID":"a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4","FILENAME":"myFile01.pdf"}'
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test04.json")
            with open(file_path, "w", encoding="utf-8") as fp:
                fp.write(content)

            with self.assertRaises(EnterpriseManagementException) as cm:
                EnterpriseManager.register_document(file_path)
            self.assertIn("The file is not JSON formatted", str(cm.exception))

    def test_TC_SYN_05_missing_closing_brace(self):
        """TC_SYN_05: Missing closing }"""
        content = '{"PROJECT_ID":"a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4","FILENAME":"myFile01.pdf"'
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test05.json")
            with open(file_path, "w", encoding="utf-8") as fp:
                fp.write(content)

            with self.assertRaises(EnterpriseManagementException) as cm:
                EnterpriseManager.register_document(file_path)
            self.assertIn("The file is not JSON formatted", str(cm.exception))

    def test_TC_SYN_06_missing_separator(self):
        """TC_SYN_06: Missing separator , between fields"""
        content = '{"PROJECT_ID":"a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4" "FILENAME":"myFile01.pdf"}'
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test06.json")
            with open(file_path, "w", encoding="utf-8") as fp:
                fp.write(content)

            with self.assertRaises(EnterpriseManagementException) as cm:
                EnterpriseManager.register_document(file_path)
            self.assertIn("The file is not JSON formatted", str(cm.exception))

    def test_TC_SYN_07_missing_colon(self):
        """TC_SYN_07: Missing : after PROJECT_ID key"""
        content = '{"PROJECT_ID" "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4","FILENAME":"myFile01.pdf"}'
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test07.json")
            with open(file_path, "w", encoding="utf-8") as fp:
                fp.write(content)

            with self.assertRaises(EnterpriseManagementException) as cm:
                EnterpriseManager.register_document(file_path)
            self.assertIn("The file is not JSON formatted", str(cm.exception))

    def test_TC_SYN_08_missing_project_id(self):
        """TC_SYN_08: Missing PROJECT_ID field entirely"""
        data = {"FILENAME": "myFile01.pdf"}
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test08.json")
            with open(file_path, "w", encoding="utf-8") as fp:
                json.dump(data, fp)

            with self.assertRaises(EnterpriseManagementException) as cm:
                EnterpriseManager.register_document(file_path)
            self.assertIn("JSON does not have the expected structure", str(cm.exception))

    def test_TC_SYN_09_missing_filename(self):
        """TC_SYN_09: Missing FILENAME field entirely"""
        data = {"PROJECT_ID": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4"}
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test09.json")
            with open(file_path, "w", encoding="utf-8") as fp:
                json.dump(data, fp)

            with self.assertRaises(EnterpriseManagementException) as cm:
                EnterpriseManager.register_document(file_path)
            self.assertIn("JSON does not have the expected structure", str(cm.exception))

    def test_TC_SYN_10_project_id_too_short(self):
        """TC_SYN_10: PROJECT_ID value has 31 hex chars (1 deleted)"""
        data = {"PROJECT_ID": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3", "FILENAME": "myFile01.pdf"}
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test10.json")
            with open(file_path, "w", encoding="utf-8") as fp:
                json.dump(data, fp)

            with self.assertRaises(EnterpriseManagementException) as cm:
                EnterpriseManager.register_document(file_path)
            self.assertIn("JSON data has no valid values", str(cm.exception))

    def test_TC_SYN_11_filename_too_short(self):
        """TC_SYN_11: NAME has 7 chars instead of 8"""
        data = {"PROJECT_ID": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4", "FILENAME": "myFile0.pdf"}
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test11.json")
            with open(file_path, "w", encoding="utf-8") as fp:
                json.dump(data, fp)

            with self.assertRaises(EnterpriseManagementException) as cm:
                EnterpriseManager.register_document(file_path)
            self.assertIn("JSON data has no valid values", str(cm.exception))

    def test_TC_SYN_12_no_extension(self):
        """TC_SYN_12: Extension deleted (no extension in FILENAME)"""
        data = {"PROJECT_ID": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4", "FILENAME": "myFile01"}
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test12.json")
            with open(file_path, "w", encoding="utf-8") as fp:
                json.dump(data, fp)

            with self.assertRaises(EnterpriseManagementException) as cm:
                EnterpriseManager.register_document(file_path)
            self.assertIn("JSON data has no valid values", str(cm.exception))

    def test_TC_SYN_13_project_id_too_long(self):
        """TC_SYN_13: PROJECT_ID value has 33 hex chars (1 duplicated)"""
        data = {"PROJECT_ID": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4a", "FILENAME": "myFile01.pdf"}
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test13.json")
            with open(file_path, "w", encoding="utf-8") as fp:
                json.dump(data, fp)

            with self.assertRaises(EnterpriseManagementException) as cm:
                EnterpriseManager.register_document(file_path)
            self.assertIn("JSON data has no valid values", str(cm.exception))

    def test_TC_SYN_14_filename_too_long(self):
        """TC_SYN_14: NAME has 9 chars instead of 8"""
        data = {"PROJECT_ID": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4", "FILENAME": "myFile011.pdf"}
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test14.json")
            with open(file_path, "w", encoding="utf-8") as fp:
                json.dump(data, fp)

            with self.assertRaises(EnterpriseManagementException) as cm:
                EnterpriseManager.register_document(file_path)
            self.assertIn("JSON data has no valid values", str(cm.exception))

    def test_TC_SYN_15_duplicate_opening_brace(self):
        """TC_SYN_15: Duplicate { at start"""
        content = '{{"PROJECT_ID":"a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4","FILENAME":"myFile01.pdf"}'
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test15.json")
            with open(file_path, "w", encoding="utf-8") as fp:
                fp.write(content)

            with self.assertRaises(EnterpriseManagementException) as cm:
                EnterpriseManager.register_document(file_path)
            self.assertIn("The file is not JSON formatted", str(cm.exception))

    def test_TC_SYN_16_duplicate_separator(self):
        """TC_SYN_16: Duplicate , between fields"""
        content = '{"PROJECT_ID":"a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4",,"FILENAME":"myFile01.pdf"}'
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test16.json")
            with open(file_path, "w", encoding="utf-8") as fp:
                fp.write(content)

            with self.assertRaises(EnterpriseManagementException) as cm:
                EnterpriseManager.register_document(file_path)
            self.assertIn("The file is not JSON formatted", str(cm.exception))

    def test_TC_SYN_17_modified_opening_brace(self):
        """TC_SYN_17: { replaced by ["""
        content = '["PROJECT_ID":"a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4","FILENAME":"myFile01.pdf"}'
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test17.json")
            with open(file_path, "w", encoding="utf-8") as fp:
                fp.write(content)

            with self.assertRaises(EnterpriseManagementException) as cm:
                EnterpriseManager.register_document(file_path)
            self.assertIn("The file is not JSON formatted", str(cm.exception))

    def test_TC_SYN_18_modified_separator(self):
        """TC_SYN_18: , replaced by ;"""
        content = '{"PROJECT_ID":"a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4";"FILENAME":"myFile01.pdf"}'
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test18.json")
            with open(file_path, "w", encoding="utf-8") as fp:
                fp.write(content)

            with self.assertRaises(EnterpriseManagementException) as cm:
                EnterpriseManager.register_document(file_path)
            self.assertIn("The file is not JSON formatted", str(cm.exception))

    def test_TC_SYN_19_modified_colon(self):
        """TC_SYN_19: : replaced by ="""
        content = '{"PROJECT_ID"="a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4","FILENAME":"myFile01.pdf"}'
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test19.json")
            with open(file_path, "w", encoding="utf-8") as fp:
                fp.write(content)

            with self.assertRaises(EnterpriseManagementException) as cm:
                EnterpriseManager.register_document(file_path)
            self.assertIn("The file is not JSON formatted", str(cm.exception))

    def test_TC_SYN_20_wrong_project_id_key(self):
        """TC_SYN_20: PROJECT_ID key modified"""
        data = {"PROJECT": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4", "FILENAME": "myFile01.pdf"}
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test20.json")
            with open(file_path, "w", encoding="utf-8") as fp:
                json.dump(data, fp)

            with self.assertRaises(EnterpriseManagementException) as cm:
                EnterpriseManager.register_document(file_path)
            self.assertIn("JSON does not have the expected structure", str(cm.exception))

    def test_TC_SYN_21_wrong_filename_key(self):
        """TC_SYN_21: FILENAME key modified"""
        data = {"PROJECT_ID": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4", "FILE": "myFile01.pdf"}
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test21.json")
            with open(file_path, "w", encoding="utf-8") as fp:
                json.dump(data, fp)

            with self.assertRaises(EnterpriseManagementException) as cm:
                EnterpriseManager.register_document(file_path)
            self.assertIn("JSON does not have the expected structure", str(cm.exception))

    def test_TC_SYN_22_invalid_project_id_hex(self):
        """TC_SYN_22: PROJECT_ID contains invalid hex"""
        data = {"PROJECT_ID": "g1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4", "FILENAME": "myFile01.pdf"}
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test22.json")
            with open(file_path, "w", encoding="utf-8") as fp:
                json.dump(data, fp)

            with self.assertRaises(EnterpriseManagementException) as cm:
                EnterpriseManager.register_document(file_path)
            self.assertIn("JSON data has no valid values", str(cm.exception))

    def test_TC_SYN_23_invalid_filename_char(self):
        """TC_SYN_23: invalid char in filename"""
        data = {"PROJECT_ID": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4", "FILENAME": "myFil@01.pdf"}
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test23.json")
            with open(file_path, "w", encoding="utf-8") as fp:
                json.dump(data, fp)

            with self.assertRaises(EnterpriseManagementException) as cm:
                EnterpriseManager.register_document(file_path)
            self.assertIn("JSON data has no valid values", str(cm.exception))

    def test_TC_SYN_24_invalid_extension(self):
        """TC_SYN_24: invalid extension"""
        data = {"PROJECT_ID": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4", "FILENAME": "myFile01.txt"}
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test24.json")
            with open(file_path, "w", encoding="utf-8") as fp:
                json.dump(data, fp)

            with self.assertRaises(EnterpriseManagementException) as cm:
                EnterpriseManager.register_document(file_path)
            self.assertIn("JSON data has no valid values", str(cm.exception))

    def test_TC_SYN_25_file_not_found(self):
        """TC_SYN_25: file path does not exist"""
        with self.assertRaises(EnterpriseManagementException) as cm:
            EnterpriseManager.register_document("nonexistent.json")
        self.assertIn("Input file not found", str(cm.exception))

    def test_TC_SYN_26_not_json_content(self):
        """TC_SYN_26: file content is not JSON"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test26.json")
            with open(file_path, "w", encoding="utf-8") as fp:
                fp.write("notajson")

            with self.assertRaises(EnterpriseManagementException) as cm:
                EnterpriseManager.register_document(file_path)
            self.assertIn("The file is not JSON formatted", str(cm.exception))

    def test_TC_SYN_27_hash_failure(self):
        """TC_SYN_27: simulate SHA-256 failure"""

        original_sha256 = hashlib.sha256

        def mock_sha256(*args, **kwargs):
            raise ValueError("hash error is present")

        hashlib.sha256 = mock_sha256

        data = {"PROJECT_ID": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4", "FILENAME": "myFile01.pdf"}
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                file_path = os.path.join(tmpdir, "test27.json")
                with open(file_path, "w", encoding="utf-8") as fp:
                    json.dump(data, fp)

                with self.assertRaises(EnterpriseManagementException) as cm:
                    EnterpriseManager.register_document(file_path)

                self.assertIn("Internal processing error", str(cm.exception))
        finally:
            hashlib.sha256 = original_sha256
