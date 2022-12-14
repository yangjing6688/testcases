# Author        : Ramkumar
# Date          : September 23 2022
# Description   : Basic XIQ UI response time verification
#
# Topology      :
# Aerohive AP ----- Cloud

*** Variables ***
${FILE_NAME}               ${CURDIR}/performance.csv
${TIME_FORMAT}             %Y-%m-%d %H:%M:%S
${LOCATION}                auto_location_01, Santa Clara, building_02, floor_04
${COLUMNS}                 Tescase Name, Start Time, End Time, Elapsed Time, Testbed, VIQ ID, Datacenter Name, XIQ Version\n

*** Settings ***
Library     OperatingSystem
Library     DateTime
Library     extauto/common/Cli.py
Library     extauto/common/Utils.py
Library     extauto/common/Screen.py
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
    # Create a random string for the variables
    ${random_string}=         Get Random String

    ${POLICY_01}=              Catenate       POLICY_NAME_01_${random_string}
    ${SSID_01}=                Catenate       SSID_NAME_01_${random_string}

    Set Global Variable        ${POLICY_01}
    Set Global Variable        ${SSID_01}
    
	${LOGIN_STATUS}=              Login User          ${tenant_username}      ${tenant_password}
    should be equal as integers             ${LOGIN_STATUS}               1

    ${FLAG}=          File Exists    ${FILE_NAME}
    Run Keyword If    ${FLAG} != True     Append to file    ${FILE_NAME}  ${COLUMNS}

    ${DELETE_DEVICE}=               Delete Device                  device_serial=${ap1.serial}
    should be equal as integers     ${DELETE_DEVICE}    1

    ${POLICY_STATUS}=           Create Open Auth Express Network Policy     ${POLICY_01}      ${SSID_01}
    should be equal as integers             ${POLICY_STATUS}                1

    ${DATACENTER_NAME}=             Get Data Center Name
    Should Not be equal as Strings      '${DATACENTER_NAME}'        ${EMPTY}
    Set Global Variable  ${DATACENTER_NAME}

    ${XIQ_BUILD}=             Get Xiq Version
    Should Match Regexp      ${XIQ_BUILD}   [0-9]{1,2}\.([0-9]+\.){2}[0-9]
    Set Global Variable      ${XIQ_BUILD}

    ${VIQ_ID}=               Get VIQ ID
    Should Match Regexp      ${VIQ_ID}   [0-9]{1,4}
    Set Global Variable      ${VIQ_ID}

    [Teardown]   run keywords       logout user
    ...                             quit browser
	

Test suite Cleanup

    ${DEL_DEVICE}=                  Delete Device                  device_serial=${ap1.serial}
    should be equal as integers     ${DEL_DEVICE}                   1

    ${DELETE_NW_POLICY_STATUS}=     Delete network policy           ${POLICY_01}
    should be equal as integers     ${DELETE_NW_POLICY_STATUS}      1

    ${DELETE_SSIDS}=                Delete SSIDs                    ${SSID_01}
    should be equal as integers     ${DELETE_SSIDS}                 1

    [Teardown]  Run Keywords   Logout User
    ...                        Quit Browser


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

    [Teardown]  Run Keywords   Logout User
    ...                        Quit Browser

XIQ-10314 - TCXM-25835 - Automation: XIQ Measure time taken to Onboard device
    [Documentation]         XIQ Measure time taken to login and traverse to Manage device Page
    [Tags]                  development       tcxm-25835   client-experience
    ${LOGIN_STATUS}=         Login User          ${tenant_username}      ${tenant_password}
    Should Be Equal As Integers             ${LOGIN_STATUS}               1

    ${START_TIME}=           Get Current Date Time   time_format=${TIME_FORMAT}

    ${ONBOARD_RESULT}=       onboard device quick     ${ap1}
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
    Log To Console  DataCenter Name : ${DATACENTER_NAME}
    Log To Console  XIQ Version : ${XIQ_BUILD}

    Log To Console  \n################################################################################

    ${ADD_INFO_TO_FILE}=    Append to file    ${FILE_NAME}    ${TEST NAME}, ${START_TIME}, ${END_TIME}, ${ELAPSED_TIME} Seconds, ${TESTBED}, ${VIQID}, ${DATACENTER_NAME}, ${XIQ_BUILD}\n

    [Teardown]  Run Keywords   Logout User
    ...                        Quit Browser

XIQ-10316 - TCXM-25837 - Automation: XIQ Measure time taken to upgrade the firmware of a device
    [Documentation]         XIQ Measure time taken to upgrade the firmware of a device
    [Tags]                  development       tcxm-25837   client-experience
    ${LOGIN_STATUS}=        Login User          ${tenant_username}      ${tenant_password}
    Should Be Equal As Integers             ${LOGIN_STATUS}               1

    Save Screen Shot

    ${DEVICE_STATUS}=        Get Device Status       device_mac=${ap1.mac}
    Should contain any  ${DEVICE_STATUS}    green     config audit mismatch

    ${START_TIME}=           Get Current Date Time   time_format=${TIME_FORMAT}

    ${UPGRADE_DEVICE_STATUS}=       Upgrade Device To Latest Version       ${ap1.serial}
    Should Not be equal as Strings      '${UPGRADE_DEVICE_STATUS}'        '-1'

    ${WAIT_DEVICE_UPDATE}=        Wait Until Device Update Done         device_serial=${ap1.serial}
    should be equal as integers     ${WAIT_DEVICE_UPDATE}             1

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
    Log To Console  DataCenter Name : ${DATACENTER_NAME}
    Log To Console  XIQ Version : ${XIQ_BUILD}


    Log To Console  \n################################################################################

    ${ADD_INFO_TO_FILE}=    Append to file   ${FILE_NAME}    ${TEST NAME}, ${START_TIME}, ${END_TIME}, ${ELAPSED_TIME} Seconds, ${TESTBED}, ${VIQID}, ${DATACENTER_NAME}, ${XIQ_BUILD}\n

    [Teardown]  Run Keywords   Logout User
    ...                        Quit Browser
	
XIQ-10315 - TCXM-25836 - Automation: XIQ Measure time taken to do a Configuration Push
    [Documentation]         XIQ Measure time taken to do a Configuration push to a device
    [Tags]                  development       tcxm-25836   client-experience

    ${LOGIN_STATUS}=         Login User          ${tenant_username}      ${tenant_password}
    Should Be Equal As Integers             ${LOGIN_STATUS}                1

    ${DEVICE_STATUS}=        Get Device Status       device_mac=${ap1.mac}
    Should Be Equal As Strings        '${DEVICE_STATUS}'           'green'

    ${START_TIME}=                  Get Current Date Time     time_format=${TIME_FORMAT}

    ${deploy_status}=                 Deploy Network Policy with Complete Update      ${POLICY_01}       ${ap1.serial}
    should be equal as Integers       ${deploy_status}              1

    ${wait_till_reboots}=             Wait Until Device Reboots    ${ap1.serial}
    should be equal as integers       ${wait_till_reboots}         1

    ${device_status}=                 Get Device Status            device_mac=${ap1.mac}
    Should Be Equal As Strings        '${device_status}'           'green'

    ${END_TIME}=                    Get Current Date Time   time_format=${TIME_FORMAT}

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
    Log To Console  DataCenter Name : ${DATACENTER_NAME}
    Log To Console  XIQ Version : ${XIQ_BUILD}


    Log To Console  \n################################################################################

    ${ADD_INFO_TO_FILE}=    Append to file   ${FILE_NAME}    ${TEST NAME}, ${START_TIME}, ${END_TIME}, ${ELAPSED_TIME} Seconds, ${TESTBED}, ${VIQID}, ${DATACENTER_NAME}, ${XIQ_BUILD}\n