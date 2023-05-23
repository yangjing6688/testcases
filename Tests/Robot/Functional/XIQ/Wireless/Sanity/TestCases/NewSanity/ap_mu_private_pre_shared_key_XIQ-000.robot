# Author        : hshivanagi
# Date          : April 2020
# Description   : private pre-shared connectivity check

# Topology      :
# Client -----> AP --->XIQ Instance
# Pre-Condtion
# Uses cloud3tenant3@gmail.com, cloud4tenant4@gmail.com
# 1. AP should be onboarded and it is online
# 2. start the remote srevre in MU. Starting remote server on MU refer testsuite/xiq/config/remote_server_config.txt
# 3. Start the stand alone selenium server on MU refer:testsuite/xiq/config/remote_server_config.txt
# 4. Required Device: 1 AP, 1 Windows10 MU

# Execution Command:
# robot -L INFO -v DEVICE:AP630 -v TOPO:g7r2  private_pre_shared_key.robot
# Select the "TOPO" and "DEVICE" variable based on Test bed

*** Variables ***
# Arguments passed from the command line
# Until keyword is created.. variable names created in resources file

# !!!!!
# Policy,SSID and Group variables Moved to Resources python file for randomization 2022-08-31
# !!!!!

${PAGE_TITLE}       End-to-End Cloud Driven Networking Solutions - Extreme Networks
${LOCATION}         auto_location_01, Santa Clara, building_02, floor_04

*** Settings ***
Library     Collections
Library     extauto/common/Cli.py
Library     extauto/common/GmailHandler.py
Library     extauto/common/LoadBrowser.py
Library     extauto/common/TestFlow.py
Library     extauto/common/Utils.py
# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     extauto/xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     extauto/xiq/flows/common/MuCaptivePortal.py
Library     extauto/xiq/flows/common/Navigator.py
Library     extauto/xiq/flows/configure/CommonObjects.py
Library     extauto/xiq/flows/configure/NetworkPolicy.py
Library     extauto/xiq/flows/configure/UserGroups.py
Library     extauto/xiq/flows/globalsettings/GlobalSetting.py
Library     extauto/xiq/flows/manage/Client.py
Library     extauto/xiq/flows/manage/ClientMonitor.py
Library     extauto/xiq/flows/manage/Devices.py
Library     extauto/xiq/flows/manage/DeviceCliAccess.py
Library     extauto/xiq/flows/mlinsights/MLInsightClient360.py
Library     ExtremeAutomation/Imports/CommonObjectUtils.py
Library     ExtremeAutomation/Keywords/UserDefinedKeywords/NetworkElements/SetupTeardown/SetupTeardownUdks.py

Variables   TestBeds/${TESTBED}
Variables   Environments/${TOPO}
Variables   Environments/${ENV}
Variables   Environments/Config/device_commands.yaml
Variables   Environments/Config/waits.yaml
Variables   Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/private_pre_shared_key_config.py
Variables   Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/test_email_ids.py

Library	    Remote 	http://${mu1.ip}:${mu1.port}   WITH NAME   mu1

Force Tags  testbed_1_node

Suite Setup         Suite Setup
Suite Teardown      Run Keyword And Warn On Failure    Suite Teardown

*** Keywords ***
Suite Setup
    [Documentation]     Cleanup before running the suite
    [Tags]      production  cleanup

    Log To Console      DOING CLEANUP BEFORE RUNNING THE SUITE!
    Set Suite Variable     ${BULK_CLOUD_NW_SSID}

    # Use this method to convert the ap, wing, netelem to a generic device object
    # ap1      => device1
    # wing1    => device1
    # netelem1 => device1 (EXOS/VOSS)
    Convert To Generic Device Object    device      index=1     look_for_device_type=ap     set_to_index=1

    # Create the connection to the device
    Base Test Suite Setup
    Set Global Variable     ${MAIN_DEVICE_SPAWN}            ${device1.name}

    ${LOGIN_RESULT}=            Login User                  ${tenant_username}      ${tenant_password}      check_warning_msg=True
    Should Be Equal As Integers     ${LOGIN_RESULT}         1

    ${SEARCH_RESULT}=           Search Device               device_serial=${device1.serial}     ignore_failure=True
    IF  ${SEARCH_RESULT} == 1
        ${DISCONNECT_DEVICE_RESULT}=    Disconnect Device From Cloud        ${device1.cli_type}      ${MAIN_DEVICE_SPAWN}
        Should Be Equal As Integers     ${DISCONNECT_DEVICE_RESULT}         1

        ${DELETE_DEVICE_RESULT}=        Delete Device                       device_serial=${device1.serial}
        Should Be Equal As Integers     ${DELETE_DEVICE_RESULT}             1
    END

    ${CONF_RESULT}=         Configure Device To Connect To Cloud             ${device1.cli_type}     ${generic_capwap_url}   ${MAIN_DEVICE_SPAWN}
    Should Be Equal As Integers     ${CONF_RESULT}          1

    ${ONBOARD_RESULT}=      Onboard Device Quick        ${device1}
    Should Be Equal As Strings      ${ONBOARD_RESULT}       1

    ${WAIT_CONF_RESULT}=    Wait For Configure Device To Connect To Cloud   ${device1.cli_type}     ${generic_capwap_url}   ${MAIN_DEVICE_SPAWN}
    Should Be Equal As Integers     ${WAIT_CONF_RESULT}     1

    ${ONLINE_STATUS}=       Wait Until Device Online    ${device1.serial}
    Should Be Equal As Integers     ${ONLINE_STATUS}        1

    ${MANAGED_STATUS}=      Wait Until Device Managed   ${device1.serial}
    Should Be Equal As Integers     ${MANAGED_STATUS}       1

    ${DEVICE_STATUS_RESULT}=       Get Device Status           device_mac=${device1.mac} 
    Should contain any                  ${DEVICE_STATUS_RESULT}    green     config audit mismatch

    # Upgrade the device to latest/supported version to avoid config push issues.
    ${LATEST_VERSION}=              Upgrade Device                  ${device1}
    Should Not be Empty             ${LATEST_VERSION}

    ${REBOOT_STATUS}=               Wait Until Device Reboots       ${device1.serial}       retry_count=15
    Should Be Equal as Integers     ${REBOOT_STATUS}                    1

    ${CONNECTED_STATUS}=            Wait Until Device Online        ${device1.serial}
    Should Be Equal as Integers     ${CONNECTED_STATUS}                 1

    ${DELETE_POLICIES_RESULT}=      Delete Network Polices          ${OPEN_POLICY}      ${BULK_CLOUD_NW_POLICY}     ${BULK_LOCAL_NW_POLICY}
    Should Be Equal As Integers     ${DELETE_POLICIES_RESULT}           1

    ${DELETE_SSID_RESULT}=          Delete SSIDs                    ${OPEN_SSID}        ${BULK_CLOUD_NW_SSID}       ${BULK_LOCAL_NW_SSID}
    Should Be Equal As Integers     ${DELETE_SSID_RESULT}               1

    ${DELETE_UG_RESULT}=            Delete User Groups              ${BULK_CLOUD_USER_GROUP}        ${BULK_LOCAL_USER_GROUP}
    Should Be Equal As Integers     ${DELETE_UG_RESULT}                 1

    ${CREATE_POLICY_RESULT}=        Create Network Policy           ${OPEN_POLICY}      ${CONFIG_PUSH_OPEN_NW_01}       cli_type=${device1.cli_type}
    Should Be Equal As Integers     ${CREATE_POLICY_RESULT}             1

    ${UPDATE_POLICY_RESULT}=        Update Network Policy To AP     ${OPEN_POLICY}      ap_serial=${device1.serial}     update_method=Complete
    Should Be Equal As Integers     ${UPDATE_POLICY_RESULT}             1

    ${WAIT_UNTIL_UPDATE}=           Wait Until Device Update Done   device_serial=${device1.serial}
    Should Be Equal As Integers     ${WAIT_UNTIL_UPDATE}                1

    ${CONNECTED_STATUS}=            Wait Until Device Online                ${device1.serial}   None   30   20
    Should Be Equal as Integers     ${CONNECTED_STATUS}          1
    
    mu1.Disconnect WiFi

Suite Teardown
    [Documentation]     Cleanup after running the suite
    [Tags]      production  cleanup

    Log To Console      DOING CLEANUP AFTER RUNNING THE SUITE!

    ${SEARCH_RESULT}=   Search Device               device_serial=${device1.serial}     ignore_failure=True
    IF  ${SEARCH_RESULT} == 1
        ${DISCONNECT_DEVICE_RESULT}=    Disconnect Device From Cloud        ${device1.cli_type}     ${MAIN_DEVICE_SPAWN}
        Should Be Equal As Integers     ${DISCONNECT_DEVICE_RESULT}         1

        ${DELETE_DEVICE_RESULT}=        Delete Device                       device_serial=${device1.serial}
        Should Be Equal As Integers     ${DELETE_DEVICE_RESULT}             1
    END

    ${DELETE_POLICIES_RESULT}=      Delete Network Polices          ${OPEN_POLICY}      ${BULK_CLOUD_NW_POLICY}     ${BULK_LOCAL_NW_POLICY}
    Should Be Equal As Integers     ${DELETE_POLICIES_RESULT}           1

    ${DELETE_SSID_RESULT}=          Delete SSIDs                    ${OPEN_SSID}        ${BULK_CLOUD_NW_SSID}       ${BULK_LOCAL_NW_SSID}
    Should Be Equal As Integers     ${DELETE_SSID_RESULT}               1

    ${DELETE_UG_RESULT}=            Delete User Groups              ${BULK_CLOUD_USER_GROUP}        ${BULK_LOCAL_USER_GROUP}
    Should Be Equal As Integers     ${DELETE_UG_RESULT}                 1

    ${LOGOUT_RESULT}=               Logout User
    Should Be Equal As Integers     ${LOGOUT_RESULT}                1

    ${QUIT_BROWSER_RESULT}=         Quit Browser
    Should Be Equal As Integers     ${QUIT_BROWSER_RESULT}          1

    mu1.Disconnect WiFi

Test Case Teardown
    [Arguments]     ${POLICY}   ${SSID}     ${USER_GROUP}
    ${UPDATE_POLICY_RESULT}=        Update Network Policy To AP     ${OPEN_POLICY}      ap_serial=${device1.serial}
    Should Be Equal As Integers     ${UPDATE_POLICY_RESULT}         1

    ${WAIT_UNTIL_UPDATE}=           Wait Until Device Update Done   device_serial=${device1.serial}
    Should Be Equal As Integers     ${WAIT_UNTIL_UPDATE}            1

    ${DELETE_POLICY_RESULT}=        Delete Network Polices          ${POLICY}
    Should Be Equal As Integers     ${DELETE_POLICY_RESULT}         1

    ${DELETE_SSID_RESULT}=          Delete SSIDs                    ${SSID}
    Should Be Equal As Integers     ${DELETE_SSID_RESULT}           1

    ${DELETE_UG_RESULT}=            Delete User Groups              ${USER_GROUP}
    Should Be Equal As Integers     ${DELETE_UG_RESULT}             1

    mu1.Disconnect WiFi
    mu1.Delete WLAN Profile         ${SSID}

Connect To PPSK Wireless Network
    [Arguments]     ${SSID}     ${KEY}
    ${CONNECT_RESULT}=      mu1.Connect WPA2 PPSK Network       ${SSID}     ${KEY}
    Should Be Equal As Integers     ${CONNECT_RESULT}           1

Wi-Fi Interface IP Address Check
    ${WIFI_IP_ADDRESS}=     mu1.Get Wi Fi Interface Ip Address
    Should Contain Any      ${WIFI_IP_ADDRESS}           ${mu1.wifi_network}     ${mu1.wifi_network_vlan10}

Negative Internet Connectivity Check
    ${FLAG}=    mu1.Verify Internet Connectivity
    Should Be Equal As Integers     ${FLAG}     -1
    Log To Console      Internet is NOT available on the MU machine, as expected!

Positive Internet Connectivity Check
    ${FLAG}=    mu1.Verify Internet Connectivity
    Should Be Equal As Integers     ${FLAG}     1
    Log To Console      Internet is available on the MU machine, as expected!

*** Test Cases ***
TCCS-7678: Cloud DB PPSK Network Client Connectivity With Bulk Users Group
    [Documentation]     Check client connectivity to Wi-Fi PPSK network with user group and cloud password DB
    [Tags]              development     tccs_7678

    ${USER_GROUP_CREATE_RESULT}=    Create User Group               ${BULK_CLOUD_USER_GROUP}    user_group_profile=&{USER_GROUP_PROFILE_CLOUD_BULK}
    Should Be Equal As Integers     ${USER_GROUP_CREATE_RESULT}     1

    ${CREDENTIALS}=     Get Login Credential From Attachments       ${PPSK_MAIL_ID}     ${PPSK_MAIL_PASSWORD}

    ${CREATE_POLICY_RESULT}=        Create Network Policy           ${BULK_CLOUD_NW_POLICY}     ${WIRELESS_PPSK_NW_CLOUD_BULK}
    Should Be Equal As Integers     ${CREATE_POLICY_RESULT}         1

    ${UPDATE_POLICY_RESULT}=        Update Network Policy To Ap     policy_name=${BULK_CLOUD_NW_POLICY}    ap_serial=${device1.serial}
    Should Be Equal As Integers     ${UPDATE_POLICY_RESULT}         1

    ${WAIT_UNTIL_UPDATE}=           Wait Until Device Update Done   device_serial=${device1.serial} 
    Should Be Equal As Integers     ${WAIT_UNTIL_UPDATE}            1

    # wait for SSID to become available
    Log to Console      Sleep for ${client_connect_wait} seconds
    Sleep               ${client_connect_wait}

    Negative Internet Connectivity Check

    Connect To PPSK Wireless Network        ${BULK_CLOUD_NW_SSID}       ${CREDENTIALS['user_1']['Access Key']}

    # wait for client to connect to SSID
    Log to Console      Sleep for ${client_connect_wait} seconds
    Sleep               ${client_connect_wait}

    Wi-Fi Interface IP Address Check

    Positive Internet Connectivity Check

    [Teardown]      run keyword     Test Case Teardown      ${BULK_CLOUD_NW_POLICY}     ${BULK_CLOUD_NW_SSID}   ${BULK_CLOUD_USER_GROUP}

TCCS-7691: Local DB PPSK Network Client Connectivity With Bulk Users Group
    [Documentation]     Check client connectivity to Wi-Fi PPSK network with user group and local password DB
    [Tags]              development     tccs_7691

    ${USER_GROUP_CREATE_RESULT}=    Create User Group               ${BULK_LOCAL_USER_GROUP}    user_group_profile=&{USER_GROUP_PROFILE_LOCAL_BULK}
    Should Be Equal As Integers     ${USER_GROUP_CREATE_RESULT}     1

    ${CREDENTIALS}=     Get Login Credential From Attachments       ${PPSK_MAIL_ID}     ${PPSK_MAIL_PASSWORD}

    ${CREATE_POLICY_RESULT}=        Create Network Policy           ${BULK_LOCAL_NW_POLICY}     ${WIRELESS_PPSK_NW_LOCAL_BULK}
    Should Be Equal As Integers     ${CREATE_POLICY_RESULT}         1

    ${UPDATE_POLICY_RESULT}=        Update Network Policy To Ap     policy_name=${BULK_LOCAL_NW_POLICY}    ap_serial=${device1.serial}
    Should Be Equal As Integers     ${UPDATE_POLICY_RESULT}         1

    ${WAIT_UNTIL_UPDATE}=           Wait Until Device Update Done   device_serial=${device1.serial}
    Should Be Equal As Integers     ${WAIT_UNTIL_UPDATE}            1

    # wait for SSID to become available
    Log to Console      Sleep for ${client_connect_wait} seconds
    Sleep               ${client_connect_wait}

    Negative Internet Connectivity Check

    Connect To PPSK Wireless Network        ${BULK_LOCAL_NW_SSID}       ${CREDENTIALS['user2_1']['Access Key']}

    # wait for client to connect to SSID
    Log to Console      Sleep for ${client_connect_wait} seconds
    Sleep               ${client_connect_wait}

    Wi-Fi Interface IP Address Check

    Positive Internet Connectivity Check

    [Teardown]      run keyword     Test Case Teardown      ${BULK_LOCAL_NW_POLICY}     ${BULK_LOCAL_NW_SSID}   ${BULK_LOCAL_USER_GROUP}