from bs4 import BeautifulSoup
import requests
import json


def post_info(book):
    headers = {'Content-Type': 'application/json'}
    r = requests.post("http://localhost:1864/book", data=book, headers=headers)
    r.encoding = 'utf-8'
    print(r.text)


def main():
    indexreq = requests.get("https://www.kadokawa.com.tw/")
    indexreq.encoding = 'utf-8'
    index = BeautifulSoup(indexreq.text, "html.parser")
    Class2 = str()
    Class2 = index.find(id='a3').parent['href'].replace('p1-products.php?Class2=', '').replace('&page=1', '')
    if Class2 == '' or Class2 is None:
        return

    url = "https://www.kadokawa.com.tw/p1-products.php"
    payload = "Class2=%s&intM=2&Page=1" % Class2
    headers = {'content-type': "application/x-www-form-urlencoded"}
    response = requests.request("POST", url, data=payload, headers=headers)
    response.encoding = 'utf-8'
    totalPage = int(BeautifulSoup(response.text, "html.parser").
                find_all(class_='_page-menu-next')[0].contents[1]['href'].
                replace('javascript:GotoPage(', '').replace(',document.form1);', ''))

    JSONList = list()
    for page in range(1, totalPage+1):
        url = "https://www.kadokawa.com.tw/p1-products.php"
        payload = "Class2=%s&intM=2&Page=%s" % (Class2, page)
        headers = {'content-type': "application/x-www-form-urlencoded"}
        response = requests.request("POST", url, data=payload, headers=headers)
        response.encoding = 'utf-8'
        bookList = BeautifulSoup(response.text, "html.parser").find_all(class_='pro_set')

        for book in bookList:
            bookname = book.find(class_='pro_bookname').text.strip()
            subbookname = book.find(class_='pro_sub_bookname').text.strip()
            author = book.find(class_='pro_people').text.strip()
            cover_image = 'https://www.kadokawa.com.tw/' + str(book.find(class_='pro_pic').contents[1].contents[0]['src'])
            link = 'https://www.kadokawa.com.tw/'+str(book.find(class_='pro_word').contents[1]['href'])
            priceList = book.find(class_='pro_price').text.replace(' ', '').replace(u'\xa0', u'').splitlines()
            publish_date = priceList[2]
            if len(priceList) == 5:
                import re
                price = (re.split(r'\D+', priceList[4], re.UNICODE))[2]
            else:
                price = int(int(priceList[6].replace('元', ''))/0.85)
            JSONBook = dict()
            JSONBook['bookname'] = bookname
            JSONBook['subbookname'] = subbookname
            JSONBook['author'] = author
            JSONBook['cover_image'] = cover_image
            JSONBook['link'] = link
            JSONBook['price'] = price
            JSONBook['publish_date'] = publish_date
            JSONList.append(JSONBook)
            print(json.dumps(JSONBook))
            post_info(json.dumps(JSONBook))

    print(json.dumps(JSONList))




if __name__ == '__main__':
    main()
