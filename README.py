import requests
from lxml import etree
import re
import csv
import multiprocessing
import time

def get_all_page(n_num):
    """
    获取首页的链接的url和页面数
    :return:
    """
    base_url = 'http://www.haodf.com//keshi/{}/zixun.htm'.format(n_num)
    print(base_url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Host': 'www.haodf.com',
    }

    response = requests.get(url=base_url, headers=headers)

    res = etree.HTML(response.text)

    num = res.xpath('//div[@class="p_bar"]//a[@class="p_text"]//text()')
    # print(num)
    page = str(num[0])
    page_num = int(page.split(' ')[1])
    # print(page_num)
    return page_num


def get_info(name, n_num):
    """
    获取所有的链接url
    :param page_num:
    :return:
    """
    pages = get_all_page(n_num)
    all_urls = []
    if pages > 3000:
        pages = 3000
    for page in range(1, pages):
        url = 'https://www.haodf.com/keshi/{}/zixun_{}.htm'.format(n_num, page)
        # print(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Host': 'www.haodf.com',
        }
        response = requests.get(url=url, headers=headers)

        res = etree.HTML(response.text)

        urls = res.xpath('//table[@class="hplb blueg"]//a[@class="blue_link"]/@href')
        # print(len(urls))
		
		# 生成csv文件
        # with open('./result/{}.csv'.format(name),'a')as csvfile:
        #     writer = csv.writer(csvfile)
        #     writer.writerow(["question","content","keshi"])
        pool = multiprocessing.Pool(multiprocessing.cpu_count())

        for new_url in urls:
            pool.apply_async(get_detail, (new_url, name))

        pool.close()
        pool.join()


        print(page)


def get_detail(url, name):
    title = ''
    new_list = []
    m = 0

    list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Host': 'www.haodf.com',
    }
    response = requests.get(url=url, headers=headers)

    res = etree.HTML(response.text)

    try:


        if 'doctorteam' in url:

            title = res.xpath('//div[@class="fl-title ellps"]//text()')[0]
            content1 = res.xpath('//div[@class="f-c-r-content"]/div[@class="f-c-r-wrap"]//h4//text()')
            content2 = res.xpath('//div[@class="f-c-r-content"]/div[@class="f-c-r-wrap"]//p//text()')
            con = ''

            for n in range(0, len(content1)):
                content1[n] = re.sub(r'[\r\t\n]', '', content1[n])
                content2[n] = re.sub(r'[\r\t\n]', '', content2[n])
                con = con + content1[n] + ":" + content2[n] + ' '

            keshi = res.xpath('//div[@class="hh"]/a//text()')
            keshi1 = ''.join(keshi)
            keshi2 = re.sub(r'\n                        ', '', keshi1)
            new_keshi = keshi2.split(' ')[1]

        else:
            title = res.xpath('//h1[@class="fl f20 fn fyahei pl20 bdn"]//text')[0]

            con1 = res.xpath('//div[@class="h_s_cons_info"]/div[@class="h_s_info_cons"]/*//text()')
            con2 = ''.join(con1)
            con = re.sub(r'[\r\t\n|  ]', '', con2)

            keshi = res.xpath('//div[@class="hh"]/a//text()')
            keshi1 = ''.join(keshi)
            keshi2 = re.sub(r'\n                        ', '', keshi1)
            new_keshi = keshi2.split(' ')[1]
    except:
        pass

    list.append(title.strip())
    list.append(con.strip())
    list.append(new_keshi.strip())

    new_list.append(list)
    if(new_list!=[]):
    # 生成csv文件
        with open('./result/{}.csv'.format(name), 'a', encoding ='utf8')as csvfile:
            writer = csv.writer(csvfile)
            # writer.writerow(["question", "content", "keshi"])
            writer.writerows(new_list)


if __name__ == '__main__':
    toCrawlList = {
        # '普通内科':'1006000',
        '普外科':'2004000','烧伤科':'31000000',
    '整形科':'2009000',
    "妇科":'6002000',"产科":'6001000',"计划生育科":'6005000',
    "新生儿科":'3012000',
    '小儿神经内科':'3006000',"小儿心内科":'3004000',"小儿肾内科":'3019000',"小儿内分泌科":'3014000',
    "小儿皮肤科":'3025000',"小儿耳鼻喉":'3024000',"小儿心外科":'3021000',"小儿胸外科":'3029000',"小儿神经外科":'3028000',"小儿整形科":'3022000',
    '针灸科':'26001000',"中医骨科":'26010000',"中医按摩科":'26012000',
    '口腔修复科':'10004000','颌面外科':'10002000','正畸科':'10006000',
    "麻醉医学科":'45002000',
    "理疗科":'44001000',
    "放射科":'46003000',
    "预防保健科":'21000000'}
    # name = "普通内科"
    n_num = '25000000'
    for key, value in toCrawlList.items():
        # try:
        get_info(key, value)
        time.sleep(3)
        # except Exception as err:
            # print(err)
            # continue
