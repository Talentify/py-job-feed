from datetime import datetime
from pathlib import Path

from feed_generator.settings import FEED_FILE_MAX_RECORDS


class FeedFilesManager:
    _current_file = None
    _current_file_size = None
    _current_file_index = None

    def __init__(self, exporter_class, output_directory_path: Path, last_build_date: datetime, quantity_of_jobs: int):
        super().__init__()
        self._exporter_class = exporter_class
        self._output_directory_path = output_directory_path
        self.feed_file_limit = FEED_FILE_MAX_RECORDS
        self.extra_fields = FeedFilesExtraData(
            last_build_date=last_build_date,
            quantity_of_jobs=quantity_of_jobs,
            limit=self.feed_file_limit

        )
        self._initialize_new_file()

    def add_es_hits(self, hits):
        for hit in hits:
            if self._current_file_size == self.feed_file_limit:
                self._close_current_file()
                self._initialize_new_file()
            self._add_es_hit(hit)

    def close(self):
        self._close_current_file()

    def _initialize_new_file(self):
        if self._current_file:
            self._current_file_index += 1
            self.extra_fields.inc_offset(self.feed_file_limit)
        else:
            self._current_file_index = 0
        self._current_file_size = 0
        file_path = self._output_directory_path / f"feed_{self._current_file_index+1}.{self._exporter_class.extension}"
        self._current_file = self._exporter_class(file_path, vars(self.extra_fields))

    def _add_es_hit(self, es_hit):
        self._current_file.add_es_hit(es_hit)
        self._current_file_size += 1

    def _close_current_file(self):
        self._current_file.close()


class FeedFilesExtraData:

    def __init__(self, last_build_date: datetime, quantity_of_jobs: int, limit: int):
        self.publisher = "Talentify"
        self.publisher_url = "https://app.talentify.io"
        self.last_build_date = last_build_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
        self.quantity_of_jobs = quantity_of_jobs
        self.pagination = {
            "limit": limit,
            "offset": 0,
        }

    def inc_offset(self, inc):
        self.pagination["offset"] += inc
