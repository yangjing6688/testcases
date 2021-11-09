class SuiteVariable:

    def __init__(self):
        # Initialise required variables globally
        self.fa_mode_server = 'Server'
        self.fa_mode_proxy = 'Proxy'
        self.fa_mode_client = 'Client'
        self.server_loopback_vlan_name = 'SYS_BGP_LO0'
        self.fa_client_vlan_id = '11'
        self.fa_client_vlan_nsi = '11111'
        self.isc_vlan = 'isc'
        self.isc_vlan_id = '4001'
        self.isc_vlan_ipaddr_a = '1.1.1.1'
        self.isc_vlan_ipaddr_b = '1.1.1.2'
        self.isc_vlan_ipaddr_mask = '255.255.255.0'
        self.mlag_peer_name_a = 's1'
        self.mlag_peer_name_b = 's2'
        self.mlag_peer_id = '101'
        self.policy_profile_id = '1'
        self.policy_profile_name = 'test'
        self.policy_vlan_id = '33'
        self.policy_vlan_nsi = '33333'
