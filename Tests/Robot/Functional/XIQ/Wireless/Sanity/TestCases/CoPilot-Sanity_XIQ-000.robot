# Author        : Shrisha
# Date          : Aug 24,2022
# Description   : Co-Pilot Wireless client Experience
#
# Topology      :
# AP1----- Cloud-----Ubuntu(MU1) or Windows MU

# Execution Command:
# ------------------
#  robot -v TESTBED:BANGALORE/Prod/wireless/adsptestbed1.yaml -v TOPO:topo.test.g2r1.xim.automation.yaml -v ENV:environment.adsp.remote.win10.chrome.yaml CoPilot-Sanity.robot

*** Variables ***
${LOCATION}                 auto_location_01, San Jose, building_01, floor_01
${NW_POLICY_NAME}           copilot_gf_policy
${SSID_NAME}                copilot_gf_sanity_ssid
${BUILDING_NAME}            building_01
${FLOOR_NAME}               floor_01
${MAP_FILE_NAME}            auto_location_01_1595321828282.tar.gz
${DURATION_OPTION}          Last 1 Hour
${VIEW_BY_LOCATION}         Location
${VIEW_BY_SSID}             SSID
${QUALITY_INDEX}            10
@{Quality_index_list}=                    5    6    7    8    9    10
@{performance_index_list}=                    5    6    7    8    9    10

${LOCATION_2}       Sant Clara
${BUILDING_NAME_2}            building_02
${BULDING_FLOOR_NAME_2_1}               floor_03
${BULDING_FLOOR_NAME_2_2}               floor_04


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
Library     xiq/flows/copilot/Copilot.py

Library     xiq/flows/manage/Client.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Location.py

Library     xiq/flows/configure/Wips.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/configure/DeviceTemplate.py

Library     ExtremeAutomation/Imports/CommonObjectUtils.py

Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/mlinsights/Network360Plan.py
Library     xiq/flows/common/MuCaptivePortal.py
Library     ExtremeAutomation/Keywords/UserDefinedKeywords/NetworkElements/SetupTeardown/SetupTeardownUdks.py

Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml


Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml
Resource     Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/extreme_copilot_sanity_config.robot
Library	     Remote   http://${mu1.ip}:${mu1.port}  WITH NAME   Remote_Server

Force Tags   testbed_1_node

Suite Setup     Test Suite Setup
Suite Teardown  Test Suite Clean Up

*** Keywords ***
Test Suite Setup
    # Use this method to convert the ap, wing, netelem to a generic device object
    # ap1       => device1
    # wing1     => device1
    # netelem1  => device1 (EXOS / VOSS)
    Convert To Generic Device Object    device      index=1     look_for_device_type=ap     set_to_index=1

    # Create the connection to the device
    Base Test Suite Setup
    Set Global Variable     ${MAIN_DEVICE_SPAWN}            ${device1.name}


Test Suite Clean Up
    [Documentation]    delete created network policies,ssid

    [Tags]      sanity      cleanup
    ${result}=    Login User       ${tenant_username}     ${tenant_password}
    Remote_Server.Disconnect WiFi
    Delete Device  device_serial=${ap1.serial}
    Delete Network Polices         ${NW_POLICY_NAME}
    delete ap template profile     ${ap1.template_name}
    Delete ssids                   ${SSID_NAME}
    Logout User
    Quit Browser

*** Test Cases ***
TCCS-13495_Step1 : Login and Onboard AP on XIQ Account
    [Documentation]         Onboard AP to XIQ Account
    [Tags]                  tccs_13495    tccs_13495_step1    development

    ${LOGIN_XIQ}=               Login User          ${tenant_username}     ${tenant_password}

    # Enable the Co-pilot if not enabled.
    ${copilot_enable_status}    enable_copilot_feature_for_this_viq
    Should Be Equal As Strings      ${copilot_enable_status}       1

    # Check if devices exist and disconnect and delete
    ${SEARCH_RESULT}=           Search Device               device_serial=${device1.serial}     ignore_cli_feedback=true
    IF  ${SEARCH_RESULT} == 1
        ${DISCONNECT_DEVICE_RESULT}=    Disconnect Device From Cloud        ${device1.cli_type}      ${MAIN_DEVICE_SPAWN}
        Should Be Equal As Integers     ${DISCONNECT_DEVICE_RESULT}         1

        ${DELETE_DEVICE_RESULT}=        Delete Device                       device_serial=${device1.serial}
        Should Be Equal As Integers     ${DELETE_DEVICE_RESULT}             1
    END

    ${ONBOARD_RESULT}=      Onboard Device Quick        ${device1}
    Should Be Equal As Strings      ${ONBOARD_RESULT}       1

    ${CONF_RESULT}=         Configure Device To Connect To Cloud            ${device1.cli_type}     ${generic_capwap_url}   ${MAIN_DEVICE_SPAWN}
    Should Be Equal As Integers     ${CONF_RESULT}          1

    ${WAIT_CONF_RESULT}=    Wait For Configure Device To Connect To Cloud   ${device1.cli_type}     ${generic_capwap_url}   ${MAIN_DEVICE_SPAWN}
    Should Be Equal As Integers     ${WAIT_CONF_RESULT}     1

    ${ONLINE_STATUS}=       Wait Until Device Online    ${device1.serial}
    Should Be Equal As Integers     ${ONLINE_STATUS}        1

    ${MANAGED_STATUS}=      Wait Until Device Managed   ${device1.serial}
    Should Be Equal As Integers     ${MANAGED_STATUS}       1

    ${AP1_STATUS}=               Get AP Status       ap_mac=${ap1.mac}
    Should Be Equal As Strings  '${AP1_STATUS}'     'green'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TCCS-13495_Step2 : Create Network policy and Attach Network policy to AP
    [Documentation]         Assign network policy to AP
    [Tags]                  tccs_13495    tccs_13495_step2    development
    Depends on      TCCS-13495_Step1
    ${LOGIN_XIQ}=                   Login User          ${tenant_username}     ${tenant_password}

    ${CREATE_POLICY1}=              Create Network Policy   ${NW_POLICY_NAME}      ${LOCATION_OPEN_NW}
    Should Be Equal As Strings      '${CREATE_POLICY1}'   '1'

    ${CREATE_AP_TEMPLATE}=          Add AP Template     ${ap1.model}    ${ap1.template_name}    ${AP_TEMPLATE_CONFIG}
    Should Be Equal As Strings      '${CREATE_AP_TEMPLATE}'   '1'

    ${AP1_UPDATE_CONFIG}=           Update Network Policy To AP   ${NW_POLICY_NAME}     ap_serial=${ap1.serial}   update_method=Complete
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'

    ${WAIT_UNTIL_UPDATE}=           Wait Until Device Update Done   device_serial=${device1.serial}
    Should Be Equal As Integers     ${WAIT_UNTIL_UPDATE}                1

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TCCS-13495_Step3 : Connect WIFI Client and sleep for 20 min
    [Documentation]         Connect wifi client
    [Tags]                  tccs_13495    tccs_13495_step3    development
    Depends on      TCCS-13495_Step2

    ${LOGIN_XIQ}=                  Login User          ${tenant_username}     ${tenant_password}

    Remote_Server.Connect Open Network    ${SSID_NAME}

    Log to Console      Sleep for ${client_connect_wait}
    sleep                         ${client_connect_wait}

    ${CLIENT_STATUS}=                Get Client Status   client_mac=${mu1.wifi_mac}
    Should Be Equal As Strings       '${CLIENT_STATUS}'      '1'

    Log to Console      Sleep for ${client_connect_wait}
    sleep                         ${client_connect_wait}

    ### It takes around 45 min to show up the first data
    Wait Until Device Online    ${ap1.serial}

    Refresh Devices Page
    sleep   600s

    Refresh Devices Page
    sleep   600s

    Refresh Devices Page
    sleep   600s

    Refresh Devices Page
    sleep   600s

    Refresh Devices Page
    sleep   600s

    Refresh Devices Page
    sleep   600s


    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TCCS-13495_Step4: Verify wireless client experience quality index by location
    [Documentation]         Verify wireless client experience quality index by location
    [Tags]                  tccs_13495    tccs_13495_step4    development
    Depends on      TCCS-13495_Step3

    ${LOGIN_XIQ}=                  Login User          ${tenant_username}     ${tenant_password}

    ${return_Quality_Index_val}=     get wirless clientexp quality index by location    ${BUILDING_NAME}    ${VIEW_BY_LOCATION}    ${DURATION_OPTION}
    should contain match    ${Quality_index_list}   ${return_Quality_Index_val}

    ${DEVICE_PAGE_NAVIGATION}=  navigate_to_devices
    should be equal as strings       '${DEVICE_PAGE_NAVIGATION}'    '1'

    ${return_Quality_Index_val_ssid}=     get wirless clientexp quality index by ssid    ${SSID_NAME}    ${VIEW_BY_SSID}    ${DURATION_OPTION}
    should contain match    ${Quality_index_list}   ${return_Quality_Index_val_ssid}

    ${DEVICE_PAGE_NAVIGATION}=  navigate_to_devices
    should be equal as strings       '${DEVICE_PAGE_NAVIGATION}'    '1'

    ${return_performance_Index_val}=     get wirless clientexp performance index by location    ${BUILDING_NAME}    ${VIEW_BY_LOCATION}    ${DURATION_OPTION}
    should contain match    ${performance_index_list}   ${return_performance_Index_val}

    ${DEVICE_PAGE_NAVIGATION}=  navigate_to_devices
    should be equal as strings       '${DEVICE_PAGE_NAVIGATION}'    '1'

    ${return_performance_Index_val_ssid}=     get wirless clientexp performance index by ssid    ${SSID_NAME}    ${VIEW_BY_SSID}    ${DURATION_OPTION}
    should contain match    ${performance_index_list}   ${return_performance_Index_val_ssid}

    ${DEVICE_PAGE_NAVIGATION}=  navigate_to_devices
    should be equal as strings       '${DEVICE_PAGE_NAVIGATION}'    '1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

