"""class for testing the regsiter_order method"""
import json
import os
import tempfile
import unittest
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
