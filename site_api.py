import requests
import config
import logging

site_api_logger = logging.getLogger(__name__)
site_api_logger.setLevel(logging.INFO)

site_api_handler = logging.FileHandler(f'{__name__}.log')
site_api_formatter = logging.Formatter('%(name)s %(asctime)s %(levelname)s %(message)s')

site_api_handler.setFormatter(site_api_formatter)
site_api_logger.addHandler(site_api_handler)

sess = requests.session()
headers = {'Accept': "application/json, text/plain, */*", 'X-Requested-With': 'XMLHttpRequest', 'Authorization':
    f'Bearer {config.shop_script_token}'}

sess.headers = headers

site_api_logger.info('Start work site api module')


# Функция для получения товара по UUID. Так как UUID уникален, то выдаст только 1 товар
def get_product(uuid):
    try:
        method = '/shop.product.search?'
        res = sess.get(f'{config.shop_script_url_api}{method}hash=search/uuid={uuid}')
        res_json = res.json()
        # Проверяем, есть ли товары в выдаче, если нет то отправляем False
        if res_json['count'] > 0:
            return res_json['products'][0]
    except Exception as e:
        logging.error(f'Не удалось выполнить поиск товара. UUID товара:{uuid}', exc_info=True)
    return False


# Функция для добавления картинки к товару. Получаем изображение от поставщика и кодируем его в байты,
# а затем отправляем в запросе и добавляем к товару
def add_images(img_url, product_id):
    try:
        url = f'{config.shop_script_url_api}/shop.product.images.add?product_id={product_id}'
        file = {'file': (f'img_{product_id}.jpg', requests.get(img_url).content, 'image/jpg')}
        res = sess.post(url, files=file)
        return res
    except Exception as e:
        logging.error(f'Не удалось добавить картинку. \nURL картинки: {img_url}\nID товара: '
                      f'{product_id}', exc_info=True)
        return False


# Функция для обновления продукта. Обновляется товар по его ID.
def product_update(product_id, name=None, description=None, price=None):
    data = {}
    # Проверяем что было передано в функцию, если есть параметр, то добавляем его для обновления в словарь с данными
    if name:
        data.update({'name': name, 'meta_title': name})
    if description:
        data.update({'description': description, 'meta_description': description})
    if price:
        data.update({'base_price_selectable': price})

    method = '/shop.product.update'
    # Если же ничего не было передано в функцию из параметров для обновления, то выходим из функции и возвращаем False
    if not data:
        return False
    try:
        ress = sess.post(f'{config.shop_script_url_api}{method}?id={product_id}', data=data)
    except Exception as e:
        logging.error(f'Возникла ошибка при отправке запроса на обновление товара. ID товара: {product_id}\nСсылка: '
                      f'{config.shop_script_url_api}{method}?id={product_id}\nДанные запроса:\n{data}', exc_info=True)
        return False
    return ress


# Функция для добавления товара. Принимает uuid товара, название, описание, картинки массивом, цену и артикул
def product_add(uuid, name, description, images: list, price, article):
    # Собираем данные в словарь для отправки
    data = {
        'name': name,
        'type_id': config.none_category_id,
        'description': description,
        'meta_title': name,
        'meta_description': description,
        'base_price_selectable': price,
        'sku_id': article,
        'sku_type': 1,
        'status': 0,
        'features[uuid]': uuid
    }
    try:
        res = sess.post(f'{config.shop_script_url_api}/shop.product.add', data=data)
        # Проверяем, возникла ли ошибка при запросе (почему-то при некоторых ошибках сервер возвращает 200-ый код,
        # но все равно присылает ошибку, так что это дополнительно проверяем)
        if res.status_code == 200 and 'error' not in res.text:
            # Если же товар успешно добавился, добавляем картинки к нему, сразу при создании, увы, сделать этого нельзя
            for img in images:
                add_images(img, res.json()['id'])
        return res
    except Exception as e:
        logging.error(f'Возникла ошибка при создании товара. UUID товара: {uuid}\nСсылка: '
                      f'{config.shop_script_url_api}/shop.product.add\nДанные запроса:\n{data}', exc_info=True)
