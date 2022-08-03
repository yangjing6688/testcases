*** Variables ***

###Network Policy Config##
&{XR_ROUTER_NW_01}                ssid_name=Router_XR_template                network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}
...                               auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}
&{BORADCAST_SSID_DEFAULT}=        WIFI0=Enable        WIFI1=Enable
&{OPEN_AUTHENTICATION_PROFILE0}   auth_type=Open    cwp_profile=&{OPEN_CWP}
&{OPEN_CWP}                       enable_cwp=Disable

&{CONFIG_PUSH_OPEN_NW_01}    ssid_name=Openauthsocial                 network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}   auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}

####Router Template Config###
&{ROUTER_TEMPLATE_CONFIG1}       router_model=${router1.model}  template_name=${router1.device_template}  interface_name=ETH2    new_port_type_config=&{PORT_TYPE_CONFIG1}   network_allocation_config=&{NETWORK_ALLOCATION_CONFIG1}
&{PORT_TYPE_CONFIG1}             port_type_name=test_trunk_xr   description=Trunk  port_status=Enable   port_usage_config=&{PORT_USAGE_CONFIG1}    mac_authentication=Disable  traffic_filter_settings=&{TRAFFIC_FILTER_DEFAULT}
&{NETWORK_ALLOCATION_CONFIG1}    vlan_object_config=&{VLAN_OBJECT_CONFIG1}  sub_network_config=&{SUB_NETWORK_CONFIG1}
&{VLAN_OBJECT_CONFIG1}           vlan_name=test_router_vlan   vlan_id=98
&{SUB_NETWORK_CONFIG1}           basic_config=&{BASIC_CONFIG}    advance_config=None
&{BASIC_CONFIG}                  sub_network_name=test_subnetwork   sub_network_description=test_subnetwork  network_type=Internal Use  unique_subnetwork=Enable  local_ip_address_space=30.1.1.0/24   gateway_options=firstip
&{SUB_NETWORK_ADVANCED_CONFIG1}  dhcp_status=enable  dhcp_server_as_branch_router=enable  lease_time=90400

&{PORT_USAGE_CONFIG1}       port_usage_type=Trunk   allowed_vlans=10-20
&{PORT_USAGE_CONFIG2}       port_usage_type=Access
&{PORT_USAGE_CONFIG3}       port_usage_type=Wan

&{TRAFFIC_FILTER_DEFAULT}   ssh=Enable    telnet=Disable   ping=Enable   snmp=Disable



