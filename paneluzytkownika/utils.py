
from io import BytesIO, StringIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    # return HttpResponse(html)
    # result = StringIO()
    pdf = pisa.CreatePDF(BytesIO(html.encode('utf-8')), result)
    # pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    # pdf = pisa.pisaDocument(html, result, encoding='UTF-8')

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
