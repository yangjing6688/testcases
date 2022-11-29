#########################################################################################################
# Author        : Binh Nguyen
# Date          : Sept 19th 2022
# Description   : TCXM-9348	 Verify device template wireless interface wifi0 default-mode
#                 TCXM-9349	 Verify device template wireless interface wifi1 default config
#                 TCXM-9351  Verify device template wireless interface wifi2 default config
#                 TCXM-9350  verify backhaul mesh link support for wifi0/wif1
#                 TCXM-9352  Verify 6 GHz (Sensor) mode on wifi2 interface
#                 TCXM-11671 Verify 6 GHz Dual (Client Access & Backhaul Mesh) mode on wifi2 interface
#########################################################################################################

**** Variables ***
### Step0 ############### Expect Device Template Setting ###############################
### AP4000 ###
&{AP_TEMPLATE_2}         wifi0_configuration=&{AP_TEMPLATE_2_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_2_WIFI1}   wifi2_configuration=&{AP_TEMPLATE_2_WIFI2}
&{AP_TEMPLATE_2_WIFI0}   radio_status=True     radio_profile=radio_ng_11ax-2g     client_mode=False    client_access=True    backhaul_mesh_link=False    sensor=Disable    enable_SDR=False
&{AP_TEMPLATE_2_WIFI1}   radio_status=True     radio_profile=radio_ng_11ax-5g     client_mode=False    client_access=True    backhaul_mesh_link=False    sensor=Disable
&{AP_TEMPLATE_2_WIFI2}   radio_status=True     radio_profile=radio_ng_11ax-6g                          client_access=True    backhaul_mesh_link=False    sensor=False

### Step1 ############### Policy Detail & Wireless Network ###############################
&{WIRELESS_PESRONAL_00}     ssid_name=""    network_type=Standard    ssid_profile=&{BORADCAST_SSID_00}     auth_profile=&{PERSONAL_AUTH_PROFILE_00}
&{WIRELESS_PESRONAL_01}     ssid_name=""    network_type=Standard    ssid_profile=&{BORADCAST_SSID_00}     auth_profile=&{PERSONAL_AUTH_PROFILE_00}
&{WIRELESS_PESRONAL_02}     ssid_name=""    network_type=Standard    ssid_profile=&{BORADCAST_SSID_00}     auth_profile=&{PERSONAL_AUTH_PROFILE_00}

&{BORADCAST_SSID_00}            WIFI0=Enable        WIFI1=Enable      WIFI2=Enable
&{PERSONAL_AUTH_PROFILE_00}     auth_type=PSK   key_encryption=&{PSK_KEY_ENCRYPTION_00}   cwp_config=&{PSK_CWP_00}
&{PSK_KEY_ENCRYPTION_00}        key_management=WPA3 (SAE)    encryption_method=CCMP (AES)   sae_group=All    transition_mode=disable    key_value=aerohive
...                             anti_logging_Threshold=5     key_type=ASCII Key
&{PSK_CWP_00}                   enable_cwp=Disable
################## Device Templates ###############################
&{AP_TEMPLATE_3}         wifi0_configuration=&{AP_TEMPLATE_3_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_3_WIFI1}   wifi2_configuration=&{AP_TEMPLATE_3_WIFI2}
&{AP_TEMPLATE_3_WIFI0}   radio_status=On     radio_profile=radio_ng_11ax-2g     client_mode=Disable    client_access=Enable    backhaul_mesh_link=Disable
&{AP_TEMPLATE_3_WIFI1}   radio_status=On     radio_profile=radio_ng_11ax-5g     client_mode=Disable    client_access=Enable    backhaul_mesh_link=Disable
&{AP_TEMPLATE_3_WIFI2}   radio_status=On     radio_profile=radio_ng_11ax-6g                            client_access=Enable    backhaul_mesh_link=Disable    sensor=Disable

*** Settings ***
Library     String
Library     Collections

Library     common/Cli.py
Library     common/Utils.py
Library     common/TestFlow.py
Library     common/tools/remote/WinMuConnect.py

Library     xiq/flows/common/Login.py
Library     xiq/flows/common/MuCaptivePortal.py
Library     xiq/flows/common/Navigator.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/DevicesActions.py
Library     xiq/flows/manage/DeviceConfig.py
Library     xiq/flows/manage/DeviceCliAccess.py

Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/configure/DeviceTemplate.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/CommonObjects.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Force Tags       testbed_1_node     testbed_2_node     testbed_3_node
Suite Setup      Pre_condition
Suite Teardown   Post_condition

*** Test Cases ***
Step0: Verify device template wireless interface wifi0-1-2 default config - AP4000
    [Documentation]    Get device template wireless interface wifi0-1-2 default config - AP4000
    [Tags]             tcxm-9348       tcxm-9349     tcxm-9351    development     step0    steps
    &{AP_TEMPLATE_1_WIFI0}    create dictionary     radio_status=get    radio_profile=get   client_mode=get     client_access=get     backhaul_mesh_link=get     sensor=get    enable_SDR=get
    &{AP_TEMPLATE_1_WIFI1}    create dictionary     radio_status=get    radio_profile=get   client_mode=get     client_access=get     backhaul_mesh_link=get     sensor=get
    &{AP_TEMPLATE_1_WIFI2}    create dictionary     radio_status=get    radio_profile=get                       client_access=get     backhaul_mesh_link=get     sensor=get
    &{AP_TEMPLATE_1}          create dictionary     wifi0_configuration=&{AP_TEMPLATE_1_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_1_WIFI1}   wifi2_configuration=&{AP_TEMPLATE_1_WIFI2}

    ${OUT}    Get AP Template Wifi     ${ap1.template}   &{AP_TEMPLATE_1}
    log       ${OUT}
    log       ${AP_TEMPLATE_2}
    should be equal as strings      ${OUT}[wifi0_configuration][radio_profile]          ${AP_TEMPLATE_2}[wifi0_configuration][radio_profile]
    should be equal as strings      ${OUT}[wifi0_configuration][client_access]          ${AP_TEMPLATE_2}[wifi0_configuration][client_access]
    should be equal as strings      ${OUT}[wifi0_configuration][sensor]                 ${AP_TEMPLATE_2}[wifi0_configuration][sensor]

    should be equal as strings      ${OUT}[wifi1_configuration][radio_profile]          ${AP_TEMPLATE_2}[wifi1_configuration][radio_profile]
    should be equal as strings      ${OUT}[wifi1_configuration][client_access]          ${AP_TEMPLATE_2}[wifi1_configuration][client_access]
    should be equal as strings      ${OUT}[wifi1_configuration][sensor]                 ${AP_TEMPLATE_2}[wifi1_configuration][sensor]

    should be equal as strings      ${OUT}[wifi2_configuration][radio_profile]          ${AP_TEMPLATE_2}[wifi2_configuration][radio_profile]
    should be equal as strings      ${OUT}[wifi2_configuration][client_access]          ${AP_TEMPLATE_2}[wifi2_configuration][client_access]
    should be equal as strings      ${OUT}[wifi2_configuration][backhaul_mesh_link]     ${AP_TEMPLATE_2}[wifi2_configuration][backhaul_mesh_link]
    should be equal as strings      ${OUT}[wifi2_configuration][sensor]                 ${AP_TEMPLATE_2}[wifi2_configuration][sensor]

Step1a: Onboard AP - AP4000
    [Documentation]    Onboard AP
    [Tags]             tcxm-9350   development     step1     step1a    steps
    ${STATUS}                      onboard device quick    ${ap1}
    ${AP_SPAWN}        Open Spawn          ${ap1.ip}           ${ap1.port}      ${ap1.username}      ${ap1.password}      ${ap1}[cli_type]
    ${OUTPUT0}         Send Commands       ${AP_SPAWN}        capwap client server name ${capwap_url}, capwap client default-server-name ${capwap_url}, capwap client server backup name ${capwap_url}, no capwap client enable, capwap client enable, save config
    ${OUTPUT0}         Send                ${AP_SPAWN}        console page 0
    ${OUTPUT0}         Send                ${AP_SPAWN}        show version detail
    ${OUTPUT0}         Send                ${AP_SPAWN}        show capwap client
    ${OUTPUT2}         Send                ${AP_SPAWN}        ${cmd_capwap_hm_primary_name}
    ${OUTPUT3}         Send                ${AP_SPAWN}        ${cmd_capwap_server_ip}
    ${OUTPUT1}         Wait For CLI Output                    ${AP_SPAWN}         ${cmd_capwap_client_state}          ${output_capwap_status}
    Close Spawn        ${AP_SPAWN}

    Wait Until Device Online               ${ap1.serial}
    ${AP_STATUS}=                          Get AP Status      ap_mac=${ap1.mac}
    Should Be Equal As Strings            '${AP_STATUS}'      'green'

Step1b: Create and Assign network policy to AP - AP4000
    [Documentation]    Create and Assign network policy to AP
    [Tags]             tcxm-9350    development     step1    step1b    steps
    Depends On         Step1a
    ${NUM}=                        Generate Random String    5     012345678
    Set Suite Variable             ${POLICY}                       personal_w0_1_${NUM}
    Set Suite Variable             ${SSID_00}                      w0_1_M1_${NUM}
    Set Suite Variable             ${SSID_01}                      w0_1_M2_${NUM}
    Set Suite Variable             ${SSID_02}                      w0_1_M3_${NUM}
    Set Suite Variable             ${AP_TEMP_NAME}                 ${ap1.model}_${NUM}
    Set To Dictionary              ${WIRELESS_PESRONAL_00}         ssid_name=${SSID_00}
    Set To Dictionary              ${WIRELESS_PESRONAL_01}         ssid_name=${SSID_01}
    Set To Dictionary              ${WIRELESS_PESRONAL_02}         ssid_name=${SSID_02}

    ${STATUS}                      Create Network Policy    ${POLICY}      ${WIRELESS_PESRONAL_00}
    should be equal as strings     '${STATUS}'       '1'
    ${STATUS}                      create ssid to policy    ${POLICY}      &{WIRELESS_PESRONAL_01}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      create ssid to policy    ${POLICY}      &{WIRELESS_PESRONAL_02}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      add ap template from common object      ${ap1.model}       ${AP_TEMP_NAME}   &{AP_TEMPLATE_3}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      add ap template to network policy       ${AP_TEMP_NAME}    ${POLICY}
    Should Be Equal As Strings     '${STATUS}'        '1'
    ${UPDATE}                      Update Network Policy To Ap             ${POLICY}          ${ap1.serial}      Complete
    should be equal as strings     '${UPDATE}'        '1'
    Wait Until Device Online       ${ap1.serial}
    ${AP_STATUS}                   Get AP Status      ap_mac=${ap1.mac}
    Should Be Equal As Strings    '${AP_STATUS}'     'green'

tep1c: verify backhaul mesh link support for wifi0-1 - AP4000
    [Documentation]    Get backhaul mesh link support for wifi0-1
    [Tags]             tcxm-9350    development     step1    step1c    steps
    Depends On         Step1b
    &{AP_TEMPLATE_01_WIFI0}   create dictionary     client_access=Enable       backhaul_mesh_link=Enable
    &{AP_TEMPLATE_01_WIFI1}   create dictionary     client_access=Enable       backhaul_mesh_link=Enable
    &{AP_TEMPLATE_01}         create dictionary     wifi0_configuration=&{AP_TEMPLATE_01_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_01_WIFI1}

    Set AP Template Wifi        ${AP_TEMP_NAME}      &{AP_TEMPLATE_01}
    Navigate To Devices
    sleep             10s
    ${OUT}            get_device_config_audit_delta     ${ap1.mac}
    should contain    ${OUT}    no interface wifi0 ssid ${SSID_00}
    should contain    ${OUT}    no interface wifi0 ssid ${SSID_01}
    should contain    ${OUT}    no interface wifi0 ssid ${SSID_02}
    should contain    ${OUT}    interface wifi0 mode dual
    should contain    ${OUT}    interface wifi0 ssid ${SSID_00}
    should contain    ${OUT}    no interface wifi0 ssid ${SSID_00} shutdown
    should contain    ${OUT}    interface wifi0 ssid ${SSID_01}
    should contain    ${OUT}    no interface wifi0 ssid ${SSID_01} shutdown
    should contain    ${OUT}    interface wifi0 ssid ${SSID_02}
    should contain    ${OUT}    no interface wifi0 ssid ${SSID_02} shutdown
    should contain    ${OUT}    no interface wifi1 ssid ${SSID_00}
    should contain    ${OUT}    no interface wifi1 ssid ${SSID_01}
    should contain    ${OUT}    no interface wifi1 ssid ${SSID_02}
    should contain    ${OUT}    interface wifi1 mode dual
    should contain    ${OUT}    no interface wifi1 ssid ${SSID_00} shutdown
    should contain    ${OUT}    interface wifi1 ssid ${SSID_01}
    should contain    ${OUT}    no interface wifi1 ssid ${SSID_01} shutdown
    should contain    ${OUT}    interface wifi1 ssid ${SSID_02}
    should contain    ${OUT}    no interface wifi1 ssid ${SSID_02} shutdown

tep1d: verify backhaul mesh link support for wifi0-1 - AP4000
    [Documentation]    Get backhaul mesh link support for wifi0-1
    [Tags]             tcxm-9350    development     step1    step1d    steps
    Depends On         Step1b
    &{AP_TEMPLATE_02_WIFI0}   create dictionary     client_access=Disable      backhaul_mesh_link=Enable
    &{AP_TEMPLATE_02_WIFI1}   create dictionary     client_access=Disable      backhaul_mesh_link=Enable
    &{AP_TEMPLATE_02}         create dictionary     wifi0_configuration=&{AP_TEMPLATE_02_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_02_WIFI1}

    Set AP Template Wifi        ${AP_TEMP_NAME}      &{AP_TEMPLATE_02}
    Navigate To Devices
    sleep             10s
    ${OUT}            get_device_config_audit_delta     ${ap1.mac}
    should contain    ${OUT}    interface wifi0 mode backhaul
    should contain    ${OUT}    interface wifi1 mode backhaul

step2: Verify 6 GHz (Sensor) mode on wifi2 interface - AP4000
    [Documentation]    Verify 6 GHz (Sensor) mode on wifi2 interface
    [Tags]             tcxm-9352    development    step2    steps
    Depends On         Step1b
    &{AP_TEMPLATE_03_WIFI2}   create dictionary     client_access=Disable   backhaul_mesh_link=Disable   sensor=Enable
    &{AP_TEMPLATE_03}         create dictionary     wifi2_configuration=&{AP_TEMPLATE_03_WIFI2}

    Set AP Template Wifi        ${AP_TEMP_NAME}         &{AP_TEMPLATE_03}
    Navigate To Devices
    sleep             10s
    ${OUT}            get_device_config_audit_delta     ${ap1.mac}
    should contain    ${OUT}    interface wifi2 mode sensor

step3: Verify 6 GHz Dual (Client Access & Backhaul Mesh) mode on wifi2 interface - AP4000
    [Documentation]    Verify 6 GHz Dual (Client Access & Backhaul Mesh) mode on wifi2 interface
    [Tags]             tcxm-11671    development    step3    steps
    Depends On         Step1b
    &{AP_TEMPLATE_04_WIFI2}   create dictionary     client_access=Enable   backhaul_mesh_link=Enable   sensor=Disable
    &{AP_TEMPLATE_04}         create dictionary     wifi2_configuration=&{AP_TEMPLATE_04_WIFI2}
    Set AP Template Wifi        ${AP_TEMP_NAME}         &{AP_TEMPLATE_04}
    Navigate To Devices
    sleep             10s
    ${OUT}            get_device_config_audit_delta     ${ap1.mac}
    should contain    ${OUT}    interface wifi2 mode dual

*** Keywords ***
Pre_condition
    ${STATUS}                           Login User    ${tenant_username}   ${tenant_password}
    should be equal as strings          '${STATUS}'   '1'
    ${failed}     ${success}            reset device to default    ${ap1.serial}
    log to console                      Wait for 2 minutes for completing reboot....
    sleep                               2m
    delete all aps
    delete all network policies
    delete all ssids
    delete all ap templates

Post_condition
    Logout User
    Quit Browser
