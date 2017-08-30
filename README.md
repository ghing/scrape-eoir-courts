Scrape EOIR Courts
==================

Scraper to scrape [EOIR's list of courts](https://www.justice.gov/eoir/eoir-immigration-court-listing).

Assumptions
-----------

* Python 3.5+ (Will probably work with Python 3.4+)

Installation
------------

Clone the repo.

Install dependencies:

    pip install -r requirements.txt

Run the scraper
---------------

    scrapy crawl courts -o courts.jl
