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

Library     xiq/flows/configure/UserGroups.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/CommonObjects.py

Library     xiq/flows/mlinsights/MLInsightClient360.py
Library     xiq/flows/globalsettings/GlobalSetting.py

Resource    test_email_ids.robot
Resource    private_pre_shared_key_config.robot

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Library	    Remote 	http://${mu1.ip}:${mu1.port}   WITH NAME   mu1
Library	    Remote 	http://${mu2.ip}:${mu2.port}   WITH NAME   mu2

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
Test1: Cloud DB PPSK Network Client Connectivity With Bulk Users Group
    [Documentation]    Check ppsk network client connectivity with group user and cloud passwd db location
    [Tags]             regression   ppsk    cloud-db    bulk-user    P1  Test1   Test2   Test3   Test4  production

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

Test2: Check Authentication Logs For PPSK CLoud DB Network
    [Documentation]    check authentication logs
    [Tags]             regression   aut-logs    cloud-db    bulk-user     P2  Test2

    depends on        Test1
    ${LOGIN_STATUS}=                Login User           ${tenant_username}     ${tenant_password}
    should be equal as strings     '${LOGIN_STATUS}'     '1'
    ${AUTH_LOGS}=                   Get Authentication Logs Details       ${LOGIN_TIME[:-2:]}     ${mu1.wifi_mac}

    # Logs Verification
    should be equal as strings    '${AUTH_LOGS}[reply]'              'auth-logs-accept'
    should be equal as strings    '${AUTH_LOGS}[userName]'           'user_1'
    should be equal as strings    '${AUTH_LOGS}[ssid]'               '${BULK_CLOUD_NW_SSID}'
    should be equal as strings    '${AUTH_LOGS}[authType]'           'Private PSK'
    should be equal as strings    '${AUTH_LOGS}[callingStationId]'   '${mu1.wifi_mac}'
    should be equal as strings    '${AUTH_LOGS}[rejectReason]'        ''

    ${TIME_STAMP}=                 get_from_dictionary        ${AUTH_LOGS}               authdate
    should contain                 ${TIME_STAMP}              ${LOGIN_TIME[:-2:]}
    ${TIME_DELTA}=                 Get Utc Time Difference    ${TIME_STAMP[:-3:]}        ${LOGIN_TIME}
    should be true                 ${TIME_DELTA} <= 60.0

    # check the config push details
    ${CONFIG_OUTPUT}               Send Cmd On Device Advanced Cli     device_serial=${ap1.serial}    cmd=show running-config
    Should Contain                 ${CONFIG_OUTPUT}   security-object ${BULK_CLOUD_NW_SSID} security aaa radius-server idm
    Should Contain                 ${CONFIG_OUTPUT}   security-object ${BULK_CLOUD_NW_SSID} security protocol-suite wpa2-aes-psk hex-key
    Should Contain                 ${CONFIG_OUTPUT}   security-object ${BULK_CLOUD_NW_SSID} security private-psk
    Should Contain                 ${CONFIG_OUTPUT}   ssid ${BULK_CLOUD_NW_SSID} security mac-filter ${BULK_CLOUD_NW_SSID}
    Should Contain                 ${CONFIG_OUTPUT}   interface wifi0 ssid ${BULK_CLOUD_NW_SSID}
    Should Contain                 ${CONFIG_OUTPUT}   interface wifi1 ssid ${BULK_CLOUD_NW_SSID}

    [Teardown]   run keywords      logout user
    ...                            quit browser

Test3: Check Authentication Logs For PPSK CLoud DB Network With Wrong Password Client Connect
    [Documentation]    validating authentication logs, connecting client to ppsk network with wrong password
    [Tags]             regression   aut-logs   P2   Test3

    depends on        Test1

    ${CONNECT_STATUS}=   mu1.connect_wpa2_ppsk_network     ${BULK_CLOUD_NW_SSID}      ${WRONG_PPSK_PASSWORD}    retry_count=1
    should be equal as strings       '${CONNECT_STATUS}'    '-1'

    ${LOGIN_TIME}=                  Get Current Date Time
    ${LOGIN_UTC_TIME}=              Get Utc Time              %Y-%m-%d %H:%M
    sleep                           ${client_connect_wait}

    ${LOGIN_STATUS}=                Login User           ${tenant_username}     ${tenant_password}
    should be equal as strings     '${LOGIN_STATUS}'     '1'
    ${AUTH_LOGS}=                   Get Authentication Logs Details       ${LOGIN_TIME[:-2:]}     ${mu1.wifi_mac}

    # Logs Verification
    should be equal as strings    '${AUTH_LOGS}[reply]'              'auth-logs-reject'
    should be equal as strings    '${AUTH_LOGS}[userName]'           ''
    should be equal as strings    '${AUTH_LOGS}[ssid]'               '${BULK_CLOUD_NW_SSID}'
    should be equal as strings    '${AUTH_LOGS}[authType]'           'Private PSK'
    should be equal as strings    '${AUTH_LOGS}[callingStationId]'   '${mu1.wifi_mac}'
    should be equal as strings    '${AUTH_LOGS}[rejectReason]'        'Incorrect-Password'

    ${TIME_STAMP}=                 get_from_dictionary        ${AUTH_LOGS}       authdate
    should contain                 ${TIME_STAMP}              ${LOGIN_TIME[:-2:]}
    ${TIME_DELTA}=                 Get Utc Time Difference    ${TIME_STAMP[:-3:]}        ${LOGIN_TIME}
    should be true                 ${TIME_DELTA} <= 60.0

    [Teardown]     run keywords    Test Case Level Cleanup
    ...            AND             mu1.delete_wlan_profile   ${BULK_CLOUD_NW_SSID}

Test4: Check Accounting Logs For PPSK CLoud DB Network With Valid Password
    [Documentation]    check accounting logs
    [Tags]             regression   accounting-logs    P3  Test4

    depends on        Test1
    ${CONNECT_STATUS}=              mu1.connect_wpa2_ppsk_network     ${BULK_CLOUD_NW_SSID}      ${CREDENTIALS['user_1']['Access Key']}    retry_count=1
    should be equal as strings     '${CONNECT_STATUS}'    '1'
    ${CLIENT_CONNECT_TIME}=         Get Current Date Time

    ${LOGIN_STATUS}=                Login User           ${tenant_username}     ${tenant_password}
    should be equal as strings     '${LOGIN_STATUS}'     '1'

    # Manage Client Verification
    ${CLIENT_DETAILS}=              Get Real Time Client Details            ${mu1.wifi_mac}
    should be equal as strings     '${CLIENT_DETAILS}[connectionType]'     'WIRELESS'
    should be equal as strings     '${CLIENT_DETAILS}[connectionStatus]'   'CONNECTED'
    should be equal as strings     '${CLIENT_DETAILS}[macAddress]'         '${mu1.wifi_mac}'
    should be equal as strings     '${CLIENT_DETAILS}[ssidOrPort]'         '${BULK_CLOUD_NW_SSID}'

    ${CLIENT360_DETAILS}=           Get Real Time Client360 Details            ${mu1.wifi_mac}
    should be equal as strings     '${CLIENT360_DETAILS}[connectionType]'     'WIRELESS'
    should be equal as strings     '${CLIENT360_DETAILS}[connectionStatus]'   'CONNECTED'
    should be equal as strings     '${CLIENT360_DETAILS}[macAddress]'         '${mu1.wifi_mac}'
    should be equal as strings     '${CLIENT360_DETAILS}[ssidOrPort]'         '${BULK_CLOUD_NW_SSID}'

    sleep                           5 minutes
    mu1.disconnect_wifi
    ${CLIENT_DISCONNECT_TIME}=      Get Current Date Time
    Sleep                           ${acct_logs_duration_wait}

    ${ACCOUNT_LOGS}=                Get Accounting Logs Details           ${CLIENT_DISCONNECT_TIME}     user_1
    should be equal as strings     '${ACCOUNT_LOGS}[ssid]'               '${BULK_CLOUD_NW_SSID}'
    should be equal as strings     '${ACCOUNT_LOGS}[callingStationId]'   '${mu1.wifi_mac}'
    should contain                 ${ACCOUNT_LOGS}[acctStartTime]         ${CLIENT_CONNECT_TIME}
    should contain                 ${ACCOUNT_LOGS}[acctStopTime]          ${CLIENT_DISCONNECT_TIME}

    [Teardown]    run keywords     Test Case Level Cleanup
    ...           AND              mu1.delete_wlan_profile   ${BULK_CLOUD_NW_SSID}


Test5: Local DB PPSK Network Client Connectivity With Bulk Users Group
    [Documentation]    Check ppsk network client connectivity with group user and local passwd db location
    [Tags]             regression   ppsk   local-db   bulk-user   P1  Test5    production

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

Test6: Cloud DB PPSK Network Client Connectivity With Single User Group
    [Documentation]    Check ppsk network client connectivity with single user and cloud passwd db location
    [Tags]             regression    ppsk   cloud-db  single-user   P1   Test6

    ${LOGIN_STATUS}=                  Login User              ${tenant_username}     ${tenant_password}
    should be equal as strings       '${LOGIN_STATUS}'        '1'

    ${USER_GROUP_CREATE}=             Create User Group        ${SINGLE_CLOUD_USER_GROUP}   user_group_profile=&{USER_GROUP_PROFILE_CLOUD_SINGLE}
    should be equal as strings       '${USER_GROUP_CREATE}'   '1'

    ${NW_STATUS}=                     Create Network Policy    ${SINGLE_CLOUD_NW_POLICY}   &{WIRELESS_PPSK_NW_CLOUD_SINGLE}
    should be equal as strings       '${NW_STATUS}'   '1'


    ${DELTA_UPDATE}=                  Update Network Policy To Ap    policy_name=${SINGLE_CLOUD_NW_POLICY}    ap_serial=${ap1.serial}
    should be equal as strings       '${DELTA_UPDATE}'   '1'
    sleep                             ${config_push_wait}

    ${URL_TITLE}=                     Check Internet Connectivity    ${mu1.ip}
    should not be equal as strings   '${URL_TITLE}'               '${PAGE_TITLE}'

    ${ACCESS_CODE}    ${USERNAME} =   Get Login Credential        ${MAIL_ID1}     ${MAIL_ID1_PASS}

    Connect Ppsk Wireless Network     ${SINGLE_CLOUD_NW_SSID}     ${ACCESS_CODE}
    sleep                             ${client_connect_wait}

    Wi-Fi Interface IP Address Check

    ${URL_TITLE}=                   Check Internet Connectivity     ${mu1.ip}
    Run keyword if  "${URL_TITLE}" != "${PAGE_TITLE}"  Re Connect To PPSK Network  ${SINGLE_CLOUD_NW_SSID}  ${ACCESS_CODE}

    [Teardown]   run keywords       Test Case Level Cleanup
    ...           AND               mu1.delete_wlan_profile   ${SINGLE_CLOUD_NW_SSID}

Test7: Local DB PPSK Network Client Connectivity With Single User Group
    [Documentation]    Check ppsk network client connectivity with single user and Local passwd db location
    [Tags]             regression   ppsk   local-db   single-user   P1  Test7

    ${LOGIN_STATUS}=                  Login User              ${tenant_username}     ${tenant_password}
    should be equal as strings       '${LOGIN_STATUS}'        '1'

    ${USER_GROUP_CREATE}=             Create User Group       ${SINGLE_LOCAL_USER_GROUP}   user_group_profile=&{USER_GROUP_PROFILE_LOCAL_SINGLE}
    should be equal as strings       '${USER_GROUP_CREATE}'   '1'

    ${NW_STATUS}=                     Create Network Policy   ${SINGLE_LOCAL_NW_POLICY}   &{WIRELESS_PPSK_NW_LOCAL_SINGLE}
    should be equal as strings       '${NW_STATUS}'   '1'

    ${DELTA_UPDATE}=                  Update Network Policy To Ap    policy_name=${SINGLE_LOCAL_NW_POLICY}    ap_serial=${ap1.serial}
    should be equal as strings       '${DELTA_UPDATE}'   '1'
    sleep                             ${config_push_wait}

    ${URL_TITLE}=                     Check Internet Connectivity    ${mu1.ip}
    should not be equal as strings   '${URL_TITLE}'               '${PAGE_TITLE}'

    Connect Ppsk Wireless Network     ${SINGLE_LOCAL_NW_SSID}     extremextreme
    sleep                             ${client_connect_wait}

    Wi-Fi Interface IP Address Check

    ${URL_TITLE}=                   Check Internet Connectivity     ${mu1.ip}
    Run keyword if  "${URL_TITLE}" != "${PAGE_TITLE}"  Re Connect To PPSK Network  ${SINGLE_LOCAL_NW_SSID}     extremextreme

    [Teardown]     run keywords    Test Case Level Cleanup
    ...             AND            mu1.delete_wlan_profile   ${SINGLE_LOCAL_NW_SSID}

Test8: CWP Passing of PPSK and Client Connectivity With Employee Approval
    [Documentation]  User registration with open network, and network access with ppsk network after employye aproval
    [Tags]          regression   ppsk  cwp-passing   employee-approval   P1  Test8   Test9

    ${LOGIN_STATUS}=                 Login User              ${tenant_username}     ${tenant_password}
    should be equal as strings      '${LOGIN_STATUS}'        '1'

    ${USER_GROUP_CREATE}=            Create User Group       group_name=${CLOUD_CWP_USER_GROUP}   user_group_profile=&{USER_GROUP_PROFILE_CWP}
    should be equal as strings      '${USER_GROUP_CREATE}'   '1'

    ${NW_STATUS}=                    Create Network Policy   ${CLOUD_CWP_NW_POLICY}   &{WIRELESS_OPEN_PPSK_NW_CLOUD_CWP}
    should be equal as strings      '${NW_STATUS}'   '1'

    ${ADD_WR_NW}=                    Add Wireless Nw To Network Policy    ${CLOUD_CWP_NW_POLICY}    &{OPEN_CWP_NW1}
    should be equal as strings      '${ADD_WR_NW}'   '1'

    ${DELTA_UPDATE}=                 Update Network Policy To Ap    policy_name=${CLOUD_CWP_NW_POLICY}    ap_serial=${ap1.serial}
    should be equal as strings      '${DELTA_UPDATE}'   '1'
    sleep                            ${config_push_wait}

    ${CONNECT_STATUS}=               mu1.connect_open_network         ${CLOUD_CWP_OPEN_NW_SSID}
    should be equal as strings      '${CONNECT_STATUS}'    '1'
    sleep                            ${client_connect_wait}

    ${TITLE}=                        Open Cp Browser    ${mu1.ip}
    Run keyword if  "${TITLE}" != "Secure Internet Portal"   Re Connect To Open Network    OPEN_CWP_SELF_REG

    ${first_name}=                   get random string   length=5
    ${last_name}=                    get random string   length=5

    ${REG_STATUS}=                   User Self Registration    first_name=${first_name}    last_name=${last_name}   &{self_reg_user1_info}
    should be equal as strings      '${REG_STATUS}'   '1'
    sleep                            ${self_registration_wait}

    ${PASSCODE}=                     Get Ppsk Passcode User Registration
    ${url}=                          Get User Approval Url      ${MAIL_ID2}     ${MAIL_ID2_PASS}

    close cp browser
    ${CONNECT_STATUS}=               mu1.connect_wpa2_ppsk_network    ${CLOUD_CWP_NW_SSID}         ${PASSCODE}   retry_count=1
    should not be equal as strings   '${CONNECT_STATUS}'    '1'

    ${URL_TITLE}=                    Check Internet Connectivity    ${mu1.ip}
    should not be equal as strings   '${URL_TITLE}'               '${PAGE_TITLE}'

    # Approve email
    Load Browser                     ${url}                       ${WINDOWS10}
    sleep                            ${self_registration_wait}
    Quite Approve Browser

    Connect Ppsk Wireless Network    ${CLOUD_CWP_NW_SSID}         ${PASSCODE}
    sleep                            ${client_connect_wait}

    ${URL_TITLE}=                   Check Internet Connectivity     ${mu1.ip}
    Run keyword if  "${URL_TITLE}" != "${PAGE_TITLE}"  Re Connect To PPSK Network  ${CLOUD_CWP_NW_SSID}  ${PASSCODE}

    [Teardown]  run keywords     Test Case Level Cleanup
    ...         AND              mu1.delete_wlan_profile   ${CLOUD_CWP_NW_SSID}
    ...         AND              mu1.delete_wlan_profile   ${CLOUD_CWP_OPEN_NW_SSID}

Test9: CWP passing of PPSK and Client Connectivity Without Employee Approval
    [Documentation]    User registration with open network, and network access with ppsk network without employye aproval
    [Tags]             regression    ppsk   cwp-passing   P1   Test9

    depends on                       Test8
    ${LOGIN_STATUS}=                 Login User          ${tenant_username}     ${tenant_password}
    should be equal as strings      '${LOGIN_STATUS}'    '1'

    ${DIS_CWP_EMAIL_APPROVAL}=       Disable Cwp Employee Approval    ${SELF_REG_RETURN_PPSK_CWP}
    should be equal as strings      '${DIS_CWP_EMAIL_APPROVAL}'   '1'

    ${DELTA_UPDATE}=                 Update Network Policy To Ap    policy_name=${CLOUD_CWP_NW_POLICY}    ap_serial=${ap1.serial}
    should be equal as strings      '${DELTA_UPDATE}'   '1'
    sleep                            ${config_push_wait}

    ${CONNECT_STATUS}=               mu1.connect_open_network         ${CLOUD_CWP_OPEN_NW_SSID}
    should be equal as strings      '${CONNECT_STATUS}'    '1'
    sleep                            ${client_connect_wait}

    ${TITLE}=                        Open Cp Browser    ${mu1.ip}
    Run keyword if  "${TITLE}" != "Secure Internet Portal"   Re Connect To Open Network    OPEN_CWP_SELF_REG

    ${first_name}=                   get random string   length=5
    ${last_name}=                    get random string   length=5

    ${REG_STATUS}=                   User Self Registration    first_name=${first_name}    last_name=${last_name}   &{self_reg_user1_info}
    should be equal as strings      '${REG_STATUS}'   '1'

    ${PASSCODE}=                     Get Ppsk Passcode User Registration
    sleep                            ${cp_page_open_wait}
    close cp browser

    ${URL_TITLE}=                    Check Internet Connectivity    ${mu1.ip}
    should not be equal as strings   '${URL_TITLE}'               '${PAGE_TITLE}'

    Connect Ppsk Wireless Network    ${CLOUD_CWP_NW_SSID}     ${PASSCODE}
    sleep                            ${client_connect_wait}

    ${URL_TITLE}=                   Check Internet Connectivity     ${mu1.ip}
    Run keyword if  "${URL_TITLE}" != "${PAGE_TITLE}"  Re Connect To PPSK Network   ${CLOUD_CWP_NW_SSID}     ${PASSCODE}

    [Teardown]   run keywords       Test Case Level Cleanup
    ...           AND               mu1.delete_wlan_profile     ${CLOUD_CWP_NW_SSID}
    ...           AND               mu1.delete_wlan_profile     ${CLOUD_CWP_OPEN_NW_SSID}

Test10: Validate Client Per PPSK With Cloud DB Location
    [Documentation]   Set the client per ppsk field to 1 and connect the 2 clients for the same SSID.
    ...               one client should connect and other client should not connect with using same password
    [Tags]            regression    ppsk    P1   Test10

    ${LOGIN_STATUS}=                 Login User          ${tenant_username}     ${tenant_password}
    should be equal as strings      '${LOGIN_STATUS}'    '1'

    ${NW_STATUS}=                    Create Network Policy   ${CLIENT_PER_PPSK_POLICY}   &{WIRELESS_CLIENT_PER_PPSK}
    should be equal as strings      '${NW_STATUS}'   '1'

    ${DELTA_UPDATE}=                 Update Network Policy To Ap    policy_name=${CLIENT_PER_PPSK_POLICY}    ap_serial=${ap1.serial}
    should be equal as strings      '${DELTA_UPDATE}'   '1'
    sleep                            ${config_push_wait}

    ${CREDENTIALS}=                  Get Login Credential From Attachments    ${MAIL_ID1}     ${MAIL_ID1_PASS}

    # Check connectivity of Client1
    Connect Ppsk Wireless Network     ${CLIENT_PER_PPSK_SSID}     ${CREDENTIALS['user100_1']['Access Key']}
    sleep                             ${client_connect_wait}

    ${URL_TITLE}=                     Check Internet Connectivity     ${mu1.ip}
    Run keyword if  "${URL_TITLE}" != "${PAGE_TITLE}"  Re Connect To PPSK Network  ${CLIENT_PER_PPSK_SSID}   ${CREDENTIALS['user100_1']['Access Key']}

    # Check Connectivity of Client2
    mu1.connect_wpa2_ppsk_network     ${CLIENT_PER_PPSK_SSID}     ${CREDENTIALS['user100_1']['Access Key']}
    sleep                             ${client_connect_wait}

    ${URL_TITLE}=                     Check Internet Connectivity     ${mu2.ip}
    should not be equal as strings   '${URL_TITLE}'   '${PAGE_TITLE}'

    [Teardown]    run keywords        Test Case Level Cleanup
    ...            AND                mu1.delete_wlan_profile     ${CLIENT_PER_PPSK_SSID}
    ...            AND                mu2.disconnect_wifi
    ...            AND                mu2.delete_wlan_profile     ${CLIENT_PER_PPSK_SSID}

Test11: Validate Generated Authentication Error Entries
    [Documentation]    connect the client 3 times with wrong password, authentication error will generate
    [Tags]             regression    ppsk   auth-error  P1   Test11

    ${LOGIN_STATUS}=                 Login User          ${tenant_username}     ${tenant_password}
    should be equal as strings      '${LOGIN_STATUS}'    '1'

    ${AUTH_COUNT_BEF}                Get Authentication Counts

    ${NW_STATUS}=                    Create Network Policy   ${SINGLE_CLOUD_NW_POLICY1}   &{WIRELESS_PPSK_NW_CLOUD_SINGLE1}
    should be equal as strings      '${NW_STATUS}'   '1'

    ${DELTA_UPDATE}=                  Update Network Policy To Ap    policy_name=${SINGLE_CLOUD_NW_POLICY1}    ap_serial=${ap1.serial}
    should be equal as strings       '${DELTA_UPDATE}'   '1'
    sleep                             ${config_push_wait}

    mu1.connect_wpa2_ppsk_network     ${SINGLE_CLOUD_NW_SSID1}     ${WRONG_PPSK_PASSWORD}      retry_count=3
    sleep                             ${client_connect_wait}

    ${AUTH_COUNT_AFT}                 Get Authentication Counts

    ${CLIENT_ISSUE_ENTRIES}           Get Client Issue Entries   ${mu1.wifi_mac}

    should be equal as strings       '${CLIENT_ISSUE_ENTRIES}[summary]'                'PPSK Rejected by Guest Access'
    should be equal as strings       '${CLIENT_ISSUE_ENTRIES}[issue_type]'             'Authentication'
    should be equal as strings       '${CLIENT_ISSUE_ENTRIES}[client_mac]'             '${mu1.wifi_mac}'
    should be equal as strings       '${CLIENT_ISSUE_ENTRIES}[extreme_net_device]'     '${ap1.name}'

    [Teardown]  run keywords         Test Case Level Cleanup
    ...          AND                 mu1.delete_wlan_profile   ${SINGLE_CLOUD_NW_SSID1}

Test12: Verification of user group Expiration time set is pushed to the AP in pre-set format
    [Documentation]   check expiration time format in AP console with created user group with local db
    [Tags]             regression   P3   Test12   CFD4627

    ${LOGIN_STATUS}=                 Login User              ${tenant_username}     ${tenant_password}
    should be equal as strings      '${LOGIN_STATUS}'        '1'

    ${USER_GROUP_CREATE}=            Create User Group       group_name=${LOCAL_DB_PPSK_GROUP}   user_group_profile=&{USER_GROUP_PROFILE_LOCAL1}
    should be equal as strings      '${USER_GROUP_CREATE}'   '1'

    ${NW_STATUS}=                    Create Network Policy   ${LOCAL_DB_PPSK_NW1}   &{LOCAL_PPSK_NETWORK1}
    should be equal as strings      '${NW_STATUS}'   '1'

    ${DELTA_UPDATE}=                 Update Network Policy To Ap    policy_name=${LOCAL_DB_PPSK_NW1}    ap_serial=${ap1.serial}
    should be equal as strings      '${DELTA_UPDATE}'   '1'

    ${EXPIRY_TIME}                  Get Current Date Time          %Y-%m-%d
    log to console                  ${EXPIRY_TIME}


    ${USER_GROUP_OUTPUT}=           Send Cmd On Device Advanced Cli    device_serial=${ap1.serial}    cmd=show user-group
    should contain                  ${USER_GROUP_OUTPUT}           ${EXPIRY_TIME} 00:00:00
    should contain                  ${USER_GROUP_OUTPUT}           ${EXPIRY_TIME} 23:45:00

    [Teardown]   run keywords       logout user
    ...                             quit browser

Test13_Step1: Check User Group Creation With Non English Xiq Account
    [Documentation]   When CloudIQ UI is any non-English language, creating a Cloud PPSK user group with expiration
    ...               and renewal causes "Start time must be before the end time." error message

    [Tags]             regression   P3   Test13    CFD4501

    ${LOGIN_STATUS}=                 Login User              ${tenant_username}     ${tenant_password}
    Change Xiq Account Language      Deutsche
    sleep                            20
    quit browser

    ${LOGIN_STATUS}=                 Login User              ${tenant_username}     ${tenant_password}
    ${USER_GROUP_CREATE}=            Create User Group       group_name=CLOUD_VALID_TIME   user_group_profile=&{USER_GROUP_PROFILE_CLOUD2}
    should be equal as strings      '${USER_GROUP_CREATE}'   '1'

    [Teardown]   run keyword        quit browser

Test13_Step2: Change Xiq Account Language to English
    [Tags]             regression   P3   Test13    CFD4501
    ${LOGIN_STATUS}=                 Login User              ${tenant_username}     ${tenant_password}
    Change Xiq Account Language      English
    sleep                            20
    [Teardown]  run keyword  quit browser

Test Suite Clean Up
    [Documentation]    delete created network policies, usergroups, radius server
    [Tags]             regression   ppsk   cwp-passing   cloud-db  local-db  bulk-user  single-user  P1
    ...                Test1   Test2   Test3   Test4  Test5  Test6  Test7  Test8   production   cleanup

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

    [Teardown]   run keywords      logout user
    ...                            quit browser
