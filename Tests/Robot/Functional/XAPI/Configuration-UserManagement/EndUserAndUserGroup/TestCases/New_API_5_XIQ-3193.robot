# Author        : Subramani R
# Date          : 02 JUNE 2022
# Description   : XAPI - PPSK Usergroups and PPSK Users

# Moved to XAPI Location and modified by Subanesh Amarasekaran(samarasekaran)
# Date : 11 NOVEMBER 2022
# Separated the XAPI keywords and moved into Librarires - Robot/Libraries/XAPI/XAPI-Account-Keywords.robot

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
# robot  -v TOPO:topo.xapi-g2.yaml New_API_5_XIQ-3193.robot
#
#


*** Variables ***

${PPSK_USER_GROUP_ID}=  0

${PPSK_USER_ID}=  0
${PPSK_USERGROUP_GLOBAL}=    group3
${PPSK_USERNAME_GLOBAL}=    ppskuser1
${PPSK_USERGROUP}=    group1
${PPSK_USERNAME}=    ppskuser



*** Settings ***
Force Tags  testbed_none

Library     common/TestFlow.py
Library     common/Xapi.py
Library     common/Utils.py

Variables   Environments/${TOPO}

Resource    Tests/Robot/Libraries/XAPI/XAPI-Configuration-UserManagement-Keywords.robot


Suite Setup      Pre Condition

*** Keywords ***

Pre Condition
    [Documentation]   Login and generate access_token. Create PPSK Usergroup

# generate the key once per suite
    ${ACCESS_TOKEN}=        generate_access_token    ${tenant_username}      ${tenant_password}      login
    set global variable     ${ACCESS_TOKEN}
    
# create ppsk usergroup and set it suite variable
    ${PPSK_USER_GROUP_ID}=   xapi create ppsk user group   ${PPSK_USERGROUP_GLOBAL}
    set suite variable  ${PPSK_USER_GROUP_ID}
    skip if   ${PPSK_USER_GROUP_ID}==0


*** Test Cases ***

TCXM-6677: Create PPSK User Group
    [Documentation]         create ppsk usergroup

    [Tags]                  tcxm_6677     development

    ${UG_ID}=  xapi create ppsk user group  ${PPSK_USERGROUP}
    log     ${UG_ID}
    should be true  ${UG_ID}>0
    set suite variable      ${UG_ID}

TCXM-6676: PPSK-Get list of PPSK Gser Groups
    [Documentation]         fetch ppsk usergroups

    [Tags]                  tcxm_6676     development

    ${PPSK_USER_GROUPS_COUNT}=  xapi get ppsk usergroups
    log     ${PPSK_USER_GROUPS_COUNT}
    should be true  ${PPSK_USER_GROUPS_COUNT}>0

TCXM-16308: Create PPSK User for a particular User Group with EMAIL and SMS
    [Documentation]         Create PPSK User for a particular user group with EMAIL and SMS

    [Tags]                  tcxm_16308     development

    ${PPSK_USER_ID}=  xapi create ppsk user     ${PPSK_USER_GROUP_ID}  ${PPSK_USERNAME}
    should be true  ${PPSK_USER_ID}>0
    log     ${PPSK_USER_ID}
    skip if   ${PPSK_USER_ID}==0
    set suite variable      ${PPSK_USER_ID}

TCXM-16319: PPSK-Get list of PPSK Users
    [Documentation]         PPSK-Get list of PPSK users
    
    [Tags]                  tcxm_16319       development

    ${PPSK_USERS_COUNT}=  xapi get ppsk users   ${PPSK_USERNAME}
    log     ${PPSK_USERS_COUNT}
    should be true  ${PPSK_USERS_COUNT}>0


Test Suite Clean Up
    [Documentation]    Delete PPSK User Group(s) and PPSK User(s)

    [Tags]           tcxm_16319	development  cleanup

    [Teardown]

    skip if   ${PPSK_USER_ID}==0
    skip if   ${UG_ID}==0
    skip if   ${PPSK_USER_GROUP_ID}==0

    xapi delete ppsk usergroup  ${UG_ID}
    xapi delete ppsk usergroup   ${PPSK_USER_GROUP_ID}
    xapi delete ppsk user   ${PPSK_USER_ID}
