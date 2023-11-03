from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator

class Task(models.Model):
    STATUS_CHOICES=(('T', 'To Do'), ('P','In Progress'), ('D','Done'))
    
    PRIORITY_CHOICES=(('1','High Priority'), ('2','Medium Priority'), ('3','Low Priority'))
    
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    description = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='T')
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Comment', related_name='comments_owned')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) :
        return self.title

class Comment(models.Model) :
    text = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'
    
    
