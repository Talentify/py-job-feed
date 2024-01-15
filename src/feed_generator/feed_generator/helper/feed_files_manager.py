from pathlib import Path

from feed_generator.settings import FEED_FILE_MAX_RECORDS


class FeedFilesManager:
    _current_file = None
    _current_file_size = None
    _current_file_index = None

    def __init__(self, exporter_class, output_directory_path: Path):
        super().__init__()
        self._exporter_class = exporter_class
        self._output_directory_path = output_directory_path
        self._initialize_new_file()

    def add_es_hits(self, hits):
        for hit in hits:
            if self._current_file_size == FEED_FILE_MAX_RECORDS:
                self._close_current_file()
                self._initialize_new_file()
            self._add_es_hit(hit)

    def close(self):
        self._close_current_file()

    def _initialize_new_file(self):
        self._current_file_size = 0
        self._current_file_index = (self._current_file_index or 0) + 1
        file_path = self._output_directory_path / f"feed_{self._current_file_index}.{self._exporter_class.extension}"
        self._current_file = self._exporter_class(file_path)

    def _add_es_hit(self, es_hit):
        self._current_file.add_es_hit(es_hit)
        self._current_file_size += 1

    def _close_current_file(self):
        self._current_file.close()
