from pathlib import Path
from django import forms
from django.conf import settings

class DocumentUploadForm(forms.Form):
    file = forms.FileField()
    allowed_extensions = {".pdf", ".docx", ".txt"}
    allowed_content_types = {
        ".pdf": {"application/pdf"},
        ".docx": {"application/vnd.openxmlformats-officedocument.wordprocessingml.document"},
        ".txt": {"text/plain"},
    }
    def clean_file(self):
        file = self.cleaned_data["file"]
        if file.size > settings.MAX_UPLOAD_SIZE:
            raise forms.ValidationError("File must be 10 MB or smaller.")
        extension = Path(file.name).suffix.lower()
        if extension not in self.allowed_extensions:
            raise forms.ValidationError("Upload a PDF, DOCX, or TXT file.")
        if file.content_type and file.content_type not in self.allowed_content_types[extension]:
            raise forms.ValidationError("The file type does not match its extension.")
        return file
