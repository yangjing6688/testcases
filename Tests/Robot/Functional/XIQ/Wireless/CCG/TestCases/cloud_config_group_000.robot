# Author        : bsainath
# Date          : December 2022
# Description   : Cloud Config Group

# Topology      :
# Client -----> AP --->XIQ Instance
# Pre-Condtion
# 1. AP should be onboarded and it is online
# 2. Required Device: 3 AP
# 3. ML Insights -> Network 360 Plan -> Import MAP.
# 4. Please Configure ${LOCATION1}, &{LOCATION01} correctly based on MAP as this location will be assigned to AP1

# Execution Command :
# robot -L INFO -v TESTBED:blr_tb_1 -v DEVICE1:AP460C -v DEVICE2:AP630 -v ap3:AP410C -v TOPO:topo-1   cloud_config_group.robot
# Select the "TESTBED" ,"TOPO" and "DEVICE" variable based on Test bed

*** Variables ***
# Arguments passed from the command line
${LOCATION1}                        auto_location_01, Santa Clara, building_02, floor_04
&{LOCATION01}                       loc_node=auto_location_01                     country_node=Santa Clara           building_node=building_02            floor_node=floor_04


${USERS_CRED_EMAIL}                 extremeautomation2020@gmail.com
${USERS_CRED_EMAIL_PASS}            Symbol@123

${CCG_BULK}                         CCG
${NUM}                              11
${EMPTY}
${CCG_NAME1}                        AutoCCG1234567890123456789012345
${CCG_DESC1}                        CCG Group for AutoCCG1234567890123456789012345
${CCG_NAME2}                        CCG_MANAGE
${CCG_DESC2}                        CCG Group for CCG_MANAGE
${CCG_NAME3}                        CCG_CFD_4567
${CCG_DESC3}                        CCG Group for CCG_CFD_4567
${CCG_NAME4}                        CCG_CFD_4667
${CCG_DESC4}                        CCG Group for CCG_CFD_4667
${CCG_DUPLICATE}                    CCG_DUPLICATE
${CCG_DUPLICATE_DESC}               CCG Group for CCG_DUPLICATE
${CCG_NAME5}                        CCG_PPSK_SSID
${CCG_DESC5}                        CCG Group for CCG_PPSK_SSID
${CCG_NAME6}                        CCG_DOT1X_SSID
${CCG_DESC6}                        CCG Group for CCG_DOT1X_SSID
${RULE1_NAME}                       CLASSIFICATION_CCG
${RULE1_DESC}                       Classification Rule for CLASSIFICATION_CCG
${RULE2_NAME}                       LOCATION_RULE
${RULE2_DESC}                       Classification Rule for LOCATION
${RULE3_NAME}                       PPSK_RULE
${RULE3_DESC}                       Classification Rule for PPSK_RULE
${RULE4_NAME}                       DOT1X_RULE
${RULE4_DESC}                       Classification Rule for DOT1X_RULE
${NETWORK}                          Network_CCG
${NETWORK1}                         OPEN_CCG
${SSID_NAME}                        test_wpa_quatation
${OPEN_SSID_NAME}                   AutoOPen_Nw
${CONFIG_PUSH_SSID}                 AutoOPenNetwork
${TEST_SSID}                        TestOPenNetwork
${BULK_CLOUD_USER_GROUP}            AUTO_CLOUD_CCG_GRP
${BULK_CLOUD_NW_SSID}               AUTO_CLOUD_BULK_SSID
${ENTERPRISE_USERGROUP1}            AutoEnterprisedot1x
${ENTERPRISE_SSID}                  AutoEnterprisedot1x
${MATCH_FLAG}                       YES
${LOCATION}                 auto_location_01, Santa Clara, building_02, floor_04

*** Settings ***
Library     common/Utils.py
Library     extauto/common/Cli.py
Library     extauto/common/TestFlow.py
Library     common/LoadBrowser.py
Library     xiq/flows/common/Login.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Device360.py
Library     xiq/flows/manage/DeviceCliAccess.py
Library     xiq/flows/configure/UserGroups.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/configure/CloudConfigGroup.py
Library     xiq/flows/configure/ClassificationRule.py
Library     xiq/flows/manage/Location.py
Library     xiq/flows/globalsettings/GlobalSetting.py
Library     extauto/common/Utils.py
Library     ExtremeAutomation/Imports/CommonObjectUtils.py



Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/device_commands.yaml
Variables    Environments/Config/waits.yaml

Resource    Tests/Robot/Functional/XIQ/Wireless/CCG/Resources/cloud_config_group_config.robot

Force Tags   testbed_3_node
Suite Setup      Pre Condition
Suite Teardown    Run Keyword And Warn On Failure  Test Suite Cleanup

*** Keywords ***
Pre Condition

    # Use this method to convert the ap, wing, netelem to a generic device object
    # device1       => device1
    # wing1     => device1
    # netelem1  => device1 (EXOS / VOSS)
    #convert to generic device object   device  index=1 look_for_device_type='ap'
    #convert to generic device object   device  index=2 look_for_device_type='ap'
    #convert to generic device object   device  index=3 look_for_device_type='ap'

    ${LOGIN_STATUS}=                Login User                 ${tenant_username}     ${tenant_password}    check_warning_msg=True
    should be equal as integers     ${LOGIN_STATUS}               1

    delete network polices          ${NETWORK1}
    delete ssids                    ${SSID_NAME}        ${OPEN_SSID_NAME}       ${ENTERPRISE_SSID}      ${BULK_CLOUD_NW_SSID}
    ...                             ${TEST_SSID}

    delete user groups              ${BULK_CLOUD_USER_GROUP}        ${ENTERPRISE_USERGROUP1}
 
 

Test Suite Cleanup

    Create Network Policy           ${NETWORK1}                  ${CONFIG_PUSH_OPEN_NW_03}
    Update Network Policy To Multiple AP    policy_name=${NETWORK1}    ap_serial=${ap1.serial},${ap2.serial},${ap3.serial}

    delete network polices          ${NETWORK}
    delete ssids                    ${SSID_NAME}        ${OPEN_SSID_NAME}       ${ENTERPRISE_SSID}      ${BULK_CLOUD_NW_SSID}
    ...                             ${CONFIG_PUSH_SSID}

    delete user groups              ${BULK_CLOUD_USER_GROUP}        ${ENTERPRISE_USERGROUP1}
    delete classification rules     ${RULE1_NAME}       ${RULE2_NAME}       ${RULE3_NAME}       ${RULE4_NAME}
    delete cloud config groups      ${CCG_NAME1}        ${CCG_NAME2}        ${CCG_NAME3}        ${CCG_NAME5}        ${CCG_NAME6}
    ...                             ${CCG_DUPLICATE}    ${CCG_NAME4}
    delete bulk cloud config group     ${CCG_BULK}      ${NUM}

    ${DELETE_DEVICE_STATUS}=            Delete Device       device_serial=${ap1.serial}
    should be equal as integers     ${DELETE_DEVICE_STATUS}               1

    ${DELETE_DEVICE_STATUS}=            Delete Device       device_serial=${ap2.serial}
    should be equal as integers     ${DELETE_DEVICE_STATUS}               1

    ${DELETE_DEVICE_STATUS}=            Delete Device       device_serial=${ap3.serial}
    should be equal as integers     ${DELETE_DEVICE_STATUS}               1

    [Teardown]  run keywords       logout user
    ...                            Quit Browser


*** Test Cases ***
TCCS-7651_Step1: Onboard Aerohive AP
    [Documentation]         Checks for ap onboarding is success in case of valid scenario
    [Tags]                  production      tccs_7651       tccs_7651_step_1
    ${DELETE_DEVICE_STATUS}=            Delete Device       device_serial=${ap1.serial}
    should be equal as integers     ${DELETE_DEVICE_STATUS}               1

    ${DELETE_DEVICE_STATUS}=            Delete Device       device_serial=${ap2.serial}
    should be equal as integers     ${DELETE_DEVICE_STATUS}               1

    ${DELETE_DEVICE_STATUS}=            Delete Device       device_serial=${ap3.serial}
    should be equal as integers     ${DELETE_DEVICE_STATUS}               1

    ${CHANGE_PASSWORD_STATUS}=      Change Device Password                  Aerohive123
    should be equal as integers     ${CHANGE_PASSWORD_STATUS}               1

    ${ONBOARD_RESULT}=              onboard device quick      ${ap1}
    should be equal as integers     ${ONBOARD_RESULT}       1

    ${search_result}=               search device    device_serial=${ap1.serial}
    should be equal as integers     ${search_result}        1

    ${ONBOARD_RESULT}=              onboard device quick      ${ap2}
    should be equal as integers     ${ONBOARD_RESULT}       1

    ${search_result}=               search device    device_serial=${ap2.serial}
    should be equal as integers     ${search_result}        1

    ${ONBOARD_RESULT}=              onboard device quick      ${ap3}
    should be equal as integers     ${ONBOARD_RESULT}       1

    ${search_result}=               search device    device_serial=${ap3.serial}
    should be equal as integers     ${search_result}        1

TCCS-7651_Step2: Config AP to Report AIO and Check status
    [Documentation]     Configure Capwap client server
    [Tags]              production      tccs_7651       tccs_7651_step_2
    Depends On          TCCS-7651_Step1

    ${AP_SPAWN}=        Open Spawn          ${ap1.ip}   ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.cli_type}
    Should not be equal as Strings      '${AP_SPAWN}'        '-1'

    ${CONF_STATUS_RESULT}=      Configure Device To Connect To Cloud      ${ap1.cli_type}         ${capwap_url}       ${AP_SPAWN}
    Should Be Equal As Strings                  ${CONF_STATUS_RESULT}       1

    ${WAIT_STATUS_RESULT}=      Wait for Configure Device to Connect to Cloud       ${ap1.cli_type}         ${capwap_url}       ${AP_SPAWN}
    Should Be Equal As Strings                  ${WAIT_STATUS_RESULT}       1

    ${CONNECTED_STATUS}=    Wait Until Device Online                ${ap1.serial}
    Should Be Equal as Integers             ${CONNECTED_STATUS}          1

    ${DEVICE_STATUS}=       Get Device Status       device_serial=${ap1.serial}
    Should contain any  ${DEVICE_STATUS}    green     config audit mismatch


    ${AP_SPAWN}=        Open Spawn          ${ap2.ip}   ${ap2.port}      ${ap2.username}       ${ap2.password}        ${ap2.cli_type}
    Should not be equal as Strings      '${AP_SPAWN}'        '-1'

    ${CONF_STATUS_RESULT}=      Configure Device To Connect To Cloud      ${ap2.cli_type}         ${capwap_url}       ${AP_SPAWN}
    Should Be Equal As Strings                  ${CONF_STATUS_RESULT}       1

    ${WAIT_STATUS_RESULT}=      Wait for Configure Device to Connect to Cloud       ${ap2.cli_type}         ${capwap_url}       ${AP_SPAWN}
    Should Be Equal As Strings                  ${WAIT_STATUS_RESULT}       1

    ${CONNECTED_STATUS}=    Wait Until Device Online                ${ap2.serial}
    Should Be Equal as Integers             ${CONNECTED_STATUS}          1

    ${DEVICE_STATUS}=       Get Device Status       device_serial=${ap2.serial}
    Should contain any  ${DEVICE_STATUS}    green     config audit mismatch


    ${AP_SPAWN}=        Open Spawn          ${ap3.ip}   ${ap3.port}      ${ap3.username}       ${ap3.password}        ${ap3.cli_type}
    Should not be equal as Strings      '${AP_SPAWN}'        '-1'

    ${CONF_STATUS_RESULT}=      Configure Device To Connect To Cloud      ${ap3.cli_type}         ${capwap_url}       ${AP_SPAWN}
    Should Be Equal As Strings                  ${CONF_STATUS_RESULT}       1

    ${WAIT_STATUS_RESULT}=      Wait for Configure Device to Connect to Cloud       ${ap3.cli_type}         ${capwap_url}       ${AP_SPAWN}
    Should Be Equal As Strings                  ${WAIT_STATUS_RESULT}       1

    ${CONNECTED_STATUS}=    Wait Until Device Online                ${ap3.serial}
    Should Be Equal as Integers             ${CONNECTED_STATUS}          1

    ${DEVICE_STATUS}=       Get Device Status       device_serial=${ap3.serial}
    Should contain any  ${DEVICE_STATUS}    green     config audit mismatch

    [Teardown]    Close Spawn    ${AP_SPAWN}

TCCS-9268: CCG CommonObject Add Edit Delete
    [Documentation]    CCG CommonObject Add Edit Delete
    [Tags]             development         tccs_9268
    Depends On          TCCS-7651_Step1    TCCS-7651_Step2

    ${CREATE_NW_POLICY_STATUS}=     Create Network Policy           ${NETWORK}                  ${CONFIG_PUSH_OPEN_NW_02}
    should be equal as integers     ${CREATE_NW_POLICY_STATUS}               1

    ${UPDATE_NW_POLICY_STATUS}=     Update Network Policy To Multiple AP    policy_name=${NETWORK}    ap_serial=${ap1.serial},${ap2.serial},${ap3.serial}
    sleep                           ${CONFIG_PUSH_WAIT}
    should be equal as integers     ${UPDATE_NW_POLICY_STATUS}        1

    ${CCG_STATUS1}                  add cloud config group      ${EMPTY}        ${CCG_DESC1}        ${ap1.serial}
    should be equal as strings     '${CCG_STATUS1}'     '-2'

    ${CCG_STATUS2}                  add cloud config group      ${CCG_NAME1}        ${CCG_DESC1}        ${ap1.serial}
    should be equal as strings     '${CCG_STATUS2}'     '1'

    ${ASSIGN_CCG_POLICY}            assign cloud config group       ${CCG_NAME1}        Delta       none        ${ap2.serial}       ${ap3.serial}
    should be equal as strings     '${ASSIGN_CCG_POLICY}'     '1'

    ${EDIT_CCG_REMOVE_DEVICE}       edit cloud config group         ${CCG_NAME1}        remove           ${ap1.serial}
    should be equal as strings     '${EDIT_CCG_REMOVE_DEVICE}'     '1'

    ${EDIT_CCG_ADD_DEVICE}          edit cloud config group         ${CCG_NAME1}        add              ${ap1.serial}
    should be equal as strings     '${EDIT_CCG_ADD_DEVICE}'     '1'

    ${DELETE_CCG}                   delete cloud config group       ${CCG_NAME1}



TCCS-9271: CCG_CommonObject_Assign_Duplicate_Device_to_Group
    [Documentation]    CCG_CommonObject_Assign_Duplicate_Device_to_Group
    [Tags]             development         tccs_9271
    Depends On          TCCS-7651_Step1    TCCS-7651_Step2


    ${CCG_STATUS1}                  add cloud config group      ${CCG_NAME1}        ${CCG_DESC1}        ${ap1.serial}
    should be equal as strings     '${CCG_STATUS1}'     '1'

    ${ASSIGN_CCG_POLICY1}            assign cloud config group       ${CCG_NAME1}        Delta       None       ${ap2.serial}
    should be equal as strings     '${ASSIGN_CCG_POLICY1}'     '1'

    ${CCG_STATUS2}                  add cloud config group      ${CCG_DUPLICATE}        ${CCG_DUPLICATE_DESC}        ${ap1.serial}
    should be equal as strings     '${CCG_STATUS2}'     '1'

    ${ASSIGN_CCG_POLICY2}            assign cloud config group       ${CCG_DUPLICATE}        Delta       None       ${ap2.serial}		${ap3.serial}
    should be equal as strings     '${ASSIGN_CCG_POLICY2}'     '1'


TCCS-9342: CCG_Assign_Device_to_Exiting_Group_from_Monitor
    [Documentation]    CCG_Assign_Device_to_Exiting_Group_from_Monitor
    [Tags]             development          tccs_9342
    Depends On          TCCS-7651_Step1    TCCS-7651_Step2


    ${ASSIGN_CCG_POLICY}            assign cloud config group       ${CCG_NAME1}        Delta       Cancel      ${ap3.serial}
    should be equal as strings     '${ASSIGN_CCG_POLICY}'     '1'


TCCS-9261: CCG_Assign_Device_to_New_Create_Group_from_Monitor
    [Documentation]    CCG_Assign_Device_to_New_Create_Group_from_Monitor
    [Tags]             development         tccs_9261
    Depends On          TCCS-7651_Step1    TCCS-7651_Step2

    ${CCG_STATUS1}                  add cloud config group from manage     ${CCG_NAME2}        ${CCG_DESC2}        ${ap1.serial}
    should be equal as strings     '${CCG_STATUS1}'     '1'


TCCS-9243 : CFD_4567 Editing the SSID in the common object will remove the Classification Rules based on CCG configured for the same SSID
    [Documentation]    CFD_4567 Editing the SSID in the common object will remove the Classification Rules based on CCG configured for the same SSID
    [Tags]             development         tccs_9243
    Depends On          TCCS-7651_Step1    TCCS-7651_Step2

    ${CCG_STATUS1}                  add cloud config group from manage     ${CCG_NAME3}        ${CCG_DESC3}        ${ap1.serial}
    should be equal as strings     '${CCG_STATUS1}'     '1'

    ${SSID_ADD_STATUS}               add wireless nw to network policy           ${NETWORK}            &{WIRELESS_PESRONAL_NW4}
    should be equal as strings     '${SSID_ADD_STATUS}'     '1'

    ${CLASS_RULE_STATUS}             add classification rule with ccg        ${RULE1_NAME}       ${RULE1_DESC}        ${MATCH_FLAG}        ${CCG_NAME3}
    should be equal as strings     '${CLASS_RULE_STATUS}'     '1'

    ${RULE_SSID_STATUS}             add classification rule to ssid          ${NETWORK}          ${SSID_NAME}        ${RULE1_NAME}
    should be equal as strings     '${RULE_SSID_STATUS}'     '1'

    Update Network Policy To Multiple AP    policy_name=${NETWORK}    ap_serial=${ap1.serial},${ap2.serial},${ap3.serial}
    sleep                           ${CONFIG_PUSH_WAIT}

    ## check the config push details
    ${CONFIG_OUTPUT}               Send Cmd On Device Advanced Cli     device_serial=${ap1.serial}    cmd=show ssid
    Should Contain                 ${CONFIG_OUTPUT}         ${SSID_NAME}

    refresh devices page

    ${CONFIG_OUTPUT1}               Send Cmd On Device Advanced Cli     device_serial=${ap2.serial}    cmd=show ssid
    Should Not Contain              ${CONFIG_OUTPUT1}         ${SSID_NAME}

    ${EDIT_SSID}                    edit network policy ssid            ${NETWORK}          ${SSID_NAME}        ${SSID_NAME}
    should be equal as strings     '${EDIT_SSID}'           '1'

    ${CHECK_RULE}                   check classification rule to ssid   ${NETWORK}          ${SSID_NAME}        ${RULE1_NAME}
    should be equal as strings     '${CHECK_RULE}'           '1'



TCCS-9170: CFD-4667 Edit the CCG report error The item cannot be saved because the name null already exists
    [Documentation]    CFD-4667 Edit the CCG report error the item cannot be saved because the name null already exists
    [Tags]             development         tccs_9170
    Depends On          TCCS-7651_Step1    TCCS-7651_Step2

    ${CCG_STATUS1}                  add cloud config group from manage     ${CCG_NAME4}        ${CCG_DESC4}        ${ap1.serial}
    should be equal as strings     '${CCG_STATUS1}'     '1'

    ${EDIT_CCG_ADD_DEVICE}          edit cloud config group         ${CCG_NAME4}        add              ${ap2.serial}
    should be equal as strings     '${EDIT_CCG_ADD_DEVICE}'     '1'



TCCS-9281: CFD_4691 SSIDs configured via CCG will be seen on the device interface settings of APs that are not included in the CCG
    [Documentation]    CFD_4691 SSIDs configured via CCG will be seen on the device interface settings of APs that are not included in the CCG
    [Tags]             development         tccs_9281       tccs_9243
    Depends On          TCCS-7651_Step1    TCCS-7651_Step2   TCCS-9243


    ${AP1_INFO}                     Get Device System Information  device_mac=${ap1.mac}
    should contain                  '${AP1_INFO}[ssids]'        ${SSID_NAME}

    ${AP2_INFO}                     Get Device System Information  device_mac=${ap2.mac}
    should not contain              '${AP2_INFO}[ssids]'        ${SSID_NAME}


TCCS-9267: CFD_5201 Cannot view more than 10 cloud config group (CCG) XIQ
    [Documentation]    CFD_5201 Cannot view more than 10 cloud config group (CCG) XIQ
    [Tags]             development         tccs_9267
    Depends On          TCCS-7651_Step1    TCCS-7651_Step2


    ${CCG_STATUS1}                  create bulk cloud config group     ${CCG_BULK}        ${ap1.serial}         ${NUM}
    should be equal as strings     '${CCG_STATUS1}'     '1'

    ${CCG_STATUS2}                  delete bulk cloud config group     ${CCG_BULK}      ${NUM}
    should be equal as strings     '${CCG_STATUS2}'     '1'



TCCS-9251: CCGII_SSID_Enable_Classification_Rule_With_Location
    [Documentation]    CCGII_SSID_Enable_Classification_Rule_with_location
    [Tags]             development         tccs_9251
    Depends On          TCCS-7651_Step1    TCCS-7651_Step2

    ${SSID_ADD_STATUS}              add wireless nw to network policy           ${NETWORK}            &{CONFIG_PUSH_OPEN_NW_01}
    should be equal as strings     '${SSID_ADD_STATUS}'     '1'

    Update Network Policy To Multiple AP    policy_name=${NETWORK}    ap_serial=${ap1.serial},${ap2.serial},${ap3.serial}

    ${CLASS_RULE_STATUS}            add classification rule with location        ${RULE2_NAME}       ${RULE2_DESC}       ${LOCATION01}
    should be equal as strings     '${CLASS_RULE_STATUS}'     '1'

    ${RULE_SSID_STATUS}             add classification rule to ssid          ${NETWORK}          ${OPEN_SSID_NAME}        ${RULE2_NAME}
    should be equal as strings     '${RULE_SSID_STATUS}'     '1'

    Update Network Policy To Multiple AP    policy_name=${NETWORK}    ap_serial=${ap1.serial},${ap2.serial},${ap3.serial}
    sleep                           ${CONFIG_PUSH_WAIT}

    # check the config push details
    ${CONFIG_OUTPUT}               Send Cmd On Device Advanced Cli     device_serial=${ap1.serial}    cmd=show ssid
    Should Contain                 ${CONFIG_OUTPUT}         ${OPEN_SSID_NAME}

    refresh devices page

    ${CONFIG_OUTPUT1}               Send Cmd On Device Advanced Cli     device_serial=${ap2.serial}    cmd=show ssid
    Should Contain              ${CONFIG_OUTPUT1}         ${OPEN_SSID_NAME}

    ${DELETE_RULE}                  remove classification rule from ssid        ${NETWORK}          ${OPEN_SSID_NAME}        ${RULE2_NAME}
    should be equal as strings     '${DELETE_RULE}'     '1'

    Update Network Policy To Multiple AP    policy_name=${NETWORK}    ap_serial=${ap1.serial},${ap2.serial},${ap3.serial}
    sleep                           ${CONFIG_PUSH_WAIT}

    ${CONFIG_OUTPUT3}               Send Cmd On Device Advanced Cli     device_serial=${ap1.serial}    cmd=show ssid
    Should Contain                  ${CONFIG_OUTPUT3}         ${OPEN_SSID_NAME}

    refresh devices page

    ${CONFIG_OUTPUT4}               Send Cmd On Device Advanced Cli     device_serial=${ap2.serial}    cmd=show ssid
    Should Contain                  ${CONFIG_OUTPUT4}         ${OPEN_SSID_NAME}



TCCS-9194: CCGII_SSID_Enable_Classification_User_Group_Profile
    [Documentation]    CCGII_SSID_Enable_Classification_User_Group_Profile
    [Tags]             development         tccs_9194
    Depends On          TCCS-7651_Step1    TCCS-7651_Step2

    ${PPSK_USER_GROUP}=             Create User Group   ${BULK_CLOUD_USER_GROUP}   user_group_profile=&{USER_GROUP_PROFILE_CLOUD_BULK}
    should be equal as strings     '${PPSK_USER_GROUP}'     '1'

    ${PPSK_SSID_STATUS}              add wireless nw to network policy           ${NETWORK}            &{WIRELESS_PPSK_NW_CLOUD_BULK}
    should be equal as strings     '${PPSK_SSID_STATUS}'     '1'

    ${RADIUS_USER_GROUP}=           create user group   group_name=${ENTERPRISE_USERGROUP1}    user_group_profile=&{USER_GROUP_PROFILE_Enterprise2}
    Should Be Equal As Strings      '${RADIUS_USER_GROUP}'   '1'

    ${DOT1X_SSID_STATUS}            add wireless nw to network policy           ${NETWORK}            &{WIRELESS_ENTERPRISE_NW3}
    should be equal as strings     '${DOT1X_SSID_STATUS}'     '1'

    ${CCG_STATUS1}                  add cloud config group      ${CCG_NAME5}        ${CCG_DESC5}        ${ap1.serial}
    should be equal as strings     '${CCG_STATUS1}'     '1'

    ${CCG_STATUS2}                  add cloud config group      ${CCG_NAME6}        ${CCG_DESC6}        ${ap1.serial}       ${ap2.serial}
    should be equal as strings     '${CCG_STATUS2}'     '1'

    Update Network Policy To Multiple AP    policy_name=${NETWORK}    ap_serial=${ap1.serial},${ap2.serial},${ap3.serial}
    sleep                           ${CONFIG_PUSH_WAIT}

    # check the config push details
    ${CONFIG_OUTPUT1}               Send Cmd On Device Advanced Cli     device_serial=${ap2.serial}    cmd=show ssid
    Should Contain                  ${CONFIG_OUTPUT1}         ${BULK_CLOUD_NW_SSID}
    Should Contain                  ${CONFIG_OUTPUT1}         ${ENTERPRISE_SSID}

    refresh devices page

    ${RULE_STATUS1}                 add classification rule with ccg        ${RULE3_NAME}       ${RULE3_DESC}       ${MATCH_FLAG}       ${CCG_NAME5}
    should be equal as strings     '${RULE_STATUS1}'     '1'

    ${RULE_STATUS2}                 add classification rule with ccg        ${RULE4_NAME}       ${RULE4_DESC}       ${MATCH_FLAG}       ${CCG_NAME6}
    should be equal as strings     '${RULE_STATUS2}'     '1'

    ${RULE_SSID_STATUS1}             add classification rule to ssid          ${NETWORK}          ${BULK_CLOUD_NW_SSID}        ${RULE3_NAME}
    should be equal as strings     '${RULE_SSID_STATUS1}'     '1'

    ${RULE_SSID_STATUS2}             add classification rule to ssid          ${NETWORK}          ${ENTERPRISE_SSID}           ${RULE4_NAME}
    should be equal as strings     '${RULE_SSID_STATUS2}'     '1'

    Update Network Policy To Multiple AP    policy_name=${NETWORK}    ap_serial=${ap1.serial},${ap2.serial},${ap3.serial}
    sleep                           ${CONFIG_PUSH_WAIT}

    # check the config push details
    ${CONFIG_OUTPUT2}               Send Cmd On Device Advanced Cli     device_serial=${ap1.serial}    cmd=show ssid
    Should Contain                 ${CONFIG_OUTPUT2}         ${BULK_CLOUD_NW_SSID}
    Should Contain                 ${CONFIG_OUTPUT2}         ${ENTERPRISE_SSID}

    refresh devices page

    ${CONFIG_OUTPUT3}               Send Cmd On Device Advanced Cli     device_serial=${ap2.serial}    cmd=show ssid
    Should Not Contain                  ${CONFIG_OUTPUT3}         ${BULK_CLOUD_NW_SSID}
    Should Contain                      ${CONFIG_OUTPUT3}         ${ENTERPRISE_SSID}

    refresh devices page

    ${DELETE_RULE1}                 remove classification rule from ssid        ${NETWORK}          ${BULK_CLOUD_NW_SSID}        ${RULE3_NAME}
    should be equal as strings     '${DELETE_RULE1}'     '1'

    ${DELETE_RULE2}                 remove classification rule from ssid        ${NETWORK}          ${ENTERPRISE_SSID}           ${RULE4_NAME}
    should be equal as strings     '${DELETE_RULE2}'     '1'

    Update Network Policy To Multiple AP    policy_name=${NETWORK}    ap_serial=${ap1.serial},${ap2.serial},${ap3.serial}
    sleep                           ${CONFIG_PUSH_WAIT}

    # check the config push details
    ${CONFIG_OUTPUT4}               Send Cmd On Device Advanced Cli     device_serial=${ap1.serial}    cmd=show ssid
    Should Contain                 ${CONFIG_OUTPUT4}         ${BULK_CLOUD_NW_SSID}
    Should Contain                 ${CONFIG_OUTPUT4}         ${ENTERPRISE_SSID}

    refresh devices page

    ${CONFIG_OUTPUT5}               Send Cmd On Device Advanced Cli     device_serial=${ap2.serial}    cmd=show ssid
    Should Contain                  ${CONFIG_OUTPUT5}         ${BULK_CLOUD_NW_SSID}
    Should Contain                  ${CONFIG_OUTPUT5}         ${ENTERPRISE_SSID}
