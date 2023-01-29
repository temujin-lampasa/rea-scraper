from scrapy.exporters import CsvItemExporter
from rea_scraper.settings import CSV_SEP


class CsvCustomSeperator(CsvItemExporter):
    def __init__(self, *args, **kwargs):
        kwargs['delimiter'] = CSV_SEP
        super(CsvCustomSeperator, self).__init__(*args, **kwargs)
