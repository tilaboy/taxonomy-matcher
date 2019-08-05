'''A Module to output the selected values to the chosen format'''

import os
import sys
import csv
import json


class DataSaver:
    """
    DataSaver:
    - open/create targed output file
    - save the selected values to file with corresponding format
    """

    def __init__(self, output_file):
        if output_file == 'STDOUT':
            self.format = output_file
            self.ostream = sys.stdout
        else:
            output_dir = os.path.dirname(output_file)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

            _, self.format = os.path.splitext(output_file)
            self.ostream = open(output_file, 'w', encoding='utf-8')

            self.csv_writer = None
            if self.format == '.csv' or self.format == '.tsv':
                self.csv_writer = csv.writer(
                    self.ostream,
                    delimiter="\t",
                    quotechar="'",
                    quoting=csv.QUOTE_MINIMAL)

    def store(self, row):
        """Store one row at a time"""
        if self.format == '.csv' or self.format == '.tsv':
            self._store_csv_row(row)
        elif self.format == '.jsonl':
            self._store_jsonl_row(row)
        else:
            self._store_txt_row(row)

    def close_stream(self):
        """close the file"""
        self.ostream.close()

    def _store_csv_row(self, row):
        """Store the row under csv format"""
        self.csv_writer.writerow(row)

    def _store_txt_row(self, row):
        """Store the row under text format"""
        self.ostream.write(str(row))

    def _store_jsonl_row(self, row):
        """Store the row under json line format"""
        self.ostream.write(json.dumps(row, ensure_ascii=False) + '\n')
