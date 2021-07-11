import requests
from io import BytesIO
import time
from PIL import Image, ImageDraw, ImageFont
import textwrap
import random

TIMEOUT = 300 # Какая задержка перед проверкой лайков (в секундах)
TIMEOUT_GETIMAGE = 10 # Какая задержка на запрос авы после проверки лайков
TIMEOUT_EDITPAGE = 10 # Какая задержка на запрос изм поста после заливки фото
API_TOKEN = "ТУТ СВОЙ ТОКЕН И ЛУЧШЕ СО ВСЕМИ ПРАВАМИ"
OWNER_ID = 182639497 # Там, где будет происходить действие(ид странички вк)
POST = 1132 # ID ПОСТА где будет происходить
DEBUG_MODE = True # Админский режим
font = ImageFont.truetype('font.otf', size=8)
VANILLA_MESSAGE = ["Завтра другое, сегодня одно",
                   "Я люблю спать, но тебя больше <3",
                   "Я ПОЛУПОКЕР а как живете вы?",
                   "Я УМНЫЙ? да вроде нет...",
                   "Я твой волшебник!",
                   "А вы видите мою корону?",
                   "Как я сюда попал?",
                   "САЛАМ МАНСОР"] # Текст, который будет писаться в облачке (ВАНИЛЬНЫЕ СТАТУСЫ)

while True:
    response_like = requests.get(f"https://api.vk.com/method/likes.getList?type=post&owner_id={OWNER_ID}&item_id={POST}&offse=0t&count=1&access_token={API_TOKEN}&v=5.21")
    ID_VKONTAKTE = response_like.json()['response']['items'][0]
    file = open('last_user.txt')
    last_user = file.read()

    if str(ID_VKONTAKTE) not in last_user:
        if DEBUG_MODE == True:
            print(response_like.json())
            time.sleep(TIMEOUT_GETIMAGE)
        response_photo = requests.get(f"https://api.vk.com/method/users.get?&user_ids={ID_VKONTAKTE}&fields=photo_100&access_token={API_TOKEN}&v=5.21")
        PHOTO_VKONTAKE_URL = response_photo.json()['response'][0]['photo_100']
        NAME_VKONTAKTE = F"{response_photo.json()['response'][0]['first_name']} {response_photo.json()['response'][0]['last_name']}"
        PHOTO_VKONTAKE = requests.get(PHOTO_VKONTAKE_URL)
        if DEBUG_MODE == True:
            print(response_photo.json())
        img = Image.new('RGBA', (500, 300)) #Создание чистого слоя
        bg = Image.open('Mixxe73(TG)_SOFTWARE.jpg') # Закачка в память картинки
        img_vk = Image.open(BytesIO(PHOTO_VKONTAKE.content)) # Получение картинки по URL (Не хотел лишний раз скачивать на пк в папку)
        img.paste(bg, (0, 0)) # Заливка заднего фона
        img.paste(img_vk, (110, 50))  # Вставка аватарки на картинку
        draw_text = ImageDraw.Draw(img)
        text = textwrap.fill(random.choice(VANILLA_MESSAGE), width=14)
        draw_text.text((15, 85),text,font=font,fill='#5b5b5b')
        draw_text.text((88, 165), NAME_VKONTAKTE, font=(ImageFont.truetype('font.otf', size=15)), fill='#5b5b5b')
        img.save("out.png")
        file_last_user = open('last_user.txt', 'w')
        file_last_user.write(str(ID_VKONTAKTE))
        file_last_user.close()
        print('Успешно сделали изображение!')

        try: # Загрузка изображения на сервера VK
            respone = requests.get(
                f'https://api.vk.com/method/photos.getWallUploadServer?owner_id={OWNER_ID}&access_token={API_TOKEN}&v=5.131')
            respone_url = respone.json()['response']['upload_url']
            payload = {'file': open('out.png', "rb")}
            sendphoto = requests.post(respone_url, files=payload)
            server = sendphoto.json()['server']
            p_hash = sendphoto.json()['hash']
            photo = sendphoto.json()['photo']
            savephoto = requests.post(f'https://api.vk.com/method/photos.saveWallPhoto?user_id={OWNER_ID}&photo={photo}&server={server}&hash={p_hash}&access_token={API_TOKEN}&v=5.131')
            savephoto_ID= savephoto.json()['response'][0]['id']
            print(f'Фотография успешно загружена на сервера вк (ID {savephoto_ID})')
        except:
            print('Не удалось загрузить пикчу')

        try: # Изменение поста
            payload = {"message": "Поставь лайк и окажись на стене! github.com/Mixxe73/Like-and-Photo-in-Wall"}
            respone = requests.post(
                f'https://api.vk.com/method/wall.edit?owner_id={OWNER_ID}&post_id={POST}&attachments=photo{OWNER_ID}_{savephoto_ID}&access_token={API_TOKEN}&v=5.131', payload)
            print(respone.json())
            print('Пост успешно изменен! ПОБЕДА!')
        except:
            print('Не удалось изменить пост')
    else:
        print('Ошибка! Пользователь уже был!')
    print(f'Начинаю запускать ожидание в {TIMEOUT} секунд')
    time.sleep(TIMEOUT) # Запуск тайм аута
