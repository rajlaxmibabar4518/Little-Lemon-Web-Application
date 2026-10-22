from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Booking",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=200)),
                ("reservation_date", models.DateField()),
                ("reservation_slot", models.SmallIntegerField(default=10)),
            ],
            options={"ordering": ["reservation_date", "reservation_slot"]},
        ),
        migrations.CreateModel(
            name="Menu",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(db_index=True, max_length=255)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("inventory", models.SmallIntegerField()),
            ],
            options={"ordering": ["title"]},
        ),
    ]
