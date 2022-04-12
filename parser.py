import lxml.etree as ET
import base64
from sys import argv
import pdfkit
import imgkit

filename = argv[1].split(".")[0]

dom = ET.parse("{}.xml".format(filename))
root = dom.getroot()

for tag in root:
    if tag.tag.split("}")[1] == "AdditionalDocumentReference":
        for element in tag:
            if element.tag.split("}")[1] == "Attachment":
                data = base64.b64decode(element[0].text)
                open("{}.xslt".format(filename),"w+",encoding="utf-8").write(data.decode())

xslt = ET.parse("{}.xslt".format(filename))
transform = ET.XSLT(xslt)
newdom = transform(dom)
with open("{}_img.html".format(filename),'w') as file:
    file.write(ET.tostring(newdom, pretty_print=True).decode().replace("<title/>","").replace("800px","1000px").replace("width=\"800\"","width=\"1000\""))
    
with open("{}_pdf.html".format(filename),'w') as file:
    file.write(ET.tostring(newdom, pretty_print=True).decode().replace("<title/>","").replace("800px","1000px").replace("width=\"800\"","width=\"1000\""))

options = {
    'margin-top': '5',
    'margin-left': '5',
    'page-size':'A4',
    'encoding': "UTF-8"
}


pdfkit.from_file("{}_pdf.html".format(filename), "{}.pdf".format(filename),options=options)
imgkit.from_file("{}_img.html".format(filename), "{}.jpg".format(filename),options={ 'enable-smart-width': ''})
