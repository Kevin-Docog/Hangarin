from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
import random

from taskmanager.models import Category, Priority, Task, SubTask, Note


class Command(BaseCommand):
    help = "Generate fake data for Hangarin"

    def handle(self, *args, **kwargs):
        self.create_tasks(10)
        self.create_subtasks(20)
        self.create_notes(20)

    def create_tasks(self, count):
        fake = Faker()
        for _ in range(count):
            Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                priority=Priority.objects.order_by('?').first(),
                category=Category.objects.order_by('?').first(),
            )
        self.stdout.write(self.style.SUCCESS("Tasks created"))

    def create_subtasks(self, count):
        fake = Faker()
        for _ in range(count):
            SubTask.objects.create(
                parent_task=Task.objects.order_by('?').first(),
                title=fake.sentence(nb_words=4),
                status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
            )
        self.stdout.write(self.style.SUCCESS("SubTasks created"))

    def create_notes(self, count):
        fake = Faker()
        for _ in range(count):
            Note.objects.create(
                task=Task.objects.order_by('?').first(),
                content=fake.paragraph()
            )
        self.stdout.write(self.style.SUCCESS("Notes created"))