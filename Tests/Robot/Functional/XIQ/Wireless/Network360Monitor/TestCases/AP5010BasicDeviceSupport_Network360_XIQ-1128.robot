# Author        : Barbara Sochor
# Date          : April 8th 2022
# Description   : XIQ-1128 AP5010 Basic Device Support - Network 360
# Only Devices onboarded by this automamation script can be in the location under test.
#
# Topology      :
# Host ----- AIO
#
#  To run using topo and environment:
#  ----------------------------------
#  robot -v TOPO:topology.yaml -v ENV:environment.yaml -v TESTBED:testbed.yaml XIQ-1128.robot
#
#
#  ---------------------
#  This file contains test cases.
#
#  Test Cases:
#  TCXM-18636: N360M_DeviceScoring_DeviceAvailabilityScore_100_1
#              Verifies that N360M_DEVICES_DeviceAvailabilityScore is correct.
#
########################################################################################################################

*** Variables ***
${AVAILABILITY_SCORE}       100
${SLEEP_TIME}               240s
${FLOOR_NAME}               Floor1

*** Settings ***
# import libraries
Library     xiq/flows/common/Login.py
Library     common/Utils.py
Library     common/Screen.py
Library     common/ImageHandler.py
Library     common/ScreenDiff.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/mlinsights/Network360Monitor.py
Library     common/Mu.py
Library     common/ImageAnalysis.py
Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/ExpressNetworkPolicies.py
Library     extauto/common/Cli.py
Library     extauto/common/TestFlow.py
Library     extauto/xiq/flows/common/Login.py
Library     extauto/xiq/flows/common/Navigator.py
Library     extauto/xiq/flows/manage/Client.py

Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    TestBeds/SJ/${TESTBED}
Variables    Environments/Config/device_commands.yaml

*** Test Cases ***
TCXM-18636: N360M_DeviceScoring_DeviceAvailabilityScore_100_1
    [Documentation]   Correctness of N360M Device Availability Score is verified.
#                     Assumption is that there is only 1 Device (added by this script) listed in XIQ, in this location.
    [Tags]            TCXM-18636
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${result1}=             Login User          ${TENANT_USERNAME}    ${TENANT_PASSWORD}
    should be equal as integers                 ${result1}            1
    Delete AP               ap_serial=${ap1.serial}
    ${onboard_result}=      Onboard Device      ${ap1.serial}         ${ap1.make}       location=${ap1.location}      device_os=${ap1.os}
    ${search_result}=       Search AP Serial    ${ap1.serial}
    should be equal as integers                 ${onboard_result}     1
    should be equal as integers                 ${search_result}      1
    ${AP_SPAWN}=            Open Spawn          ${ap1.console_ip}     ${ap1.console_port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=             Send Commands       ${AP_SPAWN}           capwap client server name ${CAPWAP_URL}, capwap client default-server-name ${CAPWAP_URL}, capwap client server backup name ${CAPWAP_URL}, no capwap client enable, capwap client enable, save config
    ${OUTPUT0}=             Send                ${AP_SPAWN}           ${CMD_CONSOLE_PAGE_0}
    ${OUTPUT0}=             Send                ${AP_SPAWN}           ${CMD_SHOW_VERSION_DETAIL}
    ${OUTPUT0}=             Send                ${AP_SPAWN}           ${CMD_SHOW_CAPWAP_CLIENT}
    ${OUTPUT1}=             Send                ${AP_SPAWN}           ${CMD_CAPWAP_HM_PRIMARY_NAME}
    ${OUTPUT2}=             Send                ${AP_SPAWN}           ${CMD_CAPWAP_SERVER_IP}
    ${OUTPUT3}=             Wait For CLI Output                       ${AP_SPAWN}         ${CMD_CAPWAP_CLIENT_STATE}          ${OUTPUT_CAPWAP_STATUS}
    Close Spawn             ${AP_SPAWN}
    Should Be Equal as Integers                 ${OUTPUT3}            1
    sleep     ${SLEEP_TIME}
    ${availability}     ${hw_health}     ${fw_health}=                Get Network360monitor Device Health Overall Score     ${FLOOR_NAME}
    Log to Console          DeviceAvailabilityScore ${availability}
    Should Be Equal As Integers                 ${availability}       ${AVAILABILITY_SCORE}





