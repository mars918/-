import requests
import os 
from urllib.parse import urlencode
from hashlib import md5
from multiprocessing.pool import Pool
GROUP_START = 1
GROUP_END = 5
#写个网页函数
def get_page(offset):
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '3',
        'from': 'gallery',
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(params)
    
        ###返回的是形如key2=value2&key1=value1字符串。
    
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        print("个屁了")
#写个解析函数
def get_images(json):
    data = json.get('data')
    if data:
        for item in data:
            image_list = item.get('image_detail')
            title = item.get('title')
            for image in image_list:
                #yield 迭代器，生成迭代对象
                yield {
                    'image':image.get('url'),
                    'title':title
                }
#写个保存函数
def save_image(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        url = item.get('image')
        r = requests.get(url)
        if r.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(item.get('title'), md5(r.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(r.content)
            else:
                print('Already Downloaded', file_path)
    except:
        print('failed to save image')
#在写个猪函数
def main(offset):
    json = get_page(offset)
    for item in get_images(json):
        print(item)
        save_image(item)

if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()

