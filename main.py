import xml.etree.ElementTree as ET

def main():
   punto_tree = ET.parse('ejemplos/punto.kml')
   coordenadas_tree = ET.parse('ejemplos/coordenadas.kml')

   punto_tree_root = punto_tree.getroot()
   coordenadas_tree = coordenadas_tree.getroot()

   # Dictionary namespaces
   ns = {'default': 'http://www.opengis.net/kml/2.2'}
   
   print(punto_tree_root.find('default:Placemark',ns))

if __name__ == '__main__':
    main()