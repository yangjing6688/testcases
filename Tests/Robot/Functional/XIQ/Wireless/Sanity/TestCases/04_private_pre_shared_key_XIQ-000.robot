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

*** Settings ***
Library     Collections

Library     common/GmailHandler.py
Library     common/Utils.py
Library     common/LoadBrowser.py
Library     common/Cli.py
Library     common/TestFlow.py

Library     xiq/flows/common/Login.py
Library     xiq/flows/common/MuCaptivePortal.py

Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/DeviceCliAccess.py
Library     xiq/flows/manage/ClientMonitor.py
Library     xiq/flows/manage/Client.py
Library     xiq/flows/common/Navigator.py

Library     xiq/flows/configure/UserGroups.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/CommonObjects.py

Library     xiq/flows/mlinsights/MLInsightClient360.py
Library     xiq/flows/globalsettings/GlobalSetting.py

# Moved to python Resources file for randomizing 2022-08-31
#Resource    Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/test_email_ids.robot
#Resource    Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/private_pre_shared_key_config.robot

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml
Variables    Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/test_email_ids.py
Variables    Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/private_pre_shared_key_config.py

Library	    Remote 	http://${mu1.ip}:${mu1.port}   WITH NAME   mu1

Force Tags   testbed_1_node

Suite Setup      Pre Condition
Suite Teardown   Test Suite Clean Up

*** Keywords ***
Pre Condition
    [Documentation]   AP Should be onboarded  and it is online

    ${LOGIN_STATUS}=                Login User                 ${tenant_username}     ${tenant_password}    check_warning_msg=True
    should be equal as integers     ${LOGIN_STATUS}               1

    ${DEVICE_STATUS}=               Get Device Status       device_serial=${ap1.serial}
    Should contain any              ${DEVICE_STATUS}        green     config audit mismatch

    ${CREATE_NW_POLICY_STATUS}=     Create Network Policy          ${OPEN_POLICY}            &{CONFIG_PUSH_OPEN_NW_01}
    should be equal as integers     ${CREATE_NW_POLICY_STATUS}               1

    ${UPDATE_NW_POLICY_STATUS}=     Update Network Policy To Ap If Needed   policy_name=${OPEN_POLICY}   ap_serial=${ap1.serial} 
    should be equal as integers     ${UPDATE_NW_POLICY_STATUS}               1

    ${DELETE_STATUS}=               Delete network polices      ${BULK_CLOUD_NW_POLICY}     ${BULK_LOCAL_NW_POLICY}
    should be equal as strings     '${DELETE_STATUS}'           '1'     ppsk network policy assigned to other AP,disassociate it or issue with deleting policy

    ${SSID_DLT_STATUS}=             Delete ssids                ${BULK_CLOUD_NW_SSID}       ${BULK_LOCAL_NW_SSID}
    should be equal as strings      '1'                        '${SSID_DLT_STATUS}'       Issue with deleting the SSID's

    ${DELETE_CWP_STATUS}=           Delete captive web portal      ${SELF_REG_RETURN_PPSK_CWP}
    should be equal as integers     ${DELETE_CWP_STATUS}               1

    ${DELETE_UGS}=                  Delete user groups              ${BULK_CLOUD_USER_GROUP}    ${BULK_LOCAL_USER_GROUP}
    should be equal as integers     ${DELETE_UGS}               1

    [Teardown]   run keywords      mu1.disconnect_wifi
    ...                            logout user
    ...                            quit browser

Test Suite Clean Up
    [Documentation]    delete created network policies, usergroups, radius server

    [Tags]             production       cleanup

    ${LOGIN_STATUS}=    Login User       ${tenant_username}        ${tenant_password}
    should be equal as integers             ${LOGIN_STATUS}               1

    Navigate To Devices

    ${DELETE_DEVICE_STATUS}=        Delete Device       device_serial=${ap1.serial}
    should be equal as integers         ${DELETE_DEVICE_STATUS}               1
    # delete policy is showing 'in use' error. Even though device was successfully deleted. Table cleanup assumed.
    sleep                          5

    ${DELETE_STATUS}=              delete network polices    ${BULK_CLOUD_NW_POLICY}  ${BULK_LOCAL_NW_POLICY}   ${OPEN_POLICY}
    should be equal as strings    '${DELETE_STATUS}'           '1'     ppsk network policy assigned to other AP,disassociate it or issue with deleting policy

    ${SSID_DLT_STATUS}=            Delete ssids              ${BULK_CLOUD_NW_SSID}       ${BULK_LOCAL_NW_SSID}      ${OPEN_SSID}
    should be equal as strings      '1'                        '${SSID_DLT_STATUS}'       Issue with deleting the SSID's

    ${DELETE_CWP_STATUS}=           Delete captive web portal      ${SELF_REG_RETURN_PPSK_CWP}
    should be equal as integers     ${DELETE_CWP_STATUS}               1

    ${DELETE_UGS}=                  Delete user groups              ${BULK_CLOUD_USER_GROUP}    ${BULK_LOCAL_USER_GROUP}
    should be equal as integers     ${DELETE_UGS}               1

    [Teardown]   run keywords      logout user
    ...                            quit browser

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
     Logout User
     Quit Browser
     mu1.disconnect_wifi

*** Test Cases ***
TCCS-7678: Cloud DB PPSK Network Client Connectivity With Bulk Users Group
    [Documentation]    Check ppsk network client connectivity with group user and cloud passwd db location

    [Tags]             production       tccs_7678

    ${LOGIN_STATUS}=                Login User           ${tenant_username}     ${tenant_password}
     should be equal as integers             ${LOGIN_STATUS}               1

    ${USER_GROUP_CREATE}=           Create User Group   ${BULK_CLOUD_USER_GROUP}   user_group_profile=&{USER_GROUP_PROFILE_CLOUD_BULK}
    should be equal as strings     '${USER_GROUP_CREATE}'     '1'

    ${NW_STATUS}=                   Create Network Policy   ${BULK_CLOUD_NW_POLICY}   &{WIRELESS_PPSK_NW_CLOUD_BULK}
    should be equal as strings     '${NW_STATUS}'           '1'

    ${DELTA_UPDATE}=                Update Network Policy To Ap    policy_name=${BULK_CLOUD_NW_POLICY}    ap_serial=${ap1.serial}
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

    [Tags]             production       tccs_7691

    ${LOGIN_STATUS}=                Login User              ${tenant_username}     ${tenant_password}
     should be equal as integers             ${LOGIN_STATUS}               1

    ${USER_GROUP_CREATE}=           Create User Group        ${BULK_LOCAL_USER_GROUP}  user_group_profile=&{USER_GROUP_PROFILE_LOCAL_BULK}
    should be equal as strings     '${USER_GROUP_CREATE}'    '1'

    ${NW_STATUS}=                   Create Network Policy    ${BULK_LOCAL_NW_POLICY}   &{WIRELESS_PPSK_NW_LOCAL_BULK}
    should be equal as strings     '${NW_STATUS}'      '1'

    ${DELTA_UPDATE}=                Update Network Policy To Ap    policy_name=${BULK_LOCAL_NW_POLICY}    ap_serial=${ap1.serial}
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


