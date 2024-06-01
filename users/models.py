from django.db import models

from django.contrib.auth.models import User

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario que envía el mensaje
    content = models.TextField()  # Contenido del mensaje
    timestamp = models.DateTimeField(auto_now_add=True)  # Fecha y hora del mensaje

    def __str__(self):
        return f'{self.user.username}: {self.content[:50]}'
    

class BotMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario que envía el mensaje
    content = models.TextField()  # Contenido del mensaje
    timestamp = models.DateTimeField(auto_now_add=True)  # Fecha y hora del mensaje

    def __str__(self):
        return f'{self.user.username}: {self.content[:50]}'