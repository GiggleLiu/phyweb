from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget

from essay.models import Essay,Topic

class NewEssayForm(forms.ModelForm):
    class Meta:
        model = Essay
        fields=('content','title','content_type')
class UpdateEssayForm(forms.ModelForm):
    class Meta:
        model = Essay
        fields=('title','content')

class EssayAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Essay

class EssayAdmin(admin.ModelAdmin):
    form = EssayAdminForm

class NewTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields=('title','description','default_content_type')

class UpdateTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields=('title','description','default_content_type')
