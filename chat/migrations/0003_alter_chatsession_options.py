from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [("chat", "0002_chatsession_updated_at")]
    operations = [migrations.AlterModelOptions(name="chatsession", options={"ordering": ["-updated_at"]})]
