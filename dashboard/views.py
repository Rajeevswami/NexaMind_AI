from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from documents.models import Document
@login_required
def home(request):
    docs = Document.objects.filter(owner=request.user)
    return render(request, "dashboard/home.html", {"document_count": docs.count(), "recent_documents": docs[:5]})

