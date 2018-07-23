from .models import Photo
import django_filters


class PhotoFilter(django_filters.FilterSet):
    class Meta:
        model = Photo
        fields = ['category']
