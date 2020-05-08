# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

class OrganizacionesSpider(scrapy.Spider):
    name = 'organizaciones'
    allowed_domains = ['mapeosociedadcivil.uy']
    start_urls = ['http://www.mapeosociedadcivil.uy/organizaciones/']

    def parse(self, response):
        org_rows = response.xpath("//div[@class='row blog blog-medium margin-bottom-20']")
        for row in org_rows:
            #self.logger.info(" ####### PROCESA ROW .....")
            for org in self.parse_org(row, response):
                yield org

        current_page = response.xpath("//ul[@class='pagination pagination-v2']/li[@class=' active']/a/text()").extract_first()
        base_url = response.xpath("//ul[@class='pagination pagination-v2']/li/a/@href")[0].extract()
        position = base_url.find("?page=")
        if position != -1:
            base_url = base_url[0:position+6]
            new_page = int(current_page) + 1
            new_url = base_url + str(new_page)
            #check if new url exists
            selector = response.xpath("//ul[@class='pagination pagination-v2']/li/a[@href='" +  new_url + "']").extract_first()
            if selector:
                absolute_next_page_url = response.urljoin(new_url)
                yield scrapy.Request(absolute_next_page_url)


    def parse_org(self, row, response):
 
        #self.logger.info(" ******** ENTRO A PARSE ORG .....")

        profile_link = row.xpath(".//h4/a/@href").extract_first()
        absolute_profile_url = response.urljoin(profile_link)
        
        request = Request(absolute_profile_url, callback=self.parse_org_detail)
        
        yield request        


    def parse_org_detail(self, response):

        #self.logger.info(" >>>>>>>> ENTRO A PARSE ORG DETAIL .....")

        properties = response.xpath("//p[@class='md-margin-top-20']")

        nombre = ""
        telefono = ""
        mail = ""
        web = ""
        referentes = ""

        for prop in properties:
            prop_name = prop.xpath(".//b/text()").extract_first()            
            if not prop_name:
                continue
            prop_name = prop_name.strip()             
            prop_value = prop.xpath(".//text()")[2].extract()
            if  prop_value:
                prop_value = prop_value.replace(",", "|").strip()
            if "Nombre:" == prop_name:
                nombre = prop_value
                continue
            if "Teléfono:" == prop_name:
                telefono = prop_value
                continue
            if "Email:" == prop_name:
                mail = prop_value
                continue
            if "Referentes:" == prop_name:
                referentes = prop_value
                continue
            if "Web:" == prop_name:
                web = prop.xpath(".//a/@href").extract_first()
                if web:
                    web = web.strip()
                continue
        
        #telefono = response.xpath("//p[@class='md-margin-top-20']/text()")[13].extract()
        #mail = response.xpath("//p[@class='md-margin-top-20']/text()")[15].extract()
        #web = response.xpath("//p[@class='md-margin-top-20']/a/@href").extract_first()
        #referentes = response.xpath("//p[@class='md-margin-top-20']/text()")[20].extract()

        org = {
            "nombre" : nombre,
            "telefono" : telefono,
            "mail" : mail,
            "web" : web,
            "referentes": referentes
        }

        yield org