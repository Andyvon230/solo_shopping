import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from mall.models import Category, Merchandise, MerchandiseDiscount, MerchandiseRating
from django.db import transaction


class Command(BaseCommand):
    help = 'Load a list of categories, merchandises, discounts, and ratings from CSV files.'

    def handle(self, *args, **kwargs):

        def parse_price(price_str):
            # Strip out common currency symbols and whitespace
            clean_str = price_str.strip('?€£$ ').replace(',', '')
            # Attempt to convert the cleaned string to float
            try:
                price = float(clean_str)
            except ValueError:
                raise ValueError("The input price string is not a valid number.")

            return price

        def parse_int(int_str):
            # Strip out common currency symbols and whitespace
            clean_str = int_str.strip('?€£$ ').replace(',', '')
            # Attempt to convert the cleaned string to float
            try:
                integer = int(clean_str)
            except ValueError:
                raise ValueError("The input integer is not a valid number.")

            return integer

        # Get CSV file path
        csv_dir_name = 'csv_data_set'
        csv_file_path = os.path.join(settings.BASE_DIR, csv_dir_name)
        categories_file = os.path.join(csv_file_path, 'Categories.csv')
        merchandises_file = os.path.join(csv_file_path, 'merchandises.csv')
        discount_file = os.path.join(csv_file_path, 'mer_discount.csv')
        rating_file = os.path.join(csv_file_path, 'mer_rating.csv')

        # Delete all records before loading
        try:
            with transaction.atomic():
                Category.objects.all().delete()
                Merchandise.objects.all().delete()
                MerchandiseDiscount.objects.all().delete()
                MerchandiseRating.objects.all().delete()
        except Exception as e:
            print(e)
        else:
            self.stdout.write(self.style.SUCCESS('All records deleted'))

        try:
            with transaction.atomic():
                # Load Categories
                with open(categories_file, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        Category.objects.update_or_create(
                            id=int(row['category_id']),
                            defaults={
                                'name': row['category_name'],
                                'category_level': int(row['category_level']),
                                'parent_level_id': int(row['main_category_id']) if row['main_category_id'] else None
                            }
                        )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading categories: {e}'))
        else:
            self.stdout.write(self.style.SUCCESS('Categories loaded'))

        try:
            with transaction.atomic():
                # Load Discounts
                with open(discount_file, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        discount_price = row['discount_price']
                        # Skip load current data if discount price is empty
                        if '' == discount_price or discount_price is None:
                            continue
                        merchandise = row['mer_id']
                        MerchandiseDiscount.objects.update_or_create(
                            merchandise=merchandise,
                            defaults={
                                'merchandise': merchandise,
                                'discount': parse_price(discount_price),
                                'is_valid': row['is_valid'] == '1'
                            }
                        )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading categories: {e}'))
        else:
            self.stdout.write(self.style.SUCCESS('Merchandise discount loaded'))

        try:
            with transaction.atomic():
                # Load Ratings
                with open(rating_file, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        ratings = row['ratings']
                        no_of_ratings = row['no_of_ratings']
                        if '' == no_of_ratings or no_of_ratings is None or '' == ratings or ratings is None:
                            continue
                        merchandise = row['mer_id']
                        MerchandiseRating.objects.update_or_create(
                            merchandise=merchandise,
                            defaults={
                                'merchandise': merchandise,
                                'ratings': ratings,
                                'no_of_ratings': parse_int(no_of_ratings),
                                'is_valid': row['is_valid'] == '1'
                            }
                        )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading categories: {e}'))
        else:
            self.stdout.write(self.style.SUCCESS('Merchandise ratings loaded'))

        try:
            # with transaction.atomic():
                # Load Merchandises
                with open(merchandises_file, newline='', encoding='GBK') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        main_category = Category.objects.get(id=row['main_category'])
                        sub_category = Category.objects.get(id=row['sub_category'])
                        discount_id = None
                        if row['discount_id']:
                            discount_id = MerchandiseDiscount.objects.filter(merchandise=row['discount_id'], is_valid=True).first()
                        ratings_id = None
                        if row['ratings_id'].strip():
                            ratings_id = MerchandiseRating.objects.filter(merchandise=row['ratings_id'], is_valid=True).first()
                        Merchandise.objects.update_or_create(
                            id=int(row['id']),
                            defaults={
                                'name': row['name'],
                                'image': row['image'],
                                'main_category': main_category,
                                'sub_category': sub_category,
                                'price': parse_price(row['actual_price']),
                                'discount_id': discount_id if discount_id else None,
                                'ratings_id': ratings_id if ratings_id else None
                            }
                        )
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.stdout.write(self.style.ERROR(f'Error loading categories: {e}'))
        else:
            self.stdout.write(self.style.SUCCESS('Merchandises loaded'))
            self.stdout.write(self.style.SUCCESS('Successfully loaded all data from CSV files'))
