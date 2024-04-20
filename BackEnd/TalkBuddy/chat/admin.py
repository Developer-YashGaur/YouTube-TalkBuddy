from django.contrib import admin
from chat.models import ChatRoom, Message

# Register your models here.
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'room_user1', 'room_user2', 'created_at', 'updated_at']
    ordering = ['id']

class MessagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat_room', 'sender']
    ordering = ['id']


admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(Message, MessagesAdmin)
