# Импорт для работы с JSON
import json 
# Импорт для асинхронного программирования
from channels.generic.websocket import AsyncWebsocketConsumer
# Импорт для работы с БД в асинхронном режиме
from channels.db import database_sync_to_async
# Импорт модели сообщений

import django
django.setup()

from .models import Message
from users.models import Users
from loguru import logger
from trips.db_communication import push_notify
 
# Класс ChatConsumer
class ChatConsumer(AsyncWebsocketConsumer):
    
    # Метод подключения к WS
    async def connect(self):
        # Назначим пользователя в комнату
        token = self.scope['path'].split('/')[-1]
        user = await self.get_user(token)
        self.room_name = user.id
        self.room_group_name = 'chat_%s' % self.room_name
        logger.info(f'Created new room: {self.room_name}')
        # Добавляем новую комнату
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # Принимаем подключаем
        await self.accept()
 
    # Метод для отключения пользователя
    async def disconnect(self, close_code):
        # Отключаем пользователя
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
 
    # Декоратор для работы с БД в асинхронном режиме
    @database_sync_to_async
    # Функция для создания нового сообщения в БД
    def new_message(self, from_id, to_id, message):
        # Создаём сообщение в БД
        user_to = Users.objects.get(id=to_id)
        Message.objects.create(
            from_user = Users.objects.get(id=from_id),
            to_user = user_to,
            text=message
        )
        push_notify(user_to.fcm_token, f'Новое сообщение от {Users.objects.get(id=from_id).first_name}', message)

    @database_sync_to_async
    def get_user(self, token):
        return Users.objects.get(token=token)

    @database_sync_to_async
    def get_user_by_id(self, user_id):
        return Users.objects.filter(id=user_id).first()
 
    # Принимаем сообщение от пользователя
    async def receive(self, text_data=None, bytes_data=None):
        # Форматируем сообщение из JSON
        logger.debug(text_data)
        text_data_json = json.loads(text_data)
        # Получаем текст сообщения
        message = text_data_json['message']
        to = text_data_json['to']
        
        # Добавляем сообщение в БД 
        await self.new_message(from_id=int(self.room_name), to_id=int(to), message=message)
        
        # Отправляем сообщение 
        await self.channel_layer.group_send(
            'chat_' + to,
            {
                'type': 'chat_message',
                'from': self.room_name,
                'message': message,
            }
        )
    
    # Метод для отправки сообщения клиентам
    async def chat_message(self, event):
        # Получаем сообщение от receive
        message = event['message']
        # Отправляем сообщение клиентам
        if event['from'] != 'BAZA':
            user = await self.get_user_by_id(int(event['from']))
        else:
            user = None
        await self.send(text_data=json.dumps({
            'from_name': f'{user.first_name} {user.last_name}' if user else 'BAZA',
            'from': event['from'],
            'message': message,
        }, ensure_ascii=False))


    async def notify(self, reciever_id, message):
        await self.channel_layer.group_send(
            'chat_' + reciever_id,
            {
                'type': 'notification',
                'from': self.room_name,
                'message': message,
            }
        )
