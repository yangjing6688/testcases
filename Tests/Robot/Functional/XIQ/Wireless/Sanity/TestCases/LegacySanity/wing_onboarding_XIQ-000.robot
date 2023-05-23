# Author        : Rameswar
# Date          : January 15th 2020
# Description   : Basic Login Test Cases
#
# Topology      :
# Host ----- Cloud

*** Variables ***
${SSH_TIMEOUT}              5min
${SSH_ACTIVE}               SSH Active

*** Settings ***
Library     Collections
Library     common/Utils.py
Library     extauto/common/Cli.py
Library     common/Rest.py
Library     common/Screen.py
Library     common/TestFlow.py
Library     xiq/flows/manage/Tools.py

# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     xiq/flows/common/Navigator.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Device360.py
Library     xiq/flows/globalsettings/GlobalSetting.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Force Tags   testbed_1_node

Suite Teardown  Test Suite Clean Up

*** Keywords ***

Test Suite Clean Up
    [Documentation]     Cleanup

    [Tags]              production		cleanup

    ${LOGIN_STATUS}=                Login User          ${tenant_username}      ${tenant_password}
    should be equal as integers     ${LOGIN_STATUS}               1

    ${DELETE_STATUS}=               Delete Device       device_serial=${wing1.serial}
    Should be Equal As Integers     ${DELETE_STATUS}      1

    [Teardown]   run keywords       logout user
    ...                             quit browser

*** Test Cases ***
TCCS-7279_Step1: Onboard WiNG AP
    [Documentation]         Checks for ap onboarding is success in case of valid scenario

    [Tags]                  production      tccs_7279   tccs_7279_step1

    ${LOGIN_STATUS}=                Login User          ${tenant_username}      ${tenant_password}     check_warning_msg=True
    should be equal as integers     ${LOGIN_STATUS}               1

    ${DELETE_STATUS}=               Delete Device           device_serial=${wing1.serial}
    Should be Equal As Integers     ${DELETE_STATUS}      1

    ${ONBOARD_RESULT}=              onboard device quick         ${wing1}
    Should Be Equal As Integers     ${ONBOARD_RESULT}           1

    ${search_result}=               search device    device_serial=${wing1.serial}
    should be equal as integers     ${search_result}        1

    [Teardown]      run keywords    logout user
     ...                            quit browser

TCCS-7279_Step2: Config AP to Report XIQ
    [Documentation]     Configure Capwap client server

    [Tags]              production      tccs_7279   tccs_7279_step2

    Depends On          TCCS_7279_Step1

    ${SPAWN_CONNECTION}=      Open Spawn    ${wing1.ip}     ${wing1.port}   ${wing1.username}   ${wing1.password}    ${wing1.cli_type}

    ${CONF_STATUS_RESULT}=      Configure Device To Connect To Cloud    ${wing1.cli_type}     ${wing_capwap_url}      ${SPAWN_CONNECTION}
    Should Be Equal As Strings                  ${CONF_STATUS_RESULT}       1

    [Teardown]      Close Spawn         ${SPAWN_CONNECTION}

TCCS-7279_Step3: Check AP Status On UI
    [Documentation]     Checks for ap status

    [Tags]              production      tccs_7279   tccs_7279_step3

    Depends On          TCCS-7279_Step2
    ${LOGIN_STATUS}=                Login User          ${tenant_username}      ${tenant_password}
    should be equal as integers     ${LOGIN_STATUS}               1

    ${CONNECTED_STATUS}=            Wait Until Device Online                ${wing1.serial}
    Should Be Equal as Integers     ${CONNECTED_STATUS}          1

    ${DEVICE_STATUS}=               Get Device Status       device_mac=${wing1.serial}
    Should contain any              ${DEVICE_STATUS}    green     config audit mismatch

    [Teardown]      run keywords    logout user
     ...                            quit browser

TCCS-7279_Step4: Check for SSH CLI Reachability
    [Documentation]     Check for SSH CLI Reachability

    [Tags]              production      tccs_7279   tccs_7279_step4

    Depends On          TCCS-7279_Step3

    ${LOGIN_STATUS}=                Login User          ${tenant_username}      ${tenant_password}
    should be equal as integers     ${LOGIN_STATUS}               1

    ${ENABLE_SSH}=                  Enable SSH Availability
    should be equal as integers     ${ENABLE_SSH}               1

    Navigate To Devices

	&{ip_port_info}=                Device360 Enable SSH CLI Connectivity     device_mac=${wing1.mac}    run_time=5

    ${IP_ADDR}=                     Get From Dictionary  ${ip_port_info}  ip
    ${PORT_NUM}=                    Get From Dictionary  ${ip_port_info}  port

    Should not be Empty     ${IP_ADDR}
    Should not be Empty     ${PORT_NUM}

    ${SPAWN1}=                      Open Spawn      ${IP_ADDR}    ${PORT_NUM}     ${wing1.username}   ${wing1.password}   ${wing1.cli_type}
    Should Not be Equal As Strings  '${SPAWN1}'       '-1'

    ${OUTPUT1}=                     Send Commands       ${SPAWN1}       en, show version
    Should Contain                  ${OUTPUT1}          Extreme Networks, Inc.

    Close spawn         ${SPAWN1}

    ${SSH STATUS}=                  UI SSH Status Check
    should be equal as strings              ${SSH STATUS}   ${SSH_ACTIVE}

    Sleep               ${SSH_TIMEOUT}

    ${SPAWN1}=                      Open Paramiko Ssh Spawn     ${IP_ADDR}    ${wing1.username}   ${wing1.password}     ${PORT_NUM}
    Should be Equal As Strings      '${SPAWN1}'       '-1'

    [Teardown]   run keywords       logout user
    ...                             quit browser

#   Commenting the test case based on AIQ-1611
#TCCS-7279_Step5: Check for SSH WEB Reachability
#    [Documentation]     Check for SSH WEB Reachability
#
#    [Tags]              production      tccs_7279_step5
#    Depends On          tccs_7279_step1               tccs_7279_step2               tccs_7279_step3           tccs_7279_step4
#    ${result}=          Login User          ${tenant_username}     ${tenant_password}
#
#    ${URL}=             Device360 Enable SSH WEB Connectivity   device_name=${wing1.name}         run_time=5
#    Log                 ${URL}
#    ${RESULT1}=           CURL COMMAND       ${URL}
#    Should be Equal As Integers         ${RESULT1}      200
#    Log To Console       ${RESULT1}
#
#    ${RESULT2}=         Device360 Disable SSH WEB Connectivity   device_name=${wing1.name}
#    Should be Equal As Integers         ${RESULT2}      1
#    Sleep                   30
#
#    ${RESULT2}=           CURL COMMAND       ${URL}
#    Should be Equal As Integers         ${RESULT2}      0
#
#    [Teardown]   run keywords       logout user
#    ...                             quit browser
