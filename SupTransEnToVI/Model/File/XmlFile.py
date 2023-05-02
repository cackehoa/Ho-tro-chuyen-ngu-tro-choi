'''XmlFile.py
Đọc nội dung tập tin xml'''
import xml.etree.ElementTree as ET
from .TypeFile import TypeFile

class XmlFile(TypeFile):
    def __init__(self, fileName):
        super().__init__(fileName)

    def read_all(self):
        tree = ET.parse(self.get_file_name())
        root = tree.getroot()
        return root