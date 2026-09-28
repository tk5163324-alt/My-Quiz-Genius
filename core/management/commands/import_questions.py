import csv

from django.core.management.base import BaseCommand
from core.models import Question


class Command(BaseCommand):

    help = "Import questions from CSV"

    def add_arguments(self, parser):

        parser.add_argument(
            "csv_path",
            type=str
        )

    def handle(self, *args, **kwargs):

        path = kwargs["csv_path"]

        count = 0

        with open(
            path,
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                Question.objects.create(
                    subject=row["subject"],
                    difficulty=row["difficulty"],
                    question=row["question"],
                    option_a=row["option_a"],
                    option_b=row["option_b"],
                    option_c=row["option_c"],
                    option_d=row["option_d"],
                    answer=row["answer"],
                    explanation=row["explanation"]
                )

                count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"{count} questions imported successfully"
            )
        )