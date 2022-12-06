#########################################################################################################
# Author        : Binh Nguyen
# Date          : April 19th 2022
# Description   : TCXM-16059
#                 Client Mode Wifi1 End to End without Web GUI
#########################################################################################################

**** Variables ***
################## Policy Detail & Wireless Network ###############################
&{WIRELESS_PESRONAL_ENT_00}     ssid_name=""    network_type=Standard    ssid_profile=&{BORADCAST_SSID_ENT_00}      auth_profile=&{PERSONAL_AUTH_PROFILE}
&{WIRELESS_PESRONAL_ENT_01}     ssid_name=""    network_type=Standard    ssid_profile=&{BORADCAST_SSID_ENT_01}      auth_profile=&{PERSONAL_AUTH_PROFILE}
&{WIRELESS_PESRONAL_CM}         ssid_name=""    network_type=Standard    ssid_profile=&{BORADCAST_SSID_CM}          auth_profile=&{PERSONAL_AUTH_PROFILE}

&{BORADCAST_SSID_ENT_00}=       WIFI0=Enable        WIFI1=Disable
&{BORADCAST_SSID_ENT_01}=       WIFI0=Disable       WIFI1=Enable
&{BORADCAST_SSID_CM}=           WIFI0=Enable        WIFI1=Enable

&{PERSONAL_AUTH_PROFILE}        auth_type=PSK   key_encryption=&{PSK_KEY_ENCRYPTION}   cwp_config=&{PSK_CWP_DEFAULT}
&{PSK_KEY_ENCRYPTION}           key_management=WPA2-(WPA2 Personal)-PSK    encryption_method=CCMP (AES)   key_type=ASCII Key     key_value=aerohive
&{PSK_CWP_DEFAULT}              enable_cwp=Disable

################## Device Templates ###############################
##### AP410C ######
&{AP_TEMPLATE_CONFIG_1}         wifi0_configuration=&{AP_TEMPLATE_CONFIG_1_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_CONFIG_1_WIFI1}
&{AP_TEMPLATE_CONFIG_1_WIFI0}   radio_status=On    radio_profile=radio_ng_11ax-2g     client_mode=Disable    client_mode_profile=&{client_mode_profile_wifi0}  client_access=Enable     backhaul_mesh_link=Disable   sensor=Disable
&{AP_TEMPLATE_CONFIG_1_WIFI1}   radio_status=Off   radio_profile=radio_ng_11ax-5g     client_mode=Disable    client_mode_profile=&{client_mode_profile_wifi1}  client_access=Disable    backhaul_mesh_link=Disable   sensor=Disable

##### AP150W & AP302W #####
&{AP_TEMPLATE_CONFIG_2}         wifi0_configuration=&{AP_TEMPLATE_CONFIG_2_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_CONFIG_2_WIFI1}
&{AP_TEMPLATE_CONFIG_2_WIFI0}   radio_status=On   radio_profile=radio_ng_ng0        client_mode=Enable     client_mode_profile=&{client_mode_profile_wifi0}    client_access=Disable    backhaul_mesh_link=Disable   sensor=Disable
&{AP_TEMPLATE_CONFIG_2_WIFI1}   radio_status=On   radio_profile=radio_ng_11ax-5g    client_mode=Disable    client_mode_profile=&{client_mode_profile_wifi1}    client_access=Enable     backhaul_mesh_link=Disable   sensor=Disable

&{CLIENT_MODE_PROFILE_WIFI0}    client_mode_profile_name=""    dhcp_server_scope=192.168.150.1     local_web_page=Disable     ssid_name=""     password=""    auth_method=Pre-Shared Key    key_type=ASCII
&{CLIENT_MODE_PROFILE_WIFI1}    client_mode_profile_name=""    dhcp_server_scope=192.168.151.1     local_web_page=Disable     ssid_name=""     password=""    auth_method=Pre-Shared Key    key_type=ASCII

*** Settings ***
Library     String
Library     Collections

Library     common/Cli.py
Library     common/Utils.py
Library     common/TestFlow.py
Library     common/tools/remote/MacMuConnect.py

Library     xiq/flows/common/Login.py
Library     xiq/flows/manage/AdvOnboard.py
Library     xiq/flows/manage/AdvanceOnboarding.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/DevicesActions.py
Library     xiq/flows/manage/DeviceConfig.py
Library     xiq/flows/manage/DeviceCliAccess.py

Library     xiq/flows/configure/DeviceTemplate.py

Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/ExternalWeb/ClientMode.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Library	    Remote 	http://${mu1.ip}:${mu1.port}   WITH NAME   mu1

Force Tags       testbed_1_node      testbed_2_node     testbed_3_node
Suite Setup      Pre_condition
Suite Teardown   Post_condition

*** Test Cases ***
Test1: Advance Onboard AP1 and AP2 - TCXM-16059
    [Documentation]    Advance Onboard AP1 and AP2
    [Tags]             tcxm-16059     development     test1     test
    ${aps}       Create List        ${ap1}        ${ap2}
    FOR     ${ap}   IN    @{aps}
        ${ONBOARD_STATUS}             onboard device quick    ${ap}
        should be equal as integers   ${ONBOARD_STATUS}       1
    END

Test2: Config AP1 and AP2 Capwap to Report AIO - TCXM-16059
    [Documentation]     Configure Capwap client server
    [Tags]              tcxm-16059     development    test2      test
    Depends On          Test1
    ${aps}       Create List        ${ap1}        ${ap2}
    FOR    ${ap}    IN    @{aps}
        ${AP_SPAWN}        Open Spawn          ${ap}[ip]   ${ap}[port]   ${ap}[username]   ${ap}[password]   ${ap}[cli_type]
        ${STATUS}          Configure Device To Connect To Cloud            ${ap}[cli_type]   ${capwap_url}    ${AP_SPAWN}
        Should Be Equal As Strings      '${STATUS}'       '1'
        ${STATUS}          Wait for Configure Device to Connect to Cloud   ${ap}[cli_type]   ${capwap_url}    ${AP_SPAWN}
        Should Be Equal As Strings      '${STATUS}'       '1'
        Close Spawn        ${AP_SPAWN}
    END
    [Teardown]      Run Keyword If Test Failed      Close Spawn     ${AP_SPAWN}

Test3: Check AP1 and AP2 Status On UI - TCXM-16059
    [Documentation]     Checks for ap1 ap2 status
    [Tags]              tcxm-16059      development     test3       test
    Depends On          Test2
    ${aps}=      Create List        ${ap1}        ${ap2}
    FOR    ${ap}    IN    @{aps}
        ${STATUS}       Wait Until Device Reboots          ${ap}[serial]
        Should Be Equal As Strings       '${STATUS}'       '1'
        ${STATUS}       Wait Until Device Online           ${ap}[serial]
        Should Be Equal As Strings       '${STATUS}'       '1'
        ${STATUS}       Get Device Status                  ${ap}[serial]
        Should contain any               ${STATUS}         green           config audit mismatch
    END

Test4: Create Policy and Update Policy to AP1 and AP2 - CXM-16059
    [Documentation]     Create policy and Update policy to AP1 and AP2
    [Tags]              tcxm-16059     development     test4      test
    Depends On          Test3
    ${NUM}                      Generate Random String    5     0123456789
    Set Suite Variable          ${POLICY}                       BkHaul_wifi0_${NUM}
    Set Suite Variable          ${SSID}                         bk_0_${NUM}
    Set Suite Variable          ${AP_TEMP_NAME}                 ${ap1.model}_${NUM}
    Set To Dictionary           ${WIRELESS_PESRONAL_ENT_00}     ssid_name=${SSID}

    Set Suite Variable          ${POLICY_CM}                    CM_wifi0_${NUM}
    Set Suite Variable          ${SSID_CM}                      CM_0_${NUM}
    Set Suite Variable          ${AP_TEMP_NAME_CM}              ${ap2.model}_${NUM}
    Set To Dictionary           ${WIRELESS_PESRONAL_CM}         ssid_name=${SSID_CM}
    ${CLIENT_PROFLE_NAME_CM}    set variable                    wifi0_${NUM}
    Set To Dictionary           ${CLIENT_MODE_PROFILE_WIFI0}    client_mode_profile_name=${CLIENT_PROFLE_NAME_CM}    ssid_name=${SSID}     password=${WIRELESS_PESRONAL_ENT_00}[auth_profile][key_encryption][key_value]
    Set To Dictionary           ${AP_TEMPLATE_CONFIG_2_WIFI0}   client_mode_profile=${CLIENT_MODE_PROFILE_WIFI0}
    Set To Dictionary           ${AP_TEMPLATE_CONFIG_2}         wifi0_configuration=${AP_TEMPLATE_CONFIG_2_WIFI0}

    ${STATUS}                      create network policy if does not exist            ${POLICY}          ${WIRELESS_PESRONAL_ENT_00}
    should be equal as strings     '${STATUS}'               '1'
    ${DHCP_STATUS}                 navigate to device config device config dhcp       ${ap1.mac}          enable
    Should Be Equal As Strings    '${DHCP_STATUS}'           '1'
    ${CREATE_AP_TEMPLATE}          add ap template from common object     ${ap1.model}         ${AP_TEMP_NAME}      &{AP_TEMPLATE_CONFIG_1}
    Should Be Equal As Strings     '${CREATE_AP_TEMPLATE}'   '1'
    ${SELECT_AP_TEMPLATE}          add ap template to network policy      ${AP_TEMP_NAME}      ${POLICY}
    Should Be Equal As Strings     '${SELECT_AP_TEMPLATE}'   '1'

    ${STATUS}                      create network policy if does not exist            ${POLICY_CM}       ${WIRELESS_PESRONAL_CM}
    should be equal as strings     '${STATUS}'               '1'
    ${CREATE_AP_TEMPLATE}          add ap template from common object      ${ap2.model}            ${AP_TEMP_NAME_CM}      &{AP_TEMPLATE_CONFIG_2}
    Should Be Equal As Strings     '${CREATE_AP_TEMPLATE}'   '1'
    ${SELECT_AP_TEMPLATE}          add ap template to network policy       ${AP_TEMP_NAME_CM}      ${POLICY_CM}
    Should Be Equal As Strings     '${SELECT_AP_TEMPLATE}'   '1'

    ${UPDATE}                      Update Network Policy To Ap    policy_name=${POLICY}       ap_serial=${ap1.serial}     update_method=Complete
    should be equal as strings     '${UPDATE}'               '1'
    ${STATUS}                      Wait Until Device Reboots      ${ap1.serial}
    Should Be Equal As Strings     '${STATUS}'               '1'
    ${STATUS}                      Wait Until Device Online       ${ap1.serial}
    Should Be Equal As Strings     '${STATUS}'               '1'
    ${STATUS}                      Get Device Status              ${ap1.serial}
    Should Be Equal As Strings     '${STATUS}'               'green'

    ${UPDATE}                      Update Network Policy To Ap    policy_name=${POLICY_CM}    ap_serial=${ap2.serial}     update_method=Complete
    should be equal as strings     '${UPDATE}'               '1'
    ${STATUS}                      Wait Until Device Reboots      ${ap2.serial}
    Should Be Equal As Strings     '${STATUS}'               '1'
    ${STATUS}                      Wait Until Device Online       ${ap2.serial}
    Should Be Equal As Strings     '${STATUS}'               '1'
    ${STATUS}                      Get Device Status              ${ap2.serial}
    Should Be Equal As Strings     '${STATUS}'               'green'

Test5: Setup WIFI on STA2 and Connect to AP2 - TCXM-16059
    [Documentation]     Setup WIFI on STA2 and Connect to AP2 on Client Mode
    [Tags]              tcxm-16059       development        test5      test
    Depends On          Test4
    Setup AP in Client Mode          ${ap2}
    mu1.connect wpa2 ppsk network    ${SSID_CM}          aerohive

Test6: Verify Connection - TCXM-16059
    [Documentation]     Setup WIFI on STA2 and Connect to AP2 on Client Mode
    [Tags]              tcxm-16059     development    test6      test
    Depends On          Test5
    sleep               20s
    Verify client mode ap     ${ap2}
    Verify station            ${mu1}     ${AP_TEMPLATE_CONFIG_2}[wifi0_configuration][client_mode_profile][dhcp_server_scope]

*** Keywords ***
Setup AP in Client Mode
    [Arguments]     ${ap}
    ${spawn}	        Open Spawn         ${ap}[console_ip]    ${ap}[console_port]    ${ap}[username]	 ${ap}[password]    AH-XR    connection_method=console
    Send                ${spawn}           console page 0
    Send                ${spawn}           interface eth0 shutdown
    ${out}     Send     ${spawn}           show interface
    log        ${out}
    ${out}     Send     ${spawn}           show station
    log        ${out}
    ${out}     Send     ${spawn}           show l3 interface
    log        ${out}
    Close Spawn         ${spawn}

Get Check Ping
    [Arguments]    ${output}
    ${loss}       Utils.Get Regexp Matches  ${output}   ([\\d\\.]+)% packet loss
    ${status}     Run Keyword And Return Status   Should Not Be Empty   ${loss}
    ${loss}       Run Keyword If    ${status}    Remove String    ${loss[0]}   % packet loss
    ${loss}       Set Variable If   ${status}   ${loss}    -1
    [Return]  ${loss}

Verify client mode ap
    [Arguments]    ${ap}
    ${spawn}	        Open Spawn         ${ap}[console_ip]    ${ap}[console_port]    ${ap}[username]	 ${ap}[password]    AH-XR    connection_method=console
    ${out}     Send     ${spawn}           show interface
    log        ${out}
    ${out}     Send     ${spawn}           show l3 interface
    log        ${out}
    Close Spawn         ${spawn}

Verify station
    [Arguments]    ${mu}    ${cm_gw_ip}
    ${spawn}        open paramiko ssh_spawn     ${mu}[ip]     ${mu}[username]    ${mu}[password]
    ${out}          send paramiko cmd           ${spawn}       ping -c 5 ${cm_gw_ip}
    log             ${out}
    ${out}          send paramiko cmd           ${spawn}       traceroute -m 5 www.google.com
    log             ${out}
    Should Contain  ${out}                      ${cm_gw_ip}
    ${out}          send paramiko cmd           ${spawn}        ping -c 5 www.google.com
    log             ${out}
    ${loss}         Get Check Ping              ${out}
    ${loss}         convert to number           ${loss}
    run keyword if                              ${loss} > 50    FAIL
    close paramiko spawn                        ${spawn}

    ${spawn}	    Open Spawn     ${ap2.console_ip}    ${ap2.console_port}    ${ap2.username}	 ${ap2.password}    AH-XR    connection_method=console
    Send            ${spawn}       no interface eth0 shutdown
    Close Spawn     ${spawn}

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
    delete_all_client_mode_profiles

Post_condition
    Logout User
    Quit Browser
