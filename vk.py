from vk_api import VkApi
from vk_api.keyboard import VkKeyboard
from vk_api.longpoll import VkLongPoll, VkEventType

from DBSM import get_state, upload_database , set_state

from environs import Env
from threading import Thread as th
import requests, time

answers_json = {
    "quest0": 'Здравствуйте, это AND Group\n\nПеред началом сотрудничества необходимо ответить на несколько вопросов. Пожалуйста, следуйте подсказкам бота.\nИтак, какое у вас профильное образование?',
    "quest1": 'Сколько лет вы пишите работы для студентов? (например: 1 год, 5 лет и т.д.)',
    "quest2": 'Сколько времени вы готовы уделять написанию работ?  (например: работаю только вечером по 2-3 часа, могу работать только в выходные и т.д.)',
    "quest3": 'Какие типы работ вы пишите? (например: курсовые, дипломные, магистерские)',
    "quest4": 'Назовите ТОП 3 дисциплины, в которых вы считаете себя профессионалом? (например: менеджмент, экономика, управление персоналом)',
    "quest5": 'Работаете ли вы с системой проверки антиплагиат.вуз? (Да, нет, работаю, но не имею доступа)',
    "quest6": 'Какой примерный прайс на ваши услуги? (примерная стоимость за диплом, курсовую, реферат)',
}


def vk_apply():
    authors_sent = []

    #read env
    env = Env()
    env.read_env(".env")
    token = env.str("API_KEY")

    # Авторизуемся как сообщество
    vk = VkApi(token=token)
    api = vk.get_api()
    
    
    
    def write_msg(user_id, message, kb) -> None: # пишем сообщение
        api.messages.send(
            user_id=user_id,
            random_id= 0,
            message=message,
            keyboard = kb
        )


    def create_kb(link) -> str: # инлайн кб
        keyboard = VkKeyboard(inline=True)
        keyboard.add_openlink_button(label = 'Перейти ⚡', link = link)
        return keyboard.get_keyboard()
    
        

    def send_remind_message(user_id):
        time.sleep(86400)
        if get_state(user_id) != "quest8":
            write_msg(user_id, f"Здравствуйте, сезон работ уже стартовал, а мы по-прежнему ищем талантливых авторов, готовых работать в нашей команде AND GROUP. Не откладывайте ваши возможности на потом, с нетерпением ждем вашу анкету. Следуйте инструкциям бота.", None)


    

    while True:
        try:
            longpoll = VkLongPoll(vk) # Работа с сообщениями

            for event in longpoll.listen(): # Основной цикл

                if event.type == VkEventType.MESSAGE_NEW: # Если пришло новое сообщение

                    if event.to_me:  # if message is to me    
                        request = event.text # message.text
                        state = get_state(event.user_id)
                    
                        if state == "quest8":
                            continue

                        if event.user_id not in authors_sent:
                            th(target=send_remind_message, args= (event.user_id, )).start()
                            authors_sent.append(event.user_id)

                        if state != "quest7":
                            write_msg(event.user_id, answers_json[state], None)
                        else:
                            write_msg(event.user_id, f"Спасибо за ваши ответы! Наш HR менеджер уже получил от вас первичную анкету на вступление в команду.\n\nНа следующем этапе, вас ждет небольшое тестовое задание - это допуск к реальным оплачиваемым проектам, который получают все наши авторы перед началом сотрудничества.\n\nДля прохождения тестового задания перейдите в нашего Telegram бота по кнопке ниже", create_kb(f"https://t.me/andgroup_bot?start={event.user_id}"))
                        
                        upload_database(event.user_id, request, state)
                        next_state = state[:-1] + str(int(state[-1]) + 1)
                        set_state(event.user_id, next_state)

                        
                        
                        
        except (requests.exceptions.ReadTimeout, requests.exceptions.Timeout, requests.exceptions.ConnectTimeout):
            print("timeout")
            pass
       



vk_apply()
