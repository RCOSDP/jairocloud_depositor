from depositor_item_register.utils import dicttoxmlforsword

def test_dicttoxmlforsword():
    test_data={
    "dc:title": [{
            "dc:title": "test",
            "xml:lang": "fr"
        }],
    "dc:type": [{
            "dc:type": "data paper",
            "rdf:resource": "http://purl.org/coar/resource_type/c_beb9"
        }],
    "datacite:geoLocation":[{
        "datacite:geoLocationPoint": [
            {
                "datacite:pointLongitude": "経度",
                "datacite:pointLatitude": "緯度"
            }
        ],
        "datacite:geoLocationBox": [
            {
                "datacite:westBoundLongitude": "西部経度",
                "datacite:eastBoundLongitude": "東部経度",
                "datacite:southBoundLongitude": "南部緯度",
                "datacite:northBoundLongitude": "北部緯度"
            }
        ],
        "datacite:geoLocationPlace": [
            {
                "datacite:geoLocationPlace": "位置情報（自由記述）"
            }
        ]
    }],
    "jpcoar:file":[{
        "filename": "metadata.pdf",
        "jpcoar:mimeType": "application/pdf",
        "jpcoar:URI": [
            {
                "jpcoar:URI": "data/contentfiles/metadata.pdf",
                "label": "metadata.pdf",
                "objectType": "other"
            }
        ],
        "jpcoar:extent": [
            {
                "jpcoar:extent": "1 KB"
            }
        ],
        "jpcoar:test":{}
    }]
    }
    result = dicttoxmlforsword("jpcoar2.0", test_data).decode("utf-8")
    assert result == '<jpcoar:jpcoar xmlns:jpcoar="https://github.com/JPCOAR/schema/blob/master/2.0/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:datacite="https://schema.datacite.org/meta/kernel-4/" xmlns:oaire="http://namespace.openaire.eu/schema/oaire/" xmlns:dcndl="http://ndl.go.jp/dcndl/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="https://github.com/JPCOAR/schema/blob/master/2.0/ jpcoar_scm.xsd"><dc:title xml:lang="fr">test</dc:title><dc:type rdf:resource="http://purl.org/coar/resource_type/c_beb9">data paper</dc:type><datacite:geoLocation><datacite:geoLocationPoint><datacite:pointLongitude>経度</datacite:pointLongitude><datacite:pointLatitude>緯度</datacite:pointLatitude></datacite:geoLocationPoint><datacite:geoLocationBox><datacite:westBoundLongitude>西部経度</datacite:westBoundLongitude><datacite:eastBoundLongitude>東部経度</datacite:eastBoundLongitude><datacite:southBoundLongitude>南部緯度</datacite:southBoundLongitude><datacite:northBoundLongitude>北部緯度</datacite:northBoundLongitude></datacite:geoLocationBox><datacite:geoLocationPlace>位置情報（自由記述）</datacite:geoLocationPlace></datacite:geoLocation><jpcoar:file filename="metadata.pdf"><jpcoar:mimeType>application/pdf</jpcoar:mimeType><jpcoar:URI label="metadata.pdf" objectType="other">data/contentfiles/metadata.pdf</jpcoar:URI><jpcoar:extent>1 KB</jpcoar:extent></jpcoar:file></jpcoar:jpcoar>'