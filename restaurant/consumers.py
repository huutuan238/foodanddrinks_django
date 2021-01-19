import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Review, Product, Customer
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models import Avg
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import JsonResponse

from django.http import HttpResponse

class ReviewConsumer(WebsocketConsumer):
    def connect(self):
        self.review_name = self.scope['url_route']['kwargs']['review_name']
        self.review_group_name = 'chat_%s' % self.review_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.review_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.review_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        content = text_data_json['content']
        vote = float(text_data_json['vote'])
        productId = text_data_json['productId']
        userId = text_data_json['userId']

        user = Customer.objects.get(user_id=userId)
        product = Product.objects.get(id=productId)

        review = Review(user = user, product = product, content = content, vote = vote )

        rate = Review.objects.filter(product=product).aggregate(Avg('vote'))
        product.vote = list(rate.values())[0]

        try:
            review.full_clean()
            review.save()
            product.full_clean()
            product.save()

            reviewInfor = {
                'id' : review.id,
            }
            reviewInfor = json.dumps(reviewInfor)
            htmlRender = render_to_string("restaurant/review.html",{'review':review})

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.review_group_name,
                {
                    'type': 'chat_message',
                    'review': reviewInfor,
                    'htmlRender' : htmlRender
                }
            )

        except ValidationError as e:
            errors = JsonResponse(e.message_dict, safe=False)

            htmlRender = render_to_string("restaurant/errors.html",{'messages':errors})

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.review_group_name,
                {
                    'type': 'error_message',
                    'htmlRender' : htmlRender
                }
            )

    # # Receive message from room group
    def chat_message(self, event):
        review = event['review']
        htmlRender = event['htmlRender']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'review': review,
            'htmlRender' : htmlRender,
        }))

    def error_message(self, event):
        htmlRender = event['htmlRender']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'htmlRender' : htmlRender,
        }))
