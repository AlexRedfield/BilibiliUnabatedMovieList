import time
import requests
import lxml.html
from mysql import MysqlConnector


def download_page(url):  # 下载页面
    return requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
    }).text


def parse_html(html, page_num):  # 使用lxml爬取数据并清洗
    tree = lxml.html.fromstring(html)
    movies = []
    movie_pages = tree.xpath("..//div[@class='doulist-item']")
    mysql_connector = MysqlConnector('douban')
    sql = "INSERT INTO douban.bili(`page`, `name`, `rating`, `rating_nums`, `director`, `actors`, `category`, " \
          "country, `year`, douban_url, `quote`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    for movie_page in movie_pages:
        name = movie_page.xpath("descendant::div[@class='title']/a")[0].xpath('string(.)').strip()
        url = movie_page.xpath("descendant::div[@class='post']/a/@href")[0]
        try:
            quote = movie_page.xpath("descendant::div[@class='comment-item content']/blockquote/text()")[1].strip()
        except:
            quote = ""
        # 年份，国家，类型
        data = movie_page.xpath("descendant::div[@class='abstract']/text()")
        data = [e.strip() for e in data]
        info = {i.split(":")[0]: i.split(":")[1] for i in data}

        director, actors, category, country, year = info.get('导演'), info.get('主演'), info.get('类型'), info.get(
            '制片国家/地区'), info.get('年份')
        try:
            rating = movie_page.xpath("descendant::div[@class='rating']/span")[1].text
            rating_nums = movie_page.xpath("descendant::div[@class='rating']/span")[2].text[1:-4]
        except:
            rating = 0
            rating_nums = 0
        # rating_nums=re.findall("\d+",rating_nums)[0]

        movie = (
            page_num, name, float(rating), int(rating_nums), director, actors, category, country, int(year), url, quote)
        movies.append(movie)

    mysql_connector.multi_insert(sql, movies)
    print(f"Page {page_num} downloaded successfully!!!")
    time.sleep(1)


if __name__ == '__main__':
    for i in range(1, 85):
        parse_html(
            download_page(
                f'https://www.douban.com/doulist/135672683/?start={25 * (i - 1)}&sort=seq&playable=0&sub_type='), i)
