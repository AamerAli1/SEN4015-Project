from importlib.resources import read_text
from django.contrib import admin
from import_export.admin import ExportActionMixin
from import_export import resources
from .models import Movie, list, MovieList, UserProfile, CATEGORY_CHOICES

from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from import_export.fields import Field



class ItemResource(resources.ModelResource):

    class Meta:
        model = Movie
        fields = ('title',)
        
class MoveListAdmin(admin.ModelAdmin):
    
    list_display = ('id','user', 'movie', 'quantity', 'date_added')

    



class OrderResource(resources.ModelResource):
    user = Field(attribute='user', widget=ForeignKeyWidget(list, field='username'))
    items = Field(attribute='items', widget=ManyToManyWidget(list, field='movie'))


    class Meta:
        model = MovieList
        fields = ('user', 'items','date_added')



class listAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = OrderResource

    list_display = ['user',
                    'added'
                    ]
    list_display_links = [
        'user',
   
    ]
    search_fields = [
        'user__username',
        'ref_code'
    ]




class MovieAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = ItemResource

    list_display = ('title','itemNumber', 'isActive' , 'category')

  

admin.site.register(Movie, MovieAdmin)
admin.site.register(list,MoveListAdmin)
admin.site.register(UserProfile)
admin.site.register(CATEGORY_CHOICES)
admin.site.register(MovieList, listAdmin)
