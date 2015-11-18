import urllib.request
import json

URL = ('http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/352817'
      + '?res=3hourly&key=5d3c4660-9042-46c3-8fd3-2a408d6c0fc2')


class Manager(object):
    def __init__(self):
        self.data_dict = None

    def _call_api(self, path):
        """
        Private method
        :param path: This is our URL string
        :return: returns a decoded response from the URL
        """
        response = urllib.request.urlopen(path)
        try:
            data = response.read()
        except ValueError:
            raise Exception("DataPoint has not returned any data" +
                            "this could be due to an incorrect API key")
        datadecoded = data.decode('utf-8')
        return datadecoded

    def convert_to_dictionary(self):
        """
        Converts JSON data to a dictionary object
        :param self:
        :return: python dictionary
        """
        json_from_api = self._call_api(path=URL)
        data_dict = json.loads(json_from_api)
        if not isinstance(data_dict, dict):
            raise ValueError("Not successfully converted into a dictionary, check API key")
        return data_dict

    def extraction_from_json(self):
        """
        A function for extracting from the JSON of the Datapoint api
        This is a heavily nested JSON API
        :return: (date, day, time, temperature, location)
        """
        data_dic = self.convert_to_dictionary()
        date = data_dic['SiteRep']['DV']['dataDate']
        period = data_dic['SiteRep']['DV']['Location']['Period'][0]
        day = period['value']
        time = period['Rep'][0]['$']
        temperature = int((period['Rep'][0]['T']))
        location = (data_dic['SiteRep']['DV']['Location']['name'])
        return (date, day, time, temperature, location)

    def extract_from_api(self):
        """
        Calls all private functions
        :return: json_extract - consisting of date, day, time, temperature and location
        """
        convert_to_dict = self.convert_to_dictionary()
        json_extract = self.extraction_from_json()
        return json_extract


if __name__ == "__main__":
    print("Extract", Manager().extraction_from_json())
    print("Current Weather in Newry", Manager().extract_from_api())
