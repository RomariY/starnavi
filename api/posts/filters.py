from django_filters import rest_framework as filters
from api.posts.models import Post


class PostFilter(filters.FilterSet):
    date_from = filters.DateFilter(field_name="like__created_at", lookup_expr='gte')
    date_to = filters.DateFilter(field_name="like__created_at", lookup_expr='lte')

    class Meta:
        model = Post
        fields = ['date_from', "date_to", ]
