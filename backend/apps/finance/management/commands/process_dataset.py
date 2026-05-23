from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

from services.data_processing.process_dataset import process_financial_dataset
from services.data_processing.bulk_insert import bulk_insert_transactions


class Command(BaseCommand):
    help = "Process the raw finance dataset and optionally insert it into the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--bulk-insert",
            action="store_true",
            help="Insert processed transactions into the database for a given user.",
        )
        parser.add_argument(
            "--username",
            type=str,
            help="Username to associate imported transactions with when using --bulk-insert.",
        )
        parser.add_argument(
            "--rows",
            type=int,
            default=5,
            help="Number of sample rows to display after processing.",
        )

    def handle(self, *args, **options):
        df = process_financial_dataset()
        if df is None:
            raise CommandError(
                "Dataset processing failed. Make sure backend/datasets/raw/personal_finance.csv exists."
            )

        self.stdout.write(self.style.SUCCESS("Dataset processed successfully."))
        self.stdout.write(f"Rows: {len(df)}")
        self.stdout.write(f"Columns: {len(df.columns)}")
        self.stdout.write("Column names: %s" % ", ".join(df.columns))

        sample_rows = options["rows"]
        self.stdout.write("\nSample rows:")
        self.stdout.write(df.head(sample_rows).to_string(index=False))

        feature_columns = [col for col in ["savings", "expense_ratio"] if col in df.columns]
        if feature_columns:
            self.stdout.write("\n\nDerived feature columns: %s" % ", ".join(feature_columns))
            self.stdout.write(df[feature_columns].head(sample_rows).to_string(index=False))
        else:
            self.stdout.write(
                self.style.WARNING(
                    "Derived feature columns not created. Check the CSV column names."
                )
            )

        if options["bulk_insert"]:
            username = options.get("username")
            if not username:
                raise CommandError("--username is required when using --bulk-insert.")

            User = get_user_model()
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise CommandError(f"User '{username}' not found.")

            inserted_count = bulk_insert_transactions(df, user)
            self.stdout.write(self.style.SUCCESS(
                f"Inserted {inserted_count} transactions for user '{username}'."
            ))
