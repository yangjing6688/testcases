#########################################################################################################
# Author        : Binh Nguyen
# Date          : Feb 17th 2023
# Description   : TCXM-9348	 Verify device template wireless interface wifi0 default-mode
#                 TCXM-9349	 Verify device template wireless interface wifi1 default config
#                 TCXM-9350  verify backhaul mesh link support for wifi0/wif1
#########################################################################################################

**** Variables ***
### Step0 ############### Expect Device Template Setting ###############################
### AP3000 ###
&{AP_TEMPLATE_2}         wifi0_configuration=&{AP_TEMPLATE_2_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_2_WIFI1}    wired_configuration=&{AP_TEMPLATE_2_WIRED}
&{AP_TEMPLATE_2_WIFI0}   radio_status=On   operating_mode=2.4 GHz   radio_profile=radio_ng_11ax-2g   client_mode=Disable   client_access=Enable   backhaul_mesh_link=Disable   sensor=Disable   enable_SDR=Disable
&{AP_TEMPLATE_2_WIFI1}   radio_status=On                            radio_profile=radio_ng_11ax-5g   client_mode=Disable   client_access=Enable   backhaul_mesh_link=Disable   sensor=Disable
&{AP_TEMPLATE_2_WIRED}   eth0=On           port_type_eth0=Uplink Port     transmission_type_eth0=Auto     speed_eth0=Auto     lldp_eth0=Enable   cdp_eth0=Enable
...                      eth1=On           port_type_eth1=Uplink Port     transmission_type_eth1=Auto     speed_eth1=Auto     lldp_eth1=Enable   cdp_eth1=Enable

### Step1 ############### Policy Detail & Wireless Network ###############################
&{WIRELESS_PESRONAL_00}   ssid_name=""   network_type=Standard   ssid_profile=&{BORADCAST_SSID_00}   auth_profile=&{PERSONAL_AUTH_PROFILE_00}
&{WIRELESS_PESRONAL_01}   ssid_name=""   network_type=Standard   ssid_profile=&{BORADCAST_SSID_00}   auth_profile=&{PERSONAL_AUTH_PROFILE_00}

&{BORADCAST_SSID_00}            WIFI0=Disable   WIFI1=Enable    WIFI2=Enable
&{PERSONAL_AUTH_PROFILE_00}     auth_type=PSK   key_encryption=&{PSK_KEY_ENCRYPTION_00}   cwp_config=&{PSK_CWP_00}
&{PSK_KEY_ENCRYPTION_00}        key_management=WPA3 (SAE)    encryption_method=CCMP (AES)   sae_group=All    transition_mode=disable    key_value=aerohive
...                             anti_logging_Threshold=5     key_type=ASCII Key
&{PSK_CWP_00}                   enable_cwp=Disable

################## Device Templates ###############################
&{AP_TEMPLATE_3}         wifi0_configuration=&{AP_TEMPLATE_3_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_3_WIFI1}
&{AP_TEMPLATE_3_WIFI0}   radio_status=On     radio_profile=radio_ng_11ax-6g     client_mode=Disable    client_access=Enable    backhaul_mesh_link=Disable
&{AP_TEMPLATE_3_WIFI1}   radio_status=On     radio_profile=radio_ng_11ax-5g     client_mode=Disable    client_access=Enable    backhaul_mesh_link=Disable

*** Settings ***
Library     String
Library     Collections
Library     DependencyLibrary

Library     common/Cli.py
Library     common/Utils.py
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

Force Tags       testbed_none
Suite Setup      Pre_condition
Suite Teardown   Post_condition

*** Test Cases ***
Step1: Verify device template wireless interface wifi0-1 details and wired interface details
    [Documentation]    Get device template wireless interface wifi0-1-2 details and wired interface details
    [Tags]             tcxm-9348   tcxm-9349   development   step1   steps

    &{AP_TEMPLATE_1_WIFI0}    create dictionary     radio_status=get   operating_mode=get   radio_profile=get   client_mode=get   client_access=get   backhaul_mesh_link=get   sensor=get   enable_SDR=get
    &{AP_TEMPLATE_1_WIFI1}    create dictionary     radio_status=get                        radio_profile=get   client_mode=get   client_access=get   backhaul_mesh_link=get   sensor=get
    &{AP_TEMPLATE_1_WIRED}    create dictionary     eth0=get           port_type_eth0=get   transmission_type_eth0=get   speed_eth0=get   lldp_eth0=get   cdp_eth0=get
    ...                                             eth1=get           port_type_eth1=get   transmission_type_eth1=get   speed_eth1=get   lldp_eth1=get   cdp_eth1=get
    &{AP_TEMPLATE_1}          create dictionary     wifi0_configuration=&{AP_TEMPLATE_1_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_1_WIFI1}   wired_configuration=&{AP_TEMPLATE_1_WIRED}
    ${ITEM_1}   create list
    ${ITEM_2}   create list

    ${OUT}    Get AP Template Wifi     ${ap1.template}   ${AP_TEMPLATE_1}
    log       ${OUT}
    log       ${AP_TEMPLATE_2}
    FOR     ${item}     IN      &{AP_TEMPLATE_2}
           ${items}    Collections.Get Dictionary Items    ${item[1]}    False
           Append To List    ${ITEM_1}   ${items}
    END
    FOR     ${item}     IN      &{OUT}
           ${items}    Collections.Get Dictionary Items    ${item[1]}    False
           Append To List    ${ITEM_2}   ${items}
    END

    set global variable       ${ITEM_1}
    Lists Should Be Equal     ${ITEM_1}     ${ITEM_2}

Step2: Verify device configure wireless interface wifi0-1 details and wired interface details
    [Documentation]    Get device configure wireless interface wifi0-1-2 details and wired interface details
    [Tags]             tcxm-9348   tcxm-9349   tcxm-9351   development   step2   steps

    &{AP_TEMPLATE_1_WIFI0}    create dictionary     radio_status=get   operating_mode=get   radio_profile=get   client_mode=get   client_access=get   backhaul_mesh_link=get   sensor=get   enable_SDR=get
    &{AP_TEMPLATE_1_WIFI1}    create dictionary     radio_status=get                        radio_profile=get   client_mode=get   client_access=get   backhaul_mesh_link=get   sensor=get
    &{AP_TEMPLATE_1_WIRED}    create dictionary     eth0=get           transmission_type_eth0=get   speed_eth0=get   lldp_eth0=get   cdp_eth0=get
    ...                                             eth1=get           transmission_type_eth1=get   speed_eth1=get   lldp_eth1=get   cdp_eth1=get
    &{AP_TEMPLATE_1}          create dictionary     wifi0_configuration=&{AP_TEMPLATE_1_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_1_WIFI1}   wired_configuration=&{AP_TEMPLATE_1_WIRED}
    ${ITEM_2}   create list

    ${OUT}    Get Override AP Configure Wifi Details    ${ap1.mac}     ${AP_TEMPLATE_1}
    log       ${OUT}
    log       ${AP_TEMPLATE_2}
    FOR     ${item}     IN      &{OUT}
           ${items}    Collections.Get Dictionary Items    ${item[1]}    False
           Append To List    ${ITEM_2}   ${items}
    END
    Lists Should Be Equal     ${ITEM_1[0]}     ${ITEM_2[0]}
    Lists Should Be Equal     ${ITEM_1[1]}     ${ITEM_2[1]}

    should be equal as strings      ${OUT}[wired_configuration][eth0]                       ${AP_TEMPLATE_2}[wired_configuration][eth0]
    should be equal as strings      ${OUT}[wired_configuration][eth1]                       ${AP_TEMPLATE_2}[wired_configuration][eth1]
    should be equal as strings      ${OUT}[wired_configuration][transmission_type_eth0]     ${AP_TEMPLATE_2}[wired_configuration][transmission_type_eth0]
    should be equal as strings      ${OUT}[wired_configuration][transmission_type_eth1]     ${AP_TEMPLATE_2}[wired_configuration][transmission_type_eth1]
    should be equal as strings      ${OUT}[wired_configuration][speed_eth0]                 ${AP_TEMPLATE_2}[wired_configuration][speed_eth0]
    should be equal as strings      ${OUT}[wired_configuration][speed_eth1]                 ${AP_TEMPLATE_2}[wired_configuration][speed_eth1]
    should be equal as strings      ${OUT}[wired_configuration][lldp_eth0]                  ${AP_TEMPLATE_2}[wired_configuration][lldp_eth0]
    should be equal as strings      ${OUT}[wired_configuration][lldp_eth1]                  ${AP_TEMPLATE_2}[wired_configuration][lldp_eth1]
    should be equal as strings      ${OUT}[wired_configuration][cdp_eth0]                   ${AP_TEMPLATE_2}[wired_configuration][cdp_eth0]
    should be equal as strings      ${OUT}[wired_configuration][cdp_eth1]                   ${AP_TEMPLATE_2}[wired_configuration][cdp_eth1]

Step3: Create and Assign network policy to AP
    [Documentation]    Create and Assign network policy to AP
    [Tags]             tcxm-9350   development   step3   steps

    ${NUM}                         Generate Random String    5     012345678
    Set Suite Variable             ${POLICY}                       personal_w0_1_${NUM}
    Set Suite Variable             ${SSID_00}                      w0_temp_${NUM}
    Set Suite Variable             ${SSID_01}                      w1_temp_${NUM}
    Set Suite Variable             ${AP_TEMP_NAME}                 ${ap1.model}_${NUM}
    Set To Dictionary              ${WIRELESS_PESRONAL_00}         ssid_name=${SSID_00}
    Set To Dictionary              ${WIRELESS_PESRONAL_01}         ssid_name=${SSID_01}

    ${STATUS}                      create network policy if does not exist    ${POLICY}    ${WIRELESS_PESRONAL_00}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      create ssid to policy    ${POLICY}      &{WIRELESS_PESRONAL_01}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      add ap template from common object      ${ap1.model}       ${AP_TEMP_NAME}   ${AP_TEMPLATE_3}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      add ap template to network policy       ${AP_TEMP_NAME}    ${POLICY}
    Should Be Equal As Strings     '${STATUS}'        '1'
    ${UPDATE}                      Update Network Policy To Ap             ${POLICY}          ${ap1.serial}     Complete
    should be equal as strings     '${UPDATE}'        '1'
    Wait_device_online             ${ap1}

step4: verify client access and backhaul mesh link support for wifi0-1
    [Documentation]    Get client access and backhaul mesh link support for wifi0-1
    [Tags]             tcxm-9350   development   step4   steps

    Depends On Test    Step3: Create and Assign network policy to AP
    &{AP_TEMPLATE_01_WIFI0}   create dictionary     client_access=Enable       backhaul_mesh_link=Enable
    &{AP_TEMPLATE_01_WIFI1}   create dictionary     client_access=Enable       backhaul_mesh_link=Enable
    &{AP_TEMPLATE_01}         create dictionary     wifi0_configuration=&{AP_TEMPLATE_01_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_01_WIFI1}

    Set AP Template Wifi      ${AP_TEMP_NAME}    ${AP_TEMPLATE_01}
    Navigate To Devices
    sleep             10s
    ${OUT}            get_device_config_audit_delta     ${ap1.mac}
    should contain    ${OUT}    no interface wifi0 ssid ${SSID_00}
    should contain    ${OUT}    no interface wifi0 ssid ${SSID_01}
    should contain    ${OUT}    interface wifi0 mode dual
    should contain    ${OUT}    interface wifi0 ssid ${SSID_00}
    should contain    ${OUT}    no interface wifi0 ssid ${SSID_00} shutdown
    should contain    ${OUT}    interface wifi0 ssid ${SSID_01}
    should contain    ${OUT}    no interface wifi0 ssid ${SSID_01} shutdown
    should contain    ${OUT}    no interface wifi1 ssid ${SSID_00}
    should contain    ${OUT}    no interface wifi1 ssid ${SSID_01}
    should contain    ${OUT}    interface wifi1 mode dual
    should contain    ${OUT}    no interface wifi1 ssid ${SSID_00} shutdown
    should contain    ${OUT}    interface wifi1 ssid ${SSID_01}
    should contain    ${OUT}    no interface wifi1 ssid ${SSID_01} shutdown

step5: verify backhaul mesh link support for wifi0-1
    [Documentation]    Get backhaul mesh link support for wifi0-1
    [Tags]             tcxm-9350   development   step5   steps

    Depends On Test    Step3: Create and Assign network policy to AP
    &{AP_TEMPLATE_02_WIFI0}   create dictionary     client_access=Disable      backhaul_mesh_link=Enable
    &{AP_TEMPLATE_02_WIFI1}   create dictionary     client_access=Disable      backhaul_mesh_link=Enable
    &{AP_TEMPLATE_02}         create dictionary     wifi0_configuration=&{AP_TEMPLATE_02_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_02_WIFI1}

    Set AP Template Wifi      ${AP_TEMP_NAME}    ${AP_TEMPLATE_02}
    Navigate To Devices
    sleep             10s
    ${OUT}            get_device_config_audit_delta     ${ap1.mac}
    should contain    ${OUT}    interface wifi0 mode backhaul
    should contain    ${OUT}    interface wifi1 mode backhaul

*** Keywords ***
Pre_condition
    ${STATUS}                     Login User    ${tenant_username}   ${tenant_password}
    should be equal as strings    '${STATUS}'   '1'
    reset devices to default
    log to console                Wait for 2 minutes for completing reboot....
    sleep                         2m
    delete all devices
    delete all network policies
    delete all ssids
    delete all ap templates
    Onboard_AP

Post_condition
    Logout User
    Quit Browser

Onboard_AP
    ${STATUS}       onboard device quick                            ${ap1}
    Should Be Equal As Strings                                      '${STATUS}'       '1'
    ${AP_SPAWN}     Open Spawn                                      ${ap1.ip}         ${ap1.port}      ${ap1.username}   ${ap1.password}   ${ap1.cli_type}
    ${STATUS}       Configure Device To Connect To Cloud            ${ap1.cli_type}   ${capwap_url}    ${AP_SPAWN}
    Should Be Equal As Strings                                      '${STATUS}'       '1'

    ${STATUS}       Wait for Configure Device to Connect to Cloud   ${ap1.cli_type}   ${capwap_url}    ${AP_SPAWN}
    Should Be Equal As Strings                                      '${STATUS}'       '1'
    Wait_device_online                                              ${ap1}
    [Teardown]      Close Spawn                                     ${AP_SPAWN}

Wait_device_online
    [Arguments]    ${ap}
    ${STATUS}                       Wait Until Device Online    ${ap}[serial]
    Should Be Equal As Strings      '${STATUS}'    '1'
    ${STATUS}                       Get Device Status           ${ap}[serial]
    ${STATUS}                       Run Keyword And Return Status    Should contain any    ${STATUS}    green    config audit mismatch
    IF    not ${STATUS}
        Wait Until Device Reboots       ${ap}[serial]
        ${STATUS}                       Wait Until Device Online    ${ap}[serial]    retry_count=60
        Should Be Equal As Strings      '${STATUS}'    '1'
        ${STATUS}                       Get Device Status           ${ap}[serial]
        Should contain any              ${STATUS}      green        config audit mismatch
    END
