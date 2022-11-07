*** Variables ***

############################ AP Template Config#################
&{AP_TEMPLATE_CONFIG}            wifi0_configuration=&{AP_TEMPLATE_CONFIG_1_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_CONFIG_1_WIFI1}     wifi2_configuration=&{AP_TEMPLATE_CONFIG_1_WIFI2}

&{AP_TEMPLATE_CONFIG_1_WIFI0}    client_access=Enable    backhaul_mesh_link=Enable   sensor=Disable

&{AP_TEMPLATE_CONFIG_1_WIFI1}    client_access=Enable    backhaul_mesh_link=Enable   sensor=Disable

&{AP_TEMPLATE_CONFIG_1_WIFI2}    radio_status=Enable     primary_server_ip=1.1.1.1    primary_server_port=11

### For Regression ###
&{AP_DUAL_TEMPLATE_CONFIG}       wifi0_configuration=&{AP_TEMPLATE_CONFIG_2_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_CONFIG_2_WIFI1}

&{AP_WIFI6_TEMPLATE_CONFIG}      wifi0_configuration=&{AP_TEMPLATE_CONFIG_1_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_CONFIG_1_WIFI1}     wifi2_configuration=&{AP_TEMPLATE_CONFIG_WIFI2_WIFI6}

&{AP_TEMPLATE_CONFIG_2_WIFI0}    client_access=Enable    backhaul_mesh_link=Disable   sensor=Disable

&{AP_TEMPLATE_CONFIG_2_WIFI1}    client_access=Enable    backhaul_mesh_link=Disable   sensor=Disable

&{AP_TEMPLATE_CONFIG_WIFI2_WIFI6}    radio_status=Enable     client_access=Disable    backhaul_mesh_link=Disable    sensor=Enable


#######WIPS Configuartion#######################

&{WIPS_CONFIG_SETTINGS}         name=${WIPS_POLICY_NAME}   description=${WIPS_POLICY_NAME}   wireless_threat_detection=Enable     rougue_ap_detection=Enable      detect_ap_wired=Enable     detect_ap_mac_oui_basis=Disable   ssid_config=&{WIPS_SSID_CONFIG1}
...                             detect_client_form_adhoc=Disable     rougue_client_reporting=Enable      mitigation_mode=manual

&{WIPS_SSID_CONFIG1}             detect_ap_ssid_basis=Enable  allowed_ssid=${SSID_NAME}      authentication_type=OPEN

####WIPS WLAN CONFIG####
&{ADSP_OPEN_NW}             ssid_name=${SSID_NAME}                network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}
...                         auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}

&{ADSP_ONPREM_OPEN_NW}      ssid_name=${SSID_NAME_ONPREM}         network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}
...                         auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}

&{ADSP_WIFI6_OPEN_NW}       ssid_name=${SSID_NAME_WIFI6}          network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}
...                         auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}

&{ADSP_DUAL_OPEN_NW}        ssid_name=${SSID_NAME_DUAL}           network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}
...                         auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}

&{OPEN_NW_01}               ssid_name=Openauthssid    network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}   auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}

&{BORADCAST_SSID_DEFAULT}=       WIFI0=Enable        WIFI1=Enable

&{OPEN_AUTHENTICATION_PROFILE0}     auth_type=Open    cwp_profile=&{OPEN_CWP}

&{OPEN_CWP}        enable_cwp=Disable

####PREETI_CONFIG####

############################ Network Policy Config#################
&{ADESS_NWP}                          ssid_name=${SSID_NAME}      network_type=standard    ssid_profile=&{BROADCAST_SSID}   auth_profile=&{AUTHENTICATION_OPEN}
&{BROADCAST_SSID}=                  WIFI0=Enable                WIFI1=Enable
&{AUTHENTICATION_OPEN}     auth_type=Open    cwp_profile=&{OPEN_CWP}
&{OPEN_CWP}        enable_cwp=Disable

#######On Prem ADSP server Configuartion#######################
&{ON_PREM_ADSP_SERVER_IP_CONFIG}    primary_server_ip=10.234.124.251    primary_server_port=443     secondary_server_ip=9.9.1.1    secondary_server_port=443

### Operator account details
${OPERATOR_EMAIL}                 automationadessreg+oper@gmail.com
${OPERATOR_NAME}                  xiqextreme operator
${op_username}                    automationadessreg+oper@gmail.com
${op_password}                    Aerohive123
${TIMEOUT}                        120
${LOCATION}                       Extreme Networks

### Monitor account details
${MONITOR_EMAIL}                 automationadessreg+mon@gmail.com
${MONITOR_NAME}                  xiqextreme monitor
${mon_username}                   automationadessreg+mon@gmail.com
${mon_password}                   Aerohive123
### Helpdesk account details
${HELPDESK_EMAIL}                 automationadessreg+help@gmail.com
${HELPDESK_NAME}                  xiqextreme helpdesk
${help_username}                 automationadessreg+help@gmail.com
${help_password}                 Aerohive123

# Operator account
&{OPERATOR_ROLE}    email=${OPERATOR_EMAIL}    name=${OPERATOR_NAME}   timeout=${TIMEOUT}        role=Operator      organization=All Organizations     location=${LOCATION}
&{MONITOR_ROLE}     email=${MONITOR_EMAIL}     name=${MONITOR_NAME}     timeout=${TIMEOUT}       role=Monitor       organization=All Organizations     location=${LOCATION}
&{HELPDESK_ROLE}    email=${HELPDESK_EMAIL}     name=${HELPDESK_NAME}     timeout=${TIMEOUT}     role=Helpdesk       organization=All Organizations     location=${LOCATION}
&{LOCATION_MAP}     organization=Extreme Networks  street_addr=Ecospace   city=Bengaluru       country=India

${ONPREM_ADSP_SERVER_IP}                 10.234.124.251
${ONPREM_ADSP_SERVER_SENSOR_PORT}            443
${ONPREM_ADSP_CLI_USERNAME}                 root
${ONPREM_ADSP_CLI_PASSWORD}                 symbol
${ONPREM_ADSP_SERVER_SSH_PORT}              22
${ONPREM_ADSP_PLATFORM}                     MU-LINUX