import requests
import config

sess = requests.session()
headers = {'Accept': "application/json, text/plain, */*", 'X-Requested-With': 'XMLHttpRequest', 'Authorization':
    f'Bearer {config.shop_script_token}'}

sess.headers = headers


def get_product(uuid):
    method = '/shop.product.search?'
    res = sess.get(f'{config.shop_script_url_api}{method}hash=search/uuid={uuid}')
    res_json = res.json()
    if res_json['count'] > 0:
        return res_json['products'][0]
    return False


def product_update(uuid, name=None, ):
    pass


def product_add(uuid, article, brand, name, description, images, quantity, category, price):
    pass


print(get_product('8027f20c-bde7-11eb-a581-000c29a2a548'))
