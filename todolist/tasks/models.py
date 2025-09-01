from django.db import models


class TaskGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    URGENCY_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]

    group = models.ForeignKey(TaskGroup, null=True, blank=True, on_delete=models.SET_NULL, related_name='tasks')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)
    urgency_level = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='baixa')
    tags = models.ManyToManyField(Tag, blank=True, related_name='tasks')

    def __str__(self):
        return self.name


class TaskFile(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='files')
    file_path = models.CharField(max_length=512)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Arquivo de {self.task.name}"
