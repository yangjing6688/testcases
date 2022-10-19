*** Variables ***

############################ AP Template Config#################
&{AP_TEMPLATE_CONFIG}            wifi0_configuration=&{AP_TEMPLATE_CONFIG_1_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_CONFIG_1_WIFI1}

&{AP_TEMPLATE_CONFIG_1_WIFI0}    client_access=Enable    backhaul_mesh_link=Enable   sensor=Disable

&{AP_TEMPLATE_CONFIG_1_WIFI1}    client_access=Enable    backhaul_mesh_link=Enable   sensor=Disable

####Location WLAN CONFIG####
&{LOCATION_OPEN_NW}              ssid_name=${SSID_NAME}                network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}
...                              auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}

&{OPEN_NW_01}                    ssid_name=Openauthssid    network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}   auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}

&{BORADCAST_SSID_DEFAULT}=       WIFI0=Enable        WIFI1=Enable

&{OPEN_AUTHENTICATION_PROFILE0}     auth_type=Open    cwp_profile=&{OPEN_CWP}

&{OPEN_CWP}        enable_cwp=Disable


