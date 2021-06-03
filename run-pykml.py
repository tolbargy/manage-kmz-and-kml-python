from io import BytesIO
from pykml import parser
from lxml import etree, objectify
import logging
import zipfile

KML = objectify.ElementMaker(annotate=False)
logging.getLogger().setLevel(logging.INFO)
path_kmz_original = 'resources/final.kmz'
path_kmz_tmp = 'resources/tmp.kmz'
name_file_kml = 'puntos.kml'
path_rutas = 'resources/solo-ruta.kml'
default_namespace = "http://www.opengis.net/kml/2.2"

def main():
    modificar_kml_y_volver_comprimir()

    with open('resources/solo-punto.kml','r') as f:
        punto_tree = parser.parse(f)
        punto_root = punto_tree.getroot()


    document_punto = KML.Document("")
    punto_root.append(document_punto)

    document_ruta = ruta_root.Document
    document_punto.append(document_ruta)

    with open('resources/output.kml', 'w') as output:
        resultado = etree.tostring(punto_tree,encoding='UTF-8', method='xml',pretty_print=True,xml_declaration=True).decode()
        output.write(resultado)                


def modificar_kml_y_volver_comprimir():
   with zipfile.ZipFile(path_kmz_original) as inzip, zipfile.ZipFile(path_kmz_tmp, "w") as outzip:
    for inzipinfo in inzip.infolist():
        with inzip.open(inzipinfo) as infile:
            if inzipinfo.filename == name_file_kml:                
                content = infile.read().decode()
                xml_final = procesar_agregacion_rutas(content)                                               
                outzip.writestr(inzipinfo.filename, xml_final)
            else:
               outzip.writestr(inzipinfo.filename, infile.read())

def procesar_agregacion_rutas(content):
    puntos_tree = parser.fromstring(content)
    element_document = puntos_tree.Document
    agregarDocumentRutaHaciaDocumentPunto(element_document)               

    etree.register_namespace('',default_namespace)
    stream = BytesIO()
    etree.ElementTree(puntos_tree).write(stream,encoding='UTF-8', method='xml',xml_declaration=True)
    xml_final = stream.getvalue().decode()
    return xml_final

def agregarDocumentRutaHaciaDocumentPunto(element_document_punto):    
    with open(path_rutas,'r') as f:
        ruta_tree = parser.parse(f)
        ruta_root = ruta_tree.getroot()

        elements_document_ruta = ruta_root.Document
        for element in elements_document_ruta:
            logging.info(f"Se agregó elemento {element}")
            element_document_punto.append(element)
            
if __name__ == '__main__':
    main()