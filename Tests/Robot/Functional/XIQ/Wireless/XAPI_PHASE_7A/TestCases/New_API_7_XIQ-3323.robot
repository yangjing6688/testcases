# Author        : Jerome Ly
# Date          : 09 Aug 2022
# Description   : XAPI - Configure device-level Bluetooth settings

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
# robot  -v TOPO:topo.test.cp1r1.yaml -v TESTBED:SJ/Dev/testbed_XIQ-3323-iBeacon.yaml New_API_7_XIQ-3323.robot
#


*** Variables ***

${MAJOR_}                       -1
${MINOR_}                       -1
${POWER_}                       -128


*** Settings ***
Force Tags  testbed_1_node

Library     common/Xapi.py
Library     common/Cli.py
Library     common/TestFlow.py
Library     common/Utils.py

Resource    Tests/Robot/Libraries/XAPI/XAPI-Authentication-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-Configuration-Policy-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-Device-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-Network-Policy-Keywords.robot

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

#Get Device ID
    ${DEVICE_ID}=               xapi list and get device id     ${ap1.serial}
    should be true              ${DEVICE_ID}>0
    set suite variable          ${DEVICE_ID}

#Assign device network policy
    ${ASSIGN_NW_POLICY}=        xapi assign network policy to a device      ${DEVICE_ID}    ${ap1.nw_policy_id}
    Should Be Equal As Integers          ${ASSIGN_NW_POLICY}      1


# iBeacon Test Cases
# ------------------------

TR-23577: get iBeacon settings
    [Documentation]         get iBeacon settings by device id
    [Tags]                  tcxm_23577   development
    Depends On              tcxm_16480
    ${RESP} =               xapi Get iBeacon Settings    ${DEVICE_ID}
    ${MAJOR_} =             get json values     ${RESP}     key=major
    ${MINOR_} =             get json values     ${RESP}     key=minor
    ${POWER_} =             get json values     ${RESP}     key=power
    should be true          0<=${MAJOR_} and ${MAJOR_}<=65635
    should be true          0<=${MINOR_} and ${MINOR_}<=65635
    should be true          -127<=${POWER_} and ${POWER_}<=127

TR-23579: update iBeacon settings
    [Documentation]         update iBeacon settings for multiple devices by IDs
    [Tags]                  tcxm_23579   development
    Depends On              tcxm_23577
    ${RESP_CODE} =          xapi Update iBeacon Settings     {"device_ids": ["${DEVICE_ID}"], "major": "10","minor": "20","power": "-100"}
    should be true          ${RESP_CODE}==200
    ${RESP} =               xapi Get iBeacon Settings       ${DEVICE_ID}
    ${major} =              get json values     ${RESP}     key=major
    ${minor} =              get json values     ${RESP}     key=minor
    ${power} =              get json values     ${RESP}     key=power
    should be true          ${major}==10
    should be true          ${minor}==20
    should be true          ${power}==-100

    [Teardown]
    ${RESP_CODE} =          xapi Update iBeacon Settings    {"device_ids": [${DEVICE_ID}],"major": ${MAJOR_},"minor": ${MINOR_},"power": ${POWER_}}
    should be true          ${RESP_CODE}==200
    ${RESP} =               xapi Get iBeacon Settings       ${DEVICE_ID}
    ${major} =              get json values     ${RESP}     key=major
    ${minor} =              get json values     ${RESP}     key=minor
    ${power} =              get json values     ${RESP}     key=power
    should be true          ${major}==${MAJOR_}
    should be true          ${minor}==${MINOR_}
    should be true          ${power}==${POWER_}

