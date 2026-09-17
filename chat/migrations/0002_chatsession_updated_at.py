# Generated manually to preserve the existing initial migration.
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("chat", "0001_initial")]
    operations = [migrations.AddField(model_name="chatsession", name="updated_at", field=models.DateTimeField(auto_now=True))]
