import gzip

from src.feed_generator.settings import FEED_FILE_MAX_RECORDS


class FeedFilesBuilder:
    _current_file_handler =  None
    files = set()

    def __init__(self, format_exporter, output_file_name):
        super().__init__()
        self.format_exporter = format_exporter
        self.output_file_name = output_file_name
        self._open_new_file()

    def append_results(self, hits):
        for hit in hits:
            if self._current_file_size == FEED_FILE_MAX_RECORDS:
                self._open_new_file()
            self._current_file_handler.append_hit(hit)
            self._current_file_size += 1

    def close(self):
        self._current_file_handler.close_file()

    def _open_new_file(self):
        if self._current_file_handler:
            self._current_file_handler.close_file()
        self._current_file_size = 0
        self._current_file_handler = self.format_exporter(f"{self.output_file_name}.{len(self.files)+1}")
        self.files.add(self._current_file_handler.file_path)

