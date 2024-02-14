import xml.etree.ElementTree as ET

from feed_generator.settings import LOGGER as logger


class XMLExporter:

    extension = "xml"

    def __init__(self, file_path, extra_fields: dict = None):
        super().__init__()
        self.file_path = file_path
        self.root = ET.Element("source")
        self._fill_extra_fields(extra_fields)

    def _fill_extra_fields(self, extra_fields):
        if not extra_fields:
            return
        self._dict_to_xml(extra_fields, self.root)

    def add_es_hit(self, es_hit):
        result_element = ET.SubElement(self.root, "job")
        self._dict_to_xml(es_hit['_source'], result_element)

    def close(self):
        tree = ET.ElementTree(self.root)
        tree.write(self.file_path, encoding="utf-8", xml_declaration=True)
        logger.debug(f"File written at {self.file_path}")

    def _dict_to_xml(self, dictionary, parent):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                child = ET.SubElement(parent, key)
                self._dict_to_xml(value, child)
            else:
                child = ET.SubElement(parent, key)
                child.text = str(value)
