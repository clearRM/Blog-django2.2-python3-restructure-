from django import forms
from .models import ArticlePost

class ArticlePostForm(forms.ModelForm):
    class Meta:
        # 指明数据的来源
        model = ArticlePost
        fields = ('title','body')