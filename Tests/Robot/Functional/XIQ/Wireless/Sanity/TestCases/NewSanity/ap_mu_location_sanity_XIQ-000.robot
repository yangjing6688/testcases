# Author        : Rameswar
# Description   : Verifies the "Assign Location" functionality from the Actions button on the Manage> Devices page
#                 works as expected.  This is qTest test case TC-47557.

*** Settings ***
Library     extauto/common/Mu.py
Library     extauto/common/Utils.py
Library     extauto/common/Screen.py
Library     extauto/common/Cli.py
Library     extauto/common/TestFlow.py
# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     extauto/xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     extauto/xiq/flows/common/Navigator.py
Library     extauto/xiq/flows/manage/Location.py
Library     extauto/xiq/flows/manage/Devices.py
Library     extauto/xiq/flows/configure/CommonObjects.py
Library     extauto/xiq/flows/configure/NetworkPolicy.py
Library     extauto/xiq/flows/mlinsights/Network360Plan.py
Library     extauto/xiq/flows/mlinsights/Network360Monitor.py
Library     extauto/xiq/flows/configure/ExpressNetworkPolicies.py
Library     extauto/xiq/flows/globalsettings/GlobalSetting.py
Library     ExtremeAutomation/Imports/CommonObjectUtils.py
Library     ExtremeAutomation/Keywords/UserDefinedKeywords/NetworkElements/SetupTeardown/SetupTeardownUdks.py
Library     keywords/gui/manage/KeywordsDevices.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/location_sanity_config.py

Force Tags   testbed_1_node

Library	            Remote 	http://${mu1.ip}:${mu1.port}   WITH NAME   MU1

Suite Setup     Test Suite Setup
Suite Teardown    Run Keyword And Warn On Failure  Test Suite Clean Up 

*** Variables ***
${LOCATION}                 auto_location_01, Santa Clara, building_02, floor_04

# need to change according to the floor in ${LOCATION}
${LOCATION_DISPLAY}         auto_location_01 >> Santa Clara >> building_02 >> floor_04
${FLOOR}                    floor_04



*** Keywords ***
Test Suite Setup
    # Use this method to convert the ap, wing, netelem to a generic device object
    # ap1       => device1
    # wing1     => device1
    # netelem1  => device1 (EXOS / VOSS)
    convert to generic device object   device  index=1

    # Create the connection to the device(s)
    Base Test Suite Setup
    Set Global Variable    ${MAIN_DEVICE_SPAWN}    ${device1.name}

    # log in the user
    Login User      ${tenant_username}      ${tenant_password}

    #Onboard device
    Device Onboard
    Create Network Policy and Update to AP
    
    Set Suite Variable              ${POLICY_NAME}
    Set Suite Variable              ${SSID_NAME}

Test Suite Clean Up
    [Tags]			        production          cleanup

    Clean Up Device

    ${DLT_NW_POLICIES}=             Delete Network Polices                  ${POLICY_NAME}
    should be equal as integers     ${DLT_NW_POLICIES}          1

    ${DELETE_SSIDS}=                Delete SSIDs                            ${SSID_NAME}
    should be equal as integers     ${DELETE_SSIDS}             1

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Device Onboard
    # onboard the device
    Clean Up Device

    ${ONBOARD_RESULT}=          onboard device quick     ${device1}
    Should Be Equal As Strings                  ${ONBOARD_RESULT}       1

    configure device to connect to cloud    ${device1.cli_type}   ${generic_capwap_url}   ${MAIN_DEVICE_SPAWN}

    ${ONLINE_STATUS_RESULT}=    wait until device online     ${device1.serial}
    Should Be Equal As Strings                  ${ONLINE_STATUS_RESULT}       1

    ${MANAGED_STATUS_RESULT}=   wait until device managed   ${device1.serial}
    Should Be Equal As Strings                  ${MANAGED_STATUS_RESULT}      1

    ${DEVICE_STATUS_RESULT}=    get device status      ${device1.serial}
    Should Be Equal As Strings                  ${DEVICE_STATUS_RESULT}      green

    # Upgrade the device to latest/supported version to avoid config push issues.
    ${LATEST_VERSION}=      Upgrade Device      ${device1}
    Should Not be Empty     ${LATEST_VERSION}

    Sleep                   ${ap_reboot_wait}

    ${CONNECTED_STATUS}=    Wait Until Device Online                ${device1.serial}       retry_count=15
    Should Be Equal as Integers             ${CONNECTED_STATUS}          1

    ${REBOOT_STATUS}=    Wait Until Device Reboots               ${device1.serial}
    Should Be Equal as Integers             ${REBOOT_STATUS}          1

Clean Up Device
    ${search_result}=   keywordsdevices.search device   ${device1}    ignore_failure=True
    # Disconnect from Extreme Cloud IQ
    Run Keyword If  '${search_result}' == '1'       Delete and Disconnect Device From Cloud

Delete and Disconnect Device From Cloud
    keywordsdevices.delete device    ${device1}
    disconnect device from cloud     ${device1.cli_type}     ${MAIN_DEVICE_SPAWN}

Create Network Policy and Update to AP
    ${POLICY_RESULT}                Create Open Auth Express Network Policy     ${POLICY_NAME}      ${SSID_NAME}
    Should Be Equal As Integers     ${POLICY_RESULT}        1

    ${NP_RESULT}=                   Update Network Policy To AP     policy_name=${POLICY_NAME}     ap_serial=${device1.serial}
    Should Be Equal As Integers     ${NP_RESULT}            1       Unable to Update the Network Policy to AP

    ${UPDATE_RESULT}=               update_device_delta_configuration           ${device1.serial}
    Should Be Equal As Integers     ${UPDATE_RESULT}        1

    ${CONNECTED_STATUS}=    Wait Until Device Online                ${device1.serial}
    Should Be Equal as Integers             ${CONNECTED_STATUS}          1

*** Test Cases ***
TCCS-11596: Verify AP Hostname in ML Insights Plan Tab
    [Documentation]                 Verify AP Hostname in ML Insights Plan Tab

    [Tags]                          development      tccs_11596

    ${FLOOR_SEARCH}=                search_floor_in_network360Plan                  ${FLOOR}
    Save Screen shot
    Should Not Be Equal as Strings             '${FLOOR_SEARCH}'          '-1'

    ${AP_LIST}=                     get_aps_from_network360plan_floor               ${FLOOR}
    Should Contain                  ${AP_LIST}              ${device1.name}             ignore_case=True
    Save Screen shot

TCCS-11597: Verify AP Hostname and Client in ML Insights Monitor Tab
    [Documentation]                 Verify AP Hostname and Client in ML Insights Monitor Tab

    [Tags]                          production      tccs_11597

    ${loc_result}=                  Get Device Details      ${device1.serial}       LOCATION
    Should Contain                  ${loc_result}           ${LOCATION_DISPLAY}

    ${NP_FROM_UI}=                  Get Device Details      ${device1.serial}       POLICY
    should be equal as strings      ${NP_FROM_UI}           ${POLICY_NAME}

    ${CONNECT_STATUS}=              MU1.connect_open_network         ${SSID_NAME}
    should be equal as strings      '${CONNECT_STATUS}'    '1'

    sleep   ${client_connect_wait}

    ${FLOOR_SEARCH}=                search_floor_in_network360monitor               ${FLOOR}
    Save Screen shot
    Should Not Be Equal as Strings             '${FLOOR_SEARCH}'          '-1'

    ${AP_LIST}=                     get_devices_from_network360monitor_floor        ${FLOOR}
    Should Contain                  ${AP_LIST}              ${device1.name}
    Save Screen shot

    ${CLIENT_LIST}                  get_clients_from_network360monitor_floor        ${FLOOR}
    Save Screen shot
    Log                             ${CLIENT_LIST}
    Should Contain                  ${CLIENT_LIST}          ${mu1.wifi_mac}