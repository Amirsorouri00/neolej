from django.db import models

# def file_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     return 'user_{0}/{1}'.format(instance.remark, filename)

class File(models.Model):
    # file = models.FileField(upload_to=file_directory_path, blank=False, null=False)
    remark = models.CharField(max_length=31)
    timestamp = models.DateTimeField(auto_now_add=True)