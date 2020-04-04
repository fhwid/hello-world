import requests, re, pymysql
import time


def baidu(company, page):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
    for j in range(page):
        num = j * 10
        url = 'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word=' + company + '&pn=' + str(num)
        res = requests.get(url, headers=headers, timeout=10).text

        p_info = '<p class="c-author">(.*?)</p>'
        info = re.findall(p_info, res, re.S)
        source = []
        date = []
        for i in range(len(info)):
            info[i] = re.sub('<.*?>', '', info[i])
            info[i] = info[i].strip()
            source.append(info[i].split('&nbsp;&nbsp;')[0])
            date.append(info[i].split('&nbsp;&nbsp;')[1])
        # print(source)
        for i in range(len(date)):
            date[i] = date[i].strip()
            date[i] = date[i].split(' ')[0]
            date[i] = re.sub('[年月]', '-', date[i])
            date[i] = re.sub('日', '', date[i])
            if ('小时' in date[i]) or ('分钟' in date[i]):
                date[i] = time.strftime("%Y-%m-%d")
            else:
                date[i] = date[i]
            
        # print(date)
        p_href = '<h3 class="c-title">.*?<a href="(.*?)"'
        href = re.findall(p_href, res, re.S)
        # print(href)
        p_title = '<h3 class="c-title">.*?<em>(.*?)</a>'
        title = re.findall(p_title, res, re.S)
        for i in range(len(title)):
            title[i] = title[i].strip()
            title[i] = re.sub('<.*?>', '', title[i])
        
        db = pymysql.connect(host='localhost', port=3308, user='root', password='', database='pachong', charset='utf8')
        cur = db.cursor()
        sql = 'INSERT INTO test (company, title, href, date, source) VALUES (%s, %s, %s, %s, %s)'
        sql_1 = 'SELECT * FROM test WHERE company = %s'
        cur.execute(sql_1, company)
        data_all = cur.fetchall()
        title_all = []
        for i in data_all:
            title_all.append(i[1])
        
        for i in range(len(title)):
            if title[i] not in title_all:
                cur.execute(sql, (company, title[i], href[i], date[i], source[i]))
        db.commit()
        cur.close()
        db.close()

        # print(title)
        # file1 = open('./test.txt', 'a')
        # file1.write(company + 'data get success!' + '\n' + '\n')
        # for i in range(len(source)):
        #     file1.write(str(10 * j + i + 1) + '.' + title[i] + '(' + date[i] + '-' + source[i] + ')' + '\n')
        #     file1.write(href[i] + '\n')
        # file1.write('-----------------------------------------' + '\n' + '\n')
        # file1.close()

        # for i in range(len(source)):
        #     print(str(i + 1) + '.' + title[i] + '(' + date[i] + '-' + source[i] + ')')
        #     print(href[i])

companys = ['华能信托', '阿里巴巴', '京东', '腾讯']
for i in companys:
    try:
        baidu(i, 2)
        print(i + '百度新闻爬取成功')
    except:
        print(i + '百度新闻爬取失败')
