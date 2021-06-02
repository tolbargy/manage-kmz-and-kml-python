import xml.etree.ElementTree as ET
import logging

logging.getLogger().setLevel(logging.INFO)
path_solo_punto = 'resources/solo-punto.kml'
path_solo_ruta = 'resources/solo-ruta.kml'
default_namespace = "http://www.opengis.net/kml/2.2"
ns = {'default': default_namespace}

def main():      
   punto_tree = ET.parse(path_solo_punto)
   ruta_tree = ET.parse(path_solo_ruta)
   punto_root = punto_tree.getroot()
   ruta_root = ruta_tree.getroot()

   element_document = crearElementoHijo(punto_root,'Document')
   moverElemento(punto_root,element_document,'Placemark')
   guardar_kml(punto_tree,path_solo_punto)
   
def crearElementoHijo(element_parent: ET.Element, name_children: str):
   exist_element_children = element_parent.find(f"default:{name_children}",ns)
   if exist_element_children is None:      
      element_children = element_parent.makeelement(name_children,{})
      element_children.text = ' '
      element_parent.append(element_children)      
      logging.info(f"Elemento <{name_children}> creado en el padre {element_parent}")
      return element_children
   else:
      logging.info(f"Ya existe el elemento <{name_children}> en el padre {element_parent}")
      return exist_element_children

def moverElemento(element_old_parent: ET.Element, element_new_parent: ET.Element, name_children: str):
      element_children = element_old_parent.find(f"default:{name_children}",ns)
      if element_children is None:
         logging.info(f"No se encuentra el elemento <{name_children}> en el padre {element_old_parent}")
      else:
         element_new_parent.append(element_children)
         element_old_parent.remove(element_children)
         logging.info(f"Se ha movido el elemento <{name_children}> al nuevo padre {element_new_parent}")

def guardar_kml(tree,path_file):
   ET.register_namespace('',default_namespace)
   tree.write(
      path_file,
      encoding='UTF-8',                    
      xml_declaration=True,
      method='xml')

if __name__ == '__main__':
    main()