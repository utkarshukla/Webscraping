import scrapy
import re


class Durgajobs(scrapy.Spider):
    #website
    name="GeeksforGeeks"
    url= 'https://practice.geeksforgeeks.org/jobs/'
    #Starting the request
    def start_requests(self):
        url= 'https://practice.geeksforgeeks.org/jobs/'
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        yield scrapy.Request(url=url, callback=self.parse, headers=headers)
        
    #Response
    def parse(self, response, url=url):
        for jobs in response.selector.xpath("//div[@class='row display-flex all-jobs-row']//div[@class='job-card ']"):
            if str(jobs.xpath(".//div[@class='row job-card-row'][3]/div[2]//span[@class='job-card__subtext job-card__subtext--success ']/text()").extract_first()).find('0 t')!=-1:
            #getting results
                yield {
                    "Salary " : re.sub('\n','',str(jobs.xpath(".//div[@class='row job-card-row'][3]/div[1]//span[@class='job-card__subtext job-card__subtext--success ']/text()").extract_first())),
                    "Company" : re.sub('\n','',str(jobs.xpath(".//div[@class='col-sm-12 company-info']/h4/text()").extract_first())),
                    "Location" : re.sub('\n','',str(jobs.xpath(".//div[@class='row job-card-row'][2]/div[2]//span[@class='job-card__subtext job-card__subtext--success ']/text()").extract_first())),
                    "Position" : re.sub('\n','',str(jobs.xpath(".//div[@class='row job-card-row'][2]/div[1]//span[@class='job-card__subtext job-card__subtext--success ']/text()").extract_first())),
                    "Experience" : re.sub('\n','',str(jobs.xpath(".//div[@class='row job-card-row'][3]/div[2]//span[@class='job-card__subtext job-card__subtext--success ']/text()").extract_first())),
                    "Duration" : re.sub('\n','',str(jobs.xpath(".//div[@class='col-sm-12 company-info']/small/span/text()").extract_first())),
                    "Apply" : re.sub('\n','',url + str(jobs.xpath(".//a/@href").extract_first()))
                }
            
    

