*** Variables ***

############################ AP Template Config#################
&{AP_TEMPLATE_CONFIG}            wifi0_configuration=&{AP_TEMPLATE_CONFIG_1_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_CONFIG_1_WIFI1}     wifi2_configuration=&{AP_TEMPLATE_CONFIG_1_WIFI2}

&{AP_TEMPLATE_CONFIG_1_WIFI0}    client_access=Enable    backhaul_mesh_link=Enable   sensor=Disable

&{AP_TEMPLATE_CONFIG_1_WIFI1}    client_access=Enable    backhaul_mesh_link=Enable   sensor=Disable

&{AP_TEMPLATE_CONFIG_1_WIFI2}    radio_status=Enable     primary_server_ip=1.1.1.1    primary_server_port=11

#######WIPS Configuartion#######################

&{WIPS_CONFIG_SETTINGS}         name=${WIPS_POLICY_NAME}   description=${WIPS_POLICY_NAME}   wireless_threat_detection=Enable     rougue_ap_detection=Enable      detect_ap_wired=Enable     detect_ap_mac_oui_basis=Disable   ssid_config=&{WIPS_SSID_CONFIG1}
...                             detect_client_form_adhoc=Disable     rougue_client_reporting=Enable      mitigation_mode=manual

&{WIPS_SSID_CONFIG1}             detect_ap_ssid_basis=Enable  allowed_ssid=${SSID_NAME}      authentication_type=OPEN


####WIPS WLAN CONFIG####
&{ADSP_OPEN_NW}             ssid_name=${SSID_NAME}                network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}
...                         auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}

&{OPEN_NW_01}               ssid_name=Openauthssid    network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}   auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}

&{BORADCAST_SSID_DEFAULT}=       WIFI0=Enable        WIFI1=Enable

&{OPEN_AUTHENTICATION_PROFILE0}     auth_type=Open    cwp_profile=&{OPEN_CWP}

&{OPEN_CWP}        enable_cwp=Disable


####DoS DEAUTH CONFIG#########

&{OPEN_NW_02}               ssid_name=${SSID_NAME2}    network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}   auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}

&{BORADCAST_SSID_DEFAULT}=       WIFI0=Enable        WIFI1=Enable

&{OPEN_AUTHENTICATION_PROFILE0}     auth_type=Open    cwp_profile=&{OPEN_CWP}

&{OPEN_CWP}        enable_cwp=Disable