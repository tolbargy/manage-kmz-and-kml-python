from pykml import parser
from lxml import etree

def main():
    with open('resources/solo-punto.kml','r') as f:
        root = parser.parse(f)
    
    root.getroot().Placemark.name = 'cambia'

    with open('resources/output.kml', 'w') as output:
        output.write(etree.tostring(root,encoding='UTF-8', method='xml',pretty_print=True,xml_declaration=True).decode())
        
if __name__ == '__main__':
    main()