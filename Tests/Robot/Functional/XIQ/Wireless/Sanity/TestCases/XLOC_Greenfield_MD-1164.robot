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

*** Test Cases ***

TC-10862: Onboard AP on New customer Account
    [Documentation]         New Customer - GreenField Scenario with onboarding and assigning location to AP
    [Tags]                  production  sanity  onboard  greenfield   TC-10862

    ${LOGIN_XIQ}=               Login User          ${tenant_username}     ${tenant_password}

    ${IMPORT_MAP}=                Import Map In Network360Plan  ${MAP_FILE_NAME}
    Should Be Equal As Strings    ${IMPORT_MAP}       1

    #Onboard AP                  ${ap1.serial}       aerohive
    ${ONBOARD_RESULT}=      onboard device quick     ${ap1}
    Should be equal as integers                 ${ONBOARD_RESULT}       1

    ${AP_SPAWN}=                Open Spawn          ${ap1.ip}       ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.cli_type}
    Set Suite Variable          ${AP_SPAWN}
    ${OUTPUT0}=                 Send Commands       ${AP_SPAWN}         capwap client server name ${capwap_url}, capwap client default-server-name ${capwap_url}, capwap client server backup name ${capwap_url}, no capwap client enable, capwap client enable, save config

    Wait Until Device Online    ${ap1.serial}

    Refresh Devices Page

    ${AP1_STATUS}=               Get AP Status       ap_mac=${ap1.mac}
    Should Be Equal As Strings  '${AP1_STATUS}'     'green'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TC-7281: Check for Subscription and Validate XLOC Config for New Customer
    [Documentation]         New Customer - GreenField Scenario with subscription and XLOC Config validation
    [Tags]                  production  sanity  subscription  config  greenfield   TC-7281
    Depends On          TC-10862
    ${LOGIN_XIQ}=                   Login User          ${tenant_username}     ${tenant_password}

    ${CREATE_POLICY1}=              Create Network Policy   ${NW_POLICY_NAME}      ${LOCATION_OPEN_NW}
    Should Be Equal As Strings      '${CREATE_POLICY1}'   '1'

    ${CREATE_AP_TEMPLATE}=          Add AP Template     ${ap1.model}    ${AP_TEMPLATE_CONFIG}
    Should Be Equal As Strings      '${CREATE_AP_TEMPLATE}'   '1'

    Enable Nw Presence Analytics    ${NW_POLICY_NAME}

    ${AP1_UPDATE_CONFIG}=           Update Network Policy To AP   ${NW_POLICY_NAME}     ap_serial=${ap1.serial}   update_method=Complete
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'

    ${SUBSCRIBE_LOCATION}=          Subscribe Extreme Location Essentials
    Should Be Equal As Strings      '${SUBSCRIBE_LOCATION}'   '1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TC-10847: Validate Presence TC after connecting client in new customer account
    [Documentation]         New Customer - GreenField Scenario with presence validation after connecting client
    [Tags]                  production  sanity  presence  greenfield   TC-10847
    Depends On          TC-7281
    ${LOGIN_XIQ}=                  Login User          ${tenant_username}     ${tenant_password}
    ${CLIENT_MAC_FORMAT}=          Convert To Client MAC  ${mu5.wifi_mac}
    ${MU5_SPAWN}=                  Open Spawn                  ${mu5.ip}               ${mu5.port}             ${mu5.username}      ${mu5.password}      ${mu5.cli_type}
    Set Suite Variable             ${MU5_SPAWN}
    Connect MU5 To Open Network    ${SSID_NAME}

    Log to Console      Sleep for ${client_connect_wait}
    sleep                         ${client_connect_wait}

    ${CLIENT_STATUS}=                Get Client Status   client_mac=${mu5.wifi_mac}
    Should Be Equal As Strings       '${CLIENT_STATUS}'      '1'

    ${PING_TRAFFIC}=            Send               ${MU5_SPAWN}        nohup timeout 360 ping google.com -I wlo1 &

    Go To Extreme Location Devices Wireless Devices Menu

    ${CLIENT_INFO}=                Get Client Information In Extreme Location Devices Page   ${CLIENT_MAC_FORMAT}   ${BUILDING_NAME}

    ${CLIENT_MAC}=                 Get From Dictionary       ${CLIENT_INFO}    client_mac
    ${EXPECTED_CLIENT_MAC}=        Convert MAC To Lower  ${CLIENT_MAC_FORMAT}
    Should Be Equal As Strings    '${CLIENT_MAC}'          '${EXPECTED_CLIENT_MAC}'

    ${CLIENT_TYPE}=                 Get From Dictionary       ${CLIENT_INFO}    device_type
    Should Be Equal As Strings     '${CLIENT_TYPE}'          'Visitor'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TC-10865 Step1: Perform BackUp VIQ
    [Documentation]         New Customer - GreenField Scenario with BackUp Customer Account Data
    [Tags]                  production  sanity  backup  greenfield   TC-10865

    ${LOGIN_XIQ}=                   Login User          ${tenant_username}     ${tenant_password}
    ${BACKUP_VIQ_DATA}=             Backup VIQ Data
    Should Be Equal As Strings      '${BACKUP_VIQ_DATA}'              '1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TC-10865 Step2: Perform Reset VIQ
    [Documentation]         New Customer - GreenField Scenario with Reset Customer Account Data
    [Tags]                  production  sanity  reset  greenfield

    Sleep    2 minutes
    ${LOGIN_XIQ}=                   Login User          ${tenant_username}     ${tenant_password}
    ${RESET_VIQ_DATA}=               Reset VIQ Data
    Should Be Equal As Strings      '${RESET_VIQ_DATA}'              '1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

