from django.db import models
from users.models import User
from classroom.models import Classroom
class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    enrolled_class = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()

