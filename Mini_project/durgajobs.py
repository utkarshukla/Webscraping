import scrapy
import re
class Durgajobs(scrapy.Spider):
    #website
    name="Durgajobs"

    #Starting the request
    def start_requests(self):
        url= 'http://durgajobs.com'

        yield scrapy.Request(url=url, callback=self.parse)
        
    #Response
    def parse(self, response):
        for jobs in response.selector.xpath("//tr[@class='line']"):
            if str(jobs.xpath(".//td[5]/text()").extract_first()).find('MCA')!=-1 or str(jobs.xpath(".//td[5]/text()").extract_first()).find('Masters Degree')!=-1 or str(jobs.xpath(".//td[5]/text()").extract_first()).find('Post Graduate')!=-1:

                #getting results
                yield {
                    "Posting Date " : re.sub('\n','',str(jobs.xpath(".//td[1]/text()").extract_first())),
                    "Company" : re.sub('\n','',str(jobs.xpath(".//td[2]/text()").extract_first())),
                    "Location" : re.sub('\n','',str(jobs.xpath(".//td[3]/text()").extract_first())),
                    "Position" : re.sub('\n','',str(jobs.xpath(".//td[4]/text()").extract_first())),
                    "Eligibity" : re.sub('\n','',str(jobs.xpath(".//td[5]/text()").extract_first())),
                    "Duration" : re.sub('\n','',str(jobs.xpath(".//td[6]/text()").extract_first())),
                    "Apply" : re.sub('\n','',str(jobs.xpath(".//td[7]/a[@class='scholarship']/@href").extract_first()))
                }
