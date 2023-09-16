import json

from fastapi import FastAPI
from selenium.webdriver.common.by import By
from time import sleep

from settings import browser

app = FastAPI()


@app.get('/search')
def search_by_user_link(user_id: int, url: str):
    browser.get(url)
    sleep(0.5)
    name = browser.find_element(By.XPATH, '//*[@id="layoutPage"]/div[1]/div[4]/div[2]/div/div/div[1]/div[2]/h1').text
    sale_price = browser.find_element(By.XPATH,
                                      '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div[2]/div[2]/div/div['
                                      '1]/div/div/div[1]/div[2]/div/div[1]/span[1]').text

    without_sale = browser.find_element(By.XPATH,
                                        '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div[2]/div[2]/div/div['
                                        '1]/div/div/div[1]/div[2]/div/div[1]/span[2]').text
    with_card = browser.find_element(By.XPATH,
                                     '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div[2]/div[2]/div/div['
                                     '1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span').text

    user_data = {'Название товара': name,
                 'Цена со скидкой': sale_price,
                 'Цена без скидки': without_sale,
                 'Цена по карте': with_card}

    add_to_user_list(user_id, url, user_data)
    return user_data


def add_to_user_list(user_id: int, url: str, user_data: dict):
    try:
        with open(f'{user_id}.json', 'r+', encoding='utf-8') as json_file:
            existing_data = json.load(json_file)
            existing_data[url] = user_data
            json_file.seek(0)
            json.dump(existing_data, json_file, ensure_ascii=False)
        return user_data, 'OK 200'

    except FileNotFoundError:
        new_value = {url: user_data}
        with open(f'{user_id}.json', 'w', encoding='utf-8') as json_file:
            json.dump(new_value, json_file, ensure_ascii=False)
        return new_value, 'OK 200'


@app.post('/delete')
def remove_from_user_list(user_id: int, url: str):
    try:
        with open(f'{user_id}.json', 'r+', encoding='utf-8') as json_file:
            existing_data = json.load(json_file)

            if url in existing_data:
                del existing_data[url]
                json_file.seek(0)
                json_file.truncate()
                json.dump(existing_data, json_file, ensure_ascii=False)

                return 'OK 200: URL удален'
            else:
                return 'URL не найден в файле'

    except FileNotFoundError:
        return 'Файл не найден'
