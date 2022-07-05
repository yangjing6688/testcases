# Author        : Ramkumar
# Date          : Feb05,2021
# Description   : Extreme Location Sanity testacses
#
# Topology      :
# AP1----- Cloud-----Ubuntu

# Pre-Condtion
# 1. AP should be onboarded and it should be in online in XIQ.
# 2. AP and Client should Present Inside RF Box Environment
# 2. Need two Customer Account to run this Feature.
# 3. Customer1 is Existing customer and XLOC will be Already Subscribed
# 4. Customer2 is New customer and XLOC will not already Subscribed.Also we need to Make sure Reset VIQ is happened Properly using testcase cleanup.
# 5. For Running Test3 Need to create Category Creation Manually one time on Customer1 Account with Name "automation_enga_category"

# Execution Command:
# ------------------
#  robot -L INFO -v TEST_URL:https://extremecloudiq.com/ TESTBED:blr_tb_2 -v DEVICE1:AP410C TOPO:production extreme_location_sanity.robot

*** Variables ***
${LOCATION}                 auto_location_01, San Jose, building_01, floor_02
${NW_POLICY_NAME}           automation_extreme_location
${SSID_NAME}                automation_extreme_location
${BUILDING_NAME}            building_01
${FLOOR_NAME}               floor_02
${MAP_FILE_NAME}            auto_location_01_1595321828282.tar.gz

*** Settings ***
Library     Collections
Library     String
Library     Dialogs
Library     common/Utils.py
Library     common/Cli.py
Library     common/Mu.py
Library     common/TestFlow.py

Library     xiq/flows/common/Login.py
Library     xiq/flows/common/Navigator.py

Library     xiq/flows/extreme_location/ExtremeLocation.py

Library     xiq/flows/manage/Client.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Location.py

Library     xiq/flows/configure/Wips.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/configure/DeviceTemplate.py

Library     xiq/flows/globalsettings/GlobalSetting.py

Library     xiq/flows/mlinsights/Network360Plan.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Resource     Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/extreme_location_sanity_config.robot

Suite Setup      Pre Condition

*** Keywords ***
Pre Condition
    [Documentation]   AP Should be onboarded  and it is online
    ${result}=                      Login User          ${tenant_username}     ${tenant_password}
    ${AP1_STATUS}=                  Get AP Status       ap_mac=${ap1.mac}
    Should Be Equal As Strings      '${AP1_STATUS}'     'green'
    ${IMPORT_MAP}=                  Import Map In Network360Plan  ${MAP_FILE_NAME}
    Should Be Equal As Strings      ${IMPORT_MAP}       1
    Create Network Policy           default_network_policy     &{OPEN_NW_01}
    Update Network Policy To AP     default_network_policy      ap_serial=${ap1.serial}
    Delete Network Policy           ${NW_POLICY_NAME}
    Delete SSID                     ${SSID_NAME}
    Delete AP Template Profile      ${ap1.model}
    Logout User
    Quit Browser

*** Test Cases ***

Test1: Check Extreme Location Subscription Flow For Existing Customer
    [Documentation]                 Check Extreme Location Subscription Flow
    [Tags]                          sanity  aerohive  P1   production   regression
    ${LOGIN_XIQ}=                   Login User          ${tenant_username}     ${tenant_password}

    ${LOCATION_RESULT}=             Assign Location With Device Actions         ${ap1.serial}       ${LOCATION}
    Should Be Equal As Integers     ${LOCATION_RESULT}      1       Unable to Assign Location to Device

    ${CREATE_POLICY1}=              Create Network Policy   ${NW_POLICY_NAME}      &{LOCATION_OPEN_NW}
    Should Be Equal As Strings      '${CREATE_POLICY1}'   '1'

    ${CREATE_AP_TEMPLATE}=          Add AP Template     ${ap1.model}    &{AP_TEMPLATE_CONFIG}
    Should Be Equal As Strings      '${CREATE_AP_TEMPLATE}'   '1'

    Enable Nw Presence Analytics    ${NW_POLICY_NAME}

    ${IBEACON_STATUS}=              Enable IBeacon Service In Network Policy  ${NW_POLICY_NAME}  test
    Should Be Equal As Strings      '${IBEACON_STATUS}'   '1'

    ${AP1_UPDATE_CONFIG}=           Update Network Policy To AP   ${NW_POLICY_NAME}     ap_serial=${ap1.serial}   update_method=Complete
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'

    Wait Until Device Online        ${ap1.serial}

    ${SUBSCRIBE_LOCATION}=          Subscribe Extreme Location Essentials
    Should Be Equal As Strings      '${SUBSCRIBE_LOCATION}'   '1'

    Log to Console      Sleep for ${config_push_wait}
    sleep                         ${config_push_wait}

    ${AP_SPAWN}=               Open Spawn          ${ap1.ip}   ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.platform}
    ${SENSOR_WIFI_CONFIG}=     Send                ${AP_SPAWN}         show running-config | include "interface wifi2"
    Should Contain             ${SENSOR_WIFI_CONFIG}      interface wifi2 mode adsp-sensor

    ${IBEACON_CONFIG}=         Send                ${AP_SPAWN}         show running-config | include ble0
    Should Contain             ${IBEACON_CONFIG}      interface ble0 ibeacon enable
    Should Contain             ${IBEACON_CONFIG}      interface ble0 ibeacon-monitor enable

    ${CONFIG1}=                Send                ${AP_SPAWN}         show application-essentials info
    Should Contain             ${CONFIG1}          wifi2:  status:on  profile:default-xiq-profile

    ${CONFIG2}=                Send                ${AP_SPAWN}         show application-essentials profile
    Should Contain             ${CONFIG2}          Name:   default-xiq-profile

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test2: Presence TC-Validate Client Presence after Connecting Client For Existing Customer
    [Documentation]         Presence TC-Validate Client Presence after Connecting Client
    [Tags]                  sanity  aerohive  P1   production   regression
    Depends On          Test1
    ${LOGIN_XIQ}=                  Login User          ${tenant_username}     ${tenant_password}

    Sleep    5 minutes

    ${CLIENT_MAC_FORMAT}=          Convert To Client MAC  ${mu5.wifi_mac}
    ${MU5_SPAWN}=                  Open Spawn                  ${mu5.ip}               ${mu5.port}             ${mu5.username}      ${mu5.password}      ${mu5.platform}
    Set Suite Variable             ${MU5_SPAWN}
    Connect MU5 To Open Network    ${SSID_NAME}

    Log to Console      Sleep for ${client_connect_wait}
    sleep                         ${client_connect_wait}

    ${CLIENT_STATUS}=                Get Client Status   client_mac=${mu5.wifi_mac}
    Should Be Equal As Strings       '${CLIENT_STATUS}'      '1'
    Close Spawn  ${MU5_SPAWN}

    Sleep    5 minutes

    Go To Extreme Location Devices Wireless Devices Menu

    ${CLIENT_INFO}=                Get Client Information In Extreme Location Devices Page  ${CLIENT_MAC_FORMAT}  ${BUILDING_NAME}

    ${CLIENT_MAC}=                 Get From Dictionary       ${CLIENT_INFO}    client_mac
    ${EXPECTED_CLIENT_MAC}=        Convert MAC To Lower  ${CLIENT_MAC_FORMAT}
    Should Be Equal As Strings    '${CLIENT_MAC}'          '${EXPECTED_CLIENT_MAC}'

    ${CLIENT_TYPE}=                 Get From Dictionary       ${CLIENT_INFO}    device_type
    Should Be Equal As Strings     '${CLIENT_TYPE}'          'Visitor'


    Sleep    5 minutes

    ${CLIENT_ENTRY_VALIDATION}=     Validate Client Entry In Extreme Location Sites Page    ${BUILDING_NAME}   ${FLOOR_NAME}   ${CLIENT_MAC_FORMAT}
    Should Be Equal As Strings    '${CLIENT_ENTRY_VALIDATION}'    '${EXPECTED_CLIENT_MAC}'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test3: Category TC-Validate Client Presence Category after Connecting Client For Existing Customer
    [Documentation]         Category TC-Validate Client Presence Category after Connecting Client For Existing Customer
    [Tags]                  sanity  aerohive  P1   production   regression
    Depends On          Test1  Test2
    ${LOGIN_XIQ}=                  Login User          ${tenant_username}     ${tenant_password}

    ${CLIENT_MAC_FORMAT}=          Convert To Client MAC  ${mu5.wifi_mac}

    Go To Extreme Location Devices Wireless Devices Menu

    ${CLIENT_INFO}=                Get Client Information In Extreme Location Devices Page  ${CLIENT_MAC_FORMAT}  ${BUILDING_NAME}

    ${CLIENT_MAC}=                 Get From Dictionary       ${CLIENT_INFO}    client_mac
    ${EXPECTED_CLIENT_MAC}=        Convert MAC To Lower  ${CLIENT_MAC_FORMAT}
    Should Be Equal As Strings    '${CLIENT_MAC}'          '${EXPECTED_CLIENT_MAC}'

    ${CATEGORY_TYPE}=               Get From Dictionary       ${CLIENT_INFO}    category
    Should Be Equal As Strings     '${CATEGORY_TYPE}'          'automation_enga_category'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test4: Switch off Client WiFi Interface
    [Documentation]         Switch off Client WiFi Interface
    [Tags]                  sanity  aerohive  P1   production   regression
    Depends On          Test1
    ${LOGIN_XIQ}=                   Login User          ${tenant_username}     ${tenant_password}

    ${MU5_SPAWN}=                  Open Spawn                  ${mu5.ip}               ${mu5.port}             ${mu5.username}      ${mu5.password}      ${mu5.platform}
    Set Suite Variable             ${MU5_SPAWN}
    MU Interface Down              ${MU5_SPAWN}    ${MU5_INTERFACE}

    Log to Console      Sleep for ${client_connect_wait} secs After disconnecting Client
    sleep                         ${client_connect_wait}

    ${CLIENT_STATUS}=                Get Client Status   client_mac=${mu5.wifi_mac}
    #Should Be Equal As Strings       '${CLIENT_STATUS}'      '-1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test5: Presence TC-Validate Client Presence on Sites Page after DisConnecting Client For Existing Customer
    [Documentation]         Presence TC-Validate Client Presence after DisConnecting Client For Existing Customer
    [Tags]                  aerohive  P1  regression
    Depends On          Test1  Test3


    ${CLIENT_MAC_FORMAT}=           Convert To Client MAC  ${mu5.wifi_mac}
    Sleep    15 minutes

    ${LOGIN_XIQ}=                   Login User          ${tenant_username}     ${tenant_password}

    Go To Extreme Location Sites Menu

    ${CLIENT_ENTRY_VALIDATION}=      Validate Client Entry In Extreme Location Sites Page  ${BUILDING_NAME}   ${FLOOR_NAME}   ${CLIENT_MAC_FORMAT}
    Should Be Equal As Strings       '${CLIENT_ENTRY_VALIDATION}'   '-1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test6: Presence TC-Validate Client Presence on wireless Devices Page after DisConnecting Client For Existing Customer
    [Documentation]         Presence TC-Validate Client Presence after DisConnecting Client For Existing Customer
    [Tags]                  aerohive  P1  regression
    Depends On          Test1  Test4  Test5

    ${LOGIN_XIQ}=                   Login User          ${tenant_username}     ${tenant_password}
    ${CLIENT_MAC_FORMAT}=           Convert To Client MAC  ${mu5.wifi_mac}

    Go To Extreme Location Devices Wireless Devices Menu

    ${CLIENT_INFO}=                  Get Client Information In Extreme Location Devices Page  ${CLIENT_MAC_FORMAT}  ${BUILDING_NAME}
    Should Be Equal As Strings      '${CLIENT_INFO}'              '-1'

    Quit Browser

    ${LOGIN_XIQ}=                   Login User          ${tenant_username}     ${tenant_password}

    Delete Device  device_serial=${ap1.serial}

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test7: Onboard AP on New customer Account
    [Documentation]         Onboard AP on New customer Account
    [Tags]                  sanity  aerohive  P1   production   regression
    ${LOGIN_XIQ}=               Login User          ${TENANT_USERNAME2}     ${TENANT_PASSWORD2}

    ${IMPORT_MAP}=                Import Map In Network360Plan  ${MAP_FILE_NAME}
    Should Be Equal As Strings    ${IMPORT_MAP}       1

    Onboard AP                  ${ap1.serial}       aerohive

    ${AP_SPAWN}=               Open Spawn          ${ap1.ip}   ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.platform}
    Set Suite Variable          ${AP_SPAWN}
    ${OUTPUT0}=                 Send Commands       ${AP_SPAWN}         capwap client server name ${capwap_url}, capwap client default-server-name ${capwap_url}, capwap client server backup name ${capwap_url}, no capwap client enable, capwap client enable, save config

    Wait Until Device Online    ${ap1.serial}

    Refresh Devices Page

    ${AP1_STATUS}=               Get AP Status       ap_mac=${ap1.mac}
    Should Be Equal As Strings  '${AP1_STATUS}'     'green'

    ${LOCATION_RESULT}=             Assign Location With Device Actions         ${ap1.serial}       ${LOCATION}
    Should Be Equal As Integers     ${LOCATION_RESULT}      1       Unable to Assign Location to Device

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test8: Check Extreme Location Subscription Flow For New Customer
    [Documentation]         heck Extreme Location Subscription Flow For New Customer
    [Tags]                  sanity  aerohive  P1   production   regression
    Depends On          Test7
    ${LOGIN_XIQ}=                   Login User          ${TENANT_USERNAME2}     ${TENANT_PASSWORD2}

    ${CREATE_POLICY1}=              Create Network Policy   ${NW_POLICY_NAME}      &{LOCATION_OPEN_NW}
    Should Be Equal As Strings      '${CREATE_POLICY1}'   '1'

    ${CREATE_AP_TEMPLATE}=          Add AP Template     ${ap1.model}    &{AP_TEMPLATE_CONFIG}
    Should Be Equal As Strings      '${CREATE_AP_TEMPLATE}'   '1'

    Enable Nw Presence Analytics    ${NW_POLICY_NAME}

    ${IBEACON_STATUS}=               Enable IBeacon Service In Network Policy  ${NW_POLICY_NAME}  test
    Should Be Equal As Strings      '${IBEACON_STATUS}'   '1'

    ${AP1_UPDATE_CONFIG}=           Update Network Policy To AP   ${NW_POLICY_NAME}     ap_serial=${ap1.serial}   update_method=Complete
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'

    ${SUBSCRIBE_LOCATION}=          Subscribe Extreme Location Essentials
    Should Be Equal As Strings      '${SUBSCRIBE_LOCATION}'   '1'

    wait until device reboots       ${ap1.serial}

    Log to Console      Sleep for ${config_push_wait}
    sleep                         ${config_push_wait}

    ${AP_SPAWN}=               Open Spawn          ${ap1.ip}       ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.platform}
    ${SENSOR_WIFI_CONFIG}=     Send                ${AP_SPAWN}         show running-config | include "interface wifi2"
    Should Contain             ${SENSOR_WIFI_CONFIG}      interface wifi2 mode adsp-sensor

    ${IBEACON_CONFIG}=         Send                ${AP_SPAWN}         show running-config | include ble0
    Should Contain             ${IBEACON_CONFIG}      interface ble0 ibeacon enable
    Should Contain             ${IBEACON_CONFIG}      interface ble0 ibeacon-monitor enable

    ${CONFIG1}=                Send                ${AP_SPAWN}         show application-essentials info
    Should Contain             ${CONFIG1}          wifi2:  status:on  profile:default-xiq-profile

    ${CONFIG2}=                Send                ${AP_SPAWN}         show application-essentials profile
    Should Contain             ${CONFIG2}          Name:   default-xiq-profile

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test9: Presence TC-Validate Client Presence after Connecting Client for New Customer
    [Documentation]         Presence TC-Validate Client Presence after Connecting Client for New Customer
    [Tags]                  sanity  aerohive  P1   production   regression
    Depends On          Test8
    ${LOGIN_XIQ}=                  Login User          ${TENANT_USERNAME2}     ${TENANT_PASSWORD2}
    ${CLIENT_MAC_FORMAT}=          Convert To Client MAC  ${mu5.wifi_mac}
    ${MU5_SPAWN}=                  Open Spawn                  ${mu5.ip}               ${mu5.port}             ${mu5.username}      ${mu5.password}      ${mu5.platform}
    Set Suite Variable             ${MU5_SPAWN}
    Connect MU5 To Open Network    ${SSID_NAME}

    Log to Console      Sleep for ${client_connect_wait}
    sleep                         ${client_connect_wait}

    ${CLIENT_STATUS}=                Get Client Status   client_mac=${mu5.wifi_mac}
    Should Be Equal As Strings       '${CLIENT_STATUS}'      '1'
    Close Spawn  ${MU5_SPAWN}

    Sleep    5 minutes

    Go To Extreme Location Devices Wireless Devices Menu

    ${CLIENT_INFO}=                Get Client Information In Extreme Location Devices Page  ${CLIENT_MAC_FORMAT}  ${BUILDING_NAME}

    ${CLIENT_MAC}=                 Get From Dictionary       ${CLIENT_INFO}    client_mac
    ${EXPECTED_CLIENT_MAC}=        Convert MAC To Lower  ${CLIENT_MAC_FORMAT}
    Should Be Equal As Strings    '${CLIENT_MAC}'          '${EXPECTED_CLIENT_MAC}'

    ${CLIENT_TYPE}=                 Get From Dictionary       ${CLIENT_INFO}    device_type
    Should Be Equal As Strings     '${CLIENT_TYPE}'          'Visitor'

    Sleep    5 minutes

    ${CLIENT_ENTRY_VALIDATION}=     Validate Client Entry In Extreme Location Sites Page  ${BUILDING_NAME}  ${FLOOR_NAME}   ${CLIENT_MAC_FORMAT}
    Should Be Equal As Strings    '${CLIENT_ENTRY_VALIDATION}'    '${EXPECTED_CLIENT_MAC}'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test Suite Clean Up
    [Documentation]         Test Suite Clean Up: Reset Customer Account Data
    [Tags]                  sanity  aerohive  P1   production   regression

    ${LOGIN_XIQ}=                   Login User          ${TENANT_USERNAME2}     ${TENANT_PASSWORD2}
    ${BACKUP_VIQ_DATA}=             Backup VIQ Data
    Should Be Equal As Strings      '${BACKUP_VIQ_DATA}'              '1'

    ${RESET_VIQ_DATA}=               Reset VIQ Data
    Should Be Equal As Strings      '${RESET_VIQ_DATA}'              '1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser
