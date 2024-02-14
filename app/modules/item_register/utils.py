# -*- coding: utf-8 -*-

import json
import xml.etree.ElementTree as ET

# 現在jpcoar2.0のみ
metadata_list ={
    "jpcoar2.0":[
        "dc:title",
        "dcterms:alternative",
        "jpcoar:creator",
        "dcterms:accessRights",
        "dc:rights",
        "jpcoar:rightsHolder",
        "jpcoar:subject",
        "datacite:description",
        "dc:publisher",
        "datacite:date",
        "dcterms:date",
        "dc:language",
        "dc:type",
        "datacite:version",
        "oaire:version",
        "jpcoar:identifier",
        "jpcoar:identifierRegistration",
        "jpcoar:relation",
        "dcterms:temporal",
        "datacite:geoLocation",
        "jpcoar:fundingReference",
        "jpcoar:sourceIdentifier",
        "jpcoar:sourceTitle",
        "jpcoar:volume",
        "jpcoar:issue",
        "jpcoar:numPages",
        "jpcoar:pageStart",
        "jpcoar:pageEnd",
        "dcndl:dissertationNumber",
        "dcndl:degreeName",
        "dcndl:dateGranted",
        "jpcoar:degreeGrantor",
        "jpcoar:conference",
        "dcndl:edition",
        "dcndl:volumeTitle",
        "dcndl:originalLanguage",
        "dcterms:extent",
        "jpcoar:format",
        "jpcoar:holdingAgent",
        "jpcoar:datasetSeries",
        "jpcoar:file",
        "jpcoar:catalog"]
}

def dicttoxmlforsword(kindofproperty, item_metadata):
    def listtoxml(property_key, property_value, root):
        for proper in property_value:
            child = ET.SubElement(root, property_key)
            for proper_key, proper_value in proper.items():
                # strならxmlに値を入力する。
                if isinstance(proper_value, str):
                    # リストに対応するキーとキーが一致するならそれは値
                    if proper_key==property_key:
                        child.text = proper_value
                    # リストに対応するキーでないならそれは属性
                    else:
                        child.set(proper_key, proper_value)
                # listならxmlを入れ子にする。
                elif isinstance(proper_value, list):
                    listtoxml(proper_key, proper_value, child)

    root = ET.Element('jpcoar:jpcoar')
    json_data = item_metadata
    
    # kindofpropertyに対応するメタデータの項目を持ってくる。
    for title in metadata_list.get(kindofproperty, []):        
        properties = json_data.get(title, None)
        if not(properties):
            continue
        listtoxml(title, properties, root)

    # XMLデータを保存
    tree = ET.ElementTree(root)
    # 現在はitem_register/tmp下に配置する
    tree.write('modules/item_register/tmp/data.xml', encoding="utf-8", xml_declaration=True)
    return tree


