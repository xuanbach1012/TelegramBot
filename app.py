from flask import Flask
from flask import request
from flask import Response
import requests
from bs4 import BeautifulSoup

TOKEN = "Yourtoken"
 
app = Flask(__name__)
 
def tel_parse_message(message):
    print("message-->",message)
    try:
        chat_id = message['message']['chat']['id']
        txt = message['message']['text']
        name_client = message['message']['chat']['first_name'] + " " + message['message']['chat']['last_name']
        print("chat_id-->", chat_id)
        print("txt-->", txt)
        print("name_client-->", name_client)

        return chat_id, txt, name_client
    except:
        print("NO text found-->>")

def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': text
                }
   
    r = requests.post(url,json=payload)
    return r

def tel_send_hi(chat_id, text, name_client):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': text,
                'name_client': name_client
                }
   
    r = requests.post(url,json=payload)
    return r

def tel_send_image(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    payload = {
        'chat_id': chat_id,
        'photo': "https://i.pinimg.com/originals/2c/9c/20/2c9c20954029da1dec1020493d9b1347.jpg",
        'caption': "That's you"
    }
 
    r = requests.post(url, json=payload)
    return r

def tel_send_button(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
 
    payload = {
        'chat_id': chat_id,
        'text': "Bạn ở miền nào?",
                'reply_markup': {'keyboard': [[{'text': 'Nam'}, {'text': 'Bắc'}]]}
    }
 
    r = requests.post(url, json=payload)
    return r

def kqxs():
    resp = requests.get('https://xskt.com.vn/')
    tree = BeautifulSoup(markup = resp.text, features = 'html.parser')
    node = tree.find(name = 'table', attrs = {'id': "MB0"}).find('em')
    return "Giải đặc biệt hôm nay là: {}".format(node.text)

def tel_send_kqxs(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    kq = kqxs()
    payload = {
                'chat_id': chat_id,
                'text': kq
                }
   
    r = requests.post(url,json=payload)
    return r

def weatherHN():
    resp = requests.get('https://thoitiet.vn/ha-noi')
    tree = BeautifulSoup(markup= resp.text, features = 'html.parser')
    node1 = tree.find(name = 'span', attrs = {'class' : 'current-temperature'})
    node2 = tree.find(name = 'div', attrs = {'class' : 'overview-caption ml-3'})
    return "Thời tiết Hà Nội hiện tại: {} {}".format(node1.text, node2.text)

def weatherHCM():
    resp = requests.get('https://thoitiet.vn/ho-chi-minh')
    tree = BeautifulSoup(markup= resp.text, features = 'html.parser')
    node1 = tree.find(name = 'span', attrs = {'class' : 'current-temperature'})
    node2 = tree.find(name = 'div', attrs = {'class' : 'overview-caption ml-3'})
    return "Thời tiết TP Hồ Chí Minh hiện tại: {} {}".format(node1.text, node2.text)

def tel_send_weatherHN(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    wt = weatherHN()
    payload = {
                'chat_id': chat_id,
                'text': wt
                }

    r = requests.post(url,json=payload)
    return r

def tel_send_weatherHCM(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    wt = weatherHCM()
    payload = {
                'chat_id': chat_id,
                'text': wt
                }
   
    r = requests.post(url,json=payload)
    return r

@ app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        try:
            chat_id, txt, name_client = tel_parse_message(msg)
            if txt == "/start":
                tel_send_hi(chat_id,"Hello " + name_client + '\n' + 'Gõ help để khám phá thêm', name_client)
            elif txt == "selfie":
                tel_send_image(chat_id)
            elif txt == "thoitiet":
                tel_send_button(chat_id)
            elif txt == "kqxs":
                tel_send_kqxs(chat_id)
            elif txt == "Bắc":
                tel_send_weatherHN(chat_id)
            elif txt == "Nam":
                tel_send_weatherHCM(chat_id)
            elif txt == "help":
                tel_send_message(chat_id, '''Các tính năng:
                Gõ 'selfie' để chụp 1 tấm thử nào.
                Gõ 'thoitiet' để biết thời tiết hiện tại.
                Gõ 'kqxs' để biết kết quả xổ số hôm nay.
                ''')
            else:
                tel_send_message(chat_id, 'Gõ help để biết thêm chi tiết')
        except:
            print("from index-->")
 
        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"
 
if __name__ == '__main__':
    app.run(debug=True)