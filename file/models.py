from django.db import models
from django.contrib.auth.models import User
import os
from tika import parser
from stop_words import get_stop_words
import re
from django.db.models.signals import post_save


# Create your models here.

def user_directory_path(instance, filename):
    return 'files/user_{0}/{1}'.format(instance.user.id, filename)

class UserFile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_files")
    file = models.FileField(upload_to= user_directory_path )
    content_key_words = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.file.name

    def css_class(self):
        name, extension = os.path.splitext(self.file.name)
        if extension == '.pdf':
            return 'pdf-o'
        if extension == '.pptx':
            return 'powerpoint-o'
        if extension == '.ppt':
            return 'powerpoint-o'
        return 'o'

    def name(self):
        return os.path.basename(self.file.name)



def extract_key_words(sender,instance,*args,**kwargs):
    stop_words = get_stop_words('en')
    pattern = re.compile(r'\b(' + r'|'.join(stop_words) + r')\b\s*')
    try:
        parsed = parser.from_file(instance.file.path)
        key_words = pattern.sub('', parsed["content"]).replace('\n',' ')
        UserFile.objects.filter(id=instance.id).update(content_key_words=key_words)
    except :
        pass
post_save.connect(extract_key_words, sender=UserFile)
