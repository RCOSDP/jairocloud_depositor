# -*- coding: utf-8 -*-

import json
import xml.etree.ElementTree as ET

# 現在jpcoar2.0のみ
metadata_list ={
    "jpcoar2.0":[
        "dc:title",
        "dcterms:alternative",
        "jpcoar:creator",
        "jpcoar:contributor",
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

# xml用namespace
namespace_list={"jpcoar2.0":{
    "xmlns:jpcoar":"https://github.com/JPCOAR/schema/blob/master/2.0/",
    "xmlns:dc":"http://purl.org/dc/elements/1.1/",
    "xmlns:dcterms":"http://purl.org/dc/terms/",
    "xmlns:datacite":"https://schema.datacite.org/meta/kernel-4/",
    "xmlns:oaire":"http://namespace.openaire.eu/schema/oaire/",
    "xmlns:dcndl":"http://ndl.go.jp/dcndl/terms/",
    "xmlns:rdf":"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance",
    "xsi:schemaLocation":"https://github.com/JPCOAR/schema/blob/master/2.0/ jpcoar_scm.xsd"
}}

# xml用roottag設定用
root_tag={"jpcoar2.0":"jpcoar:jpcoar"}

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

    # rootのタグ名とnamespaceを設定
    root = ET.Element(root_tag.get(kindofproperty,""))
    for key,value in namespace_list.get(kindofproperty,{}).items():
        root.set(key, value)
        
    json_data = item_metadata
    
    # kindofpropertyに対応するメタデータの項目を持ってくる。
    for title in metadata_list.get(kindofproperty, []):        
        properties = json_data.get(title, None)
        if not(properties):
            continue
        listtoxml(title, properties, root)

    # XMLデータを保存
    # tree = ET.ElementTree(root)
    # # item_register/tmp下にxmlファイルを書きだす
    # tree.write('modules/item_register/tmp/data.xml', encoding="utf-8", xml_declaration=True)
    xml_string = ET.tostring(root, encoding="utf-8", method="xml")
    
    return xml_string


