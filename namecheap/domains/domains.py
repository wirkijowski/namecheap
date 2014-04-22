from ..connection import NamecheapConnection
from xml.etree import ElementTree

class Domains(NamecheapConnection):

    def __init__(self, **kw_params):

        super(Domains, self).__init__(**kw_params)


    def tlds_list(self):
        return list(self.get_tld_list()['Tlds'].keys())

    def get_tld_list(self):
        """
        Returns all top level domains available at Namecheap

        {
            'Error': None,
            'Tlds': {
                '<tld_name>': {},
                '<tld_name>': {},
                ...
                },
        }

        """
        return_tlds = {
                'Error': None,
                'Tlds': {},
                }
        response = ( self
                .__makerequest__(
                    Command='namecheap.domains.gettldlist') )

        xml_element = ElementTree.fromstring(response)
        ns = self.xml_namespace
       
        tlds = ( xml_element
                .findall("{0}CommandResponse/{0}Tlds/{0}Tld"
                    .format(ns)) )

        if xml_element.find("{0}Errors/{0}Error"): 
            return_tlds['Error'] = ( (xml_element
                .find("{0}Errors/{0}Error".format(ns))).text)
            
        for tld in tlds:
            return_tlds['Tlds'][tld.attrib['Name']] = {}

        return return_tlds


