# Author        : Kiran
# Date          : Aug17,2021
# Description   : Extreme Location GreenField testacses
#
# Topology      :
# AP1----- Cloud-----Ubuntu(MU1)

# Execution Command:
# ------------------
#  robot -L INFO -v TEST_URL:https://g2.qa.xcloudiq.com/login -v TESTBED:blr_tb_2 -v DEVICE1:AP460C_RF_BOX_001 -v TOPO:XLOC_topo XLOC_Greenfield_MD-1164.robot

*** Variables ***
${LOCATION}                 auto_location_01, San Jose, building_01, floor_02
${NW_POLICY_NAME}           automation_xloc_gf_policy
${SSID_NAME}                automation_xloc_gf_ssid
${BUILDING_NAME}            building_01
${FLOOR_NAME}               floor_02
${MAP_FILE_NAME}            auto_location_01_1595321828282.tar.gz
${service_name}             greenfield_ibeacon
${uuid}                     123e4567e89b12d3a456426655440000

${XLOC_SITE_NAME}                building_01
${AS_CATEGORY_NAME}              automation_xloc_assetcat
${IBEACON_NAME_WORK}             automation_xloc_ibeacon
${UUID_WORK}                     4165726f-6869-7665-4e65-74776f726b73
${BEACON_MAC_ADDRESS_WORK}       bcf31065144f

*** Settings ***

Force Tags   testbed_3_node

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
Suite Teardown   Test Suite Clean Up

*** Keywords ***
Pre Condition
    [Documentation]   AP onboarding  and check is online
    ${result}=                      Login User          ${tenant1_username}     ${tenant_password}

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

    ${LATEST_VERSION}=      Upgrade Device To Latest Version            ${ap1.serial}
    Should Not be Empty     ${LATEST_VERSION}
    
    Sleep                   ${ap_reboot_wait}

    ${REBOOT_STATUS}=    Wait Until Device Reboots               ${ap1.serial}
    Should Be Equal as Integers             ${REBOOT_STATUS}          1

    Close Spawn    ${AP_SPAWN}

Test Suite Clean Up
    [Documentation]    Check XLOC Subscription after resetviq
    Sleep    2 minutes
    ${result}=    Login User        ${tenant1_username}     ${tenant_password}

    ${XLOC_SUBSCRIPTION_STATUS}=           Check Subscription of Extreme Location Page
    Should Be Equal As Strings      '${XLOC_SUBSCRIPTION_STATUS}'              '1'

    Logout User
    Quit Browser

*** Test Cases ***

Test1: Check for Subscription and Validate XLOC Config for New Customer
    [Documentation]         New Customer - GreenField Scenario with subscription and XLOC Config validation
    [Tags]                  tccs_7281            development

    ${CREATE_POLICY1}=              Create Network Policy   ${NW_POLICY_NAME}      &{LOCATION_OPEN_NW}
    Should Be Equal As Strings      '${CREATE_POLICY1}'   '1'

    ${CREATE_AP_TEMPLATE}=          Add AP Template     ${ap1.model}    ${ap1.template_name}    &{AP_TEMPLATE_CONFIG}
    Should Be Equal As Strings      '${CREATE_AP_TEMPLATE}'   '1'

    ${ENABLE_PRESENCE}=          Enable Nw Presence Analytics    ${NW_POLICY_NAME}
    Should Be Equal As Strings      '${ENABLE_PRESENCE}'    '1'

    ${AP1_UPDATE_CONFIG}=           Update Network Policy To AP   ${NW_POLICY_NAME}     ap_serial=${ap1.serial}   update_method=Complete
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'

    ${SUBSCRIBE_LOCATION}=          Subscribe Extreme Location Essentials
    Should Be Equal As Strings      '${SUBSCRIBE_LOCATION}'   '1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test2: Validate Presence TC after connecting client in new customer account
    [Documentation]         New Customer - GreenField Scenario with presence validation after connecting client
    [Tags]                  tccs_10847             development
    Depends On          Test1
    ${LOGIN_XIQ}=                  Login User          ${tenant1_username}     ${tenant_password}
    ${CLIENT_MAC_FORMAT}=          Convert To Client MAC  ${mu5.wifi_mac}
    ${MU5_SPAWN}=                  Open Spawn                  ${mu5.ip}               ${mu5.port}             ${mu5.username}      ${mu5.password}      ${mu5.cli_type}
    Should not be equal as Strings      '${MU5_SPAWN}'        '-1'

    ${CONNECT_MU5_OPEN}=           Connect MU5 To Open Network    ${SSID_NAME}
    Should not be equal as Strings      '${CONNECT_MU5_OPEN}'        '-1'

    Log to Console      Sleep for ${client_connect_wait}
    sleep                         ${client_connect_wait}

    ${CLIENT_STATUS}=                Get Client Status   client_mac=${mu5.wifi_mac}
    Should Be Equal As Strings       '${CLIENT_STATUS}'      '1'

    ${PING_TRAFFIC}=            Send               ${MU5_SPAWN}        nohup timeout 360 ping google.com -I ${mu5.interface} &

    ${GO_TO_XLOC_DEVICES}=    Go To Extreme Location Devices Wireless Devices Menu
    Should Be Equal As Strings       '${GO_TO_XLOC_DEVICES}'      '1'

    ${CLIENT_INFO}=                Get Client Information In Extreme Location Devices Page   ${CLIENT_MAC_FORMAT}   ${BUILDING_NAME}

    ${CLIENT_MAC}=                 Get From Dictionary       ${CLIENT_INFO}    client_mac
    ${EXPECTED_CLIENT_MAC}=        Convert MAC To Lower  ${CLIENT_MAC_FORMAT}
    Should Be Equal As Strings    '${CLIENT_MAC}'          '${EXPECTED_CLIENT_MAC}'

    ${CLIENT_TYPE}=                 Get From Dictionary       ${CLIENT_INFO}    device_type
    Should Be Equal As Strings     '${CLIENT_TYPE}'          'Visitor'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test3: Validate BLE Asset
    [Documentation]         New Customer - GreenField Scenario BLE Asset validation
    [Tags]                  tccs_10847             development
    Depends On          Test1
    ${LOGIN_XIQ}=                  Login User          ${tenant1_username}     ${tenant_password}

    ${CREATE_ASSEST_XLOC}=          Create Asset Category XLOC    ${AS_CATEGORY_NAME}     ${XLOC_SITE_NAME}
    Should Be Equal As Strings      '${CREATE_ASSEST_XLOC}'   '1'

    ${CREATE_BECON}=           Create XLOC Third Party Ibeacon   ${IBEACON_NAME_WORK}    ${UUID_WORK}   ${XLOC_SITE_NAME}   ${AS_CATEGORY_NAME}   ${BEACON_MAC_ADDRESS_WORK}    major_version=1    minor_version=1

    Sleep    30s

    ${DEVICE_STATUS}=           Get ibeacon Status       ${BEACON_MAC_ADDRESS_WORK}
    Should Be Equal As Strings      '${DEVICE_STATUS}'       '1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test4: Perform BackUp VIQ
    [Documentation]         New Customer - GreenField Scenario with BackUp Customer Account Data
    [Tags]                  tccs_10865             development

    ${LOGIN_XIQ}=                   Login User          ${tenant1_username}     ${tenant_password}
    ${BACKUP_VIQ_DATA}=             Backup VIQ Data
    Should Be Equal As Strings      '${BACKUP_VIQ_DATA}'              '1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test5: Perform Reset VIQ
    [Documentation]         New Customer - GreenField Scenario with Reset Customer Account Data
    [Tags]                  tccs_10865             development

    Sleep    2 minutes
    ${LOGIN_XIQ}=                   Login User          ${tenant1_username}     ${tenant_password}
    ${RESET_VIQ_DATA}=               Reset VIQ Data
    Should Be Equal As Strings      '${RESET_VIQ_DATA}'              '1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser
