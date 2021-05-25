#scrapy crawl imdb -s DEPTH_LIMIT=1 -o test.csv
import scrapy
# from imdbdata.items import MovieItem

class ImdbSpider(scrapy.Spider):
    name = 'imdb'
    allowed_domains = ['imdb.com']
    base_url = 'https://imdb.com'
    start_urls = ['https://www.imdb.com/search/title/?num_votes=1000,&title_type=feature',]
    
    def parse(self, response):
        # item = MovieItem()

        # 1. Đối với duy nhất một phim -> dùng xpath (cố định)
        # yield{
        #     'title': response.xpath('//*[@id="main"]/div/div[3]/div/div[1]/div[3]/h3/a/text()').extract_first(),
        #     'release': response.xpath('//*[@id="main"]/div/div[3]/div/div[1]/div[3]/h3/span[2]/text()').extract_first().strip('()'),
        #     'certificate': response.xpath('//*[@id="main"]/div/div[3]/div/div[1]/div[3]/p[1]/span[1]/text()').extract_first(),
        #     'runtime': response.xpath('//*[@id="main"]/div/div[3]/div/div[1]/div[3]/p[1]/span[3]/text()').extract_first(),
        #     'genre': response.xpath('//*[@id="main"]/div/div[3]/div/div[1]/div[3]/p[1]/span[5]/text()').extract_first().strip(' \n'),
        #     'rating': response.xpath('//*[@id="main"]/div/div[3]/div/div[1]/div[3]/div/div[1]/strong/text()').extract_first(),
        #     'direcror': response.xpath('//*[@id="main"]/div/div[3]/div/div[1]/div[3]/p[3]/a[1]/text()').extract_first(),
        #     #'star'
        #     'votes': response.xpath('//*[@id="main"]/div/div[3]/div/div[1]/div[3]/p[4]/span[2]/text()').extract_first(),
        #     }

        # 2. Đối với nhiều phim trên 1 trang
        table = response.css('div[class="lister-item mode-advanced"]')

        for cell in  table:
            # Thời lượng phim
            runtimes = cell.css('p[class="text-muted "] span[class="runtime"]::text').extract_first()
            if runtimes is None:
                runtime = ''
            else:
                runtime = runtimes

            # Thể loại
            genre = cell.css('p[class="text-muted "] span[class="genre"]::text').extract_first()\
                                            .replace(' ','').replace('\n', '').replace(',', ' ').split(' ')
            genres = {'Action': 0, 'Adventure': 0, 'Animation': 0, 'Biography': 0, 'Comedy':0,\
                    'Crime': 0, 'Documentary': 0, 'Drama': 0, 'Family': 0, 'Fantasy': 0, 'Film-Noir':0,\
                    'Game-Show': 0, 'History': 0, 'Horror': 0, 'Music': 0, 'Musical': 0, 'Mystery': 0,\
                    'News': 0, 'Reality-TV': 0, 'Romance': 0, 'Sci-Fi': 0, 'Sport': 0, 'Talk-Show': 0,\
                    'Thriller': 0, 'War': 0, 'Western': 0}

            for i in range(len(genre)): # Các thể loại của phim có giá trị bằng 1, 
                genres[genre[i]] = 1 # các thể loại khác không của phim có giá trị bằng 0.
 
            # Đạo diễn và diễn viên
            direcror_cast = cell.xpath('./div[@class="lister-item-content"]/p[@class=""]/child::*') # Lấy tất cả thẻ con bên trong
            ds = []
            for tag in direcror_cast:
                ds.extend(tag.xpath('./text()').extract())

            if direcror_cast is None: # Nếu không có đạo diễn và diễn viên thì gán bằng rỗng
                direcror = []
                star = []
            else:
                if ('|' not in ds): # Dấu ngăn giữa đạo diễn và diễn viên
                    director = ds # Nếu không có dấu thì chỉ có đạo diễn
                    star = []
                else: # Nếu có dấu thì trước dấu là đạo diễn, sau dấu là diễn viên
                    i = ds.index('|')
                    director = ds[:i]
                    star = ds[i+1:]

            # Metascore
            metascores = cell.css('div[class="inline-block ratings-metascore"] span::text').extract_first()
            if metascores is None:
                metascore = ''
            else:
                metascore = metascores

            # Vote and gross value
            vote_gross = cell.xpath('./div[@class="lister-item-content"]/p[@class="sort-num_votes-visible"]/span[@name="nv"]/attribute::data-value').extract()
            vote = vote_gross[0]
            if len(vote_gross) == 2:
                gross = vote_gross[1]
            else:
                gross = ''

            yield{

                'title': cell.css('h3[class="lister-item-header"] a::text').extract_first(),
                'release': cell.css('h3[class="lister-item-header"] span[class="lister-item-year text-muted unbold"]::text')\
                                                                            .extract_first().replace('(', '').replace(')', '')\
                                                                                .replace('I', '').replace('V', '').replace('X', ''),
                'certificate': cell.css('p[class="text-muted "] span[class="certificate"]::text').extract_first(),
                'runtime': runtime.replace(' min', ''),
                'genre': cell.css('p[class="text-muted "] span[class="genre"]::text').extract_first().strip(' \n'),
                'rating': cell.css('div[class="inline-block ratings-imdb-rating"] strong::text').extract_first(),
                'metascore' : metascore.strip(),
                'summary': cell.css('div[class="lister-item-content"] p[class="text-muted"]::text').extract_first()\
                                                                            .strip().replace('\n', '').replace('"', ''),
                'director': director,
                'star': star,
                'vote': vote,
                'gross' : gross,
                'Action': genres['Action'],
                'Adventure': genres['Adventure'],
                'Animation': genres['Animation'],
                'Biography': genres['Biography'],
                'Comedy': genres['Comedy'],
                'Crime': genres['Crime'],
                'Documentary': genres['Documentary'],
                'Drama': genres['Drama'],
                'Family': genres['Family'],
                'Fantasy': genres['Fantasy'],
                'Film-Noir': genres['Film-Noir'],
                'Game-Show': genres['Game-Show'],
                'History': genres['History'],
                'Horror': genres['Horror'],
                'Music': genres['Music'],
                'Musical': genres['Musical'],
                'Mystery': genres['Mystery'],
                'News': genres['News'],
                'Reality-TV': genres['Reality-TV'],
                'Romance': genres['Romance'],
                'Sci-Fi': genres['Sci-Fi'],
                'Sport': genres['Sport'],
                'Talk-Show': genres['Talk-Show'],
                'Thriller': genres['Thriller'],
                'War': genres['War'],
                'Western': genres['Western'],

            }
        
        # 3. Tự động chuyển trang đối với nhiều phân trang
        next_page = response.css('div[class="article"] div[class="desc"] a[class="lister-page-next next-page"]::attr(href)')\
                                                                                                            .extract_first()

        if next_page:
            next_page_url = 'https://www.imdb.com/' + next_page
            yield scrapy.Request(next_page_url, callback=self.parse)
