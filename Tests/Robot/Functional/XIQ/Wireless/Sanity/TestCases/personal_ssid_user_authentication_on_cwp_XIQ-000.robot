#########################################################################################################
# Author        : Binh Nguyen
# Date          : April 25th 2023
# Description   : TS-5183 (TR-62319, TR-62320, TR-62321)
#                 TCXM-43072  PAP Authentication Method
#                 TCXM-43074  CHAP Authentication Method
#                 TCXM-43075  MS-CHAPv2 Authentication Method
#########################################################################################################

**** Variables ***
################## Policy Detail & Wireless Network ###############################
&{WIRELESS_PESRONAL_00}    ssid_name=w0_1_pap      network_type=Standard   ssid_profile=&{BORADCAST_SSID_00}   auth_profile=&{PERSONAL_AUTH_PROFILE_00}
&{WIRELESS_PESRONAL_01}    ssid_name=w0_1_chap     network_type=Standard   ssid_profile=&{BORADCAST_SSID_00}   auth_profile=&{PERSONAL_AUTH_PROFILE_01}
&{WIRELESS_PESRONAL_02}    ssid_name=w0_1_mschap   network_type=Standard   ssid_profile=&{BORADCAST_SSID_00}   auth_profile=&{PERSONAL_AUTH_PROFILE_02}

&{BORADCAST_SSID_00}       WIFI0=Enable    WIFI1=Enable    WIFI2=Disable

&{PERSONAL_AUTH_PROFILE_00}     auth_type=PSK   key_encryption=&{PSK_KEY_ENCRYPTION_00}   cwp_config=&{PSK_CWP_00}
&{PERSONAL_AUTH_PROFILE_01}     auth_type=PSK   key_encryption=&{PSK_KEY_ENCRYPTION_00}   cwp_config=&{PSK_CWP_01}
&{PERSONAL_AUTH_PROFILE_02}     auth_type=PSK   key_encryption=&{PSK_KEY_ENCRYPTION_00}   cwp_config=&{PSK_CWP_02}

&{PSK_KEY_ENCRYPTION_00}        key_management=WPA2-(WPA2 Personal)-PSK   encryption_method=CCMP (AES)   key_type=ASCII Key   key_value=aerohive

&{PSK_CWP_00}                   enable_cwp=Enable   user_auth_on_cwp=Enable   enable_upa=disable   cwp_name=cwp_w0_1_pap      authentication_method=PAP          radius_server_group_config=&{RADIUS_SERVER_GROUP_00}
&{PSK_CWP_01}                   enable_cwp=Enable   user_auth_on_cwp=Enable   enable_upa=disable   cwp_name=cwp_w0_1_chap     authentication_method=CHAP         radius_server_group_config=&{RADIUS_SERVER_GROUP_00}
&{PSK_CWP_02}                   enable_cwp=Enable   user_auth_on_cwp=Enable   enable_upa=disable   cwp_name=cwp_w0_1_mschap   authentication_method=MS-CHAP V2   radius_server_group_config=&{RADIUS_SERVER_GROUP_00}

########## RADIUS Server Configure ##############
&{RADIUS_SERVER_GROUP_00}      radius_server_group_name=Rad_Server_Grp   radius_server_config=&{RADIUS_SERVER_00}

&{RADIUS_SERVER_00}            radius_server_group_desc=External Radius server group   server_type=EXTERNAL RADIUS SERVER   external_radius_server_config=&{EXTRENAL_RADIUS_SERVER_00}

&{EXTRENAL_RADIUS_SERVER_00}   radius_server_name=Rad_Sever_ip   ip_or_host_type=IP Address   radius_server_ip_host_name=Radius-IP   radius_server_ip_address=10.254.152.59   shared_secret=Symbol@123

&{LOGIN_CWP}                   username=user1   password=Aerohive123

################## Device Templates ###############################
&{AP_TEMPLATE_1}         wifi0_configuration=&{AP_TEMPLATE_1_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_1_WIFI1}
&{AP_TEMPLATE_1_WIFI0}   radio_status=On     radio_profile=radio_ng_11ax-2g     client_mode=Disable    client_access=Enable    backhaul_mesh_link=Disable   sensor=Disable
&{AP_TEMPLATE_1_WIFI1}   radio_status=On     radio_profile=radio_ng_11ax-5g     client_mode=Disable    client_access=Enable    backhaul_mesh_link=Disable   sensor=Disable

############### Globle Variables ######################
${RETRY}      3

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
Step1: Create Policy
    [Documentation]     Create policy, select wifi0-1, and update policy to AP
    [Tags]              tcxm-43072   tcxm-43074   tcxm-43075   development   step1   steps

    Set Suite Variable             ${POLICY}                       personal_cwp
    Set Suite Variable             ${AP_TEMP_NAME}                 ${ap1.model}_cwp

    ${STATUS}                      create network policy if does not exist   ${POLICY}   ${WIRELESS_PESRONAL_00}
    should be equal as strings     '${STATUS}'       '1'
    ${STATUS}                      create ssid to policy    ${POLICY}        &{WIRELESS_PESRONAL_01}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      create ssid to policy    ${POLICY}        &{WIRELESS_PESRONAL_02}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      add ap template from common object        ${ap1.model}       ${AP_TEMP_NAME}   ${AP_TEMPLATE_1}
    Should Be Equal As Strings     '${STATUS}'       '1'
    ${STATUS}                      add ap template to network policy         ${AP_TEMP_NAME}    ${POLICY}
    Should Be Equal As Strings     '${STATUS}'       '1'

Step2: Assign network policy to AP
    [Documentation]     Assign network policy to AP
    [Tags]              tcxm-43072   tcxm-43074   tcxm-43075    development   step2   steps

    Depends On Test     Step1: Create Policy
    ${UPDATE}                           Update Network Policy To Ap   ${POLICY}   ${ap1.serial}   Complete
    should be equal as strings          '${UPDATE}'                   '1'
    Wait_device_online                  ${ap1}
    Enable disable client Wifi device   ${mu1}

Step3: MU connect to wifi0-1 - CWP PAP
    [Documentation]     MU connect to wifi0-1 - CWP PAP
    [Tags]              tcxm-43072   tcxm-43074   tcxm-43075    development   step3   steps

    Depends On Test     Step2: Assign network policy to AP
    FOR   ${i}   IN RANGE   ${RETRY}
        ${STATUS}               rem_mu.connect wpa2 psk network   ${WIRELESS_PESRONAL_00}[ssid_name]   ${WIRELESS_PESRONAL_01}[auth_profile][key_encryption][key_value]
        exit for loop if        '${STATUS}'=='1'
    END
    should be equal as strings            '${STATUS}'              '1'
    open cp browser    ${mu1.ip}          http://198.18.36.1
    ${STATUS}          Login Guest User   ${LOGIN_CWP}[username]   ${LOGIN_CWP}[password]
    should be equal as strings            '${STATUS}'              '1'
    close cp browser

Step4: Verify Client360 to wifi0_1 - CWP PAP
    [Documentation]     Verify Client360 to wifi0_1 - CWP PAP
    [Tags]              tcxm-43072   tcxm-43074   tcxm-43075    development   step4   steps

    Depends On Test     Step3: MU connect to wifi0-1 - CWP PAP
    ${OUT}             get client360 current connection status   ${mu1.wifi_mac}
    should contain     ${OUT['USER']}                            ${LOGIN_CWP}[username]
    should contain     ${OUT['CWP']}                             Used
    should contain     ${OUT['SSID']}                            ${WIRELESS_PESRONAL_00}[ssid_name]

Step5: MU connect to wifi0-1 - CWP CHAP
    [Documentation]     MU connect to wifi0-1 - CWP CHAP
    [Tags]              tcxm-43072   tcxm-43074   tcxm-43075    development   step5   steps

    Depends On Test     Step2: Assign network policy to AP
    FOR   ${i}   IN RANGE   ${RETRY}
        ${STATUS}               rem_mu.connect wpa2 psk network   ${WIRELESS_PESRONAL_01}[ssid_name]   ${WIRELESS_PESRONAL_01}[auth_profile][key_encryption][key_value]
        exit for loop if        '${STATUS}'=='1'
    END
    should be equal as strings            '${STATUS}'              '1'
    open cp browser    ${mu1.ip}          http://198.18.36.1
    ${STATUS}          Login Guest User   ${LOGIN_CWP}[username]   ${LOGIN_CWP}[password]
    should be equal as strings            '${STATUS}'              '1'
    close cp browser

Step6: Verify Client360 to wifi0_1 - CWP CHAP
    [Documentation]     Verify Client360 to wifi0_1 - CWP CHAP
    [Tags]              tcxm-43072   tcxm-43074   tcxm-43075    development   step6   steps

    Depends On Test     Step5: MU connect to wifi0-1 - CWP CHAP
    ${OUT}             get client360 current connection status   ${mu1.wifi_mac}
    should contain     ${OUT['USER']}                            ${LOGIN_CWP}[username]
    should contain     ${OUT['CWP']}                             Used
    should contain     ${OUT['SSID']}                            ${WIRELESS_PESRONAL_01}[ssid_name]

Step7: MU connect to wifi0-1 - CWP MS-CHAP V2
    [Documentation]     MU connect to wifi0-1 - CWP MS-CHAP V2
    [Tags]              tcxm-43072   tcxm-43074   tcxm-43075    development   step7   steps

    Depends On Test     Step2: Assign network policy to AP
    FOR   ${i}   IN RANGE   ${RETRY}
        ${STATUS}               rem_mu.connect wpa2 psk network   ${WIRELESS_PESRONAL_02}[ssid_name]   ${WIRELESS_PESRONAL_01}[auth_profile][key_encryption][key_value]
        exit for loop if        '${STATUS}'=='1'
    END
    should be equal as strings            '${STATUS}'              '1'
    open cp browser    ${mu1.ip}          http://198.18.36.1
    ${STATUS}          Login Guest User   ${LOGIN_CWP}[username]   ${LOGIN_CWP}[password]
    should be equal as strings            '${STATUS}'              '1'
    close cp browser

Step8: Verify Client360 to wifi0_1 - CWP MS-CHAP V2
    [Documentation]     Verify Client360 to wifi0_1 - CWP MS-CHAP V2
    [Tags]              tcxm-43072   tcxm-43074   tcxm-43075    development   step8   steps

    Depends On Test     Step7: MU connect to wifi0-1 - CWP MS-CHAP V2
    ${OUT}             get client360 current connection status   ${mu1.wifi_mac}
    should contain     ${OUT['USER']}                            ${LOGIN_CWP}[username]
    should contain     ${OUT['CWP']}                             Used
    should contain     ${OUT['SSID']}                            ${WIRELESS_PESRONAL_02}[ssid_name]

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