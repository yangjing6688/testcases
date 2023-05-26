#########################################################################################################
# Author        : Binh Nguyen
# Date          : May 12th 2022
# Description   : TCXM-18034, Personal SSID with CWP enable for Wifi2
#                 TCXM-18035, Personal SSID with CWP disabled for Wifi2
#                 TCXM-18036, Personal SSID with CWP enable for Wifi0/1
#                 TCXM-18037, Personal SSID with CWP disabled for Wifi0/1
#                 TCXM-18038, Personal SSID with CWP enable for Wifi0/1 & 2
#                 TCXM-18039, Personal SSID with CWP disabled for Wifi0/1 & 2
#########################################################################################################

**** Variables ***
################## Policy Detail & Wireless Network ###############################
&{WIRELESS_PERSONAL_00}     ssid_name=""    network_type=Standard    ssid_profile=&{BORADCAST_SSID_00}     auth_profile=&{PERSONAL_AUTH_PROFILE_00}
&{WIRELESS_PERSONAL_01}     ssid_name=""    network_type=Standard    ssid_profile=&{BORADCAST_SSID_00}     auth_profile=&{PERSONAL_AUTH_PROFILE_01}
&{WIRELESS_PERSONAL_02}     ssid_name=""    network_type=Standard    ssid_profile=&{BORADCAST_SSID_01}     auth_profile=&{PERSONAL_AUTH_PROFILE_02}
&{WIRELESS_PERSONAL_03}     ssid_name=""    network_type=Standard    ssid_profile=&{BORADCAST_SSID_01}     auth_profile=&{PERSONAL_AUTH_PROFILE_03}
&{WIRELESS_PERSONAL_04}     ssid_name=""    network_type=Standard    ssid_profile=&{BORADCAST_SSID_02}     auth_profile=&{PERSONAL_AUTH_PROFILE_00}
&{WIRELESS_PERSONAL_05}     ssid_name=""    network_type=Standard    ssid_profile=&{BORADCAST_SSID_02}     auth_profile=&{PERSONAL_AUTH_PROFILE_01}

&{BORADCAST_SSID_00}        WIFI0=Enable        WIFI1=Enable      WIFI2=Disable
&{BORADCAST_SSID_01}        WIFI0=Disable       WIFI1=Disable     WIFI2=Enable
&{BORADCAST_SSID_02}        WIFI0=Disable       WIFI1=Enable      WIFI2=Disable

&{PERSONAL_AUTH_PROFILE_00}     auth_type=PSK   key_encryption=&{PSK_KEY_ENCRYPTION_00}   cwp_config=&{PSK_CWP_00}
&{PERSONAL_AUTH_PROFILE_01}     auth_type=PSK   key_encryption=&{PSK_KEY_ENCRYPTION_00}   cwp_config=&{PSK_CWP_01}
&{PERSONAL_AUTH_PROFILE_02}     auth_type=PSK   key_encryption=&{PSK_KEY_ENCRYPTION_01}   cwp_config=&{PSK_CWP_00}
&{PERSONAL_AUTH_PROFILE_03}     auth_type=PSK   key_encryption=&{PSK_KEY_ENCRYPTION_01}   cwp_config=&{PSK_CWP_01}

&{PSK_KEY_ENCRYPTION_00}        key_management=WPA2-(WPA2 Personal)-PSK    encryption_method=CCMP (AES)    key_type=ASCII Key   key_value=aerohive
&{PSK_KEY_ENCRYPTION_01}        key_management=WPA3 (SAE)    encryption_method=CCMP (AES)   sae_group=All    transition_mode=disable    key_value=aerohive
...                             anti_logging_Threshold=5     key_type=ASCII Key

&{PSK_CWP_00}                   enable_cwp=Disable
&{PSK_CWP_01}                   enable_cwp=Enable    enable_upa=Enable    cwp_name=""

################## Device Templates ###############################
&{AP_TEMPLATE_1}         wifi0_configuration=&{AP_TEMPLATE_1_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_1_WIFI1}   wifi2_configuration=&{AP_TEMPLATE_1_WIFI2}
&{AP_TEMPLATE_1_WIFI0}   radio_status=On     radio_profile=radio_ng_11ax-2g     client_mode=Disable    client_access=Enable    backhaul_mesh_link=Disable   sensor=Disable
&{AP_TEMPLATE_1_WIFI1}   radio_status=On     radio_profile=radio_ng_11ax-5g     client_mode=Disable    client_access=Enable    backhaul_mesh_link=Disable   sensor=Disable
&{AP_TEMPLATE_1_WIFI2}   radio_status=on     radio_profile=radio_ng_11ax-6g                            client_access=Enable    backhaul_mesh_link=Disable   sensor=Disable

&{AP_TEMPLATE_2}         wifi0_configuration=&{AP_TEMPLATE_2_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_2_WIFI1}
&{AP_TEMPLATE_2_WIFI0}   radio_status=On     radio_profile=radio_ng_11ax-6g     client_mode=Disable    client_access=Enable    backhaul_mesh_link=Disable   sensor=Disable
&{AP_TEMPLATE_2_WIFI1}   radio_status=On     radio_profile=radio_ng_11ax-5g     client_mode=Disable    client_access=Enable    backhaul_mesh_link=Disable   sensor=Disable

############### Globle Variables ######################
${retry}     3

*** Settings ***
Library     String
Library     Collections
Library     DependencyLibrary

Library     common/Cli.py
Library     common/Utils.py
Library     common/tools/remote/WinMuConnect.py

# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
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

Force Tags       testbed_none
Suite Setup      Pre_condition
Suite Teardown   Post_condition

*** Test Cases ***
Step1: Create Policy - Personal SSID with CWP
    [Documentation]     Create policy, select wifi0-1, and update policy to AP
    [Tags]              tcxm-18034  tcxm-18035   tcxm-18036   tcxm-18037   tcxm-18038   tcxm-18039   development   step1   steps

    ${NUM}                         Generate Random String    5     012345678
    Set Suite Variable             ${POLICY}                       personal_w0_1_${NUM}
    Set Suite Variable             ${SSID_00}                      w0_1_dis_${NUM}
    Set Suite Variable             ${SSID_01}                      w0_1_en_${NUM}
    Set Suite Variable             ${SSID_02}                      w2_dis_${NUM}
    Set Suite Variable             ${SSID_03}                      w2_en_${NUM}
    Set To Dictionary              ${PSK_CWP_01}                   cwp_name=cwp_name_${NUM}
    Set To Dictionary              ${PERSONAL_AUTH_PROFILE_01}     cwp_config=${PSK_CWP_01}
    Set To Dictionary              ${PERSONAL_AUTH_PROFILE_03}     cwp_config=${PSK_CWP_01}
    Set Suite Variable             ${AP_TEMP_NAME}                 ${ap1.model}_${NUM}
    ${WIRELESS_PERSONAL_00}        set variable if    '${ap1.model}' != 'AP3000'    ${WIRELESS_PERSONAL_00}    ${WIRELESS_PERSONAL_04}
    ${WIRELESS_PERSONAL_01}        set variable if    '${ap1.model}' != 'AP3000'    ${WIRELESS_PERSONAL_01}    ${WIRELESS_PERSONAL_05}
    ${AP_TEMPLATE_1}               set variable if    '${ap1.model}' != 'AP3000'    ${AP_TEMPLATE_1}           ${AP_TEMPLATE_2}
    Set To Dictionary              ${WIRELESS_PERSONAL_00}         ssid_name=${SSID_00}
    Set To Dictionary              ${WIRELESS_PERSONAL_01}         ssid_name=${SSID_01}      auth_profile=${PERSONAL_AUTH_PROFILE_01}
    Set To Dictionary              ${WIRELESS_PERSONAL_02}         ssid_name=${SSID_02}
    Set To Dictionary              ${WIRELESS_PERSONAL_03}         ssid_name=${SSID_03}      auth_profile=${PERSONAL_AUTH_PROFILE_03}

    ${STATUS}                      create network policy if does not exist    ${POLICY}   ${WIRELESS_PERSONAL_00}
    should be equal as strings     '${STATUS}'       '1'
    ${STATUS}                      create ssid to policy    ${POLICY}      &{WIRELESS_PERSONAL_01}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      create ssid to policy    ${POLICY}      &{WIRELESS_PERSONAL_02}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      create ssid to policy    ${POLICY}      &{WIRELESS_PERSONAL_03}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      add ap template from common object      ${ap1.model}       ${AP_TEMP_NAME}   ${AP_TEMPLATE_1}
    Should Be Equal As Strings     '${STATUS}'       '1'
    ${STATUS}                      add ap template to network policy       ${AP_TEMP_NAME}    ${POLICY}
    Should Be Equal As Strings     '${STATUS}'       '1'

Step2: Assign network policy to AP
    [Documentation]     Assign network policy to AP
    [Tags]              tcxm-18034   tcxm-18035   tcxm-18036   tcxm-18037   tcxm-18038   tcxm-18039   development   step2   steps

    Depends On Test     Step1: Create Policy - Personal SSID with CWP
    ${UPDATE}                      Update Network Policy To Ap             ${POLICY}          ${ap1.serial}      Complete
    should be equal as strings     '${UPDATE}'        '1'
    Wait_device_online              ${ap1}
    Enable disable client Wifi device                 ${mu1}

Step3: MU connect to wifi0-1 - CWP disabled
    [Documentation]     MU connect to wifi0-1 - Personal SSID with CWP disabled
    [Tags]              tcxm-18037   tcxm-18039   development   step3   step00    steps

    Depends On Test     Step2: Assign network policy to AP
    FOR    ${i}    IN RANGE    ${retry}
        ${STATUS}               rem_mu.connect wpa2 psk network      ${SSID_00}      ${WIRELESS_PERSONAL_00}[auth_profile][key_encryption][key_value]
        exit for loop if        '${STATUS}'=='1'
    END
    should be equal as strings    '${STATUS}'    '1'

Step4: Verify Client360 to wifi0_1 - CWP disabled
    [Documentation]     Verify Client360 to wifi0_1 - Personal SSID with CWP disabled
    [Tags]              tcxm-18037   tcxm-18039   development   step4   step00   steps

    Depends On Test     Step3: MU connect to wifi0-1 - CWP disabled
    ${OUT}            get real time client360 details    ${mu1.wifi_mac}
    ${OUT}            convert to string                  ${OUT}
    should contain    ${OUT}                             ${mu1.wifi_mac}

Step5: MU connect to wifi0-1 - CWP enable
    [Documentation]     MU connect to wifi0-1 - Personal SSID with CWP enable
    [Tags]              tcxm-18036   tcxm-18038   development   step5   step01   steps

    Depends On Test     Step2: Assign network policy to AP
    FOR    ${i}    IN RANGE    ${retry}
        ${STATUS}               rem_mu.connect wpa2 psk network      ${SSID_01}        ${WIRELESS_PERSONAL_01}[auth_profile][key_encryption][key_value]
        exit for loop if        '${STATUS}'=='1'
    END
    should be equal as strings                              '${STATUS}'       '1'
    open cp browser    ${mu1.ip}                             http://198.18.32.1
    ${STATUS}          accept user acceptance page
    should be equal as strings                              '${STATUS}'       '1'
    close cp browser

Step6: Verify Client360 to wifi0-1 - CWP enable
    [Documentation]     Verify Client360 to wifi0-1 - Personal SSID with CWP enable
    [Tags]              tcxm-18036   tcxm-18038   development   step6   step01   steps

    Depends On Test     Step5: MU connect to wifi0-1 - CWP enable
    ${OUT}             get client360 current connection status      ${mu1.wifi_mac}
    should contain     ${OUT['CWP']}                     Used

Step7: MU connect to wifi2 - CWP disabled
    [Documentation]     MU connect to wifi2 - Personal SSID with CWP disabled
    [Tags]              tcxm-18035   tcxm-18039   development   step7   step02   steps

    Depends On Test     Step2: Assign network policy to AP
    FOR    ${i}    IN RANGE    ${retry}
        ${STATUS}               rem_mu.connect wpa3 psk network      ${SSID_02}      ${WIRELESS_PERSONAL_02}[auth_profile][key_encryption][key_value]
        exit for loop if        '${STATUS}'=='1'
    END
    should be equal as strings    '${STATUS}'     '1'

Step8: Verify Client360 to wifi2 - CWP disabled
    [Documentation]     Verify Client360 to wifi2 - Personal SSID with CWP disabled
    [Tags]              tcxm-18035   tcxm-18039   development   step8   step02   steps

    Depends On Test     Step7: MU connect to wifi2 - CWP disabled
    ${OUT}            get real time client360 details    ${mu1.wifi_mac}
    ${OUT}            convert to string                  ${OUT}
    should contain    ${OUT}                             ${mu1.wifi_mac}

Step9: MU connect to wifi2 - CWP enable
    [Documentation]     MU connect to wifi2 - Personal SSID with CWP enable
    [Tags]              tcxm-18034   tcxm-18038   development   step9   step03   steps

    Depends On Test     Step2: Assign network policy to AP
    FOR    ${i}    IN RANGE    ${retry}
         ${STATUS}              rem_mu.connect wpa3 psk network      ${SSID_03}        ${WIRELESS_PERSONAL_03}[auth_profile][key_encryption][key_value]
         exit for loop if       '${STATUS}'=='1'
    END
    should be equal as strings                              '${STATUS}'       '1'
    open cp browser    ${mu1.ip}                             http://198.18.32.1
    ${STATUS}          accept user acceptance page
    should be equal as strings                              '${STATUS}'       '1'
    close cp browser

Step10: Verify Client360 to wifi2 - CWP enable
    [Documentation]     Verify Client360 to wifi2 - Personal SSID with CWP enable
    [Tags]              tcxm-18034   tcxm-18038   development   step10   step03   steps

    Depends On Test     Step9: MU connect to wifi2 - CWP enable
    ${OUT}             get client360 current connection status      ${mu1.wifi_mac}
    should contain     ${OUT['CWP']}                     Used

*** Keywords ***
Pre_condition
    ${STATUS}                           Login User    ${tenant_username}   ${tenant_password}
    should be equal as strings          '${STATUS}'   '1'
    reset devices to default
    log to console                      Wait for 2 minutes for completing reboot....
    sleep                               2m
    delete all devices
    delete all network policies
    delete all ssids
    delete all captive web portals      GA-UA-Self-Reg-CWP-Profile,GA-UPA-CWP-Profile
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

Enable_disable_client_Wifi_device
    [Arguments]     ${mu}
    ${SPAWN}        Open Spawn    ${mu}[ip]     22    ${mu}[username]    ${mu}[password]    cli_type=MU-WINDOWS
    Send Commands   ${SPAWN}      pnputil /disable-device /deviceid \"PCI\\CC_0280\", pnputil /enable-device /deviceid \"PCI\\CC_0280\"
    [Teardown]      run keyword   Close Spawn   ${SPAWN}

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