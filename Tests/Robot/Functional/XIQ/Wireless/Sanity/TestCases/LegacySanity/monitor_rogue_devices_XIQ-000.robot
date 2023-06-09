# Author        : Ramkumar
# Date          : June10,2020
# Description   :Monitor Security Rogue APs and Clients
#
# Topology      :
# AP1(Sensor)----- Cloud------AP2---Client

# Pre-Condtion
# 1. AP1 and AP2 should be onboarded and it should be in online
# 2.Should Use Windows10 as Wireless client

# Execution Command:
# ------------------
# robot -v DEVICE1:AP630 -v DEVICE2:Ap410C -v TOPO:g7r2 monitor_rogue_devices.robot

*** Variables ***
${WIPS_POLICY_NAME}         test_automation_wips
${NW_POLICY_NAME}           automation_wips_ssid_based
${SSID_NAME}                test_automation_wips
${WIPS_POLICY_NAME3}        automation_wips_ssid_based
${NW_POLICY_ROGUE}          automation_wips_rogue_ssid
${SSID_NAME_ROGUE}          test_automation_rogue
${ROGUE_VENDOR_NAME}        Extreme Networks
${ROGUE_REASON_NAME}        SSID
${ROGUE_CLASSIFICATION}     Unauthorized Rogue
${CLIENT_COUNT}             0
${LOCATION}                 auto_location_01, Santa Clara, building_02, floor_04

*** Settings ***
Library     Collections
Library     common/Utils.py
Library     common/Cli.py
Library     common/TestFlow.py

# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py

Library     xiq/flows/manage/Client.py
Library     xiq/flows/manage/Devices.py

Library     xiq/flows/configure/Wips.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/configure/DeviceTemplate.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Resource     Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/monitor_rogue_devices_config.robot

Force Tags  testbed_1_node

Library	        Remote 	http://${mu1.ip}:${mu1.port}   WITH NAME   Remote_Server
Suite Setup      Pre Condition

*** Keywords ***
Pre Condition
    [Documentation]   AP Should be onboarded  and it is online
    ${result}=          Login User          ${tenant_username}     ${tenant_password}
    ${AP1_STATUS}=       get device status       device_mac=${ap1.mac}
    Should Be Equal As Strings  '${AP1_STATUS}'     'green'

    create network policy           default_network_policy     ${OPEN_NW_01}
    Update Network Policy To AP     default_network_policy      ap_serial=${ap1.serial}
    Update Network Policy To AP     default_network_policy      ap_serial=${ap2.serial}
    Delete Network Polices          ${NW_POLICY_NAME}  ${NW_POLICY_ROGUE}
    Delete SSIDs                    ${SSID_NAME}   ${SSID_NAME_ROGUE}
    Delete Wips Policy Profile      ${WIPS_POLICY_NAME}
    Delete AP Template Profile      ${ap1.model}
    Logout User
    Quit Browser

*** Test Cases ***
Test0: Pre-config
    [Documentation]         Pre-config
    [Tags]                  sanity  add   rougueap  wips_ssid   aerohive  p3  p4   regression   tcxi_49871
    ${result}=           Login User          ${tenant_username}     ${tenant_password}

    onboard device quick       ${ap2}
    ${AP_SPAWN}=         Open Spawn        ${ap2.ip}   ${ap2.port}      ${ap2.username}       ${ap2.password}        ${ap2.cli_type}
    Set Suite Variable   ${AP_SPAWN}

    ${OUTPUT0}=         Send Commands       ${AP_SPAWN}         capwap client server name ${capwap_url}, capwap client default-server-name ${capwap_url}, capwap client server backup name ${capwap_url}, no capwap client enable, capwap client enable, save config
    Wait Until Device Online                ${ap2.serial}
    Refresh Devices Page
    ${AP2_STATUS}=       get device status       device_mac=${ap2.mac}
    Should Be Equal As Strings  '${AP2_STATUS}'     'green'

    [Teardown]         run keywords    logout user
     ...                               quit browser

Test1: TC-49871 - Configure WIPS Policy on AP
    [Documentation]         Configure WIPS Policies
    [Tags]                  sanity  add   rougueap  wips_ssid   aerohive  p3  p4  production  regression    tcxi_49871
    ${LOGIN_XIQ}=              Login User          ${tenant_username}      ${tenant_password}   capture_version=True
    ${CREATE_POLICY1}=         Create Network Policy   ${NW_POLICY_NAME}      ${WIPS_OPEN_NW}
    Should Be Equal As Strings   '${CREATE_POLICY1}'   '1'
    ${CREATE_AP_TEMPLATE}=     Add AP Template     ${ap1.model}     ${ap1.template_name}    ${AP_TEMPLATE_CONFIG}
    Should Be Equal As Strings   '${CREATE_AP_TEMPLATE}'   '1'
    ${CONFIG_WIPS_POLICY}      Configure WIPS Policy On Common Objects   &{WIPS_CONFIG_SETTINGS}
    Should Be Equal As Strings   '${CONFIG_WIPS_POLICY}'   '1'
    ${NP_REUSE_WIPS}           Configure Reuse Wips Policy On Network Policy  ${NW_POLICY_NAME}  ${WIPS_POLICY_NAME}
    Should Be Equal As Strings   '${NP_REUSE_WIPS}'   '1'
    ${AP1_UPDATE_CONFIG}=      Update Network Policy To AP   ${NW_POLICY_NAME}     ap_serial=${ap1.serial}
    Should Be Equal As Strings              '${AP1_UPDATE_CONFIG}'       '1'
    Log to Console      Sleep for ${config_push_wait}
    sleep                         ${config_push_wait}

    ${AP_SPAWN}=        Open Spawn          ${ap1.ip}   ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.cli_type}
    ${SENSOR_WIFI_CONFIG}=     Send                ${AP_SPAWN}         show running-config | include "interface wifi"
    Should Contain      ${SENSOR_WIFI_CONFIG}      interface wifi0 mode sensor
    Should Contain      ${SENSOR_WIFI_CONFIG}      interface wifi1 mode sensor
    Should Contain      ${SENSOR_WIFI_CONFIG}      interface wifi0 wlan-idp profile ${SSID_NAME}
    Should Contain      ${SENSOR_WIFI_CONFIG}      interface wifi1 wlan-idp profile ${SSID_NAME}

    ${WIPS_CONFIG}=     Send                ${AP_SPAWN}         show running-config | include "security wlan-idp"
    Should Contain      ${WIPS_CONFIG}      security wlan-idp profile ${SSID_NAME}
    Should Contain      ${WIPS_CONFIG}      security wlan-idp profile ${SSID_NAME} ap-policy
    Should Contain      ${WIPS_CONFIG}      security wlan-idp profile ${SSID_NAME} ap-policy ssid
    Should Contain      ${WIPS_CONFIG}      security wlan-idp profile ${SSID_NAME} ap-policy ssid entry ${SSID_NAME}
    Should Contain      ${WIPS_CONFIG}      security wlan-idp profile ${SSID_NAME} ap-policy ssid entry ${SSID_NAME} encryption
    Should Contain      ${WIPS_CONFIG}      security wlan-idp profile ${SSID_NAME} ap-detection connected
    Should Contain      ${WIPS_CONFIG}      security wlan-idp profile ${SSID_NAME} ap-detection client-mac-in-net
    Should Contain      ${WIPS_CONFIG}      security wlan-idp profile ${SSID_NAME} sta-report
    CLOSE SPAWN         ${AP_SPAWN}

    [Teardown]         run keywords    logout user
     ...                               quit browser

Test2: Make a WiFi connection with WIPS policy Configured Non-Permiited SSID
    [Documentation]         Make a WiFi connection with WIPS policy Configured Non-Permiited SSID
    [Tags]                  sanity    wireless    rougueap  wips_ssid   aerohive p3  p4   regression    tcxi_49871

    Depends On          Test1
    ${LOGIN_XIQ}=              Login User          ${tenant_username}      ${tenant_password}
    ${CREATE_POLICY2}=          Create Network Policy   ${NW_POLICY_ROGUE}     ${WIPS_OPEN_ROGUE_NW}
    Should Be Equal As Strings   '${CREATE_POLICY2}'   '1'
    ${AP2_UPDATE_CONFIG}=       Update Network Policy To AP   ${NW_POLICY_ROGUE}     ap_serial=${ap2.serial}
    Should Be Equal As Strings              '${AP2_UPDATE_CONFIG}'       '1'
    Log to Console      Sleep for ${config_push_wait}
    sleep                         ${config_push_wait}
    Remote_Server.Connect Open Network    test_automation_rogue
    Log to Console      Sleep for ${client_connect_wait}
    sleep                         ${client_connect_wait}

    ${CLIENT_STATUS}=   Get Client Status   client_mac=${MU1_WIFI_MAC}
    Should Be Equal As Strings              '${CLIENT_STATUS}'      '1'

    [Teardown]         run keywords    logout user
     ...                               quit browser

Test3: Verify the Rogue AP Logs with Non-Permitted SSID
    [Documentation]         Verify the Rogue AP
    ...                     https://jira.aerohive.com/browse/APC-38301
    [Tags]                  sanity  rougueap  wips_ssid   aerohive  p3  p4   regression     tcxi_49871

    Depends On          Test1
    ${LOGIN_XIQ}=              Login User          ${tenant_username}      ${tenant_password}
    ${ROGUE_LOGS}=              Verify Rogue AP    ${ap1.name}
    # Logs Verification
    ${CLASSIFICATION}=     Get From Dictionary     ${ROGUE_LOGS}    status
    ${CLIENTS}=            Get From Dictionary     ${ROGUE_LOGS}    clientCount
    ${ROGUE_AP_BSSID}=     Get From Dictionary     ${ROGUE_LOGS}    idpBssid
    ${SSID}=               Get From Dictionary     ${ROGUE_LOGS}    ssid
    ${VENDOR}=             Get From Dictionary     ${ROGUE_LOGS}    vendor
    ${LOCATION_NAME}=      Get From Dictionary     ${ROGUE_LOGS}    vendor
    ${REPORTING_DEVICE}=   Get From Dictionary     ${ROGUE_LOGS}    deviceName
    ${REASON}=             Get From Dictionary     ${ROGUE_LOGS}    compliance
    ${FIRST_TIME_SEEN}=    Get From Dictionary     ${ROGUE_LOGS}    startTime
    ${LAST_TIME_SEEN}=     Get From Dictionary     ${ROGUE_LOGS}    endTime
    ${MITIGATION}=         Get From Dictionary     ${ROGUE_LOGS}    mitigationFlag

    Should Be Equal As Strings    '${CLASSIFICATION}'     ' ${ROGUE_CLASSIFICATION}'
    Should Be Equal As Strings    '${CLIENTS}'            '${CLIENT_COUNT}'
    Should Be Equal As Strings    '${ROGUE_AP_BSSID}'     '${ap2.bssid}'
    Should Be Equal As Strings    '${SSID}'               '${SSID_NAME_ROGUE}'
    Should Be Equal As Strings    '${VENDOR}'             '${ROGUE_VENDOR_NAME}'
    Should Be Equal As Strings    '${REPORTING_DEVICE}'   '${ap1.name}'
    Should Be Equal As Strings    '${REASON}'             '${ROGUE_REASON_NAME}'

    [Teardown]         run keywords    logout user
     ...                               quit browser

Test4: Make a WiFi connection with WIPS policy Configured Permitted SSID
    [Documentation]         Make a WiFi connection with WIPS policy Configured Permitted SSID
    [Tags]                  sanity    wireless    rougueap  wips_ssid   aerohive p3  p4   regression    tcxi_49871

    Depends On          Test1
    ${LOGIN_XIQ}=              Login User          ${tenant_username}      ${tenant_password}
    ${CREATE_POLICY1}=         Create Network Policy   ${NW_POLICY_NAME}      ${WIPS_OPEN_NW}
    Should Be Equal As Strings   '${CREATE_POLICY1}'   '1'
    ${AP2_UPDATE_CONFIG}=       Update Network Policy To AP   ${NW_POLICY_NAME}      ap_serial=${ap2.serial}
    Should Be Equal As Strings              '${AP2_UPDATE_CONFIG}'       '1'
    Log to Console      Sleep for ${config_push_wait}
    sleep                         ${config_push_wait}
    Remote_Server.Connect Open Network    test_automation_wips
    Log to Console      Sleep for ${client_connect_wait}
    sleep                         ${client_connect_wait}

    ${CLIENT_STATUS}=   Get Client Status   client_mac=${MU1_WIFI_MAC}
    Should Be Equal As Strings              '${CLIENT_STATUS}'      '1'

    [Teardown]         run keywords    logout user
     ...                               quit browser

Test5: Verify the Rogue AP Logs with Permitted SSID
    [Documentation]         Verify the Rogue AP
    [Tags]                  sanity  rougueap  wips_ssid   aerohive p3  p4    regression     tcxi_49871

    Depends On          Test4
    ${LOGIN_XIQ}=              Login User          ${tenant_username}      ${tenant_password}
    ${ROGUE_LOGS}=              Verify Rogue AP    test_automation_wips
    # Logs Verification
    Should Be Equal As Strings        '${ROGUE_LOGS}'     '-1'

    [Teardown]         run keywords    logout user
     ...                               quit browser

Test6: Verify the Rogue Client
    [Documentation]         Verify the Rogue Client
    ...                     https://jira.aerohive.com/browse/APC-38301
    [Tags]                  sanity  rougueclient  wips_ssid   aerohive  not-ready  p3  p4   regression      tcxi_49871

    Depends On          Test1
    ${LOGIN_XIQ}=              Login User          ${tenant_username}      ${tenant_password}
    ${ROGUE_LOGS}=              Verify Rogue Client    ${ap1.name}
    # Logs Verification
    ${CLASSIFICATION}=     Get From Dictionary     ${ROGUE_LOGS}    status
    ${CLIENTS}=            Get From Dictionary     ${ROGUE_LOGS}    clientCount
    ${ROGUE_AP_BSSID}=     Get From Dictionary     ${ROGUE_LOGS}    idpBssid
    ${SSID}=               Get From Dictionary     ${ROGUE_LOGS}    ssid
    ${VENDOR}=             Get From Dictionary     ${ROGUE_LOGS}    vendor
    ${LOCATION_NAME}=      Get From Dictionary     ${ROGUE_LOGS}    vendor
    ${REPORTING_DEVICE}=   Get From Dictionary     ${ROGUE_LOGS}    deviceName
    ${REASON}=             Get From Dictionary     ${ROGUE_LOGS}    compliance
    ${FIRST_TIME_SEEN}=    Get From Dictionary     ${ROGUE_LOGS}    startTime
    ${LAST_TIME_SEEN}=     Get From Dictionary     ${ROGUE_LOGS}    endTime
    ${MITIGATION}=         Get From Dictionary     ${ROGUE_LOGS}    mitigationFlag

    [Teardown]         run keywords    logout user
     ...                               quit browser

Test7: Delete Wips Policy
    [Documentation]         Verify Delete Wips Policy
    [Tags]                  sanity   rougueap  wips_ssid  delete  aerohive  p3  p4   regression  production     tcxi_49871

    Depends On          Test1
    ${LOGIN_XIQ}=              Login User          ${tenant_username}      ${tenant_password}
    ${DELETE_WIPS}=            Disable Wips On Network Policy   ${NW_POLICY_NAME}
    Should Be Equal As Strings     '${DELETE_WIPS}'      '1'
    ${AP1_UPDATE_CONFIG}=      Update Network Policy To AP   ${NW_POLICY_NAME}     ap_serial=${ap1.serial}
    Should Be Equal As Strings              '${AP1_UPDATE_CONFIG}'       '1'

    ${AP_SPAWN}=        Open Spawn          ${ap1.ip}   ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.cli_type}
    ${WIPS_CONFIG}=     Send                ${AP_SPAWN}         show running-config | include "security wlan-idp"
    Should Not Contain      ${WIPS_CONFIG}      security wlan-idp profile ${SSID_NAME}
    Should Not Contain      ${WIPS_CONFIG}      security wlan-idp profile ${SSID_NAME} ap-policy
    Should Not Contain      ${WIPS_CONFIG}      security wlan-idp profile ${SSID_NAME} ap-policy ssid
    Should Not Contain      ${WIPS_CONFIG}      security wlan-idp profile ${SSID_NAME} ap-policy ssid entry ${SSID_NAME}
    Should Not Contain      ${WIPS_CONFIG}      security wlan-idp profile ${SSID_NAME} ap-policy ssid entry ${SSID_NAME} encryption
    Should Not Contain      ${WIPS_CONFIG}      security wlan-idp profile ${SSID_NAME} ap-detection connected
    Should Not Contain      ${WIPS_CONFIG}      security wlan-idp profile ${SSID_NAME} ap-detection client-mac-in-net
    Should Not Contain      ${WIPS_CONFIG}      security wlan-idp profile ${SSID_NAME} sta-report
    CLOSE SPAWN         ${AP_SPAWN}

    [Teardown]         run keywords    logout user
     ...                               quit browser
