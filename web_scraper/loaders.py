import scrapy.loader
from scrapy.loader.processors import TakeFirst, Compose, MapCompose


class CurrentLegislativeActivityLoader(scrapy.loader.ItemLoader):
    """
    ItemLoader class for processing scraped data before it
    is returned as an Item instance
    """
    default_output_processor = TakeFirst()

    house_recent_in = Compose(lambda v: v[0])
    house_prev_or_next_in = Compose(lambda v: v[1])

    senate_recent_in = Compose(lambda v: v[0])
    senate_prev_or_next_in = Compose(lambda v: v[1])

    update_date_in = MapCompose(lambda v: v.isoformat(timespec='seconds'))
