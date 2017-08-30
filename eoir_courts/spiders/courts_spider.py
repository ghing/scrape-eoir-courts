from urllib.parse import urlparse

import scrapy

def strip_and_join(lines):
    return '\n'.join([l.strip() for l in lines])

def get_court_url(base_url, path):
    return '{0}{1}'.format(base_url, path)

def get_base_url(url):
    parsed = urlparse(url)
    return '{0}://{1}'.format(parsed.scheme, parsed.netloc)

def parse_table(table, base_url):
    rows = table.css('tr')
    for i, row in enumerate(rows):
        if i == 0:
            state = row.css('th strong::text').extract_first()
            continue

        if i == 1:
            # Column headers.  Skip it.
            continue

        cols = row.css('td')
        court = cols[0].xpath('.//text()').extract_first().strip()
        href = cols[0].css('a::attr(href)').extract_first()
        address = strip_and_join(cols[1].xpath('./text()').extract())
        judges = [n.strip() for n in
                  cols[2].xpath('./text()').extract()
                  if n.strip() != ""]
        court_administrator = cols[3].xpath('./text()').extract_first()
        yield({
            'state': state,
            'court': court,
            'url': get_court_url(base_url, href),
            'address': address,
            'judges': judges,
            'court_administrator': court_administrator,
        })

class CourtsSpider(scrapy.Spider):
    name = 'courts'

    def start_requests(self):
        urls = [
            'https://www.justice.gov/eoir/eoir-immigration-court-listing',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        base_url = get_base_url(response.url)
        tables = response.css('table[cellpadding="5"]')
        for table in tables:
            for court in parse_table(table, base_url):
                yield court
