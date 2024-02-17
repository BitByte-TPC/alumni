from django.core.management.base import BaseCommand
from scripts.add_batch import add_batch
from scripts.add_data import add_data
from scripts.add_degree import add_degree
from scripts.add_pass import add_pass


class Command(BaseCommand):
    help = 'Populates the database with initial data'

    def handle(self, *args, **options):
        self.stdout.write("Starting the population process")

        operations = [
            (add_batch, "Batches added successfully", "An error occured while adding batches"),
            (add_degree, "Degrees added successfully", "An error occured while adding degrees"),
            (add_data, "Data added successfully", "An error occured while adding data"),
            (add_pass, "Passwords added successfully", "An error occured while adding passwords")
        ]

        error_occured = False

        for operation, success_message, error_message in operations:
            try:
                operation()
                self.stdout.write(self.style.SUCCESS(success_message))
            except:
                error_occured = True
                self.stdout.write(self.style.ERROR(error_message))

        if error_occured:
            self.stdout.write(self.style.ERROR("Some data could not be added. Please check the error messages above."))
        else:
            self.stdout.write(self.style.SUCCESS("Population process completed successfully."))
