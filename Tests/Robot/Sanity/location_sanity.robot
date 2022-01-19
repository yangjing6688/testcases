# Author        : Rameswar
# Description   : Verifies the "Assign Location" functionality from the Actions button on the Manage> Devices page
#                 works as expected.  This is qTest test case TC-47557.

*** Settings ***
Library     common/Mu.py
Library     common/Utils.py
Library     common/Screen.py

Library     xiq/flows/common/Login.py
Library     xiq/flows/common/Navigator.py

Library     xiq/flows/manage/Location.py
Library     xiq/flows/manage/Devices.py

Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/mlinsights/Network360Plan.py
Library     xiq/flows/mlinsights/Network360Monitor.py
Library     xiq/flows/configure/ExpressNetworkPolicies.py

Library     xiq/flows/globalsettings/GlobalSetting.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml

Library	            Remote 	http://${mu1.ip}:${mu1.port}   WITH NAME   MU1

*** Variables ***
${LOCATION}                 auto_location_01, Santa Clara, building_02, floor_04

# need to change according to the floor in ${LOCATION}
${LOCATION_DISPLAY}         auto_location_01 >> Santa Clara >> building_02 >> floor_04
${FLOOR}                    floor_04

*** Test Cases ***
test1: Assign Location to AP Device
    [Documentation]                 Assigns a location to the AP being tested and confirms the action was successful
    ...                             Steps:
    ...                             Login
    ...                             Create a open network policy
    ...                             Assign above policy to the AP
    ...                             Assign Location
    ...                             Update Delta config to AP
    ...                             Validate Update result, AP's Location & Policy from Devices Grid

    [Tags]                          production

    ${result}=                      Login User      ${tenant_username}          ${tenant_password}
    ${POLICY_NAME}                  Get Random String
    ${SSID_NAME}                    Get Random String
    Set Suite Variable              ${POLICY_NAME}
    Set Suite Variable              ${SSID_NAME}

    ${POLICY_RESULT}                Create Open Auth Express Network Policy     ${POLICY_NAME}      ${SSID_NAME}
    Should Be Equal As Integers     ${POLICY_RESULT}        1

    ${NP_RESULT}=                   Update Network Policy To AP     policy_name=${POLICY_NAME}     ap_serial=${ap1.serial}
    Should Be Equal As Integers     ${NP_RESULT}            1       Unable to Update the Network Policy to AP

    ${LOCATION_RESULT}=             Assign Location With Device Actions         ${ap1.serial}       ${LOCATION}
    Should Be Equal As Integers     ${LOCATION_RESULT}      1       Unable to Assign Location to Device

    ${UPDATE_RESULT}=               update_device_delta_configuration           ${ap1.serial}

    Wait Until Device Online        ${ap1.serial}

    ${loc_result}=                  Get Device Details      ${ap1.serial}       LOCATION
    ${NP_FROM_UI}=                  Get Device Details      ${ap1.serial}       POLICY

    Should Be Equal As Integers     ${UPDATE_RESULT}        1
    should be equal as strings      ${NP_FROM_UI}           ${POLICY_NAME}
    Should Contain                  ${loc_result}           ${LOCATION_DISPLAY}

    [Teardown]
    Quit Browser

test2: Verify AP Hostname in ML Insights Plan Tab
    [Documentation]                 Verify AP Hostname in ML Insights Plan Tab
    [Tags]                          production      test2
    Login User                      ${tenant_username}      ${tenant_password}

    ${FLOOR_SEARCH}=                search_floor_in_network360Plan                  ${FLOOR}
    Save Screen shot

    ${AP_LIST}=                     get_aps_from_network360plan_floor               ${FLOOR}
    Should Contain                  ${AP_LIST}              ${ap1.name}             ignore_case=True
    Save Screen shot

    [Teardown]
    Quit Browser

test3: Verify AP Hostname and Client in ML Insights Monitor Tab
    [Documentation]                 Verify AP Hostname and Client in ML Insights Monitor Tab
    [Tags]                          production      test3
    Login User                      ${tenant_username}      ${tenant_password}

    Sleep                           300
    ${CONNECT_STATUS}=              MU1.connect_open_network         ${SSID_NAME}
    should be equal as strings      '${CONNECT_STATUS}'    '1'

    ${FLOOR_SEARCH}=                search_floor_in_network360monitor               ${FLOOR}
    Save Screen shot

    ${AP_LIST}=                     get_devices_from_network360monitor_floor        ${FLOOR}
    Should Contain                  ${AP_LIST}              ${ap1.name}
    Save Screen shot

    ${CLIENT_LIST}                  get_clients_from_network360monitor_floor        ${FLOOR}
    Save Screen shot
    Log                             ${CLIENT_LIST}
    Should Contain                  ${CLIENT_LIST}          ${mu1.wifi_mac}

    [Teardown]
    Quit Browser
