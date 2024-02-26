from lxml import etree

from feed_generator.es_hit_formatters import ESHitFormatterABC
from feed_generator.settings import LOGGER as logger


class XMLExporter:

    extension = "xml"

    def __init__(self, file_path, extra_fields: dict = None, es_hit_formatter: ESHitFormatterABC = None):
        super().__init__()
        self.file_path = file_path
        self.root = etree.Element("source")
        self._fill_extra_fields(extra_fields)
        self.es_hit_formatter = es_hit_formatter

    def _fill_extra_fields(self, extra_fields):
        if not extra_fields:
            return
        self._dict_to_xml(extra_fields, self.root)

    def add_es_hit(self, es_hit):
        result_element = etree.SubElement(self.root, "job")
        _data = es_hit['_source']
        if self.es_hit_formatter:
            _data = self.es_hit_formatter.format(_data)
        self._dict_to_xml(_data, result_element)

    def close(self):
        tree = etree.ElementTree(self.root)
        tree.write(self.file_path, encoding="utf-8", xml_declaration=True, pretty_print=True)
        logger.debug(f"File written at {self.file_path}")

    def _dict_to_xml(self, dictionary, parent):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                child = etree.SubElement(parent, key)
                self._dict_to_xml(value, child)
            else:
                child = etree.SubElement(parent, key)
                if value is None:
                    value = ""
                child.text = etree.CDATA(str(value))
