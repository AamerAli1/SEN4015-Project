from django import template
from product_catalog_app.models import MovieList

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = MovieList.objects.filter(user=user, added=False)
        if qs.exists():
            return qs[0].movies.count()
    return 0
