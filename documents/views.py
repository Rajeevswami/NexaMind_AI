from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import DocumentUploadForm
from .models import Document

@login_required
def index(request):
    return render(request, "documents/index.html", {"documents": Document.objects.filter(owner=request.user)})

@login_required
def upload(request):
    form = DocumentUploadForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        file = form.cleaned_data["file"]
        Document.objects.create(owner=request.user, title=file.name, file=file, mime_type=file.content_type or "application/octet-stream", size_bytes=file.size)
        messages.success(request, "Document uploaded. AI processing will be added in Phase 3.")
        return redirect("documents:index")
    return render(request, "documents/upload.html", {"form": form})

