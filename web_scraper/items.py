import scrapy


class CurrentLegislativeActivity(scrapy.Item):
    """
    Item class for holding scraped legislative data
    from the Current Legislative Activities section
    on congress.gov
    """
    house_status = scrapy.Field()
    house_recent = scrapy.Field()
    house_prev_or_next = scrapy.Field()

    senate_status = scrapy.Field()
    senate_recent = scrapy.Field()
    senate_prev_or_next = scrapy.Field()

    # update date in UTC
    update_date = scrapy.Field()
