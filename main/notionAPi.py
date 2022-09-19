def retrieve_infos(token,page_id,id):
    import json
    import requests
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    headers = {
        "Accept": "application/json",
        "Notion-Version": "2022-06-28",
        "Authorization": f"Bearer {token}"
    }
    results =[]
    previous = requests.get(url, headers=headers).json()
    next_cursor = previous["next_cursor"]
    results.extend(previous['results'])
    while True:
        if not next_cursor:
            break
        url = f"https://api.notion.com/v1/blocks/{page_id}/children?start_cursor={next_cursor}&page_size=100"
        next = requests.get(url, headers=headers).json()
        next_cursor = next["next_cursor"]
        results.extend(next['results'])
    with open(f"main/static/recensement/{id}/file.json","w",encoding="utf-8") as file:
        json.dump(results,file,indent=4)
def create_pdf(bde,id,unicode="•"):
    import json
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.colors import Color
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import BaseDocTemplate, PageTemplate, KeepTogether
    from reportlab.platypus import Frame, PageTemplate, Image
    from reportlab.lib.units import cm
    from reportlab.platypus import BaseDocTemplate
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from pytz import timezone
    from datetime import date,datetime
    with open(f"main/static/recensement/{id}/file.json", "r", encoding="utf-8") as file:
        results = json.loads(file.read())
    data = []
    for x in results:
        type = x["type"]
        if type not in ["heading_1","heading_2","heading_3","to_do"]:
            continue
        text = x[type]["rich_text"][0]["plain_text"].strip()
        if type == "heading_1":
            data.append((text,1))
        elif type == "heading_2":
            data.append((text,2))
        elif type == "heading_3":
            data.append((text,3))
        elif type == "to_do" and x[type]["checked"] == True :
            data.append((text,4))
    semesters = {
        1:(1,2),
        2:(3,4),
        3:(5,6),
        4:(7,8),
        5:(9,10),
    }
    # creating date instance
    casablanca = timezone("Africa/Casablanca")
    today = datetime.now(casablanca)
    year = int(today.strftime("%Y"))
    month = today.strftime("%m")
    if len(month) == 1:
        month = "0" + month
    day = today.strftime("%d")
    if int(month) in (8,9,10,11,12) :
        schoolYear = [year,year+1]
        level = semesters[id][0]
    else:
        schoolYear = [year-1,year]
        level = semesters[id][1]
    # adding Calibri font
    pdfmetrics.registerFont(TTFont('Calibri-Bold', 'calibrib.ttf'))
    pdfmetrics.registerFont(TTFont('Calibri', 'calibri.ttf'))
    # starting stylesheet
    styleSheet = getSampleStyleSheet()
    # Create a frame
    text_frame = Frame(
        x1=2.0 * cm,  # From left 3
        y1=2 * cm,  # From bottom 1.5
        height=26 * cm, #25.25
        width=16.90 * cm, # 15.90
        showBoundary=0,
        id='text_frame')
    # colors used in the paragraph styles
    colors = {
        "darkBlue":Color(red=(68/255),green=(113/255),blue=(196/255)),
        "red":Color(red=(255/255),green=(0/255),blue=(0/255)),
        "lightgreen":Color(red=(111/255),green=(172/255),blue=(70/255)),
        "lightblue":Color(red=(0/255),green=(175/255),blue=(239/255)),
        "dark":Color(red=(0/255),green=(0/255),blue=(0/255)),
    } 
    # course style and prof paragraph indent
    indent = 40
    # Title style 
    Title = ParagraphStyle("title",
                            fontName="Calibri-Bold",
                            alignment=1,
                           fontSize=24,
                           parent=styleSheet['Heading2'],
                           textColor=Color.rgb(colors['darkBlue']))
    # Module style
    Module = ParagraphStyle("module",
                            fontName="Calibri-Bold",
                            alignment=0,
                           fontSize=24,
                           parent=styleSheet['Heading2'],
                           textColor=Color.rgb(colors['red']))
    # sous module style
    SousModule = ParagraphStyle("sous-module",
                            fontName="Calibri-Bold",
                           fontSize=24,
                           parent=styleSheet['Heading2'],
                           textColor=Color.rgb(colors['lightblue']))
    # prof style
    Prof = ParagraphStyle("prof",
                            fontName="Calibri-Bold",
                            leftIndent=indent,
                           fontSize=24,
                           parent=styleSheet['Heading2'],
                           textColor=Color.rgb(colors['lightgreen']))
    Bde = ParagraphStyle("BDE",
                            fontName="Calibri-Bold",
                            leftIndent=indent * 7,
                           fontSize=12,
                           parent=styleSheet['Normal'],
                           textColor=Color.rgb(colors['dark']))
    # course style 
    course = ParagraphStyle("course",
                            fontName="Calibri-Bold",
                            leftIndent=indent,
                            bulletFont="Symbol",
                           fontSize=12,
                           parent=styleSheet['Normal'],
                           textColor=Color.rgb(colors['dark']))
    
    L = [ 
        Image("main/static/home/bde.png",hAlign="CENTER",width=125,height=125),
        Paragraph(f"""<u>Recensement des cours S{level} ({schoolYear[0]}/{schoolYear[1]})</u><br/><br/>Mis à jour le {day}/{month}/{year} - {datetime.now(casablanca).strftime("%H:%M:%S")} .<br/>""", Title)
    ]
    L.append(Paragraph(f"<br/><br/>",Bde))
    for x in bde:
        L.append(Paragraph(f"{x}<br/>",Bde))
    L.append(Paragraph(f"<br/><br/>",Bde))
    # x-> text, y->type if 1 h1 if 2 h2 if 3 h3 if 4 todo
    for x,y in data:
      if y==1:
        L.append(Paragraph(f"<br/><u>{x.strip()}</u><br/>",Module))
      elif y==2:
        L.append(Paragraph(f"<br/><u>{x.strip()}</u><br/><br/>",SousModule))
      elif y==3:
        L.append(Paragraph(f"<br/>{x.strip()}<br/><br/>",Prof))
      elif y==4:
        L.append(Paragraph(f"{unicode} {x.strip()}<br/>",course))
    story = L  
    story.append(KeepTogether([]))
    doc = BaseDocTemplate(f"main/static/recensement/{id}/recensement.pdf", pagesize=A4,title="Recensement.pdf")
    frontpage = PageTemplate(id='FrontPage',frames=[text_frame])
    doc.addPageTemplates(frontpage)
    doc.build(story)