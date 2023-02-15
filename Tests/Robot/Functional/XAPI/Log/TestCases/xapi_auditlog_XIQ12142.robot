# Author        : Kun Li
# Date          : 13 Jan 2023
# Description   : XIQ-12142 XAPI list audit logs
# Note          : First supported release is 23r2

# Topology:
# ---------
#    ScriptHost/AutoIQ
#      |________
#      |        |
#     Cloud     AP
# Pre-config:
# -----------
#
#
#
# Execution Command:
# ------------------
# robot -v ENV:environment.local.chrome.yaml -v TOPO:topo.test.aio.hz.148.yaml -v TESTBED:HANGZHOU/Dev/xiq_hz_tb1_ap250.yaml xapi_auditlog_XIQ12142.robot


*** Variables ***
${LOG_KEYWORD_1}                         dev
${LOG_KEYWORD_2}                         device config
${LOG_KEYWORD_3}                         log
${LOG_KEYWORD_4}                         logged in
${monitor_username}                      ahqa001+m@gmail.com
${monitor_password}                      aerohive
${LOG_CATEGORY_1}                        ADMIN
${LOG_CATEGORY_2}                        MONITOR
${LOG_CATEGORY_3}                        DEPLOYMENT
${LOG_CATEGORY_4}                        CONFIG


*** Settings ***

Library     xiq/flows/extreme_location/ExtremeLocation.py
Library     xiq/flows/manage/Location.py
Library     extauto/common/Utils.py
Library     extauto/common/Screen.py
Library     extauto/common/Cli.py
Library     extauto/common/TestFlow.py
Library     extauto/xiq/flows/common/Login.py
Library     extauto/xiq/flows/common/Navigator.py
Library     extauto/xiq/flows/manage/Location.py
Library     extauto/xiq/flows/manage/Devices.py
Library     extauto/xiq/flows/configure/CommonObjects.py
Library     extauto/xiq/flows/configure/NetworkPolicy.py
Library     extauto/xiq/flows/globalsettings/GlobalSetting.py
Library     ExtremeAutomation/Imports/CommonObjectUtils.py
Library     ExtremeAutomation/Keywords/UserDefinedKeywords/NetworkElements/SetupTeardown/SetupTeardownUdks.py
Library     ../Resources/xapi_log_keyword.py


Resource    Tests/Robot/Libraries/XAPI/XAPI-Logs-Keywords.robot
Resource    ../Resources/XIQ-12142_Audit_Log_Config.robot
Variables   Environments/Config/waits.yaml
Variables   Environments/${TOPO}
Variables   Environments/${ENV}
Variables   TestBeds/${TESTBED}

Force Tags  testbed_1_node

Suite Setup     Test Suite Setup
Suite Teardown  Test Suite Clean Up

*** Keywords ***

Test Suite Setup
    [Documentation]  Suite setup.

    # login/logout the user, just generate the audit logs
    Login User      ${tenant_username}      ${tenant_password}
    logout user

    # Genrate a random string which will add to profile name
    ${RANDOM_STR}=          Get Random String
    set suite variable     ${RANDOM_STR}

    # convert all ap or switch to device
    convert to generic device object   device  index=1

    # Create the connection to the device(s)
    ${DEVICE1_SPAWN}=   Open Spawn    ${device1.ip}    ${device1.port}    ${device1.username}    ${device1.password}    ${device1.cli_type}
    set suite variable    ${DEVICE1_SPAWN}

    # login the user
    Login User      ${tenant_username}      ${tenant_password}

    # Create location building floor
    Create Test Location Building Floor

    # Onboard device
    Device Onboard
    Create Network Policy and Update to AP

    # Generate xapi access token
    ${ACCESS_TOKEN}=        generate_access_token    ${tenant_username}      ${tenant_password}      login
    set suite variable     ${ACCESS_TOKEN}
    Log    Checking the Access Token not equal to -1
    skip if     '${ACCESS_TOKEN}' == '-1'

    # Encode URI of keyword and admin user to convert the special char
    Encode URI Keyword and Admin User

Test Suite Clean Up
    [Documentation]  Suite clean.

    Clean Up Device

    ${DLT_NW_POLICIES}=             Delete Network Polices                  ${POLICY_NAME}
    should be equal as integers     ${DLT_NW_POLICIES}          1

    ${DELETE_SSIDS}=                Delete SSIDs                            ${SSID_NAME}
    should be equal as integers     ${DELETE_SSIDS}             1

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Create Test Location Building Floor
    [Documentation]  Create Location Building Floor

    # Create first org
    ${FIRST_MAP_CREATION}=      Create First Organization       ${1st_LOCATION_ORG}      ${1st_LOCATION_STREET}       ${1st_LOCATION_CITY_STATE}       ${1st_LOCATION_COUNTRY}      width=${MAP_WIDTH}      height=${MAP_HIGHT}
    Should Be Equal As Integers    ${FIRST_MAP_CREATION}             1

Device Onboard
    [Documentation]  Device Onboard

    # onboard the device
    Clean Up Device

    ${ONBOARD_RESULT}=          onboard device quick     ${device1}
    Should Be Equal As Strings                  ${ONBOARD_RESULT}       1

    configure device to connect to cloud    ${device1.cli_type}   ${generic_capwap_url}   ${DEVICE1_SPAWN}

    ${ONLINE_STATUS_RESULT}=    wait until device online     ${device1.serial}
    Should Be Equal As Strings                  ${ONLINE_STATUS_RESULT}       1

    ${MANAGED_STATUS_RESULT}=   wait until device managed   ${device1.serial}
    Should Be Equal As Strings                  ${MANAGED_STATUS_RESULT}      1

    ${DEVICE_STATUS_RESULT}=    get device status      ${device1.serial}
    Should Be Equal As Strings                  ${DEVICE_STATUS_RESULT}      green

Clean Up Device
    [Documentation]  Clean Up Device

    ${search_result}=   Search Device       device_serial=${device1.serial}    ignore_cli_feedback=true
    # Disconnect from Extreme Cloud IQ
    Run Keyword If  '${search_result}' == '1'       Delete and Disconnect Device From Cloud

Delete and Disconnect Device From Cloud
    [Documentation]  Delete device from cloud, disconnect device capwap connection

    delete device   device_serial=${device1.serial}
    disconnect device from cloud     ${device1.cli_type}     ${DEVICE1_SPAWN}

Create Network Policy and Update to AP
    [Documentation]  Create a network policy and update to AP

    # Generate the policy name and ssid name with random str
    ${POLICY_NAME}=    set variable    ${NW_POLICY_NAME1}_${RANDOM_STR}
    ${SSID_NAME}=      set variable    ${PSK_WPA2CCMP_SSID_NAME}_${RANDOM_STR}

    # Setup suite variable, which will use in case step or tear down
    Set Suite Variable              ${POLICY_NAME}
    Set Suite Variable              ${SSID_NAME}

    set to dictionary    ${WIRELESS_PESRONAL_WPA2CCMP}      ssid_name=${SSID_NAME}

    ${NW_POLICY_CREATION}=  Create Network Policy   ${POLICY_NAME}   ${WIRELESS_PESRONAL_WPA2CCMP}
    Should Be Equal As Strings    ${NW_POLICY_CREATION}   1

    ${NP_RESULT}=                   Update Network Policy To AP     policy_name=${POLICY_NAME}     ap_serial=${device1.serial}
    Should Be Equal As Integers     ${NP_RESULT}            1

    ${UPDATE_RESULT}=               update_device_delta_configuration           ${device1.serial}
    Should Be Equal As Integers     ${UPDATE_RESULT}        1

    ${CONNECTED_STATUS}=    Wait Until Device Online                ${device1.serial}
    Should Be Equal as Integers             ${CONNECTED_STATUS}          1

Encode URI Keyword and Admin User
    [Documentation]  Encode the input log url of keyword and admin user, convert the specific char

    ${LOG_KEYWORD_URI_1}=    encode uri    ${LOG_KEYWORD_1}
    set suite variable       ${LOG_KEYWORD_URI_1}
    ${LOG_KEYWORD_URI_2}=    encode uri    ${LOG_KEYWORD_2}
    set suite variable       ${LOG_KEYWORD_URI_2}
    ${LOG_KEYWORD_URI_3}=    encode uri    ${LOG_KEYWORD_3}
    set suite variable       ${LOG_KEYWORD_URI_3}
    ${LOG_KEYWORD_URI_4}=    encode uri    ${LOG_KEYWORD_4}
    set suite variable       ${LOG_KEYWORD_URI_4}
    ${LOG_ADMIN_USER_1}=     encode uri    ${tenant_username}
    set suite variable       ${LOG_ADMIN_USER_1}
    ${LOG_ADMIN_USER_2}=     encode uri    ${monitor_username}
    set suite variable       ${LOG_ADMIN_USER_2}

    
*** Test Cases ***
TCXM-30671: Audit Logs - List logs filtered by keyword
    [Documentation]     TCXM-30671: Audit Logs - List audit logs filtered by keyword;
    [Tags]              development  tcxm_30671

    Comment    Step 1. Get audit logs without filter and filtered by pre-defined keyword.

    # Get first page audit log without filter
    ${AUDIT_LOG_CONTENT_NO_FILTER}=     xapi get first page audit logs
    # Get audit log count and data wihtout filter
    ${AUDIT_LOG_COUNT_NO_FILTER}=    xapi get audit log count    ${AUDIT_LOG_CONTENT_NO_FILTER}
    ${AUDIT_LOG_DATA_NO_FILTER}=    xapi get audit log data    ${AUDIT_LOG_CONTENT_NO_FILTER}

    # Get first page audit log with filter pre-defined keyword LOG_KEYWORD_1 to LOG_KEYWORD_4
    ${AUDIT_LOG_CONTENT_FILTER_KEY_1}=    xapi list first page audit logs by keyword   ${LOG_KEYWORD_URI_1}
    ${AUDIT_LOG_CONTENT_FILTER_KEY_2}=    xapi list first page audit logs by keyword   ${LOG_KEYWORD_URI_2}
    ${AUDIT_LOG_CONTENT_FILTER_KEY_3}=    xapi list first page audit logs by keyword   ${LOG_KEYWORD_URI_3}
    ${AUDIT_LOG_CONTENT_FILTER_KEY_4}=    xapi list first page audit logs by keyword   ${LOG_KEYWORD_URI_4}

    # Get audit log count with filter keyword LOG_KEYWORD_1 to LOG_KEYWORD_4
    ${AUDIT_LOG_COUNT_FILTER_KEY_1}=    xapi get audit log count    ${AUDIT_LOG_CONTENT_FILTER_KEY_1}
    ${AUDIT_LOG_COUNT_FILTER_KEY_2}=    xapi get audit log count    ${AUDIT_LOG_CONTENT_FILTER_KEY_2}
    ${AUDIT_LOG_COUNT_FILTER_KEY_3}=    xapi get audit log count    ${AUDIT_LOG_CONTENT_FILTER_KEY_3}
    ${AUDIT_LOG_COUNT_FILTER_KEY_4}=    xapi get audit log count    ${AUDIT_LOG_CONTENT_FILTER_KEY_4}

    # Get audit log data with filter keyword LOG_KEYWORD_1 to LOG_KEYWORD_4
    ${AUDIT_LOG_DATA_FILTER_KEY_1}=    xapi get audit log data    ${AUDIT_LOG_CONTENT_FILTER_KEY_1}
    ${AUDIT_LOG_DATA_FILTER_KEY_2}=    xapi get audit log data    ${AUDIT_LOG_CONTENT_FILTER_KEY_2}
    ${AUDIT_LOG_DATA_FILTER_KEY_3}=    xapi get audit log data    ${AUDIT_LOG_CONTENT_FILTER_KEY_3}
    ${AUDIT_LOG_DATA_FILTER_KEY_4}=    xapi get audit log data    ${AUDIT_LOG_CONTENT_FILTER_KEY_4}

    # Get audit log description list from audit log data
    ${AUDIT_LOG_DESC_LIST_FILTER_KEY_1}=    xapi get description list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_1}
    ${AUDIT_LOG_DESC_LIST_FILTER_KEY_2}=    xapi get description list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_2}
    ${AUDIT_LOG_DESC_LIST_FILTER_KEY_3}=    xapi get description list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_3}
    ${AUDIT_LOG_DESC_LIST_FILTER_KEY_4}=    xapi get description list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_4}

    Comment    Step 2. Checkpoint 1: AUDIT_LOG_COUNT_NO_FILTER>AUDIT_LOG_COUNT_FILTER_KEY_1>AUDIT_LOG_COUNT_FILTER_KEY_2>0 and AUDIT_LOG_COUNT_NO_FILTER>AUDIT_LOG_COUNT_FILTER_KEY_3>AUDIT_LOG_COUNT_FILTER_KEY_4>0

    # Checkpoint 1
    Log    AUDIT_LOG_COUNT_NO_FILTER=${AUDIT_LOG_COUNT_NO_FILTER}; AUDIT_LOG_COUNT_FILTER_KEY_1=${AUDIT_LOG_COUNT_FILTER_KEY_1}; AUDIT_LOG_COUNT_FILTER_KEY_2=${AUDIT_LOG_COUNT_FILTER_KEY_2}
    run keyword unless   ${AUDIT_LOG_COUNT_NO_FILTER}>${AUDIT_LOG_COUNT_FILTER_KEY_1}>${AUDIT_LOG_COUNT_FILTER_KEY_2}>0   FAIL  The condition did not meet AUDIT_LOG_COUNT_NO_FILTER>AUDIT_LOG_COUNT_FILTER_KEY_1>AUDIT_LOG_COUNT_FILTER_KEY_2>0
    Log    AUDIT_LOG_COUNT_NO_FILTER=${AUDIT_LOG_COUNT_NO_FILTER}; AUDIT_LOG_COUNT_FILTER_KEY_3=${AUDIT_LOG_COUNT_FILTER_KEY_3}; AUDIT_LOG_COUNT_FILTER_KEY_4=${AUDIT_LOG_COUNT_FILTER_KEY_4}
    run keyword unless   ${AUDIT_LOG_COUNT_NO_FILTER}>${AUDIT_LOG_COUNT_FILTER_KEY_3}>${AUDIT_LOG_COUNT_FILTER_KEY_4}>0   FAIL  The condition did not meet AUDIT_LOG_COUNT_NO_FILTER>AUDIT_LOG_COUNT_FILTER_KEY_3>AUDIT_LOG_COUNT_FILTER_KEY_4>0

    Comment    Step 3. Checkpoint 2: All filtered log entry should contain the correspond keyword, the match should be case-insensitive

    # Checkpoint 2
    log  LOG_KEYWORD_1=${LOG_KEYWORD_1}; LOG_KEYWORD_2=${LOG_KEYWORD_2}; LOG_KEYWORD_3=${LOG_KEYWORD_3}; LOG_KEYWORD_4=${LOG_KEYWORD_4}
    FOR    ${LOG_DESC}    IN    @{AUDIT_LOG_DESC_LIST_FILTER_KEY_1}
         should contain     ${LOG_DESC}    ${LOG_KEYWORD_1}    ignore_case=True
    END
    FOR    ${LOG_DESC}    IN    @{AUDIT_LOG_DESC_LIST_FILTER_KEY_2}
         should contain     ${LOG_DESC}    ${LOG_KEYWORD_2}    ignore_case=True
    END
    FOR    ${LOG_DESC}    IN    @{AUDIT_LOG_DESC_LIST_FILTER_KEY_3}
         should contain     ${LOG_DESC}    ${LOG_KEYWORD_3}    ignore_case=True
    END
    FOR    ${LOG_DESC}    IN    @{AUDIT_LOG_DESC_LIST_FILTER_KEY_4}
         should contain     ${LOG_DESC}    ${LOG_KEYWORD_4}    ignore_case=True
    END

    Comment    Step 4. Just a commnet, mark the case PASS after pass the step2-3 checkpoints.


TCXM-30672: Audit Logs - List logs filtered by admin user and keyword
    [Documentation]     TCXM-30672: Audit Logs - List audit logs filtered by admin user and keyword;
    [Tags]              development  tcxm_30672

    Comment    Step 1. Get audit logs without filter and filtered by admin user and pre-defined keyword.
    # Get first page audit log without filter
    ${AUDIT_LOG_CONTENT_NO_FILTER}=     xapi get first page audit logs
    # Get audit log count and data wihtout filter
    ${AUDIT_LOG_COUNT_NO_FILTER}=    xapi get audit log count    ${AUDIT_LOG_CONTENT_NO_FILTER}
    ${AUDIT_LOG_DATA_NO_FILTER}=    xapi get audit log data    ${AUDIT_LOG_CONTENT_NO_FILTER}

    # Get first page audit log with filter admin user and pre-defined keyword LOG_KEYWORD_1 to LOG_KEYWORD_4
    ${AUDIT_LOG_CONTENT_FILTER_KEY_1}=    xapi list first page audit logs by user and keyword   ${LOG_ADMIN_USER_1}    ${LOG_KEYWORD_URI_1}
    ${AUDIT_LOG_CONTENT_FILTER_KEY_2}=    xapi list first page audit logs by user and keyword   ${LOG_ADMIN_USER_1}    ${LOG_KEYWORD_URI_2}
    ${AUDIT_LOG_CONTENT_FILTER_KEY_3}=    xapi list first page audit logs by user and keyword   ${LOG_ADMIN_USER_2}    ${LOG_KEYWORD_URI_3}
    ${AUDIT_LOG_CONTENT_FILTER_KEY_4}=    xapi list first page audit logs by user and keyword   ${LOG_ADMIN_USER_2}    ${LOG_KEYWORD_URI_4}

    # Get audit log count with filter admin user and pre-defined keyword LOG_KEYWORD_1 to LOG_KEYWORD_4
    ${AUDIT_LOG_COUNT_FILTER_KEY_1}=    xapi get audit log count    ${AUDIT_LOG_CONTENT_FILTER_KEY_1}
    ${AUDIT_LOG_COUNT_FILTER_KEY_2}=    xapi get audit log count    ${AUDIT_LOG_CONTENT_FILTER_KEY_2}
    ${AUDIT_LOG_COUNT_FILTER_KEY_3}=    xapi get audit log count    ${AUDIT_LOG_CONTENT_FILTER_KEY_3}
    ${AUDIT_LOG_COUNT_FILTER_KEY_4}=    xapi get audit log count    ${AUDIT_LOG_CONTENT_FILTER_KEY_4}

    # Get audit log data with filter admin user and pre-defined keyword LOG_KEYWORD_1 to LOG_KEYWORD_4
    ${AUDIT_LOG_DATA_FILTER_KEY_1}=    xapi get audit log data    ${AUDIT_LOG_CONTENT_FILTER_KEY_1}
    ${AUDIT_LOG_DATA_FILTER_KEY_2}=    xapi get audit log data    ${AUDIT_LOG_CONTENT_FILTER_KEY_2}
    ${AUDIT_LOG_DATA_FILTER_KEY_3}=    xapi get audit log data    ${AUDIT_LOG_CONTENT_FILTER_KEY_3}
    ${AUDIT_LOG_DATA_FILTER_KEY_4}=    xapi get audit log data    ${AUDIT_LOG_CONTENT_FILTER_KEY_4}

    # Get audit log description list from audit log data
    ${AUDIT_LOG_DESC_LIST_FILTER_KEY_1}=    xapi get description list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_1}
    ${AUDIT_LOG_DESC_LIST_FILTER_KEY_2}=    xapi get description list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_2}
    ${AUDIT_LOG_DESC_LIST_FILTER_KEY_3}=    xapi get description list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_3}
    ${AUDIT_LOG_DESC_LIST_FILTER_KEY_4}=    xapi get description list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_4}

    # Get audit log admin user list from audit log data
    ${AUDIT_LOG_USER_LIST_FILTER_KEY_1}=    xapi get admin user list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_1}
    ${AUDIT_LOG_USER_LIST_FILTER_KEY_2}=    xapi get admin user list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_2}
    ${AUDIT_LOG_USER_LIST_FILTER_KEY_3}=    xapi get admin user list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_3}
    ${AUDIT_LOG_USER_LIST_FILTER_KEY_4}=    xapi get admin user list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_4}

    Comment    Step 2. Checkpoint 1: AUDIT_LOG_COUNT_NO_FILTER>AUDIT_LOG_COUNT_FILTER_KEY_1>AUDIT_LOG_COUNT_FILTER_KEY_2>0 and AUDIT_LOG_COUNT_NO_FILTER>AUDIT_LOG_COUNT_FILTER_KEY_3>=AUDIT_LOG_COUNT_FILTER_KEY_4>=0
    # Checkpoint 1
    Log    AUDIT_LOG_COUNT_NO_FILTER=${AUDIT_LOG_COUNT_NO_FILTER}; AUDIT_LOG_COUNT_FILTER_KEY_1=${AUDIT_LOG_COUNT_FILTER_KEY_1}; AUDIT_LOG_COUNT_FILTER_KEY_2=${AUDIT_LOG_COUNT_FILTER_KEY_2}
    run keyword unless   ${AUDIT_LOG_COUNT_NO_FILTER}>${AUDIT_LOG_COUNT_FILTER_KEY_1}>${AUDIT_LOG_COUNT_FILTER_KEY_2}>0   FAIL  The condition did not meet AUDIT_LOG_COUNT_NO_FILTER>AUDIT_LOG_COUNT_FILTER_KEY_1>AUDIT_LOG_COUNT_FILTER_KEY_2>0
    Log    AUDIT_LOG_COUNT_NO_FILTER=${AUDIT_LOG_COUNT_NO_FILTER}; AUDIT_LOG_COUNT_FILTER_KEY_3=${AUDIT_LOG_COUNT_FILTER_KEY_3}; AUDIT_LOG_COUNT_FILTER_KEY_4=${AUDIT_LOG_COUNT_FILTER_KEY_4}
    run keyword unless   ${AUDIT_LOG_COUNT_NO_FILTER}>${AUDIT_LOG_COUNT_FILTER_KEY_3}>=${AUDIT_LOG_COUNT_FILTER_KEY_4}>=0   FAIL  The condition did not meet AUDIT_LOG_COUNT_NO_FILTER>AUDIT_LOG_COUNT_FILTER_KEY_3>=AUDIT_LOG_COUNT_FILTER_KEY_4>=0

    Comment    Step 3. Checkpoint 2: All filtered log entry should contain the correspond keyword, the match should be case-insensitive
    # Checkpoint 2
    log  LOG_KEYWORD_1=${LOG_KEYWORD_1}; LOG_KEYWORD_2=${LOG_KEYWORD_2}; LOG_KEYWORD_3=${LOG_KEYWORD_3}; LOG_KEYWORD_4=${LOG_KEYWORD_4}
    FOR    ${LOG_DESC}    IN    @{AUDIT_LOG_DESC_LIST_FILTER_KEY_1}
         should contain     ${LOG_DESC}    ${LOG_KEYWORD_1}    ignore_case=True
    END
    FOR    ${LOG_DESC}    IN    @{AUDIT_LOG_DESC_LIST_FILTER_KEY_2}
         should contain     ${LOG_DESC}    ${LOG_KEYWORD_2}    ignore_case=True
    END
    FOR    ${LOG_DESC}    IN    @{AUDIT_LOG_DESC_LIST_FILTER_KEY_3}
         should contain     ${LOG_DESC}    ${LOG_KEYWORD_3}    ignore_case=True
    END
    FOR    ${LOG_DESC}    IN    @{AUDIT_LOG_DESC_LIST_FILTER_KEY_4}
         should contain     ${LOG_DESC}    ${LOG_KEYWORD_4}    ignore_case=True
    END

    Comment    Step 4. Checkpoint 3: The admin user of filtered log entry should equal to the correspond one
    # Checkpoint 3
    log  LOG_USER_1=tenant_username=${tenant_username}; LOG_USER_2=monitor_username=${monitor_username};
    FOR    ${LOG_USER}    IN    @{AUDIT_LOG_USER_LIST_FILTER_KEY_1}
         should be equal as strings  ${LOG_USER}  ${tenant_username}
    END
    FOR    ${LOG_USER}    IN    @{AUDIT_LOG_USER_LIST_FILTER_KEY_2}
         should be equal as strings  ${LOG_USER}  ${tenant_username}
    END
    FOR    ${LOG_USER}    IN    @{AUDIT_LOG_USER_LIST_FILTER_KEY_3}
         should be equal as strings  ${LOG_USER}  ${monitor_username}
    END
    FOR    ${LOG_USER}    IN    @{AUDIT_LOG_USER_LIST_FILTER_KEY_4}
         should be equal as strings  ${LOG_USER}  ${monitor_username}
    END

    Comment    Step 5. Just a commnet, mark the case PASS after pass the step2-4 checkpoints.


TCXM-30673: Audit Logs - List logs filtered by admin user, category and keyword
    [Documentation]     TCXM-30673: Audit Logs - List audit logs filtered by admin user, category and keyword;
    [Tags]              development  tcxm_30673

    Comment    Step 1. Get audit logs without filter and filtered by admin user, category and pre-defined keyword.
    # Get first page audit log without filter
    ${AUDIT_LOG_CONTENT_NO_FILTER}=     xapi get first page audit logs
    # Get audit log count and data wihtout filter
    ${AUDIT_LOG_COUNT_NO_FILTER}=    xapi get audit log count    ${AUDIT_LOG_CONTENT_NO_FILTER}
    ${AUDIT_LOG_DATA_NO_FILTER}=    xapi get audit log data    ${AUDIT_LOG_CONTENT_NO_FILTER}

    # Get first page audit log with filter admin user, category and pre-defined keyword
    ${AUDIT_LOG_CONTENT_FILTER_KEY_1}=  xapi list first page audit logs by category user and keyword  ${LOG_CATEGORY_1}  ${LOG_ADMIN_USER_1}  ${LOG_KEYWORD_URI_1}
    ${AUDIT_LOG_CONTENT_FILTER_KEY_2}=  xapi list first page audit logs by category user and keyword  ${LOG_CATEGORY_2}  ${LOG_ADMIN_USER_1}  ${LOG_KEYWORD_URI_1}
    ${AUDIT_LOG_CONTENT_FILTER_KEY_3}=  xapi list first page audit logs by category user and keyword  ${LOG_CATEGORY_3}  ${LOG_ADMIN_USER_1}  ${LOG_KEYWORD_URI_1}
    ${AUDIT_LOG_CONTENT_FILTER_KEY_4}=  xapi list first page audit logs by category user and keyword  ${LOG_CATEGORY_4}  ${LOG_ADMIN_USER_2}  ${LOG_KEYWORD_URI_2}

    # Get audit log count with filter admin user, category and pre-defined keyword
    ${AUDIT_LOG_COUNT_FILTER_KEY_1}=  xapi get audit log count    ${AUDIT_LOG_CONTENT_FILTER_KEY_1}
    ${AUDIT_LOG_COUNT_FILTER_KEY_2}=  xapi get audit log count    ${AUDIT_LOG_CONTENT_FILTER_KEY_2}
    ${AUDIT_LOG_COUNT_FILTER_KEY_3}=  xapi get audit log count    ${AUDIT_LOG_CONTENT_FILTER_KEY_3}
    ${AUDIT_LOG_COUNT_FILTER_KEY_4}=  xapi get audit log count    ${AUDIT_LOG_CONTENT_FILTER_KEY_4}

    # Get audit log data with filter admin user, category and pre-defined keyword
    ${AUDIT_LOG_DATA_FILTER_KEY_1}=  xapi get audit log data    ${AUDIT_LOG_CONTENT_FILTER_KEY_1}
    ${AUDIT_LOG_DATA_FILTER_KEY_2}=  xapi get audit log data    ${AUDIT_LOG_CONTENT_FILTER_KEY_2}
    ${AUDIT_LOG_DATA_FILTER_KEY_3}=  xapi get audit log data    ${AUDIT_LOG_CONTENT_FILTER_KEY_3}
    ${AUDIT_LOG_DATA_FILTER_KEY_4}=  xapi get audit log data    ${AUDIT_LOG_CONTENT_FILTER_KEY_4}

    # Get audit log description list from audit log data
    ${AUDIT_LOG_DESC_LIST_FILTER_KEY_1}=  xapi get description list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_1}
    ${AUDIT_LOG_DESC_LIST_FILTER_KEY_2}=  xapi get description list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_2}
    ${AUDIT_LOG_DESC_LIST_FILTER_KEY_3}=  xapi get description list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_3}
    ${AUDIT_LOG_DESC_LIST_FILTER_KEY_4}=  xapi get description list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_4}

    # Get audit log admin user list from audit log data
    ${AUDIT_LOG_USER_LIST_FILTER_KEY_1}=  xapi get admin user list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_1}
    ${AUDIT_LOG_USER_LIST_FILTER_KEY_2}=  xapi get admin user list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_2}
    ${AUDIT_LOG_USER_LIST_FILTER_KEY_3}=  xapi get admin user list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_3}
    ${AUDIT_LOG_USER_LIST_FILTER_KEY_4}=  xapi get admin user list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_4}

    # Get audit log category list from audit log data
    ${AUDIT_LOG_CAT_LIST_FILTER_KEY_1}=  xapi get category list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_1}
    ${AUDIT_LOG_CAT_LIST_FILTER_KEY_2}=  xapi get category list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_2}
    ${AUDIT_LOG_CAT_LIST_FILTER_KEY_3}=  xapi get category list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_3}
    ${AUDIT_LOG_CAT_LIST_FILTER_KEY_4}=  xapi get category list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_4}

    Comment    Step 2. Checkpoint 1: AUDIT_LOG_COUNT_NO_FILTER>AUDIT_LOG_COUNT_FILTER_KEY_1>0 and AUDIT_LOG_COUNT_NO_FILTER>AUDIT_LOG_COUNT_FILTER_KEY_2>0 and AUDIT_LOG_COUNT_NO_FILTER>AUDIT_LOG_COUNT_FILTER_KEY_3>0 and AUDIT_LOG_COUNT_NO_FILTER>AUDIT_LOG_COUNT_FILTER_KEY_4>=0
    # Checkpoint 1
    Log    AUDIT_LOG_COUNT_NO_FILTER=${AUDIT_LOG_COUNT_NO_FILTER}; AUDIT_LOG_COUNT_FILTER_KEY_1=${AUDIT_LOG_COUNT_FILTER_KEY_1}; AUDIT_LOG_COUNT_FILTER_KEY_2=${AUDIT_LOG_COUNT_FILTER_KEY_2}; AUDIT_LOG_COUNT_FILTER_KEY_3=${AUDIT_LOG_COUNT_FILTER_KEY_3}; AUDIT_LOG_COUNT_FILTER_KEY_4=${AUDIT_LOG_COUNT_FILTER_KEY_4}
    run keyword unless   ${AUDIT_LOG_COUNT_NO_FILTER}>${AUDIT_LOG_COUNT_FILTER_KEY_1}>0   FAIL  The condition did not meet AUDIT_LOG_COUNT_NO_FILTER>AUDIT_LOG_COUNT_FILTER_KEY_1>0
    run keyword unless   ${AUDIT_LOG_COUNT_NO_FILTER}>${AUDIT_LOG_COUNT_FILTER_KEY_2}>0   FAIL  The condition did not meet AUDIT_LOG_COUNT_NO_FILTER>AUDIT_LOG_COUNT_FILTER_KEY_2>0
    run keyword unless   ${AUDIT_LOG_COUNT_NO_FILTER}>${AUDIT_LOG_COUNT_FILTER_KEY_3}>0   FAIL  The condition did not meet AUDIT_LOG_COUNT_NO_FILTER>AUDIT_LOG_COUNT_FILTER_KEY_3>0
    run keyword unless   ${AUDIT_LOG_COUNT_NO_FILTER}>${AUDIT_LOG_COUNT_FILTER_KEY_4}>=0   FAIL  The condition did not meet AUDIT_LOG_COUNT_NO_FILTER>AUDIT_LOG_COUNT_FILTER_KEY_4>=0

    Comment    Step 3. Checkpoint 2: All filtered log entry should contain the correspond keyword, the match should be case-insensitive
    # Checkpoint 2
    log  LOG_KEYWORD_1=${LOG_KEYWORD_1}; LOG_KEYWORD_2=${LOG_KEYWORD_2}; LOG_KEYWORD_3=${LOG_KEYWORD_3}; LOG_KEYWORD_4=${LOG_KEYWORD_4}
    FOR    ${LOG_DESC}    IN    @{AUDIT_LOG_DESC_LIST_FILTER_KEY_1}
         should contain     ${LOG_DESC}    ${LOG_KEYWORD_1}    ignore_case=True
    END
    FOR    ${LOG_DESC}    IN    @{AUDIT_LOG_DESC_LIST_FILTER_KEY_2}
         should contain     ${LOG_DESC}    ${LOG_KEYWORD_1}    ignore_case=True
    END
    FOR    ${LOG_DESC}    IN    @{AUDIT_LOG_DESC_LIST_FILTER_KEY_3}
         should contain     ${LOG_DESC}    ${LOG_KEYWORD_1}    ignore_case=True
    END
    FOR    ${LOG_DESC}    IN    @{AUDIT_LOG_DESC_LIST_FILTER_KEY_4}
         should contain     ${LOG_DESC}    ${LOG_KEYWORD_2}    ignore_case=True
    END

    Comment    Step 4. Checkpoint 3: The admin user of filtered log entry should equal to the correspond one
    # Checkpoint 3
    log  LOG_USER_1=tenant_username=${tenant_username}; LOG_USER_2=monitor_username=${monitor_username};
    FOR    ${LOG_USER}    IN    @{AUDIT_LOG_USER_LIST_FILTER_KEY_1}
         should be equal as strings  ${LOG_USER}  ${tenant_username}
    END
    FOR    ${LOG_USER}    IN    @{AUDIT_LOG_USER_LIST_FILTER_KEY_2}
         should be equal as strings  ${LOG_USER}  ${tenant_username}
    END
    FOR    ${LOG_USER}    IN    @{AUDIT_LOG_USER_LIST_FILTER_KEY_3}
         should be equal as strings  ${LOG_USER}  ${tenant_username}
    END
    FOR    ${LOG_USER}    IN    @{AUDIT_LOG_USER_LIST_FILTER_KEY_4}
         should be equal as strings  ${LOG_USER}  ${monitor_username}
    END

    Comment    Step 5. Checkpoint 4: The category of filtered log entry should equal to the correspond one
    # Checkpoint 4
    log  LOG_CATEGORY_1=${LOG_CATEGORY_1}; LOG_CATEGORY_2=${LOG_CATEGORY_2}; LOG_CATEGORY_3=${LOG_CATEGORY_3}; LOG_CATEGORY_4=${LOG_CATEGORY_4}
    FOR    ${LOG_CAT}    IN    @{AUDIT_LOG_CAT_LIST_FILTER_KEY_1}
         should be equal as strings  ${LOG_CAT}  ${LOG_CATEGORY_1}
    END
    FOR    ${LOG_CAT}    IN    @{AUDIT_LOG_CAT_LIST_FILTER_KEY_2}
         should be equal as strings  ${LOG_CAT}  ${LOG_CATEGORY_2}
    END
    FOR    ${LOG_CAT}    IN    @{AUDIT_LOG_CAT_LIST_FILTER_KEY_3}
         should be equal as strings  ${LOG_CAT}  ${LOG_CATEGORY_3}
    END
    FOR    ${LOG_CAT}    IN    @{AUDIT_LOG_CAT_LIST_FILTER_KEY_4}
         should be equal as strings  ${LOG_CAT}  ${LOG_CATEGORY_4}
    END

    Comment    Step 6. Just a commnet, mark the case PASS after pass the step2-5 checkpoints.


TCXM-31049: Audit Logs - List logs filtered by category and keyword
    [Documentation]     TCXM-31049: Audit Logs - List audit logs filtered by category and keyword;
    [Tags]              development  tcxm_31049

    Comment    Step 1. Get audit logs without filter and filtered by category and pre-defined keyword.
    # Get first page audit log without filter
    ${AUDIT_LOG_CONTENT_NO_FILTER}=     xapi get first page audit logs
    # Get audit log count and data wihtout filter
    ${AUDIT_LOG_COUNT_NO_FILTER}=    xapi get audit log count    ${AUDIT_LOG_CONTENT_NO_FILTER}
    ${AUDIT_LOG_DATA_NO_FILTER}=    xapi get audit log data    ${AUDIT_LOG_CONTENT_NO_FILTER}

    # Get first page audit log with filter category and pre-defined keyword
    ${AUDIT_LOG_CONTENT_FILTER_KEY_1}=  xapi list first page audit logs by category and keyword  ${LOG_CATEGORY_1}  ${LOG_KEYWORD_URI_1}
    ${AUDIT_LOG_CONTENT_FILTER_KEY_2}=  xapi list first page audit logs by category and keyword  ${LOG_CATEGORY_2}  ${LOG_KEYWORD_URI_1}
    ${AUDIT_LOG_CONTENT_FILTER_KEY_3}=  xapi list first page audit logs by category and keyword  ${LOG_CATEGORY_3}  ${LOG_KEYWORD_URI_1}
    ${AUDIT_LOG_CONTENT_FILTER_KEY_4}=  xapi list first page audit logs by category and keyword  ${LOG_CATEGORY_3}  ${LOG_KEYWORD_URI_2}

    # Get audit log count with filter category and pre-defined keyword
    ${AUDIT_LOG_COUNT_FILTER_KEY_1}=  xapi get audit log count    ${AUDIT_LOG_CONTENT_FILTER_KEY_1}
    ${AUDIT_LOG_COUNT_FILTER_KEY_2}=  xapi get audit log count    ${AUDIT_LOG_CONTENT_FILTER_KEY_2}
    ${AUDIT_LOG_COUNT_FILTER_KEY_3}=  xapi get audit log count    ${AUDIT_LOG_CONTENT_FILTER_KEY_3}
    ${AUDIT_LOG_COUNT_FILTER_KEY_4}=  xapi get audit log count    ${AUDIT_LOG_CONTENT_FILTER_KEY_4}

    # Get audit log data with filter category and pre-defined keyword
    ${AUDIT_LOG_DATA_FILTER_KEY_1}=  xapi get audit log data    ${AUDIT_LOG_CONTENT_FILTER_KEY_1}
    ${AUDIT_LOG_DATA_FILTER_KEY_2}=  xapi get audit log data    ${AUDIT_LOG_CONTENT_FILTER_KEY_2}
    ${AUDIT_LOG_DATA_FILTER_KEY_3}=  xapi get audit log data    ${AUDIT_LOG_CONTENT_FILTER_KEY_3}
    ${AUDIT_LOG_DATA_FILTER_KEY_4}=  xapi get audit log data    ${AUDIT_LOG_CONTENT_FILTER_KEY_4}

    # Get audit log description list from audit log data
    ${AUDIT_LOG_DESC_LIST_FILTER_KEY_1}=  xapi get description list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_1}
    ${AUDIT_LOG_DESC_LIST_FILTER_KEY_2}=  xapi get description list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_2}
    ${AUDIT_LOG_DESC_LIST_FILTER_KEY_3}=  xapi get description list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_3}
    ${AUDIT_LOG_DESC_LIST_FILTER_KEY_4}=  xapi get description list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_4}

    # Get audit log category list from audit log data
    ${AUDIT_LOG_CAT_LIST_FILTER_KEY_1}=  xapi get category list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_1}
    ${AUDIT_LOG_CAT_LIST_FILTER_KEY_2}=  xapi get category list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_2}
    ${AUDIT_LOG_CAT_LIST_FILTER_KEY_3}=  xapi get category list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_3}
    ${AUDIT_LOG_CAT_LIST_FILTER_KEY_4}=  xapi get category list from audit log data     ${AUDIT_LOG_DATA_FILTER_KEY_4}

    Comment    Step 2. Checkpoint 1: AUDIT_LOG_COUNT_NO_FILTER>AUDIT_LOG_COUNT_FILTER_KEY_1>0 and AUDIT_LOG_COUNT_NO_FILTER>AUDIT_LOG_COUNT_FILTER_KEY_2>0 and AUDIT_LOG_COUNT_NO_FILTER>AUDIT_LOG_COUNT_FILTER_KEY_3>AUDIT_LOG_COUNT_FILTER_KEY_4>=0
    # Checkpoint 1
    Log  AUDIT_LOG_COUNT_NO_FILTER=${AUDIT_LOG_COUNT_NO_FILTER}; AUDIT_LOG_COUNT_FILTER_KEY_1=${AUDIT_LOG_COUNT_FILTER_KEY_1}; AUDIT_LOG_COUNT_FILTER_KEY_2=${AUDIT_LOG_COUNT_FILTER_KEY_2}; AUDIT_LOG_COUNT_FILTER_KEY_3=${AUDIT_LOG_COUNT_FILTER_KEY_3}; AUDIT_LOG_COUNT_FILTER_KEY_4=${AUDIT_LOG_COUNT_FILTER_KEY_4}
    run keyword unless   ${AUDIT_LOG_COUNT_NO_FILTER}>${AUDIT_LOG_COUNT_FILTER_KEY_1}>0   FAIL  The condition did not meet AUDIT_LOG_COUNT_NO_FILTER>AUDIT_LOG_COUNT_FILTER_KEY_1>0
    run keyword unless   ${AUDIT_LOG_COUNT_NO_FILTER}>${AUDIT_LOG_COUNT_FILTER_KEY_2}>0   FAIL  The condition did not meet AUDIT_LOG_COUNT_NO_FILTER>AUDIT_LOG_COUNT_FILTER_KEY_2>0
    run keyword unless   ${AUDIT_LOG_COUNT_NO_FILTER}>${AUDIT_LOG_COUNT_FILTER_KEY_3}>${AUDIT_LOG_COUNT_FILTER_KEY_4}>0   FAIL  The condition did not meet AUDIT_LOG_COUNT_NO_FILTER>AUDIT_LOG_COUNT_FILTER_KEY_3>AUDIT_LOG_COUNT_FILTER_KEY_4>0

    Comment    Step 3. Checkpoint 2: All filtered log entry should contain the correspond keyword, the match should be case-insensitive
    # Checkpoint 2
    log  LOG_KEYWORD_1=${LOG_KEYWORD_1}; LOG_KEYWORD_2=${LOG_KEYWORD_2}; LOG_KEYWORD_3=${LOG_KEYWORD_3}; LOG_KEYWORD_4=${LOG_KEYWORD_4}
    FOR    ${LOG_DESC}    IN    @{AUDIT_LOG_DESC_LIST_FILTER_KEY_1}
         should contain     ${LOG_DESC}    ${LOG_KEYWORD_1}    ignore_case=True
    END
    FOR    ${LOG_DESC}    IN    @{AUDIT_LOG_DESC_LIST_FILTER_KEY_2}
         should contain     ${LOG_DESC}    ${LOG_KEYWORD_1}    ignore_case=True
    END
    FOR    ${LOG_DESC}    IN    @{AUDIT_LOG_DESC_LIST_FILTER_KEY_3}
         should contain     ${LOG_DESC}    ${LOG_KEYWORD_1}    ignore_case=True
    END
    FOR    ${LOG_DESC}    IN    @{AUDIT_LOG_DESC_LIST_FILTER_KEY_4}
         should contain     ${LOG_DESC}    ${LOG_KEYWORD_2}    ignore_case=True
    END

    Comment    Step 4. Checkpoint 3: The category of filtered log entry should equal to the correspond one
    # Checkpoint 3
    log  LOG_CATEGORY_1=${LOG_CATEGORY_1}; LOG_CATEGORY_2=${LOG_CATEGORY_2}; LOG_CATEGORY_3=${LOG_CATEGORY_3}; LOG_CATEGORY_4=${LOG_CATEGORY_4}
    FOR    ${LOG_CAT}    IN    @{AUDIT_LOG_CAT_LIST_FILTER_KEY_1}
         should be equal as strings  ${LOG_CAT}  ${LOG_CATEGORY_1}
    END
    FOR    ${LOG_CAT}    IN    @{AUDIT_LOG_CAT_LIST_FILTER_KEY_2}
         should be equal as strings  ${LOG_CAT}  ${LOG_CATEGORY_2}
    END
    FOR    ${LOG_CAT}    IN    @{AUDIT_LOG_CAT_LIST_FILTER_KEY_3}
         should be equal as strings  ${LOG_CAT}  ${LOG_CATEGORY_3}
    END
    FOR    ${LOG_CAT}    IN    @{AUDIT_LOG_CAT_LIST_FILTER_KEY_4}
         should be equal as strings  ${LOG_CAT}  ${LOG_CATEGORY_3}
    END

    Comment    Step 5. Just a commnet, mark the case PASS after pass the step2-4 checkpoints.

