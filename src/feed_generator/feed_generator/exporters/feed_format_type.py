from enum import Enum

from feed_generator.exporters.xml_exporter import XMLExporter


class FeedFormatType(Enum):
    XML = 'xml'

    def get_class(self):
        if self == FeedFormatType.XML:
            return XMLExporter
        else:
            raise ValueError(f"invalid feed format type {self}")
