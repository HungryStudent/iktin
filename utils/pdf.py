import pdfkit
from jinja2 import Environment, FileSystemLoader

from config_parser import WKHTMLTOPDF_PATH

config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
options = {
    'page-size': 'A4',
    'encoding': "UTF-8",
    'margin-top': '0in',
    'margin-right': '0in',
    'margin-bottom': '0in',
    'margin-left': '0in'
}


def gen_doc(data):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("invoice_template.html")

    pdf_template = template.render(data)

    pdfkit.from_string(pdf_template, f'{data["invoice_id"]}.pdf', configuration=config, options=options)
