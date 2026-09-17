from django.core.files.storage import default_storage

class DocumentStorage:
    """Single storage boundary; replace default_storage configuration for S3 later."""
    @staticmethod
    def save(name, content): return default_storage.save(name, content)
    @staticmethod
    def url(name): return default_storage.url(name)

