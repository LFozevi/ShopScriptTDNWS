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


def add_images(img_url, product_id):
    url = f'{config.shop_script_url_api}/shop.product.images.add?product_id={product_id}'
    file = {'file': (f'img_{product_id}.jpg', requests.get(img_url).content, 'image/jpg')}
    res = sess.post(url, files=file)
    return res


def product_update(product_id, name=None, description=None, price=None):
    data = {}
    if name:
        data += {'name': name, 'meta_title': name}
    if description:
        data += {'description': description, 'meta_description': description}
    if price:
        data += {'skus[price]': price}

    method = '/shop.product.update'
    ress = sess.post(f'{config.shop_script_url_api}{method}?id={product_id}', data=data)
    return ress


def product_add(uuid, name, description, images, price):
    data = {
        'name': name,
        'type_id': config.none_category_id,
        'description': description,
        'meta_title': name,
        'meta_description': description,
        'skus[price]': price,
        'sku_type': 1,
        'status': 0,
        'product[uuid]': uuid
    }
    res = sess.post(f'{config.shop_script_url_api}/shop.product.add', data=data)
    if res.status_code == 200:
        for img in images:
            add_images(img, res.json()['id'])
    return res


print(product_add('f88b2b69-978c-11eb-b396-000c29add927', 'Test Product', 'Test Description', '', 1111).json())
