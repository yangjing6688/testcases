# Author        : Abhinith Anand
# Date          : June 24th 2022
# Description   : XESS-509-Guest Manager Role: Location Selection Fix
#
# Topology      : Needs to have :
#                   - a setup where eGuest is already subscribed.
# Host ----- Cloud

*** Variables ***
${CLIENT_CONNECT_WAIT}        120
${NO_OF_VOUCHERS}   2

*** Settings ***
Force Tags  testbed_wireless

Resource    Tests/Robot/Functional/XIQ/Wireless/Extreme_Guest/Resources/email_ids.robot
Resource    Tests/Robot/Functional/XIQ/Wireless/Extreme_Guest/Resources/extreme_guest_config.robot
Resource    Tests/Robot/Functional/XIQ/Wireless/Extreme_Guest/Resources/settings.robot

Variables   TestBeds/${TESTBED}
Variables   Environments/${TOPO}
Variables   Environments/${ENV}
Variables   Environments/Config/waits.yaml

Library	    Remote 	http://${mu1.ip}:${mu1.port}   WITH NAME   Remote_Server1
Library	    Remote 	http://${mu2.ip}:${mu2.port}   WITH NAME   Remote_Server2
Resource    Tests/Robot/Functional/XIQ/Wireless/Extreme_Guest/Resources/variables.robot
Library     String

#Suite Setup      Pre Condition
#Suite Teardown   Test Suite Clean Up

*** Keywords ***
Pre Condition
    [Documentation]   AP Should be onboarded  and it is online
    ${LOGIN_USER}=                Login User                          ${tenant_username}     ${tenant_password}   url=${test_url}
    Should Be Equal As Strings    '${LOGIN_USER}'                     '1'

    ${IMPORT_MAP}=                Import Map In Network360Plan        ${MAP_FILE_NAME}
    Should Be Equal As Strings    '${IMPORT_MAP}'                     '1'
    
    ${PASSWORD_CHANGED}=          change device password              ${ap1.password}
    Should Be Equal As Strings    '${PASSWORD_CHANGED}'               '1'

    ${ONBOARD_AP1}=               Onboard AP                          ${ap1.serial}       ${ap1.make}        ${LOCATION_TREE1}
    Should Be Equal As Strings    '${ONBOARD_AP1}'                    '1'

    ${ONBOARD_AP2}=               Onboard AP                          ${ap2.serial}       ${ap2.make}        ${LOCATION_TREE2}
    Should Be Equal As Strings    '${ONBOARD_AP2}'                    '1'
    
    ${AP1_SPAWN}=                 Open Spawn                          ${ap1.ip}   ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.platform}
    Set Suite Variable            ${AP1_SPAWN}

    ${AP2_SPAWN}=                 Open Spawn                          ${ap2.ip}   ${ap2.port}      ${ap2.username}       ${ap2.password}        ${ap2.platform}
    Set Suite Variable            ${AP2_SPAWN}

    ${OUTPUT0}=                   Send Commands                       ${AP1_SPAWN}         capwap client server name ${capwap_url}, capwap client default-server-name ${capwap_url}, capwap client server backup name ${capwap_url}, no capwap client enable, capwap client enable, save config

    ${OUTPUT1}=                   Send Commands                       ${AP2_SPAWN}         capwap client server name ${capwap_url}, capwap client default-server-name ${capwap_url}, capwap client server backup name ${capwap_url}, no capwap client enable, capwap client enable, save config

    ${AP1_ONLINE}=                Wait Until Device Online            ${ap1.serial}
    Should Be Equal As Strings    '${AP1_ONLINE}'                      '1'

    ${AP2_ONLINE}=                Wait Until Device Online            ${ap2.serial}
    Should Be Equal As Strings    '${AP2_ONLINE}'                      '1'

    ${AP1_STATUS}=                Get Device Status                   device_serial=${ap1.serial}
    Should Be Equal As Strings    '${AP1_STATUS}'                     'green'

    ${AP2_STATUS}=                Get Device Status                   device_serial=${ap2.serial}
    Should Be Equal As Strings    '${AP2_STATUS}'                     'green'

    ${DELETE_POLICIES}=           Delete Network Polices              ${NW_POLICY_NAME0} ${NW_POLICY_NAME1}
    Should Be Equal As Strings    '${DELETE_POLICIES}'                      '1'

    ${DELETE_SSIDS}=              Delete SSIDs                        ${SSID_NAME0} ${SSID_NAME5}
    Should Be Equal As Strings    '${DELETE_SSIDS}'                   '1'

    Run Keyword                   Modify Suite Variables

    Run Keyword                   Create and Update Network Policies

    ${GUEST_PAGE}=                Go To Extreme Guest Page
    Should be Equal As Integers   ${GUEST_PAGE}                       1

    ${CONFIGURE_PAGE}=            Go To Configure Page
    Should be Equal As Integers   ${CONFIGURE_PAGE}                   1

    ${DEVICE_REG_TEMPLATE}=      Clone Device Registration With Social WiFi Template     template_name=${TEMPLATE3_NAME}
    Should be Equal As Integers   ${DEVICE_REG_TEMPLATE}              1

    ${USER_REG_TEMPLATE}=        Clone User Registration With Social WiFi Template       template_name=${TEMPLATE9_NAME}
    Should be Equal As Integers   ${USER_REG_TEMPLATE}                1

    ${APPLY_TEMPALTE3}=          Apply Network To User Template                          network_name=${SSID_NAME0}      template_name=${TEMPLATE3_NAME}     location=${LOCATION_TREE1}
    Should be Equal As Integers   ${APPLY_TEMPALTE3}                  1

    ${APPLY_TEMPALTE9}=          Apply Network To User Template                          network_name=${SSID_NAME5}      template_name=${TEMPLATE9_NAME}     location=${LOCATION_TREE2}
    Should be Equal As Integers   ${APPLY_TEMPALTE9}                  1

Test Suite Clean Up
    [Documentation]     Cleanup
    [Tags]              development		cleanup

    ${DELETE_AP1}=                Delete Device                       device_serial=${ap1.serial}
    Should be Equal As Integers   ${DELETE_AP1}                       1

    ${DELETE_AP2}=                Delete Device                       device_serial=${ap2.serial}
    Should be Equal As Integers   ${DELETE_AP2}                       1

    [Teardown]                    run keywords                        logout user
    ...                                                               quit browser

Modify Suite Variables
    [Documentation]    Modify Suite Variables

    ${RANDOM1}=                   Generate Random String
    Set Suite Variable            ${USER_EMAIL}                       ${USER_NAME}+${RANDOM1}@gmail.com
    Log To Console                User Email 1: ${USER_EMAIL}

    ${RANDOM2}=                   Generate Random String
    Set Suite Variable            ${OPERATOR_EMAIL}                   ${USER_NAME}+${RANDOM2}@gmail.com
    Log To Console                Operator Email 2: ${OPERATOR_EMAIL}

    Set Suite Variable            &{GUEST_MANAGEMENT_ROLE}            email=${USER_EMAIL}     name=Guest Manager     timeout=30     role=GuestManagement    organization=All Organizations
    Set Suite Variable            &{OPERATOR_ROLE}                    email=${OPERATOR_EMAIL}    name=Operator   timeout=30        role=Operator      organization=All Organizations     location=${LOCATION_TREE1}

Create and Update Network Policies
    [Documentation]    Create Network Policies

    ${CREATE_POLICY0}=            Create Network Policy               ${NW_POLICY_NAME0}      &{GUEST_OPEN_NW0}
    Should Be Equal As Strings    '${CREATE_POLICY0}'                 '1'

    ${AP1_UPDATE_CONFIG}=         Update Network Policy To AP         ${NW_POLICY_NAME0}     ap_serial=${ap1.serial}        update_method=Complete
    Should Be Equal As Strings    '${AP1_UPDATE_CONFIG}'              '1'

    ${CREATE_POLICY5}=            Create Network Policy               ${NW_POLICY_NAME5}      &{GUEST_OPEN_NW5}
    Should Be Equal As Strings    '${CREATE_POLICY5}'                 '1'

    ${AP2_UPDATE_CONFIG}=         Update Network Policy To AP         ${NW_POLICY_NAME5}     ap_serial=${ap2.serial}        update_method=Complete
    Should Be Equal As Strings    '${AP2_UPDATE_CONFIG}'              '1'

    ${AP1_ONLINE}=                Wait Until Device Online            ${ap1.serial}
    Should Be Equal As Strings    '${AP1_ONLINE}'                      '1'

    ${AP2_ONLINE}=                Wait Until Device Online            ${ap2.serial}
    Should Be Equal As Strings    '${AP2_ONLINE}'                      '1'

*** Test Cases ***
 TR-1151: Adding a single user or create user at org, site, building or floor level
    [Documentation]         Adding a single user or create user at org, site, building or floor levels
    [Tags]                  development    tr_1151

    ${LOGIN_USER}=                Login User                          ${tenant_username}     ${tenant_password}   url=${test_url}
    Should Be Equal As Strings    '${LOGIN_USER}'                     '1'

    ${GUEST_PAGE}=                Go To Extreme Guest Page
    Should be Equal As Integers   ${GUEST_PAGE}                       1

    ${CONFIGURE_PAGE}=            Go To Configure Page
    Should be Equal As Integers   ${CONFIGURE_PAGE}                   1

    ${USERNAME1}=                 Generate Random String
    Set Suite Variable            ${USERNAME1}

    Set Test Variable            ${USER_EMAIL}                ${USER_NAME}+${USERNAME1}@gmail.com

    ${CONFIG_USERS}=              Go To Configure Users Page
    Should be Equal As Integers   ${CONFIG_USERS}                     1

    ${USER_COUNT1}=               Get Extreme Guest Users Count
    Log to Console                Number of Guest Users: ${USER_COUNT1}

    ${USER_CREATED}=              Create User For Client Login        email=${USER_EMAIL}    username=${USERNAME1}    password=${USERNAME1}    access_group=${ACCESS_GROUP}    location_name=${BUILDING_LOCATION1}
    Should be Equal As Integers   ${USER_CREATED}                     1
    ${VOUCHER_CREDENTIALS1}=       Create Dictionary                   ${USERNAME1}        ${USERNAME1}
    Set Suite Variable            ${VOUCHER_CREDENTIALS1}

    ${USER_COUNT2}=               Get Extreme Guest Users Count
    Log to Console                Number of Guest Users: ${USER_COUNT2}

TR-1152: Adding bulk users or vouchers at at org, site, building or floor level
    [Documentation]         Adding bulk users or vouchers at at org, site, building or floor level
    [Tags]                  development    tr_1152
        
    ${USER_COUNT1}=               Get Extreme Guest Users Count
    Log to Console                Number of Guest Users: ${USER_COUNT1}

    ${USER_CREATED}=              Create Bulk Vouchers                ${NO_OF_VOUCHERS}    access_group=${ACCESS_GROUP}    location_name=${SITE_LOCATION}
    Should be Equal As Integers   ${USER_CREATED}                     1

    ${USER_COUNT2}=               Get Extreme Guest Users Count
    Log to Console                Number of Guest Users: ${USER_COUNT2}

TR-1153: Create a voucher for one location and use it for other location
    [Documentation]         Create a voucher for one location and use it for other location
    [Tags]                  development    tr_1153

    Remote_Server2.Connect Open Network    ${SSID_NAME5}
    Log to Console                Sleep for ${CLIENT_CONNECT_WAIT}

    BuiltIn.Sleep                 ${CLIENT_CONNECT_WAIT}
    
    ${CWP}=                       Open Guest Portal Browser             ${mu2.ip}
    Should Be Equal As Strings    '${CWP}'                              'Login to WiFi'

    ${USER_AUTH_STATUS}=          validate eguest user login with voucher credentials    ${VOUCHER_CREDENTIALS}
    Should Be Equal As Strings    '${USER_AUTH_STATUS}'                 '-1'
    get gp page screen shot

    Remote_Server2.Disconnect WiFi

TR-1154: Use invalid Vouchers or credentials for authentication
    [Documentation]         Use invalid Vouchers or credentials for authentication
    [Tags]                  development    tr_1154

    ${VOUCHER_CREDENTIALS2}=       Create Dictionary                   automation        123456
    Set Suite Variable            ${VOUCHER_CREDENTIALS2}

    Remote_Server1.Connect Open Network    ${SSID_NAME0}
    Log to Console                Sleep for ${CLIENT_CONNECT_WAIT}

    BuiltIn.Sleep                 ${CLIENT_CONNECT_WAIT}
    
    ${CWP}=                       Open Guest Portal Browser             ${mu1.ip}
    Should Be Equal As Strings    '${CWP}'                              'Login to WiFi'

    ${USER_AUTH_STATUS}=          validate eguest user login with voucher credentials    ${VOUCHER_CREDENTIALS2}
    Should Be Equal As Strings    '${USER_AUTH_STATUS}'                 '-1'
    get gp page screen shot
        

TR-1156: Validate if After redirecting to failed page, user connected back to ssid gets full internet access
    [Documentation]         Validate if After redirecting to failed page, user connected back to ssid gets full internet access
    [Tags]                  development    tr_1156

    Log to Console                Sleep for ${CLIENT_CONNECT_WAIT}

    BuiltIn.Sleep                 ${CLIENT_CONNECT_WAIT}
    
    ${CWP}=                       Open Guest Portal Browser             ${mu1.ip}
    Should Be Equal As Strings    '${CWP}'                              'Login to WiFi'
    get gp page screen shot
        

TR-1155: Use valid vouchers or credentials for autentication
    [Documentation]         Use valid vouchers or credentials for autentication
    [Tags]                  development    tr_1155
    
    ${CWP}=                       Open Guest Portal Browser             ${mu1.ip}
    Should Be Equal As Strings    '${CWP}'                              'Login to WiFi'

    ${USER_AUTH_STATUS}=          validate eguest user login with voucher credentials    ${VOUCHER_CREDENTIALS1}
    Should Be Equal As Strings    '${USER_AUTH_STATUS}'                 '1'
    get gp page screen shot

    Remote_Server1.Disconnect WiFi

TR-1159: Analyze-->Users
    [Documentation]         Analyze-->Users
    [Tags]                  development    tr_1159

TR-1160: Hyperlinks on Analyze-->Users
    [Documentation]         Hyperlinks on Analyze-->Users
    [Tags]                  development    tr_1160

TR-1161: Create User at floorlevel
    [Documentation]         Create User at floorlevel
    [Tags]                  development    tr_1161

    ${USERNAME1}=                 Generate Random String
    Set Suite Variable            ${USERNAME1}

    Set Test Variable            ${USER_EMAIL}                ${USER_NAME}+${USERNAME1}@gmail.com

    ${CONFIG_USERS}=              Go To Configure Users Page
    Should be Equal As Integers   ${CONFIG_USERS}                     1

    ${USER_COUNT1}=               Get Extreme Guest Users Count
    Log to Console                Number of Guest Users: ${USER_COUNT1}

    ${USER_CREATED}=              Create User For Client Login        email=${USER_EMAIL}    username=${USERNAME1}    password=${USERNAME1}    access_group=${ACCESS_GROUP}    location_name=${LOCATION_TREE1}
    Should be Equal As Integers   ${USER_CREATED}                     1
    ${VOUCHER_CREDENTIALS1}=       Create Dictionary                   ${USERNAME1}        ${USERNAME1}
    Set Suite Variable            ${VOUCHER_CREDENTIALS1}

    ${USER_COUNT2}=               Get Extreme Guest Users Count
    Log to Console                Number of Guest Users: ${USER_COUNT2}

TR-1162: Create User at Building level
    [Documentation]         Create User at Building level
    [Tags]                  development    tr_1162

    ${USERNAME1}=                 Generate Random String
    Set Suite Variable            ${USERNAME1}

    Set Test Variable            ${USER_EMAIL}                ${USER_NAME}+${USERNAME1}@gmail.com

    ${USER_COUNT1}=               Get Extreme Guest Users Count
    Log to Console                Number of Guest Users: ${USER_COUNT1}

    ${USER_CREATED}=              Create User For Client Login        email=${USER_EMAIL}    username=${USERNAME1}    password=${USERNAME1}    access_group=${ACCESS_GROUP}    location_name=${BUILDING_LOCATION1}
    Should be Equal As Integers   ${USER_CREATED}                     1
    ${VOUCHER_CREDENTIALS1}=       Create Dictionary                   ${USERNAME1}        ${USERNAME1}
    Set Suite Variable            ${VOUCHER_CREDENTIALS1}

    ${USER_COUNT2}=               Get Extreme Guest Users Count
    Log to Console                Number of Guest Users: ${USER_COUNT2}

TR-1163: Create User at Location level
    [Documentation]         Create User at Location level
    [Tags]                  development    tr_1163

    ${USERNAME1}=                 Generate Random String
    Set Suite Variable            ${USERNAME1}

    Set Test Variable            ${USER_EMAIL}                ${USER_NAME}+${USERNAME1}@gmail.com

    ${USER_COUNT1}=               Get Extreme Guest Users Count
    Log to Console                Number of Guest Users: ${USER_COUNT1}

    ${USER_CREATED}=              Create User For Client Login        email=${USER_EMAIL}    username=${USERNAME1}    password=${USERNAME1}    access_group=${ACCESS_GROUP}    location_name=${SITE_LOCATION}
    Should be Equal As Integers   ${USER_CREATED}                     1
    ${VOUCHER_CREDENTIALS1}=       Create Dictionary                   ${USERNAME1}        ${USERNAME1}
    Set Suite Variable            ${VOUCHER_CREDENTIALS1}

    ${USER_COUNT2}=               Get Extreme Guest Users Count
    Log to Console                Number of Guest Users: ${USER_COUNT2}

TR-1164: Create offline users
    [Documentation]         Create offline users
    [Tags]                  development    tr_1164

    ${USERNAME1}=                 Generate Random String
    Set Suite Variable            ${USERNAME1}

    Set Test Variable            ${USER_EMAIL}                ${USER_NAME}+${USERNAME1}@gmail.com

    ${USER_COUNT1}=               Get Extreme Guest Users Count
    Log to Console                Number of Guest Users: ${USER_COUNT1}

    ${USER_CREATED}=              Create User For Client Login        email=${USER_EMAIL}    username=${USERNAME1}    password=${USERNAME1}    access_group=${ACCESS_GROUP}    location_name=${BUILDING_LOCATION1}
    Should be Equal As Integers   ${USER_CREATED}                     1
    ${VOUCHER_CREDENTIALS1}=       Create Dictionary                   ${USERNAME1}        ${USERNAME1}
    Set Suite Variable            ${VOUCHER_CREDENTIALS1}

    ${USER_COUNT2}=               Get Extreme Guest Users Count
    Log to Console                Number of Guest Users: ${USER_COUNT2}

TR-1157: Create User by logging as GuestUser or HelpDesk Role
    [Documentation]         Create User by logging as GuestUser or HelpDesk Role
    [Tags]                  development    tr_1157

    ${STATUS}=              Create Role Based Account   &{GUEST_MANAGEMENT_ROLE}
    Should be Equal as Strings      '${STATUS}'    '1'

    Logout User

    ${URL}=                 Get Url To Set Password For New User        ${USER_EMAIL}      ${USER_PASSWORD}

    ${DRIVER}=              Load Web Page      url=${URL}
    
    ${result2}=             Set Password       ${TENANT_PASSWORD}
    Should Be Equal As Strings      '${result2}'     '1'
    
    Quit Browser       ${DRIVER}

    Logout User
    
    ${result3}=             Login User          ${USER_EMAIL}      ${TENANT_PASSWORD}      url=${TEST_URL}
    Should Be Equal As Strings      '${result3}'     '1'

    Navigate To Configure Guest Essentials Users

    ${USER_COUNT1}=    Get Extreme Guest Users Count
    Log to Console     Number of Guest Users: ${USER_COUNT1}

    Create Guest Management Role Bulk Vouchers            ${NO_OF_VOUCHERS}    access_group=${ACCESS_GROUP}    location_name=${LOCATION_TREE1}

    ${USER_COUNT2}=    Get Extreme Guest Users Count
    Log to Console     Number of Guest Users: ${USER_COUNT2}

TR-1158: Create User by logging as Operator
    [Documentation]         Create User by logging as Operator
    [Tags]                  development    tr_1158
