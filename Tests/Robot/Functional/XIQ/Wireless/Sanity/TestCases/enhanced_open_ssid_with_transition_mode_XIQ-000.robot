#########################################################################################################
# Author        : Binh Nguyen
# Date          : June 3rd 2022
# Description   : TCXM-18041, Enhanced Open SSID for Wifi2
#                 TCXM-18043, Enhanced Open SSID with Transition mode enable for Wifi0/1
#                 TCXM-18044, Enhanced Open SSID with Transition mode disabled for Wifi0/1
#                 TCXM-18045, Enhanced Open SSID for Wifi0/1 & 2
#
#                 TCXM-12164, Open & Enhanced Open tabs while creating new SSIDs
#                 TCXM-12175, Transition mode while creating new SSID
#                 TCXM-12176, Companion SSID name validation
#                 TCXM-12180, Companion SSID should be hidden
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
${retry}     3

*** Settings ***
Library     String
Library     Collections

Library     common/Cli.py
Library     common/Utils.py
Library     common/TestFlow.py
Library     common/tools/remote/WinMuConnect.py

Library     xiq/flows/common/Navigator.py
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

Library	    Remote 	http://${mu1.ip}:${mu1.port}   WITH NAME   rem_mu

Force Tags       testbed_1_node     testbed_2_node     testbed_3_node
Suite Setup      Pre_condition
Suite Teardown   Post_condition

*** Test Cases ***
Step0: Onboard AP
    [Documentation]    Onboard AP
    [Tags]             tcxm-18041     development     step0    steps
    ${STATUS}       onboard device quick                            ${ap1}
    Should Be Equal As Strings                                      '${STATUS}'       '1'
    ${AP_SPAWN}     Open Spawn                                      ${ap1.ip}         ${ap1.port}      ${ap1.username}   ${ap1.password}   ${ap1.cli_type}
    ${STATUS}       Configure Device To Connect To Cloud            ${ap1.cli_type}   ${capwap_url}    ${AP_SPAWN}
    Should Be Equal As Strings                                      '${STATUS}'       '1'

    ${STATUS}       Wait for Configure Device to Connect to Cloud   ${ap1.cli_type}   ${capwap_url}    ${AP_SPAWN}
    Should Be Equal As Strings                                      '${STATUS}'       '1'
    ${STATUS}       Wait Until Device Online                        ${ap1.serial}
    Should Be Equal As Strings                                      '${STATUS}'       '1'
    ${STATUS}       Get Device Status                               ${ap1.serial}
    Should contain any                                              ${STATUS}          green           config audit mismatch
    [Teardown]      Close Spawn                                     ${AP_SPAWN}

Step1: Create Policy - Enhanced open with transition mode
    [Documentation]     Create policy, select wifi0,1,2, and update policy to AP
    [Tags]              tcxm-18041    tcxm-18043    tcxm-18044    tcxm-18045    development     step1      steps
    Depends On          Step0
    ${NUM}                         Generate Random String    5     012345678
    Set Suite Variable             ${POLICY}                       enhanced_${NUM}
    Set Suite Variable             ${SSID_00}                      w0_1_dis_${NUM}
    Set Suite Variable             ${SSID_01}                      w0_1_en_${NUM}
    Set Suite Variable             ${SSID_02}                      w2_dis_${NUM}
    Set Suite Variable             ${AP_TEMP_NAME}                 ${ap1.model}_${NUM}
    Set To Dictionary              ${WIRELESS_ENHANCED_00}         ssid_name=${SSID_00}
    Set To Dictionary              ${WIRELESS_ENHANCED_01}         ssid_name=${SSID_01}
    Set To Dictionary              ${WIRELESS_ENHANCED_02}         ssid_name=${SSID_02}

    ${STATUS}                      create network policy if does not exist    ${POLICY}    &{WIRELESS_ENHANCED_00}
    should be equal as strings     '${STATUS}'       '1'
    ${STATUS}                      create ssid to policy    ${POLICY}      &{WIRELESS_ENHANCED_01}
    should be equal as strings     '${STATUS}'       '1'
    ${STATUS}                      create ssid to policy    ${POLICY}      &{WIRELESS_ENHANCED_02}
    should be equal as strings     '${STATUS}'       '1'
    ${STATUS}                      add ap template from common object      ${ap1.model}       ${AP_TEMP_NAME}   &{AP_TEMPLATE_1}
    Should Be Equal As Strings     '${STATUS}'       '1'
    ${STATUS}                      add ap template to network policy       ${AP_TEMP_NAME}    ${POLICY}
    Should Be Equal As Strings     '${STATUS}'       '1'

Step2: Assign network policy to AP
    [Documentation]     Assign network policy to AP
    [Tags]              tcxm-18041    tcxm-18043    tcxm-18044    tcxm-18045       development     step2      steps
    Depends On          Step1
    ${UPDATE}                      Update Network Policy To Ap             ${POLICY}          ${ap1.serial}      Complete
    should be equal as strings     '${UPDATE}'        '1'
    ${STATUS}                      Wait Until Device Online                ${ap1.serial}
    Should Be Equal As Strings     '${STATUS}'        '1'
    ${STATUS}                      Get Device Status                       ${ap1.serial}
    Should Be Equal As Strings     '${STATUS}'        'green'
    Enable disable client Wifi device                 ${mu1}

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
    ${OUT}            get real time client360 details    ${mu1.wifi_mac}
    ${OUT}            convert to string                  ${OUT}
    should contain    ${OUT}                             ${mu1.wifi_mac}

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
    ${OUT}            get real time client360 details    ${mu1.wifi_mac}
    ${OUT}            convert to string                  ${OUT}
    should contain    ${OUT}                             ${mu1.wifi_mac}

Step7: MU connect to wifi2 - Transition mode disable
    [Documentation]     MU connect to wifi2 - Enhanced Open SSID with transition mode disable
    [Tags]              tcxm-18041     tcxm-18045     development     step7     step02    steps
    Depends On          Step2
    FOR    ${i}    IN RANGE    ${retry}
        ${STATUS}               rem_mu.connect owe network      ${SSID_02}
        exit for loop if        '${STATUS}'=='1'
    END
    should be equal as strings      '${STATUS}'     '1'

Step8: Verify Client360 to wifi2 - Transition mode disable
    [Documentation]     Verify Client360 to wifi2 - Enhanced Open SSID with transition mode disable
    [Tags]              tcxm-18041     tcxm-18045     development     step8     step02    steps
    Depends On          Step7
    ${OUT}            get real time client360 details    ${mu1.wifi_mac}
    ${OUT}            convert to string                  ${OUT}
    should contain    ${OUT}                             ${mu1.wifi_mac}

Step9: Verify cli in wifi0-1 - Transition mode enable
    [Documentation]     Verify cli in wifi0-1 - Enhanced Open SSID with transition mode anable
    [Tags]              tcxm-12175   tcxm-12176   tcxm-12180   development     step9    steps
    Depends On          Step8
    ${AP_SPAWN}         Open Spawn       ${ap1.ip}      ${ap1.port}    ${ap1.username}    ${ap1.password}    ${ap1.cli_type}
    ${OUT}              Send             ${AP_SPAWN}    show run | inc OWE
    Close Spawn         ${AP_SPAWN}
    should contain      ${OUT}    ssid OWE-${SSID_01}
    should contain      ${OUT}    ssid OWE-${SSID_01} hide-ssid
    should contain      ${OUT}    ssid OWE-${SSID_01} security-object OWE-${SSID_01}

Step10: Verify cli in wifi2 - Transition mode disable
    [Documentation]     Verify cli in wifi2 - Enhanced Open SSID with transition mode disable
    [Tags]              tcxm-12164    development     step10     steps
    Depends On          Step8
    ${AP_SPAWN}         Open Spawn       ${ap1.ip}      ${ap1.port}    ${ap1.username}    ${ap1.password}    ${ap1.cli_type}
    ${OUT}              Send             ${AP_SPAWN}    show run | inc ${SSID_02}
    Close Spawn         ${AP_SPAWN}
    should contain      ${OUT}    security-object ${SSID_02}
    should contain      ${OUT}    security-object ${SSID_02} security protocol-suite owe mfp mandatory bip
    should contain      ${OUT}    ssid ${SSID_02}
    should contain      ${OUT}    ssid ${SSID_02} security-object ${SSID_02}

*** Keywords ***
Pre_condition
    ${STATUS}                           Login User    ${tenant_username}   ${tenant_password}
    should be equal as strings          '${STATUS}'   '1'
    reset devices to default
    log to console                      Wait for 2 minutes for completing reboot....
    sleep                               2m
    delete all aps
    delete all network policies
    delete all ssids
    delete all ap templates

Post_condition
    Logout User
    Quit Browser

Enable_disable_client_Wifi_device
    [Arguments]     ${mu}
    ${SPAWN}        Open Spawn    ${mu}[ip]     22    ${mu}[username]    ${mu}[password]    cli_type=MU-WINDOWS
    Send Commands   ${SPAWN}      pnputil /disable-device /deviceid \"PCI\\CC_0280\", pnputil /enable-device /deviceid \"PCI\\CC_0280\"
    [Teardown]      run keyword   Close Spawn   ${SPAWN}