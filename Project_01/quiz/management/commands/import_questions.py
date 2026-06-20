import csv

from django.core.management.base import BaseCommand

from quiz.models import Category, Question



class Command(BaseCommand):


    help = "Import questions from CSV"



    def handle(self, *args, **kwargs):


        with open(
            "data/questions.csv",
            encoding="utf-8"
        ) as file:


            reader = csv.DictReader(file)



            for row in reader:



                category, created = Category.objects.get_or_create(

                    name=row["category"]

                )



                Question.objects.create(


                    category=category,


                    difficulty=row["difficulty"],


                    question=row["question"],


                    option1=row["option1"],


                    option2=row["option2"],


                    option3=row["option3"],


                    option4=row["option4"],


                    correct_answer=row["correct_answer"],


                    explanation=row["explanation"]

                )



        self.stdout.write(

            self.style.SUCCESS(

                "Questions imported successfully"

            )

        )