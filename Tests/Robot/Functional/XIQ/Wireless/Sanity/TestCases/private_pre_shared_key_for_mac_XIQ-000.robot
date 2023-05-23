# Author        : pdo
# Date          : 2022
# Description   : private pre-shared connectivity check for mac version

# Topology      :
# Client -----> AP --->XIQ Instance
# Pre-Condtion
# Uses cloud3tenant3@gmail.com, cloud4tenant4@gmail.com
# 1. AP should be onboarded and it is online
# 2. Required Device: 1 AP, 1 mac station

# Execution Command:
# robot -L INFO -v DEVICE:AP630 -v TOPO:g7r2  private_pre_shared_key.robot
# Select the "TOPO" and "DEVICE" variable based on Test bed

*** Variables ***
# Variables moved to resources.  These are the same as the non-mac, so the same file is used.  See Variable statement
#  below

${PAGE_TITLE}                       End-to-End Cloud Driven Networking Solutions - Extreme Networks

*** Settings ***
Library     Collections

Library     common/GmailHandler.py
Library     common/Utils.py
Library     common/LoadBrowser.py
Library     common/Cli.py
Library     common/TestFlow.py

# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     xiq/flows/common/MuCaptivePortal.py
Library     xiq/flows/common/Navigator.py

Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/DeviceCliAccess.py
Library     xiq/flows/manage/ClientMonitor.py
Library     xiq/flows/manage/Client.py

Library     xiq/flows/configure/UserGroups.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/CommonObjects.py

Library     xiq/flows/mlinsights/MLInsightClient360.py
Library     xiq/flows/globalsettings/GlobalSetting.py


Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml
Variables    Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/test_email_ids.py
Variables    Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/private_pre_shared_key_config.py

Library	    Remote 	http://${mu1.ip}:${mu1.port}   WITH NAME   mu1

Force Tags   testbed_1_node

Suite Setup     Pre Condition
Suite Teardown  Test Suite Clean Up

*** Keywords ***
Pre Condition
    [Documentation]   AP Should be onboarded  and it is online
    #[teardown]   quit browser
    ${result}=                      Login User                 ${TENANT_USERNAME}     ${TENANT_PASSWORD}
    ${AP_STATUS}=                   get device status              device_mac=${ap1.mac}
    Should Be Equal As Strings     '${AP_STATUS}'             'green'
    Create Network Policy           ${OPEN_POLICY}             ${CONFIG_PUSH_OPEN_NW_01}
    Update Network Policy To Ap     policy_name=${OPEN_POLICY}      ap_serial=${ap1.serial}

    ${DELETE_STATUS}=              delete network polices      ${CLOUD_CWP_NW_POLICY}
    should be equal as strings    '${DELETE_STATUS}'           '1'     ppsk network policy assigned to other AP,disassociate it or issue with deleting policy

    delete captive web portal      ${SELF_REG_RETURN_PPSK_CWP}
    delete ssid                    ${CLOUD_CWP_NW_SSID}
    delete user groups             ${SINGLE_CLOUD_USER_GROUP}

Test Suite Clean Up
    [Documentation]    delete created network policies, usergroups, radius server
    [Tags]             regression   ppsk   cwp-passing   cloud-db  local-db  bulk-user  single-user  p1
    ...                cleanup   production
    #${result}=    Login User       ${TENANT_USERNAME}         ${TENANT_PASSWORD}
    ${dstatus}=                    mu1.disconnect wifi

    Update Network Policy To Ap     policy_name=${OPEN_POLICY}      ap_serial=${ap1.serial}

    ${DELETE_DEVICE_STATUS}=        Delete Device       device_serial=${ap1.serial}
    should be equal as integers         ${DELETE_DEVICE_STATUS}               1

    ${DELETE_STATUS}=              delete network polices      ${CLOUD_CWP_NW_POLICY}
    should be equal as strings    '${DELETE_STATUS}'           '1'     ppsk network policy assigned to other AP,disassociate it or issue with deleting policy


    delete captive web portal      ${SELF_REG_RETURN_PPSK_CWP}
    delete ssid                    ${CLOUD_CWP_NW_SSID}
    delete ssid                    ${SINGLE_CLOUD_NW_SSID}
    delete user groups             ${SINGLE_CLOUD_USER_GROUP}
    [Teardown]   run keywords      logout user
    ...                            quit browser


*** Test Cases ***
Test1: Cloud DB PPSK Network Client Connectivity With Single Users Group
    [Documentation]    Check ppsk network client connectivity with group user and cloud passwd db location
    [Tags]             regression   ppsk    cloud-db    bulk-user    p1  test1   test2   test3   test4  production
    #[teardown]         Quit Browser

    #${LOGIN_STATUS}=                Login User           ${TENANT_USERNAME}     ${TENANT_PASSWORD}
    #should be equal as strings     '${LOGIN_STATUS}'     '1'

    ${USER_GROUP_CREATE}=           Create User Group   ${SINGLE_CLOUD_USER_GROUP}   user_group_profile=&{USER_GROUP_PROFILE_CLOUD_SINGLE}
    should be equal as strings     '${USER_GROUP_CREATE}'     '1'

    ${NW_STATUS}=                   Create Network Policy   ${CLOUD_CWP_NW_POLICY}   ${WIRELESS_PPSK_NW_CLOUD_SINGLE}
    should be equal as strings     '${NW_STATUS}'           '1'

    ${DELTA_UPDATE}=                Update Network Policy To Ap    policy_name=${CLOUD_CWP_NW_POLICY}    ap_serial=${ap1.serial}
    should be equal as strings     '${DELTA_UPDATE}'           '1'
    sleep                           30


test2: Make Client Connection
   [Tags]              production      test5
   Log To Console       \n
   Log To Console       ************Internet Connection with the ssid ${SINGLE_CLOUD_NW_SSID}************ \n
   log to console       Access REMOTE to connect MAC to AP
   ${status}=           mu1.connect wpa2 ppsk network    ${SINGLE_CLOUD_NW_SSID}   extremextreme
   Should Be Equal      ${status}     1

#test3: Get Client Status
#   [Documentation]     Get the Client Details
#   [Tags]              production     test3
#   [teardown]         Quit Browser
#
#
#   ${LOGIN_STATUS}=                Login User              ${TENANT_USERNAME}     ${TENANT_PASSWORD}
#   should be equal as strings     '${LOGIN_STATUS}'        '1'
#
#   FOR  ${i}  IN RANGE  4
#        Log To Console  Attempt(s): ${i}
#        navigate_configure_network_policies
#        ${CLIENT_STATUS}=    get_client_status   client_mac=${mu1.wifi_mac}
#        Exit For Loop If    '${CLIENT_STATUS}' == '1'
#        Sleep  45
#   END
#
#   Should Be Equal As Strings              '${CLIENT_STATUS}'      '1'
