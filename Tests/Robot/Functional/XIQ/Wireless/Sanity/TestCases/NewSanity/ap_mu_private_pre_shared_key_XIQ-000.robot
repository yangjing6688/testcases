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

${PAGE_TITLE}                       End-to-End Cloud Driven Networking Solutions - Extreme Networks
${LOCATION}                 auto_location_01, Santa Clara, building_02, floor_04

*** Settings ***
Library     Collections

Library     extauto/common/GmailHandler.py
Library     extauto/common/Utils.py
Library     extauto/common/LoadBrowser.py
Library     extauto/common/Cli.py
Library     extauto/common/TestFlow.py

Library     extauto/xiq/flows/common/Login.py
Library     extauto/xiq/flows/common/MuCaptivePortal.py

Library     extauto/xiq/flows/manage/Devices.py
Library     extauto/xiq/flows/manage/DeviceCliAccess.py
Library     extauto/xiq/flows/manage/ClientMonitor.py
Library     extauto/xiq/flows/manage/Client.py
Library     extauto/xiq/flows/common/Navigator.py

Library     extauto/xiq/flows/configure/UserGroups.py
Library     extauto/xiq/flows/configure/NetworkPolicy.py
Library     extauto/xiq/flows/configure/CommonObjects.py

Library     extauto/xiq/flows/mlinsights/MLInsightClient360.py
Library     extauto/xiq/flows/globalsettings/GlobalSetting.py
Library     extauto/common/Utils.py
Library     ExtremeAutomation/Imports/CommonObjectUtils.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml
Variables    Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/test_email_ids.py
Variables    Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/private_pre_shared_key_config.py
Library      ExtremeAutomation/Keywords/UserDefinedKeywords/NetworkElements/SetupTeardown/SetupTeardownUdks.py

Library	    Remote 	http://${mu1.ip}:${mu1.port}   WITH NAME   mu1

Force Tags   testbed_1_node

Suite Setup      Pre Condition
Suite Teardown   Test Suite Clean Up

*** Keywords ***
Pre Condition
    [Documentation]   AP will be onboarded

    # Use this method to convert the ap, wing, netelem to a generic device object
    # ap1       => device1
    # wing1     => device1
    # netelem1  => device1 (EXOS / VOSS)
    convert to generic device object   device  index=1  look_for_device_type=ap  set_to_index=1

    # Create the connection to the device(s)
    Base Test Suite Setup
    Set Global Variable    ${MAIN_DEVICE_SPAWN}    ${device1.name}

    # downgrade the device if needed
    downgrade iqagent      ${device1.cli_type}  ${MAIN_DEVICE_SPAWN}

    # log in the user
    Login User      ${tenant_username}      ${tenant_password}

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

    # Setup the test
    ${CREATE_NW_POLICY_STATUS}=     Create Network Policy          ${OPEN_POLICY}            ${CONFIG_PUSH_OPEN_NW_01}
    should be equal as integers     ${CREATE_NW_POLICY_STATUS}               1

    ${UPDATE_NW_POLICY_STATUS}=     Update Network Policy To Ap    policy_name=${OPEN_POLICY}   ap_serial=${device1.serial}
    should be equal as integers     ${UPDATE_NW_POLICY_STATUS}               1

    ${DELETE_STATUS}=               Delete network polices      ${BULK_CLOUD_NW_POLICY}     ${BULK_LOCAL_NW_POLICY}
    should be equal as strings     '${DELETE_STATUS}'           '1'     ppsk network policy assigned to other AP,disassociate it or issue with deleting policy

    ${SSID_DLT_STATUS}=             Delete ssids                ${BULK_CLOUD_NW_SSID}       ${BULK_LOCAL_NW_SSID}
    should be equal as strings      '1'                        '${SSID_DLT_STATUS}'       Issue with deleting the SSID's

    ${DELETE_CWP_STATUS}=           Delete captive web portal      ${SELF_REG_RETURN_PPSK_CWP}
    should be equal as integers     ${DELETE_CWP_STATUS}               1

    ${DELETE_UGS}=                  Delete user groups              ${BULK_CLOUD_USER_GROUP}    ${BULK_LOCAL_USER_GROUP}
    should be equal as integers     ${DELETE_UGS}               1

Test Suite Clean Up
    [Documentation]    delete created network policies, usergroups, radius server
    [Tags]             development       cleanup

    Navigate To Devices

    ${DELETE_DEVICE_STATUS}=        Delete Device       device_serial=${device1.serial}
    should be equal as integers         ${DELETE_DEVICE_STATUS}               1

    ${DELETE_STATUS}=              delete network polices    ${BULK_CLOUD_NW_POLICY}  ${BULK_LOCAL_NW_POLICY}
    should be equal as strings    '${DELETE_STATUS}'           '1'     ppsk network policy assigned to other AP,disassociate it or issue with deleting policy

    ${SSID_DLT_STATUS}=            Delete ssids              ${BULK_CLOUD_NW_SSID}       ${BULK_LOCAL_NW_SSID}
    should be equal as strings      '1'                        '${SSID_DLT_STATUS}'       Issue with deleting the SSID's

    ${DELETE_CWP_STATUS}=           Delete captive web portal      ${SELF_REG_RETURN_PPSK_CWP}
    should be equal as integers     ${DELETE_CWP_STATUS}               1

    ${DELETE_UGS}=                  Delete user groups              ${BULK_CLOUD_USER_GROUP}    ${BULK_LOCAL_USER_GROUP}
    should be equal as integers     ${DELETE_UGS}               1

    [Teardown]   run keywords      logout user
    ...                            quit browser

Clean Up Device
    ${search_result}=   Search Device       device_serial=${device1.serial}    ignore_cli_feedback=true
    # Disconnect from Extreme Cloud IQ
    Run Keyword If  '${search_result}' == '1'       Delete and Disconnect Device From Cloud

Connect Ppsk Wireless Network
    [Arguments]    ${NETWORK}    ${KEY}
    ${CONNECT_STATUS}=   mu1.connect_wpa2_ppsk_network    ${NETWORK}    ${KEY}
    should be equal as strings  '${CONNECT_STATUS}'    '1'

Wi-Fi Interface IP Address Check
    ${IP}=   mu1.Get Wi Fi Interface Ip Address
    should contain any  ${IP}     ${mu1.wifi_network}    ${mu1.wifi_network_vlan10}

Re Connect To Open Network
    [Arguments]    ${NETWORK}
    close_cp_browser
    mu1.disconnect_wifi
    sleep                        ${client_disconnect_wait}
    ${CONNECT_STATUS}=           mu1.connect_open_network     ${NETWORK}
    should be equal as strings  '${CONNECT_STATUS}'           '1'
    sleep                        ${client_connect_wait}
    ${TITLE}=                    Open Cp Browser              ${mu1.ip}

Re Connect To PPSK Network
    [Arguments]    ${NETWORK}     ${KEY}
    mu1.disconnect_wifi
    sleep                            ${client_disconnect_wait}
    Connect Ppsk Wireless Network    ${NETWORK}   ${KEY}
    ${URL_TITLE}=                    Check Internet Connectivity     ${mu1.ip}
    should be equal as strings       '${URL_TITLE}'   '${PAGE_TITLE}'

Test Case Level Cleanup
     mu1.disconnect_wifi

*** Test Cases ***
TCCS-7678: Cloud DB PPSK Network Client Connectivity With Bulk Users Group
    [Documentation]    Check ppsk network client connectivity with group user and cloud passwd db location

    [Tags]             development       tccs_7678

    ${USER_GROUP_CREATE}=           Create User Group   ${BULK_CLOUD_USER_GROUP}   user_group_profile=&{USER_GROUP_PROFILE_CLOUD_BULK}
    should be equal as strings     '${USER_GROUP_CREATE}'     '1'

    ${NW_STATUS}=                   Create Network Policy   ${BULK_CLOUD_NW_POLICY}   ${WIRELESS_PPSK_NW_CLOUD_BULK}
    should be equal as strings     '${NW_STATUS}'           '1'

    ${DELTA_UPDATE}=                Update Network Policy To Ap    policy_name=${BULK_CLOUD_NW_POLICY}    ap_serial=${device1.serial}
    should be equal as strings     '${DELTA_UPDATE}'           '1'
    sleep                           ${config_push_wait}

    ${URL_TITLE}=                    Check Internet Connectivity    ${mu1.ip}
    should not be equal as strings   '${URL_TITLE}'               '${PAGE_TITLE}'

    ${CREDENTIALS}=                 Get Login Credential From Attachments    ${MAIL_ID1}     ${MAIL_ID1_PASS}
    set global variable             ${CREDENTIALS}

    Connect Ppsk Wireless Network   ${BULK_CLOUD_NW_SSID}     ${CREDENTIALS['user_1']['Access Key']}
    ${LOGIN_TIME}=                  Get Current Date Time
    ${LOGIN_UTC_TIME}=              Get Utc Time              %Y-%m-%d %H:%M
    set global variable             ${LOGIN_TIME}
    set global variable             ${LOGIN_UTC_TIME}
    sleep                           ${client_connect_wait}

    WI-FI INTERFACE IP ADDRESS CHECK

    ${URL_TITLE}=                   Check Internet Connectivity     ${mu1.ip}
    Run keyword if  "${URL_TITLE}" != "${PAGE_TITLE}"  Re Connect To PPSK Network  ${BULK_CLOUD_NW_SSID}  ${CREDENTIALS['user_1']['Access Key']}

    [Teardown]    run keywords    Test Case Level Cleanup
    ...           AND             mu1.delete_wlan_profile   ${BULK_CLOUD_NW_SSID}

TCCS-7691: Local DB PPSK Network Client Connectivity With Bulk Users Group
    [Documentation]    Check ppsk network client connectivity with group user and local passwd db location

    [Tags]             development       tccs_7691

    ${USER_GROUP_CREATE}=           Create User Group        ${BULK_LOCAL_USER_GROUP}  user_group_profile=&{USER_GROUP_PROFILE_LOCAL_BULK}
    should be equal as strings     '${USER_GROUP_CREATE}'    '1'

    ${NW_STATUS}=                   Create Network Policy    ${BULK_LOCAL_NW_POLICY}   ${WIRELESS_PPSK_NW_LOCAL_BULK}
    should be equal as strings     '${NW_STATUS}'      '1'

    ${DELTA_UPDATE}=                Update Network Policy To Ap    policy_name=${BULK_LOCAL_NW_POLICY}    ap_serial=${device1.serial}
    should be equal as strings     '${DELTA_UPDATE}'           '1'
    sleep                           ${config_push_wait}

    ${URL_TITLE}=                   Check Internet Connectivity    ${mu1.ip}
    should not be equal as strings   '${URL_TITLE}'               '${PAGE_TITLE}'

    ${CREDENTIALS}=                 Get Login Credential From Attachments    ${MAIL_ID1}     ${MAIL_ID1_PASS}

    Connect Ppsk Wireless Network   ${BULK_LOCAL_NW_SSID}     ${CREDENTIALS['user2_1']['Access Key']}
    sleep                           ${client_connect_wait}

    Wi-Fi Interface IP Address Check

    ${URL_TITLE}=                   Check Internet Connectivity     ${mu1.ip}
    Run keyword if  "${URL_TITLE}" != "${PAGE_TITLE}"  Re Connect To PPSK Network  ${BULK_LOCAL_NW_SSID}  ${CREDENTIALS['user2_1']['Access Key']}

    [Teardown]   run keywords       Test Case Level Cleanup
    ...          AND                mu1.delete_wlan_profile   ${BULK_LOCAL_NW_SSID}


