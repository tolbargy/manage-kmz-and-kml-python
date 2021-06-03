from io import BytesIO
import xml.etree.ElementTree as ET
import logging
import zipfile
import os

logging.getLogger().setLevel(logging.INFO)
path_kmz_original = 'resources/final.kmz'
path_kmz_tmp = 'resources/tmp.kmz'
name_file_kml = 'puntos.kml'
path_rutas = 'resources/solo-ruta.kml'
default_namespace = "http://www.opengis.net/kml/2.2"
ns = {'default': default_namespace}

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
                content = infile.read().decode()
                xml_final = procesar_agregacion_rutas(content)                                               
                outzip.writestr(inzipinfo.filename, xml_final)
            else:
               outzip.writestr(inzipinfo.filename, infile.read())

def procesar_agregacion_rutas(content):
    puntos_tree = ET.fromstring(content)
    element_document = puntos_tree.find(f"default:Document",ns)
    agregarDocumentRutaHaciaDocumentPunto(element_document)               

    ET.register_namespace('',default_namespace)
    stream = BytesIO()
    ET.ElementTree(puntos_tree).write(stream,encoding='UTF-8', method='xml',xml_declaration=True)
    xml_final = stream.getvalue().decode()
    return xml_final

def agregarDocumentRutaHaciaDocumentPunto(element_document_punto):
   ruta_tree = ET.parse(path_rutas)
   ruta_root = ruta_tree.getroot()
   elements_document_ruta = ruta_root.find('default:Document',ns)
   for element in elements_document_ruta:
      logging.info(f"Se agregó elemento {element}")
      element_document_punto.append(element)

if __name__ == '__main__':
    main()