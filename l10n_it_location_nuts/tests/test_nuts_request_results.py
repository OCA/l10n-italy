from json import dumps

from requests.models import Response

NUTS = [
    {
        "s": {"type": "uri", "value": "http://data.europa.eu/nuts/code/IT"},
        "code": {"type": "literal", "value": "IT"},
        "region_name": {"type": "literal", "value": "IT Italia"},
        "level": {"type": "literal", "value": "0"},
    },
    {
        "s": {"type": "uri", "value": "http://data.europa.eu/nuts/code/IT"},
        "code": {"type": "literal", "value": "IT"},
        "region_name": {"type": "literal", "value": "IT Italia"},
        "level": {"type": "literal", "value": "0"},
    },
    {
        "s": {"type": "uri", "value": "http://data.europa.eu/nuts/code/ITC"},
        "code": {"type": "literal", "value": "ITC"},
        "region_name": {"type": "literal", "value": "ITC Nord-Ovest"},
        "level": {"type": "literal", "value": "1"},
        "parent": {"type": "literal", "value": "IT"},
    },
    {
        "s": {"type": "uri", "value": "http://data.europa.eu/nuts/code/ITC"},
        "code": {"type": "literal", "value": "ITC"},
        "region_name": {"type": "literal", "value": "ITC Nord-Ovest"},
        "level": {"type": "literal", "value": "1"},
        "parent": {"type": "literal", "value": "IT"},
    },
    {
        "s": {"type": "uri", "value": "http://data.europa.eu/nuts/code/ITF"},
        "code": {"type": "literal", "value": "ITF"},
        "region_name": {"type": "literal", "value": "ITF Sud"},
        "level": {"type": "literal", "value": "1"},
        "parent": {"type": "literal", "value": "IT"},
    },
    {
        "s": {"type": "uri", "value": "http://data.europa.eu/nuts/code/ITH"},
        "code": {"type": "literal", "value": "ITH"},
        "region_name": {"type": "literal", "value": "ITH Nord-Est"},
        "level": {"type": "literal", "value": "1"},
        "parent": {"type": "literal", "value": "IT"},
    },
    {
        "s": {"type": "uri", "value": "http://data.europa.eu/nuts/code/ITI"},
        "code": {"type": "literal", "value": "ITI"},
        "region_name": {"type": "literal", "value": "ITI Centro (IT)"},
        "level": {"type": "literal", "value": "1"},
        "parent": {"type": "literal", "value": "IT"},
    },
    {
        "s": {"type": "uri", "value": "http://data.europa.eu/nuts/code/ITI4"},
        "code": {"type": "literal", "value": "ITI4"},
        "region_name": {"type": "literal", "value": "ITI4 Lazio"},
        "level": {"type": "literal", "value": "2"},
        "parent": {"type": "literal", "value": "ITI"},
    },
    {
        "s": {"type": "uri", "value": "http://data.europa.eu/nuts/code/ITI43"},
        "code": {"type": "literal", "value": "ITI43"},
        "region_name": {"type": "literal", "value": "ITI43 Roma"},
        "level": {"type": "literal", "value": "3"},
        "parent": {"type": "literal", "value": "ITI4"},
    },
    {
        "s": {"type": "uri", "value": "http://data.europa.eu/nuts/code/ITI44"},
        "code": {"type": "literal", "value": "ITI44"},
        "region_name": {"type": "literal", "value": "ITI44 Latina"},
        "level": {"type": "literal", "value": "3"},
        "parent": {"type": "literal", "value": "ITI4"},
    },
    {
        "s": {"type": "uri", "value": "http://data.europa.eu/nuts/code/ITZ"},
        "code": {"type": "literal", "value": "ITZ"},
        "region_name": {"type": "literal", "value": "ITZ Extra-Regio NUTS 1"},
        "level": {"type": "literal", "value": "1"},
        "parent": {"type": "literal", "value": "IT"},
    },
    {
        "s": {"type": "uri", "value": "http://data.europa.eu/nuts/code/ITZ"},
        "code": {"type": "literal", "value": "ITZ"},
        "region_name": {"type": "literal", "value": "ITZ Extra-Regio NUTS 1"},
        "level": {"type": "literal", "value": "1"},
        "parent": {"type": "literal", "value": "IT"},
    },
    {
        "s": {"type": "uri", "value": "http://data.europa.eu/nuts/code/ITZZ"},
        "code": {"type": "literal", "value": "ITZZ"},
        "region_name": {"type": "literal", "value": "ITZZ Extra-Regio NUTS 2"},
        "level": {"type": "literal", "value": "2"},
        "parent": {"type": "literal", "value": "ITZ"},
    },
    {
        "s": {"type": "uri", "value": "http://data.europa.eu/nuts/code/ITZZZ"},
        "code": {"type": "literal", "value": "ITZZZ"},
        "region_name": {"type": "literal", "value": "ITZZZ Extra-Regio NUTS 3"},
        "level": {"type": "literal", "value": "3"},
        "parent": {"type": "literal", "value": "ITZZ"},
    },
]


def create_response_ok():
    response = Response()
    response.code = "200"
    response.status_code = 200
    content = {
        "head": {},
        "results": {"distinct": False, "ordered": True, "bindings": NUTS},
    }
    response._content = dumps(content).encode()
    return response
