# forge/spine.py
import xml.etree.ElementTree as ET
from zipfile import ZipFile
from pathlib import Path

def get_spine_html_files(epub_path: str) -> list:
    """
    Returns a list of XHTML/HTML file paths inside EPUB in spine order.
    """
    with ZipFile(epub_path, "r") as zf:
        # 1. Find content.opf via META-INF/container.xml
        container_xml = zf.read("META-INF/container.xml")
        root = ET.fromstring(container_xml)
        opf_path = root.find(".//{urn:oasis:names:tc:opendocument:xmlns:container}rootfile").attrib["full-path"]

        # 2. Parse content.opf
        opf_data = zf.read(opf_path)
        opf_root = ET.fromstring(opf_data)

        ns = {
            "opf": opf_root.tag.split("}")[0].strip("{")
        }

        # 3. Build manifest dictionary: id -> href
        manifest = {item.attrib["id"]: item.attrib["href"] for item in opf_root.findall(".//opf:manifest/opf:item", ns)}

        # 4. Iterate spine
        spine_files = []
        for itemref in opf_root.findall(".//opf:spine/opf:itemref", ns):
            idref = itemref.attrib["idref"]
            href = manifest[idref]
            # Normalize path relative to content.opf
            spine_files.append(str(Path(opf_path).parent / href))

        return spine_files
