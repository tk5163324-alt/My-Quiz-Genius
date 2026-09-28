import csv
import os

from django.conf import settings
from core.models import Question


DATA_FOLDER = os.path.join(
    settings.BASE_DIR,
    "data"
)


files = [
    "python_questions.csv",
    "java_questions.csv",
    "dbms_questions.csv",
    "dsa_questions.csv",
    "os_questions.csv",
    "AI & ML_questions.csv",
]


total_added = 0


for filename in files:

    file_path = os.path.join(
        DATA_FOLDER,
        filename
    )

    if not os.path.exists(file_path):
        print(f"File not found: {filename}")
        continue

    print(f"\nImporting: {filename}")

    with open(
        file_path,
        "r",
        encoding="utf-8-sig"
    ) as file:

        reader = csv.DictReader(file)

        added = 0

        for row in reader:

            if not row.get("question"):
                continue

            Question.objects.create(
                subject=row["subject"].strip(),
                difficulty=row["difficulty"].strip(),
                question=row["question"].strip(),
                option_a=row["option_a"].strip(),
                option_b=row["option_b"].strip(),
                option_c=row["option_c"].strip(),
                option_d=row["option_d"].strip(),
                answer=row["answer"].strip(),
                explanation=(row.get("explanation") or "").strip()
            )

            added += 1
            total_added += 1

    print(f"Added: {added}")


print("\n==============================")
print(f"TOTAL QUESTIONS ADDED: {total_added}")
print("==============================")