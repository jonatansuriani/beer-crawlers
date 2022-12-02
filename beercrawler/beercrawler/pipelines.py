from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class BeercrawlerPipeline:
    def process_item(self, item, spider):
        return item

class DuplicatesPipeline:

    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['original_url'] in self.urls_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.urls_seen.add(adapter['original_url'])
            return item