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
### XLOC Details
${SUBSCRIBER_PUSH_URL_HTTPS}            https://testnotification.qa.xcloudiq.com:9095/WLSwebserver/notification
${SUBSCRIBER_PUSH_URL_HTTPS_WRONG}      https://testnotification.qa.xcloudiq.com:9094/WLSwebserver/notification
${SUBSCRIBER_USERNAME}                  admin
${SUBSCRIBER_PASSWORD}                  symbol123
${WIFI_ASSET_NAME}          xloc_prod_sanity_wifi_asset
${AS_CATEGORY_NAME}         xloc_prod_sanity_as_cat

${LOCATION}                 auto_location_01, San Jose, building_01, floor_02
${NW_POLICY_NAME}           xloc_prod_sanity_nw_pol
${SSID_NAME}                xloc_prod_sanity_ssid
${BUILDING_NAME}            building_01
${FLOOR_NAME}               floor_02
${MAP_FILE_NAME}            auto_location_01_1595321828282.tar.gz

*** Settings ***

Force Tags   testbed_3_node

Library     Collections
Library     String
Library     Dialogs
Library     common/Utils.py
Library     common/Cli.py
Library     common/Mu.py
Library     common/TestFlow.py

# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
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
Suite Teardown   Test Suite Clean Up

*** Keywords ***
Pre Condition
    [Documentation]   AP onboarding  and check is online
    ${result}=                      Login User          ${tenant_username}     ${tenant_password}

    ${IMPORT_MAP}=                  Import Map In Network360Plan  ${MAP_FILE_NAME}
    Should Be Equal As Strings      '${IMPORT_MAP}'              '1'

    ${ONBOARD_RESULT}=              onboard device quick      ${ap1}
    Should be equal as integers     ${ONBOARD_RESULT}       1

    ${AP_SPAWN}=        Open Spawn          ${ap1.console_ip}   ${ap1.console_port}      ${ap1.username}       ${ap1.password}        ${ap1.cli_type}
    Should not be equal as Strings      '${AP_SPAWN}'        '-1'

    ${CONF_STATUS_RESULT}=      Configure Device To Connect To Cloud      ${ap1.cli_type}         ${capwap_url}       ${AP_SPAWN}
    Should Be Equal As Strings                  ${CONF_STATUS_RESULT}       1

    ${WAIT_STATUS_RESULT}=      Wait for Configure Device to Connect to Cloud       ${ap1.cli_type}         ${capwap_url}       ${AP_SPAWN}
    Should Be Equal As Strings                  ${WAIT_STATUS_RESULT}       1

    ${CONNECTED_STATUS}=    Wait Until Device Online                ${ap1.serial}
    Should Be Equal as Integers             ${CONNECTED_STATUS}          1

    ${DEVICE_STATUS}=       Get Device Status       device_serial=${ap1.serial}
    Should contain any  ${DEVICE_STATUS}    green     config audit mismatch

    ${LATEST_VERSION}=      Upgrade Device           ${ap1}
    Should Not be Empty     ${LATEST_VERSION}

    Sleep                   ${ap_reboot_wait}

    ${REBOOT_STATUS}=    Wait Until Device Reboots               ${ap1.serial}
    Should Be Equal as Integers             ${REBOOT_STATUS}          1

    Close Spawn    ${AP_SPAWN}

Test Suite Clean Up
    [Documentation]    Delete Devices / cleanup scripts
    ${result}=    Login User        ${tenant_username}     ${tenant_password}

    Delete Device                   device_serial=${ap1.serial}

    Go to Extreme Location Asset Management Menu

    ${DELETE_XLOC_WIFI_ASSET}=     Delete Asset In XLOC      ${WIFI_ASSET_NAME}
    Should Be Equal As Strings      '${DELETE_XLOC_WIFI_ASSET}'        '1'

    Logout User
    Quit Browser

*** Test Cases ***

Test1: Validate XLOC Config in already subscribed account
    [Documentation]         Existing Customer - BrownField Scenario with subscription and XLOC Config validation
    [Tags]                  tccs_7297         development
    #${LOGIN_XIQ}=                   Login User          ${tenant_username}     ${tenant_password}

    ${AP1_UPDATE_CONFIG}=           Update Network Policy To AP   ${NW_POLICY_NAME}     ap_serial=${ap1.serial}   update_method=Complete
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'

    Wait Until Device Online       ${ap1.serial}

    ${SUBSCRIBE_LOCATION}=          Subscribe Extreme Location Essentials
    Should Be Equal As Strings      '${SUBSCRIBE_LOCATION}'   '1'

    Log to Console      Sleep for ${config_push_wait}
    sleep                         ${config_push_wait}

    ${AP_SPAWN}=                Open Spawn          ${ap1.ip}       ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.cli_type}
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

Test2: Validate Presence and Category TC in already subscribed account after connecting client
    [Documentation]         Existing Customer - BrownField Scenario with Presence and Category TC after connecting client
    [Tags]                  tccs_7298            development
    Depends On          Test1
    ${LOGIN_XIQ}=                  Login User          ${tenant_username}     ${tenant_password}

    ${CLIENT_MAC_FORMAT}=          Convert To Client MAC  ${mu5.wifi_mac}
    ${MU5_SPAWN}=                  Open Spawn                  ${mu5.ip}               ${mu5.port}             ${mu5.username}      ${mu5.password}      ${mu5.cli_type}
    Set Suite Variable             ${MU5_SPAWN}
    Connect MU5 To Open Network    ${SSID_NAME}

    Log to Console      Sleep for ${client_connect_wait}
    sleep                         ${client_connect_wait}

    ${CLIENT_STATUS}=                Get Client Status   client_mac=${mu5.wifi_mac}
    Should Be Equal As Strings       '${CLIENT_STATUS}'      '1'

    ${PING_TRAFFIC}=            Send               ${MU5_SPAWN}        nohup timeout 360 ping google.com -I ${mu5.interface} &

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

Test3: Create WiFi Asset in already subscribed account
    [Documentation]         Existing Customer - BrownField Scenario - Create WiFi Asset in already subscribed account
    [Tags]                  tccs_7265         development
    Depends On          Test2
    ${LOGIN_XIQ}=                  Login User          ${tenant_username}     ${tenant_password}

    Go to Extreme Location Asset Management Menu

    ${CREATE_XLOC_WIFI_ASSET}=     Create WIFI Asset In XLOC     ${WIFI_ASSET_NAME}   ${BUILDING_NAME}   ${AS_CATEGORY_NAME}    ${mu5.wifi_mac}
    Should Be Equal As Strings      '${CREATE_XLOC_WIFI_ASSET}'        '1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test4: Validate WiFi Asset by Searching hostname of Asset in Device Page
    [Documentation]         Existing Customer - BrownField Scenario - Validate WiFi Asset by Searching hostname of Asset in Device Page
    [Tags]                  tccs_11562         development
    Depends On          Test2    Test3
    ${LOGIN_XIQ}=                  Login User          ${tenant_username}     ${tenant_password}

    Go to Extreme Location Devices Wireless Devices Menu

    ${CLIENT_MAC_FORMAT}=          Convert To Client MAC    ${mu5.wifi_mac}

    ${CLIENT_INFO}=     Get Client Information In Extreme Location Devices Page    ${CLIENT_MAC_FORMAT}   ${BUILDING_NAME}

    ${CLIENT_MAC}=                 Get From Dictionary       ${CLIENT_INFO}    client_mac
    ${EXPECTED_CLIENT_MAC}=        Convert MAC To Lower  ${CLIENT_MAC_FORMAT}
    Should Be Equal As Strings    '${CLIENT_MAC}'          '${EXPECTED_CLIENT_MAC}'

    ${CLIENT_TYPE}=                 Get From Dictionary       ${CLIENT_INFO}    device_type
    Should Be Equal As Strings     '${CLIENT_TYPE}'          'Asset'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

#Commenting(Removing) this Test Case as it takes more time
#Test5: Switch off Client WiFi Interface, Delete Client and Validate Presence in Devices and Sites Page after DisConnecting Client
    #[Documentation]         Existing Customer - BrownField Scenario - Switch off Client, Delete Client and Validate Presence
    #[Tags]                  tccs_10859         development
    #Depends On          Test1
    #${LOGIN_XIQ}=                   Login User          ${tenant_username}     ${tenant_password}


    #${MU5_SPAWN}=                  Open Spawn           ${mu5.ip}     ${mu5.port}     ${mu5.username}    ${mu5.password}    ${mu5.cli_type}
    #Set Suite Variable             ${MU5_SPAWN}
    #MU Interface Down              ${MU5_SPAWN}    ${mu5.interface}

    #Log to Console      Sleep for ${client_connect_wait} secs After disconnecting Client
    #sleep                         ${client_connect_wait}

    #${CLIENT_STATUS}=                Get Client Status   client_mac=${mu5.wifi_mac}
    #Should Be Equal As Strings       '${CLIENT_STATUS}'      '-1'

    #Navigate To Manage Tab

    #Navigate To Clients Tab

    #${DELETE_CLIENT_RT}=               Delete Client RealTime       ${mu5.delete_mac}
    #Should Be Equal As Strings      '${DELETE_CLIENT_RT}'        '1'

    #${CLIENT_MAC_FORMAT}=           Convert To Client MAC    ${mu5.wifi_mac}

    #Go To Extreme Location Devices Wireless Devices Menu

    #${CLIENT_INFO}=                  Get Client Information In Extreme Location Devices Page  ${CLIENT_MAC_FORMAT}  ${BUILDING_NAME}
    #Should Be Equal As Strings      '${CLIENT_INFO}'              '-1'

    #Navigate To Extreme Location Sites Menu

    #${CLIENT_ENTRY_VALIDATION}=      Validate Client Entry In Extreme Location Sites Page  ${BUILDING_NAME}   ${FLOOR_NAME}   ${CLIENT_MAC_FORMAT}
    #Should Be Equal As Strings       '${CLIENT_ENTRY_VALIDATION}'   '-1'

    #[Teardown]   run keywords       Logout User
    #...                             Quit Browser

Test5: Check for testconnection button with https working URL and correct credentials
    [Documentation]         Existing Customer - BrownField Scenario - Check for testconnection button with https working URL and correct credentials
    [Tags]                  tccs_11557         development

    ${LOGIN_XIQ}=                   Login User          ${tenant_username}     ${tenant_password}

    Go to Extreme Location Settings Third Party Config Menu

    ${TEST_CONNECTION_THIRD_PARTY_CONFIG}=       Check XLOC Test Connection Button   ${SUBSCRIBER_PUSH_URL_HTTPS}   ${SUBSCRIBER_USERNAME}   ${SUBSCRIBER_PASSWORD}
    Should Be Equal As Strings        '${TEST_CONNECTION_THIRD_PARTY_CONFIG}'       '1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test6: Check for testconnection button with https non-working URL and correct credentials
    [Documentation]         Existing Customer - BrownField Scenario - Check for testconnection button with https non-working URL and correct credentials
    [Tags]                  tccs_11559           development

    ${LOGIN_XIQ}=                   Login User          ${tenant_username}     ${tenant_password}

    Go to Extreme Location Settings Third Party Config Menu

    ${TEST_CONNECTION_THIRD_PARTY_CONFIG}=       Check XLOC Test Connection Button   ${SUBSCRIBER_PUSH_URL_HTTPS_WRONG}   ${SUBSCRIBER_USERNAME}   ${SUBSCRIBER_PASSWORD}
    Should Be Equal As Strings        '${TEST_CONNECTION_THIRD_PARTY_CONFIG}'       '-1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser


