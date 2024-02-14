from enum import Enum


class FeedFormatType(Enum):
    XML = 'xml'

    def get_class(self):
        if self == FeedFormatType.XML:
            from feed_generator.exporters.xml_exporter import XMLExporter
            return XMLExporter
        else:
            raise ValueError(f"invalid feed format type {self}")
