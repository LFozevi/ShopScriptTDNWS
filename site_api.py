import requests
import config
import logging

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


def add_images(img_url, product_id):
    url = f'{config.shop_script_url_api}/shop.product.images.add?product_id={product_id}'
    file = {'file': (f'img_{product_id}.jpg', requests.get(img_url).content, 'image/jpg')}
    res = sess.post(url, files=file)
    return res

def product_update(product_id, name=None, description=None, price=None):
    data = {}

    if name:
        data.update({'name': name, 'meta_title': name})
    if description:
        data.update({'description': description, 'meta_description': description})
    if price:
        data.update({'base_price_selectable': price})

    method = '/shop.product.update'
    if not data:
        return False
    print('update')
    print(data)
    ress = sess.post(f'{config.shop_script_url_api}{method}?id={product_id}', data=data)
    return ress


def product_add(uuid, name, description, images, price, article):
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
    res = sess.post(f'{config.shop_script_url_api}/shop.product.add', data=data)
    print(res.text)
    if res.status_code == 200 and 'error' not in res.text:
        for img in images:
            add_images(img, res.json()['id'])
    return res


print(get_product('327a490a-99ac-11e9-9273-001dd8b74132'))
