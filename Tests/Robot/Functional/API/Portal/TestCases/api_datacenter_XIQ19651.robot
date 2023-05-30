# Author        : Jing Yang
# Date          : 13 Jan 2023
# Description   : XIQ-19651 API display sdewan
# Note          : First supported release is 23r3

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
# robot -v TOPO:Private_Test/topo.test.yj.portal.yaml -L debug api_datacenter_XIQ19651.robot


*** Variables ***
${NAME}             US_East2


*** Settings ***

Library     extauto/common/Utils.py
Library     extauto/common/Screen.py
Library     extauto/common/Cli.py
Library     extauto/common/TestFlow.py
Library     extauto/common/Xapi.py
Library     Tests/Robot/Functional/API/Portal/Resources/Portal_Keywords.py

Resource    Tests/Robot/Libraries/API/API-Portal-Keywords.robot
Variables   Environments/${TOPO}

Force Tags  testbed_none

Suite Setup     Test Suite Setup

*** Keywords ***
Test Suite Setup
    [Documentation]  Suite setup.Api get token by internal(use base64)
    Comment     api get token by internal
    ${PORTAL_TOKEN_INTERNAL_URL}     set variable        acsportal/oauth/token
    Log    PORTAL_TOKEN_INTERNAL_URL = ${PORTAL_TOKEN_INTERNAL_URL}
    ${ACCESS_TOKEN}=  generate tokens by internal    ${internal_username}    ${internal_password}      path=${PORTAL_TOKEN_INTERNAL_URL}
    set suite variable     ${ACCESS_TOKEN}
    Log    Checking the Access Token not equal to -1
    skip if     '${ACCESS_TOKEN}' == '-1'

    
*** Test Cases ***
TCXM-56560: Check the interface returns a list of RDCs for the enabled SDWAN
    [Documentation]     TCXM-56560: Check the interface returns a list of RDCs for the enabled
    [Tags]              development  tcxm_56560
    Comment    Step 1.Check the interface returns a list of RDCs for the enabled SDWAN
    ${DARACENTER_SDWAN_CONTENT}=    api datacenter sdwan
    Log     ${DARACENTER_SDWAN_CONTENT}
    contain check    ${DARACENTER_SDWAN_CONTENT}        name      ${NAME}