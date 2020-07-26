# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MaoyanmoviePipeline:
    def process_item(self, item, spider):
        title = item['title']
        movietype = item['movietype']
        date = item['date']
        output = f'|{title}|\t|{movietype}|\t|{date}|\n'
        with open('./maoyanmovie2.csv', 'a+', encoding='utf-8') as mym:
            mym.write(output)
        return item
