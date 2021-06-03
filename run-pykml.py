from pykml import parser
from lxml import etree
import logging
import zipfile
import os

logging.getLogger().setLevel(logging.INFO)
path_kmz_original = 'resources/final.kmz'
path_kmz_tmp = 'resources/tmp.kmz'
name_file_kml = 'puntos.kml'
path_rutas = 'resources/solo-ruta.kml'

def main():
    modificar_kml_y_volver_comprimir()
    eliminar_antiguo_kmz_y_renombrar_nuevo_kmz()

def eliminar_antiguo_kmz_y_renombrar_nuevo_kmz():
    os.remove(path_kmz_original)
    os.rename(path_kmz_tmp,path_kmz_original)

def modificar_kml_y_volver_comprimir():
   with zipfile.ZipFile(path_kmz_original) as inzip, zipfile.ZipFile(path_kmz_tmp, "w") as outzip:
    for inzipinfo in inzip.infolist():
        with inzip.open(inzipinfo) as infile:
            if inzipinfo.filename == name_file_kml:                
                content = infile.read()
                xml_final = procesar_agregacion_rutas(content)                                               
                outzip.writestr(inzipinfo.filename, xml_final)
            else:
               outzip.writestr(inzipinfo.filename, infile.read())

def procesar_agregacion_rutas(content):
    puntos_tree = parser.fromstring(content)
    element_document = puntos_tree.Document
    agregarDocumentRutaHaciaDocumentPunto(element_document)               

    xml_final= etree.tostring(puntos_tree,pretty_print=True,xml_declaration=True, encoding='UTF-8')
    return xml_final

def agregarDocumentRutaHaciaDocumentPunto(element_document_punto):    
    with open(path_rutas,'r',encoding="utf8") as f:
        ruta_tree = parser.parse(f)        
        ruta_root = ruta_tree.getroot()

        elements_document_ruta = ruta_root.Document.getchildren()
        for element in elements_document_ruta:
            logging.info(f"Se agregó elemento {element}")
            element_document_punto.append(element)
            
if __name__ == '__main__':
    main()