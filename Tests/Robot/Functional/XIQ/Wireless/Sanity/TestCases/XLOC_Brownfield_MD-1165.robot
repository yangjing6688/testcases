# Author        : Kiran
# Date          : Aug17,2021
# Description   : Extreme Location BrownField testacses
#
# Topology      :
# AP1----- Cloud-----Ubuntu(MU1)

# Pre-Condtion
# 1. AP1 should be onboarded and it should be in online in XIQ.
# 2. AP1 and Client1 should Present Inside RF Box Environment
# 3. For Running Test3 Need to create Category Creation Manually one time on Customer1 Account with Name "xloc_prod_sanity_en_cat" and assign to site "building_01"

# Execution Command:
# ------------------
#  robot -L INFO -v TEST_URL:https://extremecloudiq.com/ -v TESTBED:blr_tb_2 -v DEVICE1:AP410C_RF_BOX_001 -v TOPO:XLOC_Brownfield_topo XLOC_Brownfield_MD-1165.robot


*** Variables ***

${LOCATION}                 auto_location_01, San Jose, building_01, floor_02
${NW_POLICY_NAME}           xloc_prod_sanity_nw_pol
${SSID_NAME}                xloc_prod_sanity_ssid
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
    [Documentation]   AP onboarding  and check is online
    ${result}=                      Login User          ${tenant_username}     ${tenant_password}

    ${IMPORT_MAP}=                Import Map In Network360Plan  ${MAP_FILE_NAME}
    Should Be Equal As Strings    ${IMPORT_MAP}       1

    #Onboard AP                  ${ap1.serial}       aerohive
    ${ONBOARD_RESULT}=      Onboard Device      ${ap1.serial}           ${ap1.make}       location=${LOCATION}      device_os=${ap1.os}
    Should be equal as integers                 ${ONBOARD_RESULT}       1

    ${AP_SPAWN}=                Open Spawn          ${ap1.console_ip}       ${ap1.console_port}      ${ap1.username}       ${ap1.password}        ${ap1.platform}
    Set Suite Variable          ${AP_SPAWN}
    ${OUTPUT0}=                 Send Commands       ${AP_SPAWN}         capwap client server name ${capwap_url}, capwap client default-server-name ${capwap_url}, capwap client server backup name ${capwap_url}, no capwap client enable, capwap client enable, save config

    Wait Until Device Online    ${ap1.serial}

    Refresh Devices Page

    ${AP1_STATUS}=               Get AP Status       ap_mac=${ap1.mac}
    Should Be Equal As Strings  '${AP1_STATUS}'     'green'

    Logout User
    Quit Browser

*** Test Cases ***

TC-7297: Validate XLOC Config in already subscribed account
    [Documentation]         Existing Customer - BrownField Scenario with subscription and XLOC Config validation
    [Tags]                  production  sanity  config  subscription  brownfield   TC-7297
    ${LOGIN_XIQ}=                   Login User          ${tenant_username}     ${tenant_password}

    ${AP1_UPDATE_CONFIG}=           Update Network Policy To AP   ${NW_POLICY_NAME}     ap_serial=${ap1.serial}   update_method=Complete
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'

    Wait Until Device Online       ${ap1.serial}

    ${SUBSCRIBE_LOCATION}=          Subscribe Extreme Location Essentials
    Should Be Equal As Strings      '${SUBSCRIBE_LOCATION}'   '1'

    Log to Console      Sleep for ${config_push_wait}
    sleep                         ${config_push_wait}

    ${AP_SPAWN}=                Open Spawn          ${ap1.console_ip}       ${ap1.console_port}      ${ap1.username}       ${ap1.password}        ${ap1.platform}
    ${SENSOR_WIFI_CONFIG}=     Send                ${AP_SPAWN}         show running-config | include "interface wifi2"
    Should Contain             ${SENSOR_WIFI_CONFIG}      interface wifi2 mode adsp-sensor

    ${IBEACON_CONFIG}=         Send                ${AP_SPAWN}         show running-config | include ble0
    Should Contain             ${IBEACON_CONFIG}      interface ble0 ibeacon enable
    Should Contain             ${IBEACON_CONFIG}      interface ble0 ibeacon-monitor enable

    ${CONFIG1}=                Send                ${AP_SPAWN}         show application-essentials info
    Should Contain             ${CONFIG1}          wifi2:  status:on  profile:default-xiq-profile

    ${CONFIG2}=                Send                ${AP_SPAWN}         show application-essentials profile
    Should Contain             ${CONFIG2}          Name:   default-xiq-profile

    ${CONFIG3}=                Send                ${AP_SPAWN}         show _adspsensor device-table | include 58:94:6B:65:11:DC
    #Should Contain             ${CONFIG3}          58:94:6B:65:11:DC

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TC-7298: Validate Presence and Category TC in already subscribed account after connecting client
    [Documentation]         Existing Customer - BrownField Scenario with Presence and Category TC after connecting client
    [Tags]                  production  sanity  connect  presence  category  brownfield   TC-7298
    Depends On          TC-7297
    ${LOGIN_XIQ}=                  Login User          ${tenant_username}     ${tenant_password}

    ${CLIENT_MAC_FORMAT}=          Convert To Client MAC  ${mu5.wifi_mac}
    ${MU5_SPAWN}=                  Open Spawn                  ${mu5.ip}               ${mu5.port}             ${mu5.username}      ${mu5.password}      ${mu5.platform}
    Set Suite Variable             ${MU5_SPAWN}
    Connect MU5 To Open Network    ${SSID_NAME}

    Log to Console      Sleep for ${client_connect_wait}
    sleep                         ${client_connect_wait}

    ${CLIENT_STATUS}=                Get Client Status   client_mac=${mu5.wifi_mac}
    Should Be Equal As Strings       '${CLIENT_STATUS}'      '1'

    ${PING_TRAFFIC}=            Send               ${MU5_SPAWN}        nohup timeout 360 ping google.com -I wlo1 &

    Go To Extreme Location Devices Wireless Devices Menu

    ${CLIENT_INFO}=                Get Client Information In Extreme Location Devices Page  ${CLIENT_MAC_FORMAT}  ${BUILDING_NAME}

    ${CLIENT_MAC}=                 Get From Dictionary       ${CLIENT_INFO}    client_mac
    ${EXPECTED_CLIENT_MAC}=        Convert MAC To Lower  ${CLIENT_MAC_FORMAT}
    Should Be Equal As Strings    '${CLIENT_MAC}'          '${EXPECTED_CLIENT_MAC}'

    ${CLIENT_TYPE}=                 Get From Dictionary       ${CLIENT_INFO}    device_type
    Should Be Equal As Strings     '${CLIENT_TYPE}'          'Visitor'

    ${CLIENT_ENTRY_VALIDATION}=     Validate Client Entry In Extreme Location Sites Page    ${BUILDING_NAME}   ${FLOOR_NAME}   ${CLIENT_MAC_FORMAT}
    Should Be Equal As Strings    '${CLIENT_ENTRY_VALIDATION}'    '${EXPECTED_CLIENT_MAC}'

    Navigate To Extreme Location Devices Menu

    ${CLIENT_INFO}=                Get Client Information In Extreme Location Devices Page  ${CLIENT_MAC_FORMAT}  ${BUILDING_NAME}

    ${CATEGORY_TYPE}=               Get From Dictionary       ${CLIENT_INFO}    category
    Should Be Equal As Strings     '${CATEGORY_TYPE}'          'xloc_prod_sanity_en_cat'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TC-10858: Switch off Client WiFi Interface, Delete Client and Validate Presence in Devices and Sites Page after DisConnecting Client
    [Documentation]         Existing Customer - BrownField Scenario - Switch off Client, Delete Client and Validate Presence
    [Tags]                  production  sanity  switchoff  delete  presence  disconnect  brownfield   TC-10858
    Depends On          TC-7297
    ${LOGIN_XIQ}=                   Login User          ${tenant_username}     ${tenant_password}


    ${MU5_SPAWN}=                  Open Spawn           ${mu5.ip}     ${mu5.port}     ${mu5.username}    ${mu5.password}    ${mu5.platform}
    Set Suite Variable             ${MU5_SPAWN}
    MU Interface Down              ${MU5_SPAWN}    ${mu5.interface}

    Log to Console      Sleep for ${client_connect_wait} secs After disconnecting Client
    sleep                         ${client_connect_wait}

    ${CLIENT_STATUS}=                Get Client Status   client_mac=${mu5.wifi_mac}
    #Should Be Equal As Strings       '${CLIENT_STATUS}'      '-1'

    Navigate To Manage Tab

    Navigate To Clients Tab

    ${DELETE_CLIENT_RT}=               Delete Client RealTime       ${CLIENT_DELETE_MAC}
    Should Be Equal As Strings      '${DELETE_CLIENT_RT}'        '1'

    ${CLIENT_MAC_FORMAT}=           Convert To Client MAC  ${mu5.wifi_mac}

    Go To Extreme Location Devices Wireless Devices Menu

    ${CLIENT_INFO}=                  Get Client Information In Extreme Location Devices Page  ${CLIENT_MAC_FORMAT}  ${BUILDING_NAME}
    Should Be Equal As Strings      '${CLIENT_INFO}'              '-1'

    Navigate To Extreme Location Sites Menu

    ${CLIENT_ENTRY_VALIDATION}=      Validate Client Entry In Extreme Location Sites Page  ${BUILDING_NAME}   ${FLOOR_NAME}   ${CLIENT_MAC_FORMAT}
    Should Be Equal As Strings       '${CLIENT_ENTRY_VALIDATION}'   '-1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TC-10860: Delete AP From Existing Customer Account
    [Documentation]         Existing Customer - BrownField Scenario - Delete AP
    [Tags]                  production  sanity  brownfield  apdelete   TC-10860

    ${LOGIN_XIQ}=                   Login User          ${tenant_username}     ${tenant_password}

    Delete Device  device_serial=${ap1.serial}

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser
