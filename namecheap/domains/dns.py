from namecheap.connection import NamecheapConnection
from xml.etree import ElementTree
from namecheap.domains.domains import Domains
from urllib.parse import urlparse

class Dns(NamecheapConnection):

    def __init__(self, **kw_params):

        super(Dns, self).__init__(**kw_params)

    
    def set_hosts(self, domain=None, hostname=None, record_type='A',
            address=None, mx_pref='', email_type=None, TTL=1800):
        pass

    def get_hosts(self, domain=None):

        if domain is None:
            raise Exception("Empty domain!")

        sld = "rshll"
        tld = self.get_tld('rshll.net')

        response = self.__makerequest__(domain=domain, SLD=sld, TLD=tld,
                Command='namecheap.domains.dns.getHosts')
           
        xml_element = ElementTree.fromstring(response)
        ns = self.xml_namespace 
        hosts = ( xml_element
                .findall("{0}CommandResponse/{0}DomainDNSGetHostsResult/{0}host"
                    .format(ns)) )



    def get_tld(self, domain=None):
        """
        Returns tld part from a given domain 
        """
        if domain is None:
            raise Exception("empty domain")

        url_elements = urlparse(domain).path.split('.')

        parameters = self.parameters
        domains = Domains(url=self.url, **self.parameters)
        tld_list = domains.tlds_list()        

        for i in range(-len(url_elements), 0):
            last_i_elements = url_elements[i:]

            tld = '.'.join(last_i_elements)
            if tld in tld_list:
                return tld

        raise Exception("TLD not found!")


    def return_sld(self, domain=None):
        pass
