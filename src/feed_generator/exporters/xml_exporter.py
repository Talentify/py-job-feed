import xml.etree.ElementTree as ET


class XMLExporter:

    def export(self, es_response, output_file):
        # Create XML tree
        root = ET.Element("results")

        # Add results to XML
        for hit in es_response['hits']['hits']:
            result_element = ET.SubElement(root, "result")
            self._dict_to_xml(hit['_source'], result_element)

        # Create and save XML file
        tree = ET.ElementTree(root)
        tree.write(output_file, encoding="utf-8", xml_declaration=True)

    def _dict_to_xml(self, dictionary, parent):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                child = ET.SubElement(parent, key)
                self._dict_to_xml(value, child)
            else:
                child = ET.SubElement(parent, key)
                child.text = str(value)
