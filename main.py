import requests
import config

# Сессия для запросов к поставщику
sess = requests.session()
sess.headers = {'Content-Type': 'application/json', 'Accept': "application/json", "Authorization": "Bearer-Token "
                                                                                                   + config.tdnws_api}

# Первый запрос к списку товаров
method = '/offers'
data = '?fields=name,images,category,collection,price,url'
# Делаем запрос
res = sess.get(config.url + method + data).json()
print(res)
# Цикл для перебора страниц товаров, пока есть следующая страница - цикл продолжается
while True:
    # TODO:
    # Запрос к самому сайту

    # Проверка наличия следующей страницы
    if res['next_page_url']:
        # Продолжаем цикл и запрашиваем следующую страницу
        res = sess.get(res['next_page_url']).json()
        print(res)
        break
    else:
        # Если нет, то выходим из цикла
        break
