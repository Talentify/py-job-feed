import xml.etree.ElementTree as ET


class XMLExporter:

    def export(self, es_response, output_file):
        # Create XML tree
        root = ET.Element("results")

        # Add results to XML
        for hit in es_response['hits']['hits']:
            result_element = ET.SubElement(root, "result")
            for key, value in hit['fields'].items():
                ET.SubElement(result_element, key).text = str(value)

        # Create and save XML file
        tree = ET.ElementTree(root)
        tree.write(output_file, encoding="utf-8", xml_declaration=True)
