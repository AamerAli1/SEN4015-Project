from importlib.resources import read_text
from django.contrib import admin
from import_export.admin import ExportActionMixin
from import_export import resources
from .models import Item, OrderItem, Order, UserProfile, CATEGORY_CHOICES

from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from import_export.fields import Field



class ItemResource(resources.ModelResource):

    class Meta:
        model = Item
        fields = ('title',)
        
class OrderItemAdmin(admin.ModelAdmin):
    
    list_display = ('id','user', 'item' , 'quantity', 'date_added')

    



class OrderResource(resources.ModelResource):
    user = Field(attribute='user', widget=ForeignKeyWidget(OrderItem, field='username'))
    items = Field(attribute='items', widget=ManyToManyWidget(OrderItem, field='item'))


    class Meta:
        model = Order
        fields = ('user', 'items','ordered_date')



class OrderAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = OrderResource

    list_display = ['user',
                    'ordered',
                    ]
    list_display_links = [
        'user',
   
    ]
    list_filter = ['ordered',
                    ]
    search_fields = [
        'user__username',
        'ref_code'
    ]




class ItemAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = ItemResource

    list_display = ('title','itemNumber', 'isActive' , 'category')

  

admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(UserProfile)
admin.site.register(CATEGORY_CHOICES)
admin.site.register(Order, OrderAdmin)
