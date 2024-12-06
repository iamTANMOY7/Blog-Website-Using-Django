from django.contrib import admin
# from myapp.models import Author
from .models import Post,Comment,Contact
# Register your models here.


admin.site.site_header = 'ADMIN PANEL'
admin.site.site_title = 'BLOGGING WEBSITE'
admin.site.index_title= 'Site Administration'

# @admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject']   
    
admin.site.register(Contact, ContactAdmin) 

class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'time']
    
admin.site.register(Comment, CommentAdmin) 

class PostAdmin(admin.ModelAdmin):
    list_display = ['postname', 'category', 'user', 'time']

admin.site.register(Post, PostAdmin)
