import xml.etree.ElementTree as ET

class gini:
    def __init__(self):
        ""

    def parse_file(self,file):
        trees = ET.parse(file)
        root = trees.getroot()
        for tree in root.findall('tree'):
            for split in tree:
                for feature in split:
                    print feature