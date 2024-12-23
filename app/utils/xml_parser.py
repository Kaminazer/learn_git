import xml.etree.ElementTree as ET

def parse_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        texts = [elem.text.strip() for elem in root.findall(".//text") if elem.text]
        return texts
    except Exception as e:
        raise ValueError(f"Error parsing XML: {e}")