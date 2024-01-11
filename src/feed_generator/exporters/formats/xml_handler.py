import xml.etree.ElementTree as ET


class XMLHandler:

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.root = ET.Element("results")

    def append_hit(self, hit):
        result_element = ET.SubElement(self.root, "result")
        self._dict_to_xml(hit['_source'], result_element)

    def close_file(self):
        tree = ET.ElementTree(self.root)
        tree.write(self.file_path, encoding="utf-8", xml_declaration=True)

    def _dict_to_xml(self, dictionary, parent):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                child = ET.SubElement(parent, key)
                self._dict_to_xml(value, child)
            else:
                child = ET.SubElement(parent, key)
                child.text = str(value)
