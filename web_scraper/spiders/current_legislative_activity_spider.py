import datetime
import logging

import scrapy

from web_scraper import items, loaders


logger = logging.getLogger(__name__)


# --------------------
# xpath strings
# ---------------------
# these are based on the layout of the congress.gov page.
# the order matters here -- dot refers to building on the previous xpath result

# This gets us the div that has current legislative data in it
legislative_activity_xpath = "//div[h2][contains(./*, 'Current Legislative Activities')]//div[contains(@class, 'home-current-house-senate-row')]"

# build off of <legislative_activity>
# we want to get each of the divs in the above set that are for the house or the senate separately
house_activity_xpath = "./div[contains(@class, 'home-current-house')]"
senate_activity_xpath = "./div[contains(@class, 'home-current-senate')]"

# builds off of <house_activity> or <senate_activity>
# get the current status string, like 'Not in Session' or 'In Session'
current_status_xpath = "./div[contains(@class, 'status')]//a[1]/text()"

# builds off of <house_activity> or <senate_activity>
# get the current string like 'Previous Meeting: Feb. 2, 2018'
# have to split into recent and prev/next when extracting
recent_prev_and_next_xpath = "./div[contains(@class, 'legislative-activities')]/div[contains(@class, 'activity')]/h4/text()"


class CurrentLegislativeActivitySpider(scrapy.Spider):
    """
    Spider for crawling current legislative activity section
    of the congress.gov website
    """
    # scrapy crawl <name> -o output.json on the command line in base directory
    name = 'current_legislative_activity'
    start_urls = ['https://www.congress.gov']

    def parse(self, response):
        """
        Parse the data contained in this response,
        and write the output to a file. See the associated Item
        class for the fields that will be output.

        sample_item = {
            "house_status": "Not in Session",
            "house_recent": "Next Meeting: Feb. 5, 2018 at 12:00 p.m.",
            "house_prev_or_next": "Previous Meeting: Feb. 2, 2018",
            "senate_status": "Not in Session",
            "senate_recent": "Next Meeting: Feb. 5, 2018 at 3:00 p.m.",
            "senate_prev_or_next": "Previous Meeting: Feb. 2, 2018",
            "update_date": "2018-02-03T20:56:07+00:00"
        }
        :param response: Response object
        :return: scrapy Item instance
        """
        now = datetime.datetime.now(datetime.timezone.utc)

        legislative_activity_data = response.xpath(legislative_activity_xpath)

        loader = loaders.CurrentLegislativeActivityLoader(
            item=items.CurrentLegislativeActivity(), selector=legislative_activity_data)

        house_loader = loader.nested_xpath(house_activity_xpath)
        house_loader.add_xpath('house_status', current_status_xpath)
        house_loader.add_xpath('house_recent', recent_prev_and_next_xpath)
        house_loader.add_xpath('house_prev_or_next', recent_prev_and_next_xpath)

        senate_loader = loader.nested_xpath(senate_activity_xpath)
        senate_loader.add_xpath('senate_status', current_status_xpath)
        senate_loader.add_xpath('senate_recent', recent_prev_and_next_xpath)
        senate_loader.add_xpath('senate_prev_or_next', recent_prev_and_next_xpath)

        loader.add_value('update_date', now)
        return loader.load_item()
