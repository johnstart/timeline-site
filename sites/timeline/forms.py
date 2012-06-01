# -*- coding: UTF-8 -*-
import re

from django.core.exceptions import ValidationError

from bootstrap.forms import BootstrapModelForm

#from easy_thumbnails.widgets import ImageClearableFileInput

from .models import Timeline, TlEvent, Comment

class TimelineForm(BootstrapModelForm):

    def __init__(self, *args, **kwargs):
        super(TimelineForm, self).__init__(*args, **kwargs)
        self.fields['status'].choices = (('draft', u'草稿'), ('pub', u'发布'), )

    class Meta:
        model = Timeline
        fields = ['title', 'cover', 'tags', 'intro', 'status']
        #widgets = { 'cover': ImageClearableFileInput(), }

    def save(self, *args, **kwargs):
        self.instance.update_updated_on(commit=False)
        timeline = super(TimelineForm, self).save(*args, **kwargs)
        return timeline
        
def valid_date(s):
    if not s:
        return
    fmts = ['^-{0,1}\d{1,4}-\d{1,2}-\d{1,2}$', '^-{0,1}\d{1,4}-\d{1,2}$', '^-{0,1}\d{1,4}$']
    for fmt in fmts:
        if re.search(fmt, s):
            return
    raise ValidationError(u'无法识别该日期格式')

class TlEventForm(BootstrapModelForm):

    def clean_startdate(self):
        v = self.cleaned_data['startdate']
        valid_date(v)
        return v

    def clean_enddate(self):
        v = self.cleaned_data['enddate']
        valid_date(v)
        return v

    def save(self, *args, **kwargs):
        tlevent = super(TlEventForm, self).save(*args, **kwargs)
        if tlevent.cover:
            for e in TlEvent.objects.filter(cover=True).exclude(pk=tlevent.pk):
                e.cover = False
                e.save()
        return tlevent

    class Meta:
        model = TlEvent
        exclude = ['timeline', 'media_credit']
        #widgets = { 'cover': ImageClearableFileInput(), }
        custom_fields = {'media': 'timeline/field_media.html'}
        

class CommentForm(BootstrapModelForm):
    class Meta:
        model = Comment
        fields = ['content', ]
