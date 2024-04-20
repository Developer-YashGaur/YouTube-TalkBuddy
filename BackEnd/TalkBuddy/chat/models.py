from django.db import models
from django.conf import settings
# Create your models here.

class ChatRoom(models.Model):
    room_user1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="chatroom_participent1", on_delete=models.CASCADE)
    room_user2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="chatroom_participent2", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('room_user1', 'room_user2')

    def __str__(self):
        return f"{self.room_user1.mobileNumber} - {self.room_user2.mobileNumber}"
    
    @classmethod
    def find_or_create(cls, user1, user2):
        user1, user2 = sorted([user1, user2], key=lambda user: user.id)
        room, created = cls.objects.get_or_create(room_user1=user1, room_user2=user2)
        return room
    

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.mobileNumber} at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    
class UserStatus(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="status")
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Status for {self.user.mobileNumber}: {'Online' if self.is_online else 'Offline'}"
