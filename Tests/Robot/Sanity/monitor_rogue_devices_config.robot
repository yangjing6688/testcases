*** Variables ***

############################ AP Template Config#################
&{AP_TEMPLATE_CONFIG}            wifi0_configuration=&{AP_TEMPLATE_CONFIG_1_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_CONFIG_1_WIFI1}

&{AP_TEMPLATE_CONFIG_1_WIFI0}    client_access=Disable    backhaul_mesh_link=Disable   sensor=Enable

&{AP_TEMPLATE_CONFIG_1_WIFI1}    client_access=Disable    backhaul_mesh_link=Disable   sensor=Enable

#######WIPS Configuartion#######################

&{WIPS_CONFIG_SETTINGS}         name=test_automation_wips   description=test_automation_wips   rougue_ap_detection=Enable      detect_ap_wired=Enable     detect_ap_mac_oui_basis=Disable   ssid_config=&{WIPS_SSID_CONFIG1}
...                             detect_client_form_adhoc=Disable     rougue_client_reporting=Enable      mitigation_mode=manual

&{WIPS_SSID_CONFIG1}             detect_ap_ssid_basis=Enable  allowed_ssid=test_automation_wips      authentication_type=OPEN


####WIPS WLAN CONFIG####
&{WIPS_OPEN_NW}             ssid_name=test_automation_wips                network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}
...                         auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}

&{WIPS_OPEN_ROGUE_NW}       ssid_name=test_automation_rogue                network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}
...                         auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}

&{OPEN_NW_01}               ssid_name=Openauthssid    network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}   auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}

&{BORADCAST_SSID_DEFAULT}=       WIFI0=Enable        WIFI1=Enable

&{OPEN_AUTHENTICATION_PROFILE0}     auth_type=Open    cwp_profile=&{OPEN_CWP}

&{OPEN_CWP}        enable_cwp=Disable