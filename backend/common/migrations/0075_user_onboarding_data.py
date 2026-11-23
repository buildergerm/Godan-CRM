from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("common", "0074_signup_business_profile_fields")]
    operations = [
        migrations.AddField(
            model_name="user",
            name="onboarding_data",
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
