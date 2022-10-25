# Author        : Jerome Ly
# Date          : 31 March 2022
# Description   : XAPI - Assign Devices Country Code

# Topology:
# ---------
#    ScriptHost
#      |________
#      |        |
#     Cloud     AP
# Pre-config:
# -----------
#
#

# Execution Command:
# ------------------
# robot  -v TOPO:topo.test.cp1r1.yaml -v TESTBED:SJ/Dev/xiq_sj_tb_sample.yaml New_API_5C_XIQ-3334.robot
#

*** Settings ***
Force Tags  testbed_1_node

Library     common/Xapi.py
Library     common/Cli.py
Library     common/TestFlow.py
Library     common/Utils.py

Resource    Tests/Robot/Libraries/XAPI/XAPI-Authentication-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-Device-Keywords.robot

Variables   Environments/Config/waits.yaml
Variables   TestBeds/${TESTBED}
Variables   Environments/${TOPO}


*** Test Cases ***

Pre Condition
    [Tags]                      tcxm_16480    development
#Login and Generate Access Token
    ${ACCESS_TOKEN} =           xapi login    ${tenant_username}      ${tenant_password}
    should not be empty         ${ACCESS_TOKEN}
    set suite variable          ${ACCESS_TOKEN}

#Onboard the device and save the device Id
    ${DEVICE_ONBOARD}=          xapi ap device onboard      ${ap1.serial}
    Log                         device onboard status: ${DEVICE_ONBOARD}
    Should Be Equal As Integers          ${DEVICE_ONBOARD}       1
    sleep                       ${device_onboarding_wait}
    sleep                       ${device_onboarding_wait}

#Get Device ID
    ${DEVICE_ID}=               xapi list and get device id     ${ap1.serial}
    should be true              ${DEVICE_ID}>0
    set suite variable          ${DEVICE_ID}


TC-18193: Assign Country Code to an AH-AP
    [Documentation]         Assign Country Code to an AP
    [Tags]                  xim_tcxm_18193     development
    Depends On              tcxm_16480
    ${RESP}=                xapi assign country code   ${DEVICE_ID}    ${ap1.country_code}
    Should Be Equal As Strings      '${RESP}'       '1'

    [Teardown]
    [Documentation]         removes the device
    ${RESP}=                xapi Delete Device    ${DEVICE_ID}
    Should Be Equal As Strings      '${RESP}'       '1'


