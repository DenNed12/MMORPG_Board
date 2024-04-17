from django_filters import FilterSet,DateTimeFilter, ChoiceFilter
from django.forms import DateTimeInput
from .models import Post

class PostFilter(FilterSet):
    category = ChoiceFilter(field_name='cat',
                                choices = Post.CATCHOICES,
                                label='Category',
                                empty_label='Select a category')
    added_after = DateTimeFilter(
        label='Дата добавления',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains']
        }