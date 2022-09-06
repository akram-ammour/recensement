
from django.shortcuts import redirect
from .notionApi import *
from django.http import FileResponse
# Create your views here.
def pdf(request):
    token = "secret_X2L56g3FjA4BH9OseDTrFGj0kNk4Xgpgmk32atVd0cv"
    page_id = "6ff3a6c0-0f1a-40ae-8ce7-6943a7a1ccd0"
    next_cursor = "7464f7db-67b5-434d-9727-0db53c14c2a5"
    try:
        retrieve_infos(token,page_id,next_cursor)
    except:
        pass
    create_pdf()
    return FileResponse(open("recensement.pdf", 'rb'), content_type='application/pdf')
def handle404(request,exception=None):
    return redirect('/')
