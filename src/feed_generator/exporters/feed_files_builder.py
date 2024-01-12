from pathlib import Path

from src.feed_generator.settings import FEED_FILE_MAX_RECORDS


class FeedFilesBuilder:
    _current_file_handler =  None
    files = set()

    def __init__(self, format_exporter, output_directory_path: Path):
        super().__init__()
        self.format_exporter = format_exporter
        self.output_directory = output_directory_path
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
        self._current_file_handler = self.format_exporter(self._build_file_name())
        self.files.add(self._current_file_handler.file_path)

    def _build_file_name(self):
        return self.output_directory / f"feed_{len(self.files)+1}.{self.format_exporter.extension}"
