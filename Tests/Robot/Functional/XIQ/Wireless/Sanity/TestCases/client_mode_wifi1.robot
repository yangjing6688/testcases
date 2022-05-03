#########################################################################################################
# Author        : Binh Nguyen
# Date          : January 29th 2022
# Description   : APC-49419: TCXM-15129 - TCXM-15131 - TCXM-16058
#                 Client Mode Wifi1 End to End with Web GUI
#########################################################################################################

**** Variables ***
# Arguments passed from the command line
${LOCATION}                  auto_location_01, Santa Clara, building_02, floor_04
${DEVICE_MAKE_AEROHIVE}      Extreme - Aerohive

################## Policy Detail & Wireless Network ###############################
&{WIRELESS_PESRONAL_ENT_00}       ssid_name=ENT_00      network_type=Standard    ssid_profile=&{BORADCAST_SSID_ENT_00}      auth_profile=&{PERSONAL_AUTH_PROFILE}
&{WIRELESS_PESRONAL_ENT_01}       ssid_name=ENT_01      network_type=Standard    ssid_profile=&{BORADCAST_SSID_ENT_01}      auth_profile=&{PERSONAL_AUTH_PROFILE}
&{WIRELESS_PESRONAL_CM}           ssid_name=CM          network_type=Standard    ssid_profile=&{BORADCAST_SSID_CM}          auth_profile=&{PERSONAL_AUTH_PROFILE}

&{BORADCAST_SSID_ENT_00}=       WIFI0=Enable        WIFI1=Disable
&{BORADCAST_SSID_ENT_01}=       WIFI0=Disable       WIFI1=Enable
&{BORADCAST_SSID_CM}=           WIFI0=Enable        WIFI1=Enable

&{PERSONAL_AUTH_PROFILE}           auth_type=PSK   key_encryption=&{PSK_KEY_ENCRYPTION}   cwp_config=&{PSK_CWP_DEFAULT}
&{PSK_KEY_ENCRYPTION}              key_management=WPA2-(WPA2 Personal)-PSK    encryption_method=CCMP (AES)   key_type=ASCII Key     key_value=aerohive
&{PSK_CWP_DEFAULT}                 enable_cwp=Disable

################## Device Templates ###############################
##### AP410C ######
&{AP_TEMPLATE_CONFIG_1}         wifi0_configuration=&{AP_TEMPLATE_CONFIG_1_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_CONFIG_1_WIFI1}
&{AP_TEMPLATE_CONFIG_1_WIFI0}   radio_status=Off  radio_profile=radio_ng_11ax-2g     client_mode=Disable    client_mode_profile=&{client_mode_profile_wifi0}  client_access=Disable     backhaul_mesh_link=Disable   sensor=Disable
&{AP_TEMPLATE_CONFIG_1_WIFI1}   radio_status=On   radio_profile=radio_ng_11ax-5g     client_mode=Disable    client_mode_profile=&{client_mode_profile_wifi1}  client_access=Enable      backhaul_mesh_link=Disable   sensor=Disable
##### AP150W & AP302W #####
&{AP_TEMPLATE_CONFIG_2}         wifi0_configuration=&{AP_TEMPLATE_CONFIG_2_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_CONFIG_2_WIFI1}
&{AP_TEMPLATE_CONFIG_2_WIFI0}   radio_status=On   radio_profile=radio_ng_ng0     client_mode=Disable    client_mode_profile=&{client_mode_profile_wifi0}  client_access=Enable      backhaul_mesh_link=Disable   sensor=Disable
&{AP_TEMPLATE_CONFIG_2_WIFI1}   radio_status=On   radio_profile=radio_a0         client_mode=Enable   client_mode_profile=&{client_mode_profile_wifi1}    client_access=Disable     backhaul_mesh_link=Disable   sensor=Disable

&{CLIENT_MODE_PROFILE_WIFI0}    client_mode_profice_name=wifi0       dhcp_server_scope=192.168.150.1     local_web_page=Enable
&{CLIENT_MODE_PROFILE_WIFI1}    client_mode_profice_name=wifi1       dhcp_server_scope=192.168.151.1     local_web_page=Enable      ssid_name=""       password=""     auth_method=Pre-Shared Key    key_type=ASCII

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

Library	    Remote 	http://${mu2.ip}:${mu2.port}   WITH NAME   mu

Force Tags      testbed_1_node      testbed_2_node     testbed_3_node
Suite Setup     Cleanup

*** Test Cases ***
Test1: Advance Onboard AP1 and AP2 - TCXM-15129 - TCXM-15131
    [Documentation]    Advance Onboard AP1 and AP2
    [Tags]             xim_tc_15129     xim_tc_15131    development     test1     test
    ${aps}=      Create List        ${ap1}        ${ap2}
    ${LOGIN_STATUS}=                Login User                     ${tenant_username}     ${tenant_password}
    should be equal as strings     '${LOGIN_STATUS}'      '1'
    FOR     ${ap}   IN    @{aps}
        ${ONBOARD_STATUS}=               Advance Onboard Device         ${ap}[serial]    device_make=${DEVICE_MAKE_AEROHIVE}   dev_location=${LOCATION}
        should be equal as integers      ${ONBOARD_STATUS}       1
    END
    [Teardown]      run keywords     Logout User
    ...             AND              Quit Browser

Test2: Config AP1 and AP2 Capwap to Report AIO - TCXM-15129 - TCXM-15131
    [Documentation]     Configure Capwap client server
    [Tags]              xim_tc_15129     xim_tc_15131     development    test2      test
    Depends On          Test1
    ${aps}=      Create List        ${ap1}        ${ap2}
    FOR    ${ap}    IN    @{aps}
        ${AP_SPAWN}=        Open Spawn          ${ap}[console_ip]   ${ap}[console_port]      ${ap}[username]       ${ap}[password]        ${ap}[platform]
        Set Suite Variable  ${AP_SPAWN}
        ${OUTPUT0}=         Send Commands       ${AP_SPAWN}         capwap client server name ${capwap_url}, capwap client default-server-name ${capwap_url}, capwap client server backup name ${capwap_url}, no capwap client enable, capwap client enable, save config
        ${OUTPUT0}=         Send                ${AP_SPAWN}         console page 0
        ${OUTPUT0}=         Send                ${AP_SPAWN}         show version detail
        ${OUTPUT0}=         Send                ${AP_SPAWN}         show capwap client
        ${OUTPUT2}=         Send                ${AP_SPAWN}         ${cmd_capwap_hm_primary_name}
        ${OUTPUT3}=         Send                ${AP_SPAWN}         ${cmd_capwap_server_ip}
        ${OUTPUT1}=         Wait For CLI Output                     ${AP_SPAWN}         ${cmd_capwap_client_state}          ${output_capwap_status}
        Should Be Equal as Integers             ${OUTPUT1}          1
        Close Spawn         ${AP_SPAWN}
    END
    [Teardown]      Run Keyword If Test Failed      Close Spawn     ${AP_SPAWN}

Test3: Check AP1 and AP2 Status On UI - TCXM-15129 - TCXM-15131
    [Documentation]     Checks for ap1 ap2 status
    [Tags]              xim_tc_15129    xim_tc_15131      development     test3       test
    Depends On          Test2
    ${aps}=      Create List        ${ap1}        ${ap2}
    ${result}=          Login User          ${tenant_username}     ${tenant_password}
    FOR    ${ap}    IN    @{aps}
        Wait Until Device Online                ${ap}[serial]
        Wait Until Device Reboots               ${ap}[serial]
        Wait Until Device Online                ${ap}[serial]
        ${AP_STATUS}=                           Get AP Status       ap_mac=${ap}[mac]
        Should Be Equal As Strings             '${AP_STATUS}'       'green'
    END
    [Teardown]      run keywords     Logout User
    ...             AND              Quit Browser

Test4: Create Policy and Update Policy to AP1 and AP2 - CXM-15129 - TCXM-15131 - TCXM-16058
    [Documentation]     Create policy and Update policy to AP1 and AP2
    [Tags]              xim_tc_15129     xim_tc_15131    xim_tc_16058     development     test4      test
    Depends On          Test3
    ${NUM}=                     Generate Random String    4     0123456789
    Set Suite Variable          ${POLICY}                       BkHaul_wifi1_${NUM}
    Set Suite Variable          ${SSID}                         bk_1_${NUM}
    Set Suite Variable          ${AP_TEMP_NAME}                 ${ap1.model}_${NUM}
    Set To Dictionary           ${WIRELESS_PESRONAL_ENT_01}     ssid_name=${SSID}

    Set Suite Variable          ${POLICY_CM}                    CM_wifi1_${NUM}
    Set Suite Variable          ${SSID_CM}                      CM_1_${NUM}
    Set Suite Variable          ${AP_TEMP_NAME_CM}              ${ap2.model}_${NUM}
    Set To Dictionary           ${WIRELESS_PESRONAL_CM}         ssid_name=${SSID_CM}
    ${CLIENT_PROFLE_NAME_CM}    set variable                    wifi1_${NUM}
    Set To Dictionary           ${CLIENT_MODE_PROFILE_WIFI1}    client_mode_profice_name=${CLIENT_PROFLE_NAME_CM}
    Set To Dictionary           ${AP_TEMPLATE_CONFIG_2_WIFI1}   client_mode_profile=${CLIENT_MODE_PROFILE_WIFI1}
    Set To Dictionary           ${AP_TEMPLATE_CONFIG_2}         wifi1_configuration=${AP_TEMPLATE_CONFIG_2_WIFI1}

    ${result}=                     Login User                 ${tenant_username}     ${tenant_password}
    Create Network Policy          policy=${POLICY}     &{WIRELESS_PESRONAL_ENT_01}
    ${DHCP_STATUS}                 navigate to device config device config dhcp       ${ap1.mac}          enable
    Should Be Equal As Strings    '${DHCP_STATUS}'           '1'
    ${CREATE_AP_TEMPLATE}=         add ap template from common object     ${ap1.model}         ${AP_TEMP_NAME}      &{AP_TEMPLATE_CONFIG_1}
    Should Be Equal As Strings     '${CREATE_AP_TEMPLATE}'   '1'
    ${SELECT_AP_TEMPLATE}=         add ap template to network policy      ${AP_TEMP_NAME}      ${POLICY}
    Should Be Equal As Strings     '${SELECT_AP_TEMPLATE}'   '1'

    Create Network Policy          policy=${POLICY_CM}     &{WIRELESS_PESRONAL_CM}
    ${CREATE_AP_TEMPLATE}=         add ap template from common object      ${ap2.model}            ${AP_TEMP_NAME_CM}      &{AP_TEMPLATE_CONFIG_2}
    Should Be Equal As Strings     '${CREATE_AP_TEMPLATE}'   '1'
    ${SELECT_AP_TEMPLATE}=         add ap template to network policy       ${AP_TEMP_NAME_CM}      ${POLICY_CM}
    Should Be Equal As Strings     '${SELECT_AP_TEMPLATE}'   '1'

    ${UPDATE}=                     Update Network Policy To Ap    policy_name=${POLICY}      ap_serial=${ap1.serial}     update_method=Complete
    should be equal as strings     '${UPDATE}'               '1'
    Wait Until Device Reboots      ${ap1.serial}
    Wait Until Device Online       ${ap1.serial}
    ${AP1_STATUS}=                 Get AP Status              ap_mac=${ap1.mac}
    Should Be Equal As Strings     '${AP1_STATUS}'            'green'

    ${UPDATE}=                     Update Network Policy To Ap    policy_name=${POLICY_CM}    ap_serial=${ap2.serial}     update_method=Complete
    should be equal as strings     '${UPDATE}'              '1'
    Wait Until Device Reboots      ${ap2.serial}
    Wait Until Device Online       ${ap2.serial}
    ${AP2_STATUS}=                 Get AP Status              ap_mac=${ap2.mac}
    Should Be Equal As Strings     '${AP2_STATUS}'            'green'
    [Teardown]      run keywords   Logout User
    ...             AND            Quit Browser

Test5: Setup WIFI on STA2 and Connect to AP2 - TCXM-16058
    [Documentation]     Setup WIFI on STA2 and Connect to AP2 on Client Mode
    [Tags]              xim_tc_16058       development        test5      test
    Depends On          Test4
    ${mu}                 set variable               ${mu2}
    ${WEB_DRIVER_LOC}     set variable               remote
    ${OS_PLATFORM}        set variable               mac
    ${BROWSER}            set variable               firefox
    ${mac}                set variable               ${mu2.ip}
    ${WEBDRIVER_PORT}     set variable               4444
    ${test_url}           set variable               http://${AP_TEMPLATE_CONFIG_1_WIFI1}[client_mode_profile][dhcp_server_scope]/

    ${pid}                           Start Selenium      ${mu}
    mu.connect wpa2 ppsk network     ${SSID_CM}          aerohive
    Stop Selenium                    ${mu}               ${pid}
    Setup AP in Client Mode          ${ap2}
    ${pid}                           Start Selenium      ${mu}
    log                              ${pid}
    ${LOGIN_STATUS}                  login user client mode    ${ap2.username}     ${ap2.password}
    Should Be Equal As Strings       '${LOGIN_STATUS}'         '1'
    navigator client mode ssid
    ${WIFI_STATUS}                   manual passphrase ssid connect       ${SSID}       aerohive     WPA2
    Set Suite Variable               ${CM_IP}         ${WIFI_STATUS}[1]
    Should Be Equal As Strings       '${WIFI_STATUS}[0]'       '1'
    [Teardown]      run keywords     quit browser client mode
    ...             AND              Stop Selenium      ${mu}     ${pid}

Test6: Verify Connection - TCXM-16058
    [Documentation]     Setup WIFI on STA2 and Connect to AP2 on Client Mode
    [Tags]              xim_tc_16058     development    test6      test
    Depends On          Test5
    ${mu}               set variable        ${mu2}
    Verify client mode ap     ${ap2}        ${CM_IP}
    Verify station            ${mu}

*** Keywords ***
Setup AP in Client Mode
    [Arguments]     ${ap}
    ${spawn}	        Open Spawn         ${ap}[console_ip]    ${ap}[console_port]    ${ap}[username]	 ${ap}[password]  ${ap}[platform]
    Send                ${spawn}           console page 0
    Send                ${spawn}           interface eth0 shutdown
    ${out}     Send     ${spawn}           show interface
    log        ${out}
    ${out}     Send     ${spawn}           show station
    log        ${out}
    ${out}     Send     ${spawn}           show l3 interface
    log        ${out}
    Close Spawn         ${spawn}

Start Selenium
    [Arguments]       ${mu}
    ${spawn}    open pxssh spawn     ${mu}[ip]     ${mu}[username]     ${mu}[password]
    sleep       8s
    ${out}      Send pxssh 		     ${spawn}       ifconfig en1    10
    ${out}      convert to string    ${out}
    log         ${out}
    ${out}      Send pxssh           ${spawn}       nohup java -jar /Users/admin/Downloads/selenium-server-standalone-3.5.3.jar -log /tmp/selenium.log \ \&     10
    log         ${out}
    ${match}    ${selenium_pid}      Should Match Regexp       ${out}       \\[\\d+\\]\\s+(\\d+)
    log         ${selenium_pid}
    Close pxssh Spawn    ${spawn}
    [Return]       ${selenium_pid}

Stop Selenium
    [Arguments]      ${mu}      ${SELE_PID}
    ${spawn}    open pxssh spawn     ${mu}[ip]     ${mu}[username]     ${mu}[password]
    sleep       8s
    Send pxssh  		             ${spawn}       kill -9 ${SELE_PID}     10
    Close pxssh Spawn                ${spawn}

Get Check Ping
    [Arguments]    ${output}
    ${loss}=      Get Regexp Matches  ${output}   ([\\d\\.]+)% packet loss
    ${status}=    Run Keyword And Return Status   Should Not Be Empty   ${loss}
    ${loss}=      Run Keyword If    ${status}    Remove String    ${loss[0]}   % packet loss
    ${loss}=      Set Variable If   ${status}   ${loss}    -1
    [Return]  ${loss}

Cleanup
#    [Arguments]     @{ap_templates}
#    log             ${ap_templates}
    Login User      ${tenant_username}      ${tenant_password}
    delete all aps
    delete all network policies
#    Delete AP Templates            ${ap_templates}[0]       ${ap_templates}[1]
    Change Device Password         Aerohive123
    Logout User
    Quit Browser

Verify client mode ap
    [Arguments]    ${ap}    ${ip}
    ${spawn}	        Open Spawn         ${ap}[console_ip]    ${ap}[console_port]    ${ap}[username]	 ${ap}[password]  ${ap}[platform]
    ${out}     Send     ${spawn}           show interface
    log        ${out}
    ${out}     Send     ${spawn}           show l3 interface
    log        ${out}
    log        ${ip}
    Should Contain      ${out}             ${ip}
    Close Spawn         ${spawn}

Verify station
    [Arguments]    ${mu}
    ${spawn}    open paramiko ssh_spawn     ${mu}[ip]     ${mu}[username]     ${mu}[password]
    ${out}      send paramiko cmd           ${spawn}       ping -c 5 192.168.151.1           10
    log         ${out}
    sleep       10s
    ${out}      send paramiko cmd           ${spawn}       traceroute -m 5 www.google.com    10
    log         ${out}
    ${out}      send paramiko cmd           ${spawn}       ping -c 5 www.google.com          10
    log         ${out}
    ${loss}     Get Check Ping       ${out}
    Should Be Equal As Strings      '${loss}'       '0.0'
    close paramiko spawn             ${spawn}
