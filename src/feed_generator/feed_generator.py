from elasticsearch import Elasticsearch
import xml.etree.ElementTree as ET

from settings import ELASTICSEARCH_HOST, ELASTICSEARCH_INDEX, ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD


def main():
    es = Elasticsearch([ELASTICSEARCH_HOST],
                       basic_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD)
                       )

    # Specify index and query
    search_query = {
        "query": {
            "match_all": {}
        }
    }

    # Output XML file
    output_file_name = "output.xml"

    # Execute query and save results to XML
    execute_query_and_save_to_xml(es, ELASTICSEARCH_INDEX, search_query, output_file_name)


def execute_query_and_save_to_xml(es, index, query, output_file):
    # Execute the query
    response = es.search(index=index, body=query)

    # Create XML tree
    root = ET.Element("results")

    # Add results to XML
    for hit in response['hits']['hits']:
        result_element = ET.SubElement(root, "result")
        for key, value in hit['_source'].items():
            ET.SubElement(result_element, key).text = str(value)

    # Create and save XML file
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    main()
