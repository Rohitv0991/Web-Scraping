import scrapy
import numpy as np


class BlueTomato(scrapy.Spider):
    name = "blueTomato"
    start_urls = [
        'https://www.blue-tomato.com/de-AT/products/categories/Snowboard+Shop-00000000/?page=1',
    ]

    def parse(self, response):
        # creates 'pids' array with values from 1 to 95
        pids = np.arange(0, 96)

        for pid in pids:
            # get product in 'section.listing' with product id 'pid'
            product = response.css('section.listing li#p'+str(pid))

            # get image url from 'data-src' attribute in 'span.productimage'
            imgURL = product.css('span.productimage img::attr(data-src)').get()
            # if 'imgURL' is still empty
            if imgURL is None:
                # then get image url from 'src' attribute in 'span.productimage'
                imgURL = product.css('span.productimage img::attr(src)').get()

            # yield will help to store the data as a dictionary
            yield {
                'Name': product.css('div.ellipsis p::text').get(),
                'Brand': product.css('span.productdesc a::attr(data-brand)').get(),
                'Price': (product.css('span.price::text').get()).strip(),
                'Image URL':  "https:" + imgURL,
                'Product URL': "https://www.blue-tomato.com" + product.css('span.productdesc a::attr(href)').get(),

                # uncommenting the following line will download the images
                # 'image_urls': ["https:" + imgURL],
            }

            # gets the 'next_page' link from current page's next button
            next_page = response.css('section.filter li.next.browse a::attr(href)').get()

            if next_page is not None:
                # if 'next_page' is valid then:
                next_page = "https://www.blue-tomato.com" + next_page
                # passes 'next_page' to 'parse' function (recursion)
                yield scrapy.Request(url=next_page, callback=self.parse)

# executing the following command will run this spider named 'blueTomato' and store the data in 'snowboardData.csv'
# scrapy crawl blueTomato -o snowboardData.csv
