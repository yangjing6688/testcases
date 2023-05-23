# Author        : Kunal Babbar
# Edited        : October 25,2021
# Modified      : Jay Moorkoth 
# Dated         : October 17, 2022
# Description   : BLE-Config and Monitoring (MD-789) -> Enabling/Disabling the iBeacon Service in Additional Settings with/without monitoring.
# Precondition  : AP should be onboarded and appear online with a network policy and a ssid.
#****************************************************************************************************************************************************************
# Execution Commands: The testcases in this script can either run independently or together depending on the tags passed.
# robot -L INFO -i p2 BLE-ConfigMonitoring_XIQ-000.robot
# robot -L INFO -i tccs-7306 BLE-ConfigMonitoring_XIQ-000.robot
# robot -L INFO -i TC-7386 BLE-ConfigMonitoring_XIQ-000.robot
# robot -L INFO -i TC-10800 BLE-ConfigMonitoring_XIQ-000.robot

# Select the "TOPO" and "DEVICE" variable based on Test bed to run the following execution
# robot -L INFO -v DEVICE:AP250 -v TOPO:g2r1  BLE-ConfigMonitoring_XIQ-000.robot
########################################################################################################################
*** Variables ***
${DEVICE}
${TOPO}
${EXIT_LEVEL}                  test_suite
${RECORD}                      True
${NTP_STATE_COLUMN}            NTP STATE
${SERVICE_NAME}                Test_Service
${UUID}                        4165726F-6869-7665-4E65-74776F726B73 
${AP_NETWORK_POLICY}           Test_Policy_BLE
${SSID_NAME}                   test2021
${LOCATION}                    Floor 1

*** Settings ***
Library     Collections
Library     common/Cli.py
Library     common/Utils.py
Library     common/TestFlow.py
# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     xiq/flows/manage/Client.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Location.py
Library     xiq/flows/manage/DeviceCliAccess.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/ExpressNetworkPolicies.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/elements/NetworkPolicyWebElements.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Force Tags   testbed_1_node
Suite Setup      Onboard AP      ${AP_NETWORK_POLICY}
Suite Teardown  Clean-up

*** Keywords ***

Clean-up
    [Documentation]         Cleanup script
    [Tags]                  cleanup    development
    ${LOGIN_STATUS}=                Login User              ${tenant_username}     ${tenant_password}
    should be equal as integers     ${LOGIN_STATUS}               1
    ${DELETE_DEVICE_STATUS}=            Delete device                  device_serial=${ap1.serial}
    should be equal as integers     ${DELETE_DEVICE_STATUS}               1
    Delete Network Policy     ${AP_NETWORK_POLICY}
    Delete SSID               ${SSID_NAME}
    [Teardown]   run keywords        Logout User
    ...                              quit browser

Onboard AP
    [Documentation]     Precondition: AP Should be onboarded and it is online
    [Arguments]         ${AP_NETWORK_POLICY}
    ${RESULT}=              Login User         ${tenant_username}     ${tenant_password}
    Should Be Equal As Strings             ${RESULT}       1
    ${SSID_NAME}=            Get Random String
    Set Global Variable         ${SSID_NAME}
    ${AP_NETWORK_POLICY_STATUS}=             Create Open Auth Express Network Policy    ${AP_NETWORK_POLICY}   ${SSID_NAME}
    Should Be Equal As Strings             ${AP_NETWORK_POLICY_STATUS}       1
    Logout User
    Quit Browser

*** Test Cases ***
TCCS-7306: HM-Bluetooth_Configuration_enable
    [Documentation]    Enable iBeacon Service without monitoring
    [Tags]             tccs-7306    development
    [Setup]            Login User      ${tenant_username}     ${tenant_password}
    ${result1}=     Enable IBeacon Service In Network Policy   ${AP_NETWORK_POLICY}    ${SERVICE_NAME}     ${UUID}      monitoring=disable
    ${DELTA_UPDATE}=                Update Network Policy To Ap    policy_name=${AP_NETWORK_POLICY}    ap_serial=${ap1.serial}
    should be equal as strings     '${DELTA_UPDATE}'           '1'
    Sleep   1min
    Wait Until Device Online    ${ap1.serial}
    ${AP1_STATUS}=           get device status       device_mac=${ap1.mac}
    Should Be Equal As Strings             '${AP1_STATUS}'       'green'
    ${SPAWN1}=              Open Spawn         ${ap1.ip}   ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.cli_type}
    ${OUTPUT2}=            Send Commands       ${SPAWN1}         sh int ble0 ibeacon
    Should Contain                          ${OUTPUT2}     ble0 status:enable   ${UUID}  Monitor mode : disable
    Close Spawn                                ${SPAWN1}
    Should Be Equal As Integers             ${result1}   1
    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TCCS-7386: HM-Bluetooth_Monitoring_enable
    [Documentation]    Enable iBeacon Service with monitoring enabled
    [Tags]             tccs-7386     development
    [Setup]            Login User      ${tenant_username}     ${tenant_password}
    ${result1}=     Enable IBeacon Service In Network Policy   ${AP_NETWORK_POLICY}    ${SERVICE_NAME}     ${UUID}      monitoring=enable
    ${DELTA_UPDATE}=                Update Network Policy To Ap    policy_name=${AP_NETWORK_POLICY}    ap_serial=${ap1.serial}
    should be equal as strings     '${DELTA_UPDATE}'           '1'
    Wait Until Device Online    ${ap1.serial}
    Sleep   1min
    Wait Until Device Online    ${ap1.serial}
    ${AP1_STATUS}=           get device status       device_mac=${ap1.mac}
    Should Be Equal As Strings             '${AP1_STATUS}'       'green'
    ${SPAWN1}=              Open Spawn         ${ap1.ip}   ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.cli_type}
    ${OUTPUT1}=            Send Commands       ${SPAWN1}         sh int ble0 ibeacon
    Should Contain                         ${OUTPUT1}    ble0 status:enable   ${UUID}  Monitor mode : enable
    Close Spawn                                ${SPAWN1}
    Should Be Equal As Integers             ${result1}   1
    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TCCS-10800: HM-Bluetooth_disable_iBeacon_Service
    [Documentation]    Disable the iBeacon Service if its already enabled
    [Tags]             tccs-10800    development
    [Setup]            Login User      ${tenant_username}     ${tenant_password}
    ${result1}=        Disable IBeacon Service In Network Policy  ${AP_NETWORK_POLICY}
    ${DELTA_UPDATE}=                Update Network Policy To Ap    policy_name=${AP_NETWORK_POLICY}    ap_serial=${ap1.serial}
    should be equal as strings     '${DELTA_UPDATE}'           '1'
    Sleep   1min
    Wait Until Device Online    ${ap1.serial}
    ${SPAWN2}=              Open Spawn         ${ap1.ip}   ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.cli_type}
    ${OUTPUT2}=            Send Commands       ${SPAWN2}         sh int ble0 ibeacon
    Should Not Contain Any                     ${OUTPUT2}     enable    ${UUID}
    Close Spawn                                ${SPAWN2}
    Should Be Equal As Integers             ${result1}   1
    [Teardown]   run keywords       Logout User
    ...                             Quit Browser
