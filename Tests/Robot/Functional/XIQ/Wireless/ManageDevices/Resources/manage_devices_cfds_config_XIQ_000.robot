*** Variables ***

############################ AP Template Config#################
&{AP_TEMPLATE_CONFIG}            wifi0_configuration=&{AP_TEMPLATE_CONFIG_1_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_CONFIG_1_WIFI1}

&{AP_TEMPLATE_CONFIG_1_WIFI0}    radio_profile=radio_ng_11ax-2g     client_access=Enable    backhaul_mesh_link=Enable   sensor=Disable

&{AP_TEMPLATE_CONFIG_1_WIFI1}    radio_profile=radio_ng_11ax-5g     client_access=Enable    backhaul_mesh_link=Enable   sensor=Disable


####NETWORK POLICY CONFIG####
&{CONFIG_PUSH_OPEN_NW_01}    ssid_name=default_network_ssid      network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}   auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}
&{OPEN_NW_01}                ssid_name=Openauthssid              network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}   auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}

&{BORADCAST_SSID_DEFAULT}=       WIFI0=Enable        WIFI1=Enable

&{OPEN_AUTHENTICATION_PROFILE0}     auth_type=Open    cwp_profile=&{OPEN_CWP}

&{OPEN_CWP}        enable_cwp=Disable

####NETWORK POLICY CONFIG####
&{OPEN_NW_DUAL_RADIO_01}        ssid_name=Openauthdualradio    network_type=standard    ssid_profile=&{BORADCAST_SSID_WIFI0}   auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}

&{BORADCAST_SSID_WIFI0}=       WIFI0=Enable        WIFI1=Disable

&{OPEN_AUTHENTICATION_PROFILE0}     auth_type=Open    cwp_profile=&{OPEN_CWP}

&{OPEN_CWP}        enable_cwp=Disable



&{OPEN_NW_DUAL_RADIO_02}        ssid_name=Openauthdualradiosecondnw    network_type=standard    ssid_profile=&{BORADCAST_SSID_WIFI1}   auth_profile=&{OPEN_AUTHENTICATION_PROFILE1}

&{BORADCAST_SSID_WIFI1}=       WIFI0=Disable        WIFI1=Enable

&{OPEN_AUTHENTICATION_PROFILE1}     auth_type=Open    cwp_profile=&{OPEN_CWP}

&{OPEN_CWP}        enable_cwp=Disable