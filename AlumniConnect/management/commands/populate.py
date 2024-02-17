from django.core.management.base import BaseCommand
from scripts.add_batch import add_batch
from scripts.add_data import add_data
from scripts.add_degree import add_degree
from scripts.add_pass import add_pass


class Command(BaseCommand):
    help = 'Populates the database with initial data'

    def handle(self, *args, **options):
        self.stdout.write("Starting the population process")
        

        try :
            add_batch()
            self.stdout.write(self.style.SUCCESS("Batches added successfully"))
        except :
            self.stdout.write(self.style.ERROR("An error occured while adding batches"))
        
        try :
            add_degree()
            self.stdout.write(self.style.SUCCESS("Degrees added successfully"))
        except :
            self.stdout.write(self.style.ERROR("An error occured while adding degrees"))

        try :
            add_data()
            self.stdout.write(self.style.SUCCESS("Data added successfully"))
        except :
            self.stdout.write(self.style.ERROR("An error occured while adding data"))

        try :
            add_pass()
            self.stdout.write(self.style.SUCCESS("Passwords added successfully"))
        except :
            self.stdout.write(self.style.ERROR("An error occured while adding passwords"))
            # ... call other functions ...

            self.stdout.write(self.style.SUCCESS("Population process completed successfully"))
