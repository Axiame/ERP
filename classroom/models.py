from django.db import models
from users.models import User
from school.models import School

class Classroom(models.Model):
    name = models.CharField(max_length=255)
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classes')
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
