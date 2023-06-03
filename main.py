import requests
import config
import site_api
import logging
# Сессия для запросов к поставщику
sess = requests.session()
sess.headers = {'Content-Type': 'application/json', 'Accept': "application/json", "Authorization": "Bearer-Token "
                                                                                                   + config.tdnws_api}

# Первый запрос к списку товаров
method = '/offers'
data = '?fields=name,images,rrc,article,description'
# Делаем запрос
res = sess.get(config.url + method + data).json()

logging.basicConfig(level=logging.INFO, filename='product_import.log',
                    format="%(asctime)s %(name) %(levelname)s %(message)s")

print(res)
logging.info('Starting work module main')
# Цикл для перебора страниц товаров, пока есть следующая страница - цикл продолжается
while True:
    if res['next_page_url']:
        # Продолжаем цикл и запрашиваем следующую страницу
        url = res['next_page_url']
        res = sess.get(url).json()
        for product in res['data']:
            try:
                # Получаем характеристики товаров
                uuid = product['uuid']
                imgs = product['images']
                name = product['name']
                article = product['article']
                description = product['description']
                price = product['rrc'].split('.')[0]

            except Exception as e:
                logging.error(f'Не удалось получить данные от поставщика\n Страница: {url}', exc_info=True)
                continue
            try:
                # Ищем товар в магазине
                product_get = site_api.get_product(uuid)
            except Exception as e:
                logging.error(f'Не удалось выполнить поиск товара в магазине. UUID товара: {uuid}', exc_info=True)
                continue

            # Если товар существует в нашем магазине, то проверяем что изменилось
            if product_get:
                product_id = product_get['id']
                name_update = None
                description_update = None
                price_update = None

                # Проверяем, есть ли что-то новое
                try:
                    if product_get['name'] != name:
                        name_update = name
                    if product_get['description'] != description:
                        description_update = description
                    if int(product_get['base_price_selectable']) != int(price):
                        price_update = price
                    # Обновляем товар
                    site_api.product_update(product_id, name=name_update, description=description_update,
                                            price=price_update)
                except Exception as e:
                    logging.error(f'Ошибка при обновлении товара. ID товара: {product_id}', exc_info=True)
                    continue
            else:
                # Если нет такого товара, то добавляем
                try:
                    site_api.product_add(uuid, name, description, imgs, price, article)
                except Exception as e:
                    logging.error(f"Не удалось добавить товар. UUID товара: {uuid}")
            # Временный break чтобы добавлялся 1 товар для проверки
            break
        break
    else:
        # Если нет, то выходим из цикла
        break

logging.info("End work module main")