from django.shortcuts import render
from django.http import FileResponse
from django.shortcuts import redirect
from .models import Bde,Promo
from .notionAPi import *
# Create your views here.
def home(request):
    return render(request,"index.html")
def pdf(request,id):
    if id not in range(1,6):
        return redirect("/")
    bde = list(Bde.objects.all().filter(promo__level =id).values_list("fullname", flat=True).order_by("?"))
    notion_token = Promo.objects.all().filter(level=id).values_list("notion_token",flat=True)[0]
    page_id = Promo.objects.all().filter(level=id).values_list("page_id",flat=True)[0]
    if not page_id or not  notion_token:
        return FileResponse(open(f"main/static/recensement/{id}/404.pdf", 'rb'), content_type='application/pdf',filename="recensement")
    page_id = page_id[:8] + '-'+ page_id[8:12]+ '-'+   page_id[12:16] + '-'+  page_id[16:20] + '-'+ page_id[20:]
    try:
        retrieve_infos(notion_token,page_id,id)
    except:
        pass
    create_pdf(bde,id)
    return FileResponse(open(f"main/static/recensement/{id}/recensement.pdf", 'rb'), content_type='application/pdf',filename="recensement.pdf")

    #return HttpResponse(bde)
def test(request):
    all_bde = Bde.objects.all().order_by("fullname","promo")
    all_promo = Promo.objects.all().order_by("level")
    return render(request,"test.html",{"Bde":all_bde,"Promo":all_promo})
