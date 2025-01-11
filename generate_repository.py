import os
import hashlib
import xml.etree.ElementTree as ET

def generate_addons_xml():
    """Generate addons.xml file from all addon.xml files"""
    root = ET.Element("addons")

    # Add repository addon
    repo_addon = ET.parse("repository.kodi-jap-subs/addon.xml").getroot()
    root.append(repo_addon)

    # Add subtitle addon
    subtitle_addon = ET.parse("service.subtitles.jplearn/addon.xml").getroot()
    root.append(subtitle_addon)

    # Write addons.xml
    tree = ET.ElementTree(root)
    tree.write("addons.xml", encoding="UTF-8", xml_declaration=True)

    # Generate MD5
    with open("addons.xml", "rb") as f:
        md5 = hashlib.md5(f.read()).hexdigest()

    with open("addons.xml.md5", "w") as f:
        f.write(md5)

if __name__ == "__main__":
    generate_addons_xml()
