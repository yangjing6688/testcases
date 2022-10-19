# Author        : Ramkumar
# Date          : September 23 2022
# Description   : Basic XIQ UI response time verification
#
# Topology      :
# Aerohive AP ----- Cloud

*** Variables ***
${FILE_NAME}               ${CURDIR}/performance.txt
${TIME_FORMAT}             %Y-%m-%d %H:%M:%S
${LOCATION}                auto_location_01, Santa Clara, building_02, floor_04

*** Settings ***
Library     OperatingSystem
Library     DateTime
Library     extauto/common/Cli.py
Library     extauto/common/Utils.py
Library     extauto/common/Screen.py
Library     extauto/xiq/flows/common/Login.py
Library     extauto/xiq/flows/common/Navigator.py
Library     extauto/xiq/flows/manage/Devices.py


Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/device_commands.yaml

Force Tags   testbed_1_node

Suite Setup     Cleanup-Delete Device   ${ap1.serial}

*** Keywords ***
Cleanup-Delete Device
    [Arguments]             ${SERIAL}
    ${LOGIN_STATUS}=              Login User          ${tenant_username}      ${tenant_password}
    should be equal as integers             ${LOGIN_STATUS}               1

    ${DELETE_DEVICE}=               Delete Device                  device_serial=${ap1.serial}
    should be equal as integers     ${DELETE_DEVICE}    1

    [Teardown]   run keywords       logout user
    ...                             quit browser

*** Test Cases ***
XIQ-10313 - TCXM-25834 - Automation: XIQ Measure time taken to login and traverse to Manage device Page
    [Documentation]         XIQ Measure time taken to login and traverse to Manage device Page
    [Tags]                  development      tcxm-25834    client-experience

    ${START_TIME}=          Get Current Date Time   time_format=${TIME_FORMAT}

    ${LOGIN_STATUS}=         Login User          ${tenant_username}      ${tenant_password}
    Should Be Equal As Integers             ${LOGIN_STATUS}               1

    Save Screen Shot

    ${DEVICE_PAGE}=          Navigate To Devices
    Should Be Equal As Integers             ${DEVICE_PAGE}               1

    Save Screen Shot

    ${END_TIME}=             Get Current Date Time   time_format=${TIME_FORMAT}

    ${ELAPSED_TIME}=         Subtract Date From Date   ${END_TIME}  ${START_TIME}

    ${ELAPSED_TIME} =        Convert To Integer   ${ELAPSED_TIME}

    ${VIQ_ID}=               Get VIQ ID
    Should Match Regexp      ${VIQ_ID}   [0-9]{1,4}
    Set Global Variable  ${VIQ_ID}


    Log To Console  \n\n#############################################################################\n

    Log To Console  Testcase Name : ${TEST NAME}\n
    Log To Console  Start Time : ${START_TIME}\n
    Log To Console  End Time : ${END_TIME}\n
    Log To Console  Elaspsed Time : ${ELAPSED_TIME} Seconds\n
    Log To Console  Testbed : ${TESTBED}
    Log To Console  VIQ ID : ${VIQID}

    Log To Console  \n################################################################################

    ${ADD_INFO_TO_FILE}=    Append to file    ${FILE_NAME}    Tescase Name: ${TEST NAME},Start Time: ${START_TIME},End Time: ${END_TIME},Elapsed Time: ${ELAPSED_TIME} Seconds,Testbed: ${TESTBED},Viq ID: ${VIQID}\n

    [Teardown]  Run Keywords   Logout User
    ...                        Quit Browser

XIQ-10314 - TCXM-25835 - Automation: XIQ Measure time taken to Onboard device
    [Documentation]         XIQ Measure time taken to login and traverse to Manage device Page
    [Tags]                  development       tcxm-25835   client-experience

    ${LOGIN_STATUS}=         Login User          ${tenant_username}      ${tenant_password}
    Should Be Equal As Integers             ${LOGIN_STATUS}               1

    ${START_TIME}=           Get Current Date Time   time_format=${TIME_FORMAT}

    ${ONBOARD_RESULT}=       Onboard Device      ${ap1.serial}           ${ap1.make}       location=${LOCATION}
    should be equal as integers     ${ONBOARD_RESULT}       1

    ${SEARCH_AP}=            Search AP Serial    ${ap1.serial}
    should be equal as integers     ${SEARCH_AP}        1

    ${AP_SPAWN}=             Open Spawn          ${ap1.ip}   ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.cli_type}
    Should Not be equal as Strings      '${AP_SPAWN}'        '-1'

    ${CONFIG_DEVICE}=        Configure Device To Connect To Cloud    ${ap1.cli_type}   ${capwap_url}   ${AP_SPAWN}
    Should Be Equal As Strings           ${CONFIG_DEVICE}       1

    ${CONNECTED_STATUS}=     Wait Until Device Online                ${ap1.serial}
    Should Be Equal as Integers           ${CONNECTED_STATUS}          1

    ${DEVICE_STATUS}=        Get Device Status       device_mac=${ap1.mac}
    Should contain any  ${DEVICE_STATUS}    green     config audit mismatch

    ${END_TIME}=             Get Current Date Time   time_format=${TIME_FORMAT}

    Save Screen Shot

    ${ELAPSED_TIME}=         Subtract Date From Date   ${END_TIME}  ${START_TIME}
    ${ELAPSED_TIME} =        Convert To Integer   ${ELAPSED_TIME}

    Log To Console  \n\n#############################################################################\n

    Log To Console  Testcase Name : ${TEST NAME}\n
    Log To Console  Start Time : ${START_TIME}\n
    Log To Console  End Time : ${END_TIME}\n
    Log To Console  Elaspsed Time : ${ELAPSED_TIME} Seconds\n
    Log To Console  Testbed : ${TESTBED}
    Log To Console  VIQ ID : ${VIQID}

    Log To Console  \n################################################################################

    ${ADD_INFO_TO_FILE}=    Append to file    ${FILE_NAME}    Tescase Name: ${TEST NAME},Start Time: ${START_TIME},End Time: ${END_TIME},Elapsed Time: ${ELAPSED_TIME} Seconds,Testbed: ${TESTBED}, Viq ID: ${VIQID}\n

    [Teardown]  Run Keywords   Logout User
    ...                        Quit Browser