## Author: Wenqi Cao
# Date: Aug 26 2022
# For CFD-7586: AP150W v10.4r3 DHCP issues(https://jira.extremenetworks.com/browse/CFD-7586)
# Workflow:
# - Login XIQ
# - Go to "Manage/Planning" to create a Location
# - Go to "Configure/Network Policies" to create a Network Policy
# - In above Network Policy, configure one PSK SSID
# - Onboard an AP150W
# - After AP150W onboarded successfully:
# ---- Upgrade AP150W to specific version
# ---- Change AP150W mode as ApAsRouter
# ---- Assign Network Policy and push complete config
# ---- Enable WAN access
# - Login AP to run commands to get vesion, eth0, mgt0 IP address
# - Login wireless client:
# ---- Get wifi interface name, and make its wifi interface connect to SSID
# ---- Get wireless station IPv4 address
# - Check if the 24 prefix of wireless station IPv4 in AP eth0 and mgt0 IPv4 address
# ---- Success if it is in AP mgt0 IPv4 address and NOT in AP Eth0 IPv4 address

*** Variables ***
########## For Local AIO testbed Start #########
${WEB_DRIVER_LOC}           local
${TENANT_USERNAME}          admin@cust001.com
${TENANT_PASSWORD}          aerohive
${TEST_URL}                 https://10.16.231.153/
${AIO_IP}                   10.16.231.153
${BROWSER}                  firefox

${SERIAL}                   01501807130357
${MAKE}                     Extreme - Aerohive
${DEVICE_FUNCTION}          ApAsRouter
${CONSOLE_IP}               10.16.143.229
${CONSOLE_PORT}             22
${AP_USERNAME}              admin
${AP_PASSWORD}              Aerohive123
${CLI_TYPE}                 AH-AP
${CONNECTION_METHOD}        ssh
${VERSION}                  10.4r3


${STA1_IP}                  10.16.141.165
${STA1_PORT}                22
${STA1_USERNAME}            admin
${STA1_PASSWORD}            Aerohive888
${STA1_CLI_TYPE}            MU-MAC
########## For Local AIO testbed End #########

*** Settings ***

# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     common/Cli.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Device360.py
Library     xiq/flows/common/Navigator.py
Library     String
Library     Collections
Library     re
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/extreme_location/ExtremeLocation.py
Library     xiq/flows/manage/Location.py
Library     xiq/flows/configure/ClassificationRule.py
Library     xiq/flows/configure/CloudConfigGroup.py
Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/manage/DeviceConfig.py
Library     xiq/flows/configure/UserGroups.py
Library     ../../extreme_automation_framework/ExtremeAutomation/Keywords/NetworkElementKeywords/Utils/NetworkElementCliSend.py


Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml
#Variables    TestBeds/${TESTBED}
#Variables    Environments/${TOPO}
#Variables    Environments/${ENV}

Resource    ../Resources/location_config.robot
Resource    ../Resources/wireless_networks_related_config.robot
Force Tags      testbed_none
Suite Setup      Pre Condition
Suite Teardown   Suite Clean Up

*** Keywords ***
Pre Condition
    [Documentation]   Login XIQ, create 1st location and Network Policy with PPSK SSID with cloud and local user groups, onboard simulate AP and assign Network Policy to it
    [Tags]                      cfd-7586     development    pre-condition

    ${device}=      Create Dictionary
    ...     serial=01501807130357
    ...     mac=123456

#### Login AIO
    ${Login_XIQ}=                  Login User              ${TENANT_USERNAME}      ${TENANT_PASSWORD}
    Should Be Equal As Integers    ${Login_XIQ}             1
## Create First Map info, you can go to /Resources/location_config.robot to change related parameters
    ${FIRST_MAP_CREATION}=      Create First Organization       ${1st_LOCATION_ORG}      ${1st_LOCATION_STREET}       ${1st_LOCATION_CITY_STATE}       ${1st_LOCATION_COUNTRY}      width=${MAP_WIDTH}      height=${MAP_HIGHT}
    Should Be Equal As Integers    ${FIRST_MAP_CREATION}             1

### Create Network Policy
    ${NW_POLICY_CREATION}=  Create Network Policy   ${NW_POLICY_NAME1}   ${WIRELESS_PESRONAL_WPA2CCMP_1}
    Should Be Equal As Strings   '${NW_POLICY_CREATION}'   '1'

### Onboard an real AP150W
    ${ONBOARD_AP_RESULT}=       Onboard AP      ${SERIAL}       ${MAKE}     location=${1st_LOCATION_ORG},${1st_LOCATION_CITY_STATE},${1st_LOCATION_STREET},Floor 1
    Should Be Equal As Integers     ${ONBOARD_AP_RESULT}        1

### Login AP150W as AP mode and set capwap server
    ${AP_SPAWN}=        Open Spawn          ${CONSOLE_IP}    ${CONSOLE_PORT}    ${AP_USERNAME}    ${AP_PASSWORD}    ${CLI_TYPE}
    Send                ${AP_SPAWN}         capwap client server name ${AIO_IP}
    Send                ${AP_SPAWN}         capwap client enable
    Send                ${AP_SPAWN}         save config
    Close Spawn     ${AP_SPAWN}

#### Wait AP to managed and online, and upgrade image to specific version
    ${WAIT_MANAGED}=        wait_until_device_managed       ${SERIAL}
    Should Be Equal As Integers    ${WAIT_MANAGED}    1

    ${WAIT_ONLINE}=         Wait Until Device Online       ${SERIAL}
    Should Be Equal As Integers    ${WAIT_ONLINE}    1

    ${UPGRADE_VERSION}=     Upgrade Device     ${device}   version=${VERSION}
    wait_until_device_update_done   device_serial=${SERIAL}

### Change AP150W device funtion as ApAsRouter mode
    configure_device_function       ${SERIAL}       ${DEVICE_FUNCTION}

### Wait AP online and push complete config to AP150W
    Wait Until Device Online       ${SERIAL}        retry_duration=10       retry_count=12
    ${UPDATE_NP_RESULT}=    Update Network Policy To Ap   policy_name=${NW_POLICY_NAME1}    ap_serial=${SERIAL}  update_method=Complete
    Should Be Equal As Integers    ${UPDATE_NP_RESULT}    1
    wait_until_device_update_done   device_serial=${SERIAL}

### Enable WAN access
    enable_device_wan_access        ${SERIAL}

Suite Clean Up
    [Documentation]    Delete all devices, all ssids, Network Policy, location user groups and quit web browser
    [Tags]             cfd-7586         cleanup     development          tcxm-21566
    Log To Console      ================================
    Log To Console      Login AP and reset it
    Log To Console      ================================
    ${AP_SPAWN}=        Open Spawn          ${CONSOLE_IP}       ${CONSOLE_PORT}      ${AP_USERNAME}       ${AP_PASSWORD}        ${CLI_TYPE}
    Send                ${AP_SPAWN}         reset config no-prompt
    Close Spawn    ${AP_SPAWN}
    Delete All devices
    Sleep    5
    delete_all_ssid_in_policy   ${NW_POLICY_NAME1}
    Delete Network Policy    ${NW_POLICY_NAME1}
    Delete Location Building Floor  ${1st_LOCATION_CITY_STATE}      ${1st_LOCATION_STREET}     Floor 1
    XIQ Quit Browser

*** Test Cases ***
CFD-7586_case: AP150W as Router: Wireless client gets IP address from WAN port DHCP server, NOT from its internal DHCP server
    [Documentation]     Make sure AP150W(Router) wireless client get IP address from internal DHCP server
    [Tags]                      cfd-7586    development    cfd-7586_case     tcxm-24873
# ssh to AP150W(Router) to get AP version, Eth0 and Mgt0 IPv4 addresses
    ${AP_SPAWN}=        Open Spawn          ${CONSOLE_IP}       ${CONSOLE_PORT}      ${AP_USERNAME}       ${AP_PASSWORD}        ${CLI_TYPE}
    Send                ${AP_SPAWN}         show version
    Send                ${AP_SPAWN}         interface wifi1 radio channel 40
    Send                ${AP_SPAWN}         interface wifi1 radio power 20
    Send                ${AP_SPAWN}         show interface eth0
    Send                ${AP_SPAWN}         show interface mgt0
    Send                ${AP_SPAWN}         show interface
    Send                ${AP_SPAWN}         show acsp
    ${MGT0_IP}=                Get Device Interface IPv4 Addr      ${AP_SPAWN}   ${CLI_TYPE}  mgt0
    ${ETH0_IP}=                Get Device Interface IPv4 Addr      ${AP_SPAWN}   ${CLI_TYPE}  eth0
    Close Spawn    ${AP_SPAWN}

    FOR    ${counter}    IN RANGE    1    11
        Log    ${counter}
        ${AP_SPAWN}=        Open Spawn          ${CONSOLE_IP}       ${CONSOLE_PORT}      ${AP_USERNAME}       ${AP_PASSWORD}        ${CLI_TYPE}
        Send                ${AP_SPAWN}         clear auth station
        Send                ${AP_SPAWN}         clear auth roaming-cache
        Send                ${AP_SPAWN}         clear auth local-cache
        Close Spawn    ${AP_SPAWN}
    # Go to wireless station to connect to SSID
        ${WIFI_CONN}=       Mac Wifi Connection     ${STA1_IP}      ${STA1_USERNAME}    ${STA1_PASSWORD}    ${WIRELESS_PESRONAL_WPA2CCMP_1}[ssid_name]      ssid_pass=${PSK_KEY_ENCRYPTION_WPA2CCMP}[key_value]
        Should Be Equal As Integers      ${WIFI_CONN}    1

    # ssh to wireless client to get its wireless IPv4 address
        ${WIFI_CLIENT_IPV4}=    Get MAC Wifi IPv4 Addr  ${STA1_IP}      ${STA1_USERNAME}    ${STA1_PASSWORD}
        ${WIFI_CLIENT_IPV4_24_NET_PREFIX}      Evaluate      re.search('\\d+\\.\\d+\\.\\d+', "${WIFI_CLIENT_IPV4}"),re

    # Make the 24 prefix of wireless client IPv4 be in Mgt0 IPv4 address and NOT in Eth0 IPv4 address
        Log To Console      The 24 prefix of wireless client IPv4 is: ${WIFI_CLIENT_IPV4_24_NET_PREFIX[0].group(0)}
        Log To Console         The Eth0 of AP150W IP Address is: ${ETH0_IP}
        Should Not Contain     ${ETH0_IP}      ${WIFI_CLIENT_IPV4_24_NET_PREFIX[0].group(0)}
        Log To Console         The Mgt0 of AP150W IP Address is: ${MGT0_IP}
        Should Contain         ${MGT0_IP}      ${WIFI_CLIENT_IPV4_24_NET_PREFIX[0].group(0)}
    END