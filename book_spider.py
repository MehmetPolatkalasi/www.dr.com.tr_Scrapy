import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    page_count = 1
    book_count = 1
    file = open("books.txt","a",encoding = "UTF-8")
    start_urls = [
        "https://www.dr.com.tr/CokSatanlar/Kitap?Page=1&SortOrder=1&SortType=0"
    ]

    def parse(self, response):
        book_names = response.css("div.prd-content div.prd-content-wrapper a.prd-name::text").extract()
        book_authors = response.css("div.prd-content div.prd-content-wrapper div.prd-row div.box-line-2.pName a::text").extract()
        book_publishers = response.css("div.prd-content div.prd-content-wrapper div.prd-info-wrapper a.prd-publisher::text").extract()
        

        i = 0

        while(i < len(book_names)):
            self.file.write("-------------------------------------------------------------------------------------------\n")
            self.file.write(str(self.book_count) + ".\n")
            self.file.write("Kitap ismi : " + book_names[i] + "\n")
            self.file.write("Yazar ismi : " + book_authors[i] + "\n")
            self.file.write("Yayınevi : " + book_publishers[i].replace("\n","").strip() + "\n")
            self.file.write("-------------------------------------------------------------------------------------------\n")
            self.book_count += 1

            i += 1

        self.page_count += 1
        next_url = "https://www.dr.com.tr/CokSatanlar/Kitap?Page=" + str(self.page_count) + "&SortOrder=1&SortType=0"
        

        if self.page_count != 6:
            yield scrapy.Request(url = next_url,callback = self.parse)

        else:
            self.file.close()
