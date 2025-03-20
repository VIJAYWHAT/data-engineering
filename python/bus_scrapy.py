import scrapy 
from datetime import datetime

class BusInfo(scrapy.Item):
    bus_name = scrapy.Field()
    departure_time = scrapy.Field()
    arrival_time = scrapy.Field()

class RedBusSpider(scrapy.Spider):
    name = "redbus"
    allowed_domains = ["redbus.in"]
    
    def __init__(self, *args, **kwargs):
        super(RedBusSpider, self).__init__(*args, **kwargs)
        
        self.from_city_name = input("Enter the from city name: ")
        self.from_city_id = input("Enter the from city ID: ")
        self.to_city_name = input("Enter the to city name: ")
        self.to_city_id = input("Enter the to city ID: ")
        self.travel_date = self.validate_travel_date(input("Enter the travel date (DD-MMM-YYYY): "))
        
        if self.travel_date == "Invalid":
            raise ValueError("Invalid date format. Please enter in DD-MMM-YYYY format.")
        
        self.start_urls = [
            f"https://www.redbus.in/bus-tickets/{self.from_city_name}-to-{self.to_city_name}?fromCityName={self.from_city_name}&fromCityId={self.from_city_id}&srcCountry=IND&toCityName={self.to_city_name}&toCityId={self.to_city_id}&destCountry=IND&onward={self.travel_date}&opId=0&busType=Any"
        ]
    
    def validate_travel_date(self, travel_date):
        try:
            return datetime.strptime(travel_date, "%d-%b-%Y").strftime("%d-%b-%Y")
        except ValueError:
            return "Invalid"
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)
    
    def parse(self, response):
        buses = response.css(".bus-items li.row-sec")
        
        for bus in buses:
            item = BusInfo()
            item['bus_name'] = bus.css(".travels::text").get(default="N/A").strip()
            item['departure_time'] = bus.css(".dp-time::text").get(default="N/A").strip()
            item['arrival_time'] = bus.css(".bp-time::text").get(default="N/A").strip()
            yield item
