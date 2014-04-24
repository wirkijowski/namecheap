from namecheap.connection import NamecheapConnection
from xml.etree import ElementTree
from namecheap.domains.domains import Domains
from urllib.parse import urlparse

class Dns(NamecheapConnection):

    def __init__(self, **kw_params):
        super(Dns, self).__init__(**kw_params)
        self.record_types = ( ['A', 'AAAA', 'CNAME', 'MX', 'MXE', 'TXT', 'URL',
            'URL301', 'FRAME'] )
        self.email_types = ['MXE', 'MX', 'FWD', 'OX']
        self.host_records = []
    
    def add_host(self, hostname=None, record_type='A',
            address=None, mx_pref=None, TTL=1800):

        """
        Prepares dns request params for given host
        """
        
        if record_type not in self.record_types:
            raise Exception("Unknown record type ", record_type)

        host = {
                "RecordType": record_type,
                "HostName": hostname,
                "Address": address,
                "TTL": TTL,
                }

        if mx_pref is not None:
            host["MXpref1"] = mx_pref
        
        self.host_records.append(host)

    def set_hosts(self, domain=None, email_type=None):

        """
        Sets dns record for given host. One host per request
        """
        
        sld, tld = self.return_sld_tld(domain)

        if email_type is not None and email_type not in self.email_types:
            raise Exception("Unknown email type ", email_type)

        request_params = {
                'SLD': sld,
                'TLD': tld,
                }

        if email_type is not None:
            request_params['EmailType'] = email_type

        for n in range(len(self.host_records)):
            #print(n)
            host = self.host_records.pop()
            #print(host)
            for key, value in host.items():
                request_params[key + "{0}".format(n+1)] = value
        response = ( self.__makerequest__(Command='namecheap.domains.dns.setHosts',
                **request_params) )
        #print(response) 

    def get_hosts(self, domain=None):

        if domain is None:
            raise Exception("Empty domain!")
        #print("self.parameteres na poczatku get_hosts")
        #print(self.parameters)
        sld, tld = self.return_sld_tld(domain)

        response = self.__makerequest__(domain=domain, SLD=sld, TLD=tld,
                Command='namecheap.domains.dns.getHosts')
           
       # print(response)
        xml_element = ElementTree.fromstring(response)
        ns = self.xml_namespace 
        hosts = ( xml_element
                .findall("{0}CommandResponse/{0}DomainDNSGetHostsResult/{0}host"
                    .format(ns)) )
        

    def return_sld_tld(self, domain=None):
        """
        Returns sld, tld 
        """
        if domain is None:
            raise Exception("empty domain")

        url_parse = urlparse(domain)
        if url_parse.scheme == '' or url_parse.hostname is None:
            url_elements = url_parse.path.split('.')
        else:
            url_elements = url_parse.hostname.split('.')

        # need to know what TLD are available at Namecheap
        #print("new domain object")
        #print(self.parameters)
        domains = Domains(url=self.url, **self.parameters)
        tld_list = domains.tlds_list()        

        for i in range(-len(url_elements), 0):
            last_i_elements = url_elements[i:]

            tld = '.'.join(last_i_elements)
            if tld in tld_list:
                sld = '.'.join(url_elements[:i])
                return sld, tld

        raise Exception("TLD not found!")




