import json
from channels.generic.websocket import AsyncWebsocketConsumer

class QuizConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_pin = self.scope['url_route']['kwargs']['game_pin']
        self.group_name = f'quiz_{self.game_pin}'
        # Долучаємось до групи
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        # Покидаємо групу
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'answer':
            answer = data.get('answer')
            user = self.scope['user'].username if self.scope['user'].is_authenticated else 'Anonymous'
            # Тут можна обчислити бали та оновити результати
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'broadcast_answer',
                    'user': user,
                    'answer': answer
                }
            )
        elif message_type == 'next_question':
            question_data = data.get('question')
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'broadcast_question',
                    'question': question_data
                }
            )

    async def broadcast_answer(self, event):
        await self.send(text_data=json.dumps({
            'type': 'answer',
            'user': event['user'],
            'answer': event['answer']
        }))

    async def broadcast_question(self, event):
        await self.send(text_data=json.dumps({
            'type': 'question',
            'question': event['question']
        }))