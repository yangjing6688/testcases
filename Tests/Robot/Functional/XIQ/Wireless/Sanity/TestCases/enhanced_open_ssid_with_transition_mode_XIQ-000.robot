#########################################################################################################
# Author        : Binh Nguyen
# Date          : June 3rd 2022
# Description   : TCXM-18041, Enhanced Open SSID for Wifi2
#                 TCXM-18043, Enhanced Open SSID with Transition mode enable for Wifi0/1
#                 TCXM-18044, Enhanced Open SSID with Transition mode disabled for Wifi0/1
#                 TCXM-18045, Enhanced Open SSID for Wifi0/1 & 2
#########################################################################################################

**** Variables ***
################## Policy Detail & Wireless Network ###############################
&{WIRELESS_ENHANCED_00}     ssid_name=""    network_type=Standard    ssid_profile=&{BORADCAST_SSID_00}    auth_profile=&{ENHANCED_AUTH_PROFILE_01}
&{WIRELESS_ENHANCED_01}     ssid_name=""    network_type=Standard    ssid_profile=&{BORADCAST_SSID_00}    auth_profile=&{ENHANCED_AUTH_PROFILE_00}
&{WIRELESS_ENHANCED_02}     ssid_name=""    network_type=Standard    ssid_profile=&{BORADCAST_SSID_01}    auth_profile=&{ENHANCED_AUTH_PROFILE_01}

&{BORADCAST_SSID_00}        WIFI0=Enable      WIFI1=Enable      WIFI2=Disable
&{BORADCAST_SSID_01}        WIFI0=Disable     WIFI1=Disable     WIFI2=Enable

&{ENHANCED_AUTH_PROFILE_00}     auth_type=ENHANCED   transition_mode=Enable
&{ENHANCED_AUTH_PROFILE_01}     auth_type=ENHANCED   transition_mode=Disable

################## Device Templates ###############################
&{AP_TEMPLATE_1}         wifi0_configuration=&{AP_TEMPLATE_1_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_1_WIFI1}   wifi2_configuration=&{AP_TEMPLATE_1_WIFI2}
&{AP_TEMPLATE_1_WIFI0}   radio_status=On     radio_profile=radio_ng_11ax-2g     client_mode=Disable    client_access=Enable    backhaul_mesh_link=Disable   sensor=Disable
&{AP_TEMPLATE_1_WIFI1}   radio_status=On     radio_profile=radio_ng_11ax-5g     client_mode=Disable    client_access=Enable    backhaul_mesh_link=Disable   sensor=Disable
&{AP_TEMPLATE_1_WIFI2}   radio_status=on     radio_profile=radio_ng_11ax-6g                            client_access=Enable    backhaul_mesh_link=Disable   sensor=Disable

############### Globle Variables ######################
${ap}        ${ap4}
${mu}        ${mu6}
${retry}     3

*** Settings ***
Library     String
Library     Collections

Library     common/Cli.py
Library     common/Utils.py
Library     common/TestFlow.py
Library     common/tools/remote/WinMuConnect.py

Library     xiq/flows/common/Login.py
Library     xiq/flows/common/MuCaptivePortal.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/DevicesActions.py
Library     xiq/flows/manage/DeviceConfig.py
Library     xiq/flows/manage/DeviceCliAccess.py
Library     xiq/flows/mlinsights/MLInsightClient360.py

Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/configure/DeviceTemplate.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/CommonObjects.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Library	    Remote 	http://${mu.ip}:${mu.port}   WITH NAME   rem_mu

Force Tags       testbed_1_node     testbed_2_node     testbed_3_node
Suite Setup      Pre_condition
Suite Teardown   Post_condition

*** Test Cases ***
Step0: Onboard AP
    [Documentation]    Onboard AP
    [Tags]             tcxm-18041     development     step0    steps
    ${STATUS}                      Onboard Device    ${ap.serial}    ${ap.make}    location=${ap.location}    device_os=${ap.os}
    should be equal as integers    ${STATUS}         1

    ${AP_SPAWN}=        Open Spawn          ${ap.console_ip}   ${ap.console_port}      ${ap.username}       ${ap.password}        ${ap.platform}
    Set Suite Variable  ${AP_SPAWN}
    ${OUTPUT0}=         Send Commands       ${AP_SPAWN}        capwap client server name ${capwap_url}, capwap client default-server-name ${capwap_url}, capwap client server backup name ${capwap_url}, no capwap client enable, capwap client enable, save config
    ${OUTPUT0}=         Send                ${AP_SPAWN}        console page 0
    ${OUTPUT0}=         Send                ${AP_SPAWN}        show version detail
    ${OUTPUT0}=         Send                ${AP_SPAWN}        show capwap client
    ${OUTPUT2}=         Send                ${AP_SPAWN}        ${cmd_capwap_hm_primary_name}
    ${OUTPUT3}=         Send                ${AP_SPAWN}        ${cmd_capwap_server_ip}
    ${OUTPUT1}=         Wait For CLI Output                    ${AP_SPAWN}         ${cmd_capwap_client_state}          ${output_capwap_status}
    Should Be Equal as Integers             ${OUTPUT1}          1
    Close Spawn         ${AP_SPAWN}

    Wait Until Device Online                ${ap.serial}
    ${AP_STATUS}=                           Get AP Status      ap_mac=${ap.mac}
    Should Be Equal As Strings             '${AP_STATUS}'      'green'

Step1: Create Policy - Enhanced open with transition mode
    [Documentation]     Create policy, select wifi0,1,2, and update policy to AP
    [Tags]              tcxm-18041    tcxm-18043    tcxm-18044    tcxm-18045    development     step1      steps
    Depends On          Step0
    ${NUM}=                        Generate Random String    5     012345678
    Set Suite Variable             ${POLICY}                       enhanced_${NUM}
    Set Suite Variable             ${SSID_00}                      w0_1_dis_${NUM}
    Set Suite Variable             ${SSID_01}                      w0_1_en_${NUM}
    Set Suite Variable             ${SSID_02}                      w2_dis_${NUM}
    Set Suite Variable             ${AP_TEMP_NAME}                 ${ap.model}_${NUM}
    Set To Dictionary              ${WIRELESS_ENHANCED_00}         ssid_name=${SSID_00}
    Set To Dictionary              ${WIRELESS_ENHANCED_01}         ssid_name=${SSID_01}
    Set To Dictionary              ${WIRELESS_ENHANCED_02}         ssid_name=${SSID_02}

    ${STATUS}                      Create Network Policy    ${POLICY}      &{WIRELESS_ENHANCED_00}
    should be equal as strings     '${STATUS}'       '1'
    ${STATUS}                      create ssid to policy    ${POLICY}      &{WIRELESS_ENHANCED_01}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      create ssid to policy    ${POLICY}      &{WIRELESS_ENHANCED_02}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      add ap template from common object      ${ap.model}        ${AP_TEMP_NAME}   &{AP_TEMPLATE_1}
    Should Be Equal As Strings     '${STATUS}'       '1'
    ${STATUS}                      add ap template to network policy       ${AP_TEMP_NAME}    ${POLICY}
    Should Be Equal As Strings     '${STATUS}'       '1'

Step2: Assign network policy to AP
    [Documentation]     Assign network policy to AP
    [Tags]              tcxm-18041    tcxm-18043    tcxm-18044    tcxm-18045       development     step2      steps
    Depends On          Step1
    ${UPDATE}                      Update Network Policy To Ap             ${POLICY}          ${ap.serial}      Complete
    should be equal as strings     '${UPDATE}'       '1'
    Wait Until Device Online       ${ap.serial}
    ${AP_STATUS}                   Get AP Status     ap_mac=${ap.mac}
    Should Be Equal As Strings    '${AP_STATUS}'    'green'

    ${UPDATE}                      update device delta configuration       ${ap.serial}       Delta
    should be equal as strings     '${UPDATE}'       '1'
    Wait Until Device Online       ${ap.serial}
    ${AP_STATUS}                   Get AP Status     ap_mac=${ap.mac}
    Should Be Equal As Strings    '${AP_STATUS}'    'green'

Step3: MU connect to wifi0-1 - Transition mode disable
    [Documentation]     MU connect to wifi0-1 - enhanced open SSID with transition mode disable
    [Tags]              tcxm-18044     tcxm-18045     development     step3     step00    steps
    Depends On          Step2
    FOR    ${i}    IN RANGE    ${retry}
        ${STATUS}               rem_mu.connect owe network        ${SSID_00}
        exit for loop if        '${STATUS}'=='1'
    END
    should be equal as strings      '${STATUS}'     '1'

Step4: Verify Client360 to wifi0-1 - Transition mode disable
    [Documentation]     Verify Client360 to wifi0-1 - Enhanced Open SSID with transition mode disable
    [Tags]              tcxm-18044     tcxm-18045     development     step4     step00    steps
    Depends On          Step3
    ${OUT}            get real time client360 details    ${mu.wifi_mac}
    ${OUT}            convert to string                  ${OUT}
    should contain    ${OUT}                             ${mu.wifi_mac}

Step5: MU connect to wifi0-1 - Transition mode enable
    [Documentation]     MU connect to wifi0-1 - Enhanced Open SSID with transition mode enable
    [Tags]              tcxm-18043     tcxm-18045     development     step5     step01    steps
    Depends On          Step2
    FOR    ${i}    IN RANGE    ${retry}
        ${STATUS}               rem_mu.connect owe network      ${SSID_01}
        exit for loop if        '${STATUS}'=='1'
    END
    should be equal as strings      '${STATUS}'     '1'

Step6: Verify Client360 to wifi0-1 - Transition mode anable
    [Documentation]     Verify Client360 to wifi0-1  - Enhanced Open SSID with transition mode anable
    [Tags]              tcxm-18043     tcxm-18045     development     step6     step01    steps
    Depends On          Step5
    ${OUT}            get real time client360 details    ${mu.wifi_mac}
    ${OUT}            convert to string                  ${OUT}
    should contain    ${OUT}                             ${mu.wifi_mac}

Step7: MU connect to wifi2 - Transition mode disable
    [Documentation]     MU connect to wifi2 - Enhanced Open SSID with transition mode enable
    [Tags]              tcxm-18041     tcxm-18045     development     step7     step02    steps
    Depends On          Step2
    FOR    ${i}    IN RANGE    ${retry}
        ${STATUS}               rem_mu.connect owe network      ${SSID_02}
        exit for loop if        '${STATUS}'=='1'
    END
    should be equal as strings      '${STATUS}'     '1'

Step8: Verify Client360 to wifi2 - Transition mode disable
    [Documentation]     Verify Client360 to wifi2 - Enhanced Open SSID with transition mode anable
    [Tags]              tcxm-18041     tcxm-18045     development     step8     step02    steps
    Depends On          Step7
    ${OUT}            get real time client360 details    ${mu.wifi_mac}
    ${OUT}            convert to string                  ${OUT}
    should contain    ${OUT}                             ${mu.wifi_mac}

*** Keywords ***
Pre_condition
    ${STATUS}                           Login User    ${tenant_username}   ${tenant_password}
    should be equal as strings          '${STATUS}'   '1'
    ${failed}     ${success}            reset device to default    ${ap.serial}
    log to console                      Wait for 2 minutes for completing reboot....
    sleep                               2m
    delete all aps
    delete all network policies
    delete all ssids                    ssid0
    delete all ap templates

Post_condition
    Logout User
    Quit Browser
