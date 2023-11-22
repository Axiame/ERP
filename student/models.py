from django.db import models

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    enrolled_class = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()

