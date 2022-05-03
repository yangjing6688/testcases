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
${BULK_CLOUD_NW_POLICY}             AUTO_CLOUD_BULK_NW
${BULK_CLOUD_NW_SSID}               AUTO_CLOUD_BULK_SSID
${BULK_CLOUD_USER_GROUP}            AUTO_CLOUD_BULK_GRP

${BULK_LOCAL_NW_POLICY}             AUTO_LOCAL_BULK_NW
${BULK_LOCAL_NW_SSID}               AUTO_LOCAL_BULK_SSID
${BULK_LOCAL_USER_GROUP}            AUTO_LOCAL_BULK_GRP

${SINGLE_CLOUD_NW_POLICY}           AUTO_CLOUD_SNGLE_NW
${SINGLE_CLOUD_NW_SSID}             AUTO_CLOUD_SNG_SSID
${SINGLE_CLOUD_USER_GROUP}          AUTO_CLOUD_SNG_GRP

${SINGLE_LOCAL_NW_POLICY}           AUTO_LOCAL_SNGL_NW
${SINGLE_LOCAL_NW_SSID}             AUTO_LOCAL_SNGL_SSID
${SINGLE_LOCAL_USER_GROUP}          AUTO_LOCAL_SNGL_GRP

${CLOUD_CWP_NW_POLICY}              AUTO_PPSK_CWP_NW
${CLOUD_CWP_NW_SSID}                AUTO_PPSK_CWP_SSID
${CLOUD_CWP_OPEN_NW_SSID}           OPEN_CWP_SELF_REG
${CLOUD_CWP_USER_GROUP}             AUTO_CWP_CLOUD_GRP
${SELF_REG_RETURN_PPSK_CWP}         SELF_REG_RET_PPSK

${SINGLE_CLOUD_NW_POLICY1}          AUTO_PPSK_CLOUD_SNGLE_NW1
${SINGLE_CLOUD_NW_SSID1}            AUTO_PPSK_CLOUD_SNGL_SSID1
${SINGLE_CLOUD_USER_GROUP1}         AUTO_PPSK_CLOUD_SNGL_GRP1
${WRONG_PPSK_PASSWORD}              abcdxyzss

${CLIENT_PER_PPSK_POLICY}          AUTO_CLIENT_PER_PPSK_NW
${CLIENT_PER_PPSK_SSID}            AUTO_CLIENT_PER_PPSK_SSID
${CLIENT_PER_PPSK_GRP}             AUTO_CLIENT_PER_PPSK_GRP

${LOCAL_DB_PPSK_NW1}               LOCAL_DB_NW1
${LOCAL_DB_PPSK_SSID1}             LOCAL_DB_SSID1
${LOCAL_DB_PPSK_GROUP}             LOCAL_DB_GRP1

&{self_reg_user1_info}              email=${MAIL_ID1}    ccode=91   ph_num=8971766359    visitor_email=${MAIL_ID2}

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

Resource    Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/test_email_ids.robot
Resource    Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/private_pre_shared_key_config.robot

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Library	    Remote 	http://${mu1.ip}:${mu1.port}   WITH NAME   mu1

Force Tags   testbed_1_node

Suite Setup      Pre Condition

*** Keywords ***
Pre Condition
    [Documentation]   AP Should be onboarded  and it is online

    ${result}=                      Login User                 ${tenant_username}     ${tenant_password}
    ${AP_STATUS}=                   Get AP Status              ap_mac=${ap1.mac}
    Should Be Equal As Strings     '${AP_STATUS}'             'green'
    Create Network Policy           OPEN_AUTO                  &{CONFIG_PUSH_OPEN_NW_01}
    Update Network Policy To Ap     policy_name=OPEN_AUTO      ap_serial=${ap1.serial}

    ${DELETE_STATUS}=              delete network polices      ${BULK_CLOUD_NW_POLICY}     ${BULK_LOCAL_NW_POLICY}    ${SINGLE_CLOUD_NW_POLICY}
    ...                            ${SINGLE_LOCAL_NW_POLICY}   ${CLOUD_CWP_NW_POLICY}     ${SINGLE_CLOUD_NW_POLICY1}
    ...                            ${CLIENT_PER_PPSK_POLICY}   ${LOCAL_DB_PPSK_NW1}
    should be equal as strings    '${DELETE_STATUS}'           '1'     ppsk network policy assigned to other AP,disassociate it or issue with deleting policy

    ${SSID_DLT_STATUS}=            delete ssids                ${BULK_CLOUD_NW_SSID}       ${BULK_LOCAL_NW_SSID}      ${SINGLE_CLOUD_NW_SSID}
    ...                            ${SINGLE_LOCAL_NW_SSID}     ${CLOUD_CWP_OPEN_NW_SSID}  ${SINGLE_CLOUD_NW_SSID1}
    ...                            ${CLIENT_PER_PPSK_SSID}     ${LOCAL_DB_PPSK_SSID1}
    should be equal as strings     '1'                        '${SSID_DLT_STATUS}'       Issue with deleting the SSID's

    delete captive web portal      ${SELF_REG_RETURN_PPSK_CWP}
    delete ssid                    ${CLOUD_CWP_NW_SSID}
    delete user groups             ${BULK_CLOUD_USER_GROUP}    ${BULK_LOCAL_USER_GROUP}   ${SINGLE_CLOUD_USER_GROUP}
    ...                            ${SINGLE_LOCAL_USER_GROUP}  ${CLOUD_CWP_USER_GROUP}    ${SINGLE_CLOUD_USER_GROUP1}
    ...                            ${CLIENT_PER_PPSK_GRP}      ${LOCAL_DB_PPSK_GROUP}

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
    should be equal as strings     '${LOGIN_STATUS}'     '1'

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
    should be equal as strings     '${LOGIN_STATUS}'        '1'

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

Test Suite Clean Up
    [Documentation]    delete created network policies, usergroups, radius server

    [Tags]             production       cleanup

    ${result}=    Login User       ${tenant_username}        ${tenant_password}
    Update Network Policy To Ap     policy_name=OPEN_AUTO      ap_serial=${ap1.serial}

    ${DELETE_STATUS}=              delete network polices      ${BULK_CLOUD_NW_POLICY}     ${BULK_LOCAL_NW_POLICY}    ${SINGLE_CLOUD_NW_POLICY}
    ...                            ${SINGLE_LOCAL_NW_POLICY}   ${CLOUD_CWP_NW_POLICY}     ${SINGLE_CLOUD_NW_POLICY1}
    ...                            ${CLIENT_PER_PPSK_POLICY}   ${LOCAL_DB_PPSK_NW1}
    should be equal as strings    '${DELETE_STATUS}'           '1'     ppsk network policy assigned to other AP,disassociate it or issue with deleting policy

    delete ssids                   ${BULK_CLOUD_NW_SSID}       ${BULK_LOCAL_NW_SSID}      ${SINGLE_CLOUD_NW_SSID}
    ...                            ${SINGLE_LOCAL_NW_SSID}     ${CLOUD_CWP_OPEN_NW_SSID}  ${SINGLE_CLOUD_NW_SSID1}
    ...                            ${CLIENT_PER_PPSK_SSID}     ${LOCAL_DB_PPSK_SSID1}

    delete captive web portal      ${SELF_REG_RETURN_PPSK_CWP}
    delete ssid                    ${CLOUD_CWP_NW_SSID}
    delete user groups             ${BULK_CLOUD_USER_GROUP}    ${BULK_LOCAL_USER_GROUP}   ${SINGLE_CLOUD_USER_GROUP}
    ...                            ${SINGLE_LOCAL_USER_GROUP}  ${CLOUD_CWP_USER_GROUP}    ${SINGLE_CLOUD_USER_GROUP1}
    ...                            ${CLIENT_PER_PPSK_GRP}      ${LOCAL_DB_PPSK_GROUP}
     Navigate To Devices
     Delete Device                 device_serial=${ap1.serial}

    [Teardown]   run keywords      logout user
    ...                            quit browser
