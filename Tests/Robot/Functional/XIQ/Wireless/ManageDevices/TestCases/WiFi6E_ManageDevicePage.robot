# Date          : 4th October 2021
# Description   : APC-45642: WiFi 6E - manage device page: Verify the 3 new columns of WiFi2 Power/WiFi2 Channel/WiFi2 Radio Profile values for AP 4000/Ap4000U.
# Precondition  : AP4000 or AP4000U Should be onboarded with a network policy having WiFi2 SSID.
#****************************************************************************************************************************************************************
# Execution Commands: The testcases in this script can be run either independently or together depending on the tags.
# robot -L INFO -i p2 WiFi6E_ManageDevicePage.robot
# robot -L INFO -i TC-8818 WiFi6E_ManageDevicePage.robot
# robot -L INFO -i TC-8809 WiFi6E_ManageDevicePage.robot
# robot -L INFO -i TC-8817 WiFi6E_ManageDevicePage.robot
# robot -L INFO -i TC-8810 WiFi6E_ManageDevicePage.robot
# robot -L INFO -i TC-10962 WiFi6E_ManageDevicePage.robot
# robot -L INFO -i TC-10961 WiFi6E_ManageDevicePage.robot
# robot -L INFO -i TC-10960 WiFi6E_ManageDevicePage.robot

# Select the "TOPO" and "DEVICE" variable based on Test bed to run the following execution
# robot -L INFO -v DEVICE:AP4000U -v TOPO:g2r1  WiFi6E_ManageDevicePage.robot
# robot -v TESTBED:/BANGALORE/Prod/wireless/xiq_blr_tb_sh_AP5010.yaml -v TOPO:topo.prod.g2r1.shilpa.yaml  -v ENV:environment.remote.win10.sh.chrome.yaml  -i tcxm-10960 WiFi6E_ManageDevicePage.robot

#****************************************************************************************************************************************************************
*** Variables ***

###WPA3 personal variable 

${INTERNET_PAGE_TITLE}           CNN International - Breaking News, US News, World News and Video
${WPA2_KEY_VALUE}                Extreme@123
${WPA3_KEY_VALUE}                Extreme@123
${WRONG_WPA2_KEY_VALUE}          Symbol@123
${CMD_SHOW_STATION}              show station
${NW_POLICY_NAME1}               automation_wpa2_personal
${NW_POLICY_NAME2}               automation_wpa3_personal
${NW_POLICY_SSID1}               automation_wpa2_personal
${NW_POLICY_SSID2}               automation_wpa3_personal
${NW_POLICY_NAME3}               AutoWPA2Auth
${WPA2_SSID}                     AutoWPA2Auth
${NW_POLICY_NAME4}               test_wpa_quatation
${NW_POLICY_SSID4}               test_wpa_quatation
${WPA2_KEY_QUATATION}            ABCD"1234

### AP1#####
${AP1_NAME}                     ${ap1.name}
${AP1_MODEL}                    ${ap1.model}
${AP1_DEVICE_TEMPLATE}          ${ap1.template}
${AP1_SERIAL}                   ${ap1.serial}
${AP1_OS}                       Cloud IQ Engine
${AP1_MAC}                      ${ap1.mac}
${AP1_BSSID}
${AP1_NETWORK_POLICY}           Test_wpa3_np
${AP1_USERNAME}                 ${ap1.username}
${AP1_PASSWORD}                 ${ap1.password}
${AP1_PLATFORM}                 ${ap1.platform}
${AP1_CONSOLE_IP}               ${ap1.console_ip}
${AP1_CONSOLE_PORT}             ${ap1.console_port}
${PORT_NUM}                     ${ap1.console_port}
${IP_ADDR}                      ${ap1.console_ip}
${AP1_IP}                       ${ap1.ip}
${AP1_COUNTRY}                  ${ap1.country}
${AP1_SSID}                     test_ssid_ap_01
${AP1_MAKE}                     ${ap1.make}
${VERSION}                      10.5r1
${AP1_Cli_Type}                 ${ap1.cli_type}
${LOCATION}                     Extreme Networks,  Eco space, 3B,  floor-1

## AP2 #######

${AP2_NAME}                     ${ap2.name}
${AP2_MODEL}                    ${ap2.model}
${AP2_DEVICE_TEMPLATE}          ${ap2.template}
${AP2_SERIAL}                   ${ap2.serial}
${AP2_OS}                       Cloud IQ Engine
${AP2_MAC}                      ${ap2.mac}
${AP2_BSSID}
${AP2_NETWORK_POLICY}           Test_np
${AP2_USERNAME}                 ${ap2.username}
${AP2_PASSWORD}                 ${ap2.password}
${AP2_PLATFORM}                 ${ap2.platform}
${AP2_CONSOLE_IP}               ${ap2.console_ip}
${AP2_CONSOLE_PORT}             ${ap2.console_port}
${PORT_NUM}                     ${ap2.console_port}
${IP_ADDR}                      ${ap2.console_ip}
${AP2_IP}                       ${ap2.ip}
${AP2_NETWORK_POLICY}           test_np_ap_01
${AP2_COUNTRY}                  ${ap2.country}
${AP2_SSID}                     test_ssid_ap_01
${AP2_MAKE}                     ${ap2.make}
${AP2_Cli_Type}                 ${ap2.cli_type}
${CHANNEL_INPUT}                '103'

*** Settings ***
Library     Collections
#Library     app/common/Cli.py
Library     extauto/common/Cli.py
Library     common/Utils.py
Library     common/TestFlow.py
Library     xiq/flows/common/Login.py
Library     xiq/flows/common/Navigator.py
Library     xiq/flows/manage/Client.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Device360.py
Library     xiq/flows/manage/DeviceCliAccess.py
Library     xiq/flows/manage/DeviceConfig.py
Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/ExpressNetworkPolicies.py
Library     xiq/elements/NetworkPolicyWebElements.py
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    TestBeds/${TESTBED}
Variables    Environments/Config/device_commands.yaml
Variables    Environments/Config/waits.yaml
Resource     Tests/Robot/Functional/XIQ/Wireless/ManageDevices/Resources/wpa3_personal_config.robot
Resource    testsuites/xiq/functional/WPA3_secuirty_config.robot

Force Tags   testbed_1_node
Suite Setup    Onboard AP5010U   ${AP1_NETWORK_POLICY}
Suite Teardown   Test Suite Clean Up

*** Keywords ***
Onboard AP5010U
    [Documentation]         AP5010 or AP5010U Should be onboarded with a network policy having WiFi2 SSID.
    [Arguments]             ${AP1_NETWORK_POLICY}
    ${result}=              Login User          ${TENANT_USERNAME}      ${TENANT_PASSWORD}
    Delete AP               ap_serial=${AP1_SERIAL}
    Change Device Password                      Aerohive123
    #${AP_SPAWN}=	Open Spawn  ${AP1_IP}  ${AP1_CONSOLE_PORT}   ${AP1_USERNAME}     ${AP1_PASSWORD}     ${AP1_PLATFORM}
    ${AP_SPAWN}=	Open Spawn      ${AP1_IP}   ${AP1_CONSOLE_PORT}   ${AP1_USERNAME}     ${AP1_PASSWORD}      ${AP1_Cli_Type}
    Set Suite Variable  ${AP_SPAWN}
    Send Commands       ${AP_SPAWN}         no capwap client enable, save config

    ${POLICY_RESULT}=                Create Network Policy   ${AP1_NETWORK_POLICY}      &{WIRELESS_PESRONAL_NW1}
    Should Be Equal As Strings      '${POLICY_RESULT}'   '1'
    ${ONBOARD_RESULT}=      onboard_ap_with_policy      ${AP1_SERIAL}           ${AP1_MAKE}       location=${LOCATION}      policy=${AP1_NETWORK_POLICY}        device_os=${AP1_OS}
    ${search_result}=       Search AP Serial    ${AP1_SERIAL}
    #${AP_SPAWN}=	Open Spawn  ${AP1_IP}  ${AP1_CONSOLE_PORT}   ${AP1_USERNAME}     ${AP1_PASSWORD}     ${AP1_PLATFORM}
    ${AP_SPAWN}=	Open Spawn      ${AP1_IP}   ${AP1_CONSOLE_PORT}   ${AP1_USERNAME}     ${AP1_PASSWORD}      ${AP1_Cli_Type}
    Set Suite Variable  ${AP_SPAWN}
    Send Commands       ${AP_SPAWN}         capwap client server name ${CAPWAP_URL}, capwap client default-server-name ${CAPWAP_URL}, capwap client server backup name ${CAPWAP_URL}, no capwap client enable, capwap client enable, save config
    Close Spawn         ${AP_SPAWN}
    Wait Until Device Online    ${AP1_SERIAL}
    Log to Console      Sleep for ${CONFIG_PUSH_WAIT}
    sleep                         ${CONFIG_PUSH_WAIT}
    Refresh Devices Page
    ${AP_STATUS}=                           Get AP Status       ap_serial=${AP1_SERIAL}
    should be equal as integers             ${result}   1
    should be equal as integers             ${ONBOARD_RESULT}   1
    should be equal as integers             ${search_result}    1
    should be equal as integers             ${POLICY_RESULT}    1
    should be equal as strings             '${AP_STATUS}'       'green'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test Suite Clean Up
    [Documentation]         delete created network policies, SSID, Device etc
    [Tags]                  sanity    p2   p3  p4  production  regression
    Login User              ${TENANT_USERNAME}      ${TENANT_PASSWORD}
    Delete AP     ${AP1_SERIAL}
    Delete AP     ${AP2_SERIAL}
    Delete Network Policy     ${AP1_NETWORK_POLICY}
    Delete ssid     ${NW_POLICY_SSID2}
    Logout User
    Quit Browser


*** Test Cases ***
TC-8818: Verify Column Wifi2 Radio Profile Default
    [Documentation]    Verify the new column values of WiFi2 Radio Profile for AP4000/AP4000U.
    [Tags]             development    tcxm-8818     p-1
    [Setup]            Login User      ${TENANT_USERNAME}     ${TENANT_PASSWORD}
    ${NAVIGATE}=    navigate_to_device_config_interface_wireless   ${AP1_MAC}
    should be equal as integers             ${NAVIGATE}         1
    ${WIFI2_RADIO_STATUS}=     enable_radio_status         ON      interface=wifi2
    should be equal as integers             ${WIFI2_RADIO_STATUS}     1
    ${RADIO_PROFILE_STATUS}=    get_wifi2_default_radio_profile
    should be equal as integers             ${RADIO_PROFILE_STATUS}      1
    #${AP_SPAWN}=	Open Spawn  ${AP1_IP}  ${AP1_CONSOLE_PORT}   ${AP1_USERNAME}     ${AP1_PASSWORD}     ${AP1_PLATFORM}
    ${AP_SPAWN}=	Open Spawn      ${AP1_IP}   ${AP1_CONSOLE_PORT}   ${AP1_USERNAME}     ${AP1_PASSWORD}      ${AP1_Cli_Type}
    ${OUTPUT2}=            Send Commands       ${AP_SPAWN}         show running-config | in wifi2
    Close Spawn            ${AP_SPAWN}
    Refresh Devices Page
    ${RADIO_PROFILE}=        Get Ap WIFI2 Radio Profile        ${AP1_SERIAL}
    should contain          ${OUTPUT2}      ${RADIO_PROFILE}
    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TC-8809: Verify Column Wifi2 Channel Default
    [Documentation]    Verify the new column values of WiFi2 Channel for AP 4000/Ap4000U.
    [Tags]             development    tcxm-8809     p-1
    [Setup]            Login User      ${TENANT_USERNAME}     ${TENANT_PASSWORD}
    ${NAVIGATE}=    navigate_to_device_config_interface_wireless   ${AP1_MAC}
    should be equal as integers             ${NAVIGATE}         1
    ${WIFI2_RADIO_STATUS}=     enable_radio_status         ON      interface=wifi2
    should be equal as integers             ${WIFI2_RADIO_STATUS}     1
    #${CHANNEL_STATUS}=      override_wifi2_channel     channel_input=Auto
    ${CHANNEL_STATUS}=      get_wifi2_default_channel_value
    should be equal as integers             ${CHANNEL_STATUS}   1
    ${CHANNEL}=      Get Ap Wifi2 Channel      ${AP1_SERIAL}
    #${AP_SPAWN}=	Open Spawn  ${AP1_IP}  ${AP1_CONSOLE_PORT}   ${AP1_USERNAME}     ${AP1_PASSWORD}     ${AP1_PLATFORM}
    ${AP_SPAWN}=	Open Spawn      ${AP1_IP}   ${AP1_CONSOLE_PORT}   ${AP1_USERNAME}     ${AP1_PASSWORD}      ${AP1_Cli_Type}
    ${OUTPUT2}=            Send Commands       ${AP_SPAWN}         show acsp | in wifi2
    Close Spawn            ${AP_SPAWN}
    Sleep   5sec
    Refresh Devices Page
    should contain    ${OUTPUT2}       ${CHANNEL}

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

#TC-10960: Verify Column Wifi2 Channel Manual
#    [Documentation]    Verify the column values of WiFi2 Channel by user entry for AP4000/AP4000U.
#    [Tags]             p2   development    tcxm-10960
#    [Setup]            Login User      ${TENANT_USERNAME}     ${TENANT_PASSWORD}
#
#    ${NAVIGATE}=    navigate_to_device_config_interface_wireless   ${AP1_MAC}
#    ${WIFI2_RADIO_STATUS}=     enable_radio_status         ON      interface=wifi2
#    ${CHANNEL_STATUS}=      set_wifi2_channel_from_d360      ${CHANNEL_INPUT}
#    sleep    2sec
#    Refresh Devices Page
#    #${AP_SPAWN}=	Open Spawn  ${AP1_IP}  ${AP1_CONSOLE_PORT}   ${AP1_USERNAME}     ${AP1_PASSWORD}     ${AP1_PLATFORM}
#    ${AP_SPAWN}=	Open Spawn      ${AP1_IP}   ${AP1_CONSOLE_PORT}   ${AP1_USERNAME}     ${AP1_PASSWORD}      ${AP1_Cli_Type}
#    ${OUTPUT2}=            Send Commands       ${AP_SPAWN}         show acsp | in wifi2
#    Close Spawn            ${AP_SPAWN}
#    ${CHANNEL}=      Get Ap Wifi2 Channel      ${AP1_SERIAL}
#    should contain          ${OUTPUT2}      ${CHANNEL}
#    should be equal as integers             ${NAVIGATE}         1
#    should be equal as integers             ${WIFI2_RADIO_STATUS}     1
#    should be equal as integers             ${CHANNEL_STATUS}   1
#    [Teardown]   run keywords       Logout User
#    ...                             Quit Browser

TC-8810: Verify Non Supported AP Model
    [Documentation]    Verify the 3 new columns names and values for non supported AP model
    [Tags]             development    tcxm-8810         p-1
    [Setup]            Login User      ${TENANT_USERNAME}     ${TENANT_PASSWORD}
    ${CHANNEL}=      Get Ap WIFI2 Channel      ${AP2_SERIAL}
    ${POWER}=        Get Ap WIFI2 Power        ${AP2_SERIAL}
    ${RADIO_PROFILE}=        Get Ap WIFI2 Radio Profile        ${AP2_SERIAL}
    should contain    ${CHANNEL}      N/A
    should contain    ${CHANNEL}      N/A
    should contain    ${RADIO_PROFILE}   N/A
    [Teardown]   run keywords       Logout User
    ...                             Quit Browser


