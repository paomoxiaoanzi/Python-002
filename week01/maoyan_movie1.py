# 使用requests、bs4库，爬取猫眼电影的前10个电影名称、电影类型和上映时间，并以UTF-8字符集保存到csv格式的文件中
import requests
from bs4 import BeautifulSoup as bs
import lxml.etree
import pandas
# 猫眼电影链接
url = 'https://maoyan.com/films?showType=3'
cookie = '__mta=248346552.1595655889984.1595684473299.1595695152064.26; uuid_n_v=v1; uuid=F31B1EC0CE3911EABF2811F0086C462E2B961B932C9E4556BABFEC9D183D533E; _csrf=23709ca53f88991009f1afbc94d34b6303e5b41aecf4efc059d2c3242fd7060f; __guid=17099173.1449692708166914000.1595655887559.8577; _lxsdk_cuid=17384809d9ec8-0b08cf05767d5c-376b4502-e1000-17384809d9ec8; _lxsdk=F31B1EC0CE3911EABF2811F0086C462E2B961B932C9E4556BABFEC9D183D533E; mojo-uuid=dff20c3981d76d2bf7147e80e80461f2; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1595655888,1595661360; _lx_utm=utm_source%3Dso.com%26utm_medium%3Dorganic; __utma=17099173.2022688508.1595663920.1595663920.1595663920.1; __utmc=17099173; __utmz=17099173.1595663920.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); monitor_count=73; mojo-session-id={"id":"144f66fbe0face5f685b44a92224b5b1","time":1595719507332}; mojo-trace-id=1; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1595719507; __mta=248346552.1595655889984.1595695152064.1595719507619.27; _lxsdk_s=173884b5895-1a9-cd3-a99%7C%7C3'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36', 'Cookie': cookie}
r = requests.get(url, headers=header)
bs_info = bs(r.text, 'html.parser')
movie_list = bs_info.find('dl', attrs={'class': 'movie-list'})
# 定义获取电影信息的函数


def get_page(only_url):
    response = requests.get(only_url, headers=header)
    # xml化处理
    selector = lxml.etree.HTML(response.text)
    # 获取电影名称、类型、上映时间
    movie_name = selector.xpath(
        '/html/body/div[3]/div/div[2]/div[1]/h1/text()')
    movie_type = selector.xpath(
        '/html/body/div[3]/div/div[2]/div[1]/ul/li[1]/a[1]/text()')
    movie_time = selector.xpath(
        '/html/body/div[3]/div/div[2]/div[1]/ul/li[3]/text()')
    movie_info = [movie_name, movie_type, movie_time]
    return movie_info


# 获取前10个电影的详细信息
movies_info = []
amount = 0
while amount < 10:
    for tags in movie_list.find_all('dd'):
        movie_link = tags.find('a').get('href')
        movie_url = 'https://maoyan.com'+movie_link
        print(movie_url)
        movies_inforeceive = get_page(movie_url)
        print(movies_inforeceive)
        movies_info.append(movies_inforeceive)

        amount += 1
        if amount == 10:
            break
print(movies_info)
# 将电影信息存入movies_info1.csv
movies_info1 = pandas.DataFrame(data=movies_info)
movies_info1.to_csv('./movies_info1.csv', encoding='utf8',
                    index=False, header=False)
