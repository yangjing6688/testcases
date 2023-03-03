# Author        : Ramkumar
# Date          : September 23 2022
# Description   : Basic XIQ UI response time verification
#
# Topology      :
# Aerohive AP ----- Cloud

*** Variables ***
${FILE_NAME}                      performance.csv
${TIME_FORMAT}                    %Y-%m-%d %H:%M:%S
${LOCATION}                       auto_location_01, Santa Clara, building_02, floor_04
${COLUMNS}                        Tescase Name, Start Time, End Time, Elapsed Time, Testbed, VIQ ID, Datacenter Name, XIQ Version\n

*** Settings ***
Library     OperatingSystem
Library     DateTime
Library     extauto/common/Cli.py
Library     extauto/common/Utils.py
Library     extauto/common/Screen.py
Library     extauto/common/TestFlow.py
Library     extauto/xiq/flows/common/Login.py
Library     extauto/xiq/flows/common/Navigator.py
Library     extauto/xiq/flows/manage/Devices.py
Library     extauto/xiq/flows/configure/NetworkPolicy.py
Library     extauto/xiq/flows/configure/ExpressNetworkPolicies.py
Library     extauto/xiq/flows/configure/CommonObjects.py


Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}

Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Force Tags   testbed_1_node

Suite Setup       Test Suite Setup
Suite Teardown    Test suite Cleanup

*** Keywords ***
Test Suite Setup
    [Documentation]     Cleanup before running the suite
    [Tags]              development  cleanup

    Log To Console      CONFIGURING PRECONDITIONS AND CLEANUP BEFORE RUNNING THE SUITE!
    # Create a random string for the variables
    ${random_string}=         Get Random String

    ${POLICY_01}=              Catenate       POLICY_NAME_01_${random_string}
    ${SSID_01}=                Catenate       SSID_NAME_01_${random_string}

    Set Global Variable        ${POLICY_01}
    Set Global Variable        ${SSID_01}

    ${NETWORK_POLICY}=       Get Variable Value  ${network_policy}
    ${SSID}=                 Get Variable Value  ${ssid}

    Set Global Variable        ${NETWORK_POLICY}
    Set Global Variable        ${SSID}

	${LOGIN_STATUS}=              Login User          ${tenant_username}      ${tenant_password}
    should be equal as integers             ${LOGIN_STATUS}               1

    ${FLAG}=          File Exists    ${FILE_NAME}
    Run Keyword If    ${FLAG} != True     Append to file    ${FILE_NAME}  ${COLUMNS}

    ${DATACENTER_NAME}=             Get Data Center Name
    Should Not be equal as Strings      '${DATACENTER_NAME}'        ${EMPTY}
    Set Global Variable  ${DATACENTER_NAME}

    ${XIQ_BUILD}=             Get Xiq Version
    Should Match Regexp      ${XIQ_BUILD}   [0-9]{1,2}\.([0-9]+\.){2}[0-9]
    Set Global Variable      ${XIQ_BUILD}

    ${VIQ_ID}=               Get VIQ ID
    Should Match Regexp      ${VIQ_ID}   [0-9]{1,4}
    Set Global Variable      ${VIQ_ID}

Test suite Cleanup
    [Documentation]     Cleanup after running the suite
    [Tags]              development  cleanup

    Log To Console      DOING CLEANUP AFTER RUNNING THE SUITE!

    IF  '${NETWORK_POLICY}' == 'None' and '${SSID}' == 'None'
        ${DELETE_NW_POLICY_STATUS}=     Delete network policy           ${POLICY_01}
        should be equal as integers     ${DELETE_NW_POLICY_STATUS}      1

        ${DELETE_SSIDS}=                Delete SSIDs                    ${SSID_01}
        should be equal as integers     ${DELETE_SSIDS}                 1
    END

    ${LOGOUT_RESULT}=               Logout User
    Should Be Equal As Integers     ${LOGOUT_RESULT}                    1

    ${QUIT_BROWSER_RESULT}=         Quit Browser
    Should Be Equal As Integers     ${QUIT_BROWSER_RESULT}              1

*** Test Cases ***

XIQ-10313 - TCXM-25834 - Automation: XIQ Measure time taken to login and traverse to Manage device Page
    [Documentation]         XIQ Measure time taken to login and traverse to Manage device Page
    [Tags]                  development      tcxm-25834    client-experience
    ${START_TIME}=          Get Current Date Time   time_format=${TIME_FORMAT}

    Save Screen Shot

    ${DEVICE_PAGE}=          Navigate To Devices
    Should Be Equal As Integers             ${DEVICE_PAGE}               1

    Save Screen Shot

    ${END_TIME}=             Get Current Date Time   time_format=${TIME_FORMAT}

    ${ELAPSED_TIME}=         Subtract Date From Date   ${END_TIME}  ${START_TIME}

    ${ELAPSED_TIME} =        Convert To Integer   ${ELAPSED_TIME}

    Log To Console  \n\n#############################################################################\n

    Log To Console  Testcase Name : ${TEST NAME}\n
    Log To Console  Start Time : ${START_TIME}\n
    Log To Console  End Time : ${END_TIME}\n
    Log To Console  Elaspsed Time : ${ELAPSED_TIME} Seconds\n
    Log To Console  Testbed : ${TESTBED}
    Log To Console  VIQ ID : ${VIQID}
    Log To Console  DataCenter Name : ${DATACENTER_NAME}
    Log To Console  XIQ Version : ${XIQ_BUILD}

    Log To Console  \n################################################################################

    ${ADD_INFO_TO_FILE}=    Append to file    ${FILE_NAME}    ${TEST NAME}, ${START_TIME}, ${END_TIME}, ${ELAPSED_TIME} Seconds, ${TESTBED}, ${VIQID}, ${DATACENTER_NAME}, ${XIQ_BUILD}\n

XIQ-10317 - TCXM-25834 - Automation: XIQ Measure time taken to login and traverse to Network Policy SSID Page
    [Documentation]         XIQ Measure time taken to login and traverse to Network Policy SSID Page
    [Tags]                  development      tcxm-258348   client-experience


    ${NETWORK_POLICY}=       Get Variable Value  ${network_policy}
    ${SSID}=                 Get Variable Value  ${ssid}

    Log To Console  ${NETWORK_POLICY}
    Log To Console  ${SSID}

    IF  '${NETWORK_POLICY}' == 'None' and '${SSID}' == 'None'
         ${POLICY_STATUS}=           Create Open Auth Express Network Policy     ${POLICY_01}      ${SSID_01}
         should be equal as integers             ${POLICY_STATUS}                1
    END

    ${START_TIME}=          Get Current Date Time   time_format=${TIME_FORMAT}

    IF  '${NETWORK_POLICY}' != 'None' and '${SSID}' != 'None'
         ${SSID_PAGE}=          open network policy ssid page      ${NETWORK_POLICY}    ${SSID}
         Should Be Equal As Integers             ${SSID_PAGE}               1
    ELSE
         ${SSID_PAGE}=          open network policy ssid page      ${POLICY_01}    ${SSID_01}
         Should Be Equal As Integers             ${SSID_PAGE}               1
    END

    Save Screen Shot

    ${END_TIME}=             Get Current Date Time   time_format=${TIME_FORMAT}

    ${ELAPSED_TIME}=         Subtract Date From Date   ${END_TIME}  ${START_TIME}

    ${ELAPSED_TIME} =        Convert To Integer   ${ELAPSED_TIME}

    Log To Console  \n\n#############################################################################\n

    Log To Console  Testcase Name : ${TEST NAME}\n
    Log To Console  Start Time : ${START_TIME}\n
    Log To Console  End Time : ${END_TIME}\n
    Log To Console  Elaspsed Time : ${ELAPSED_TIME} Seconds\n
    Log To Console  Testbed : ${TESTBED}
    Log To Console  VIQ ID : ${VIQID}
    Log To Console  DataCenter Name : ${DATACENTER_NAME}
    Log To Console  XIQ Version : ${XIQ_BUILD}

    Log To Console  \n################################################################################

    ${ADD_INFO_TO_FILE}=    Append to file    ${FILE_NAME}    ${TEST NAME}, ${START_TIME}, ${END_TIME}, ${ELAPSED_TIME} Seconds, ${TESTBED}, ${VIQID}, ${DATACENTER_NAME}, ${XIQ_BUILD}\n