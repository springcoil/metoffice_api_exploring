from data_extract import Manager

t = Manager()

def test_extract_from_api():
    extract = t.extract_from_api()
    assert isinstance(extract, tuple)

def test_json_extract():
    dictionary = t.convert_to_dictionary()
    assert isinstance(dictionary, dict)