from scrapy.exporters import CsvItemExporter

class TsvSeperator(CsvItemExporter):
    def __init__(self, *args, **kwargs):
        kwargs['encoding'] = 'utf-8'
        kwargs['delimiter'] = '\t'
        super(TsvSeperator, self).__init__(*args, **kwargs)