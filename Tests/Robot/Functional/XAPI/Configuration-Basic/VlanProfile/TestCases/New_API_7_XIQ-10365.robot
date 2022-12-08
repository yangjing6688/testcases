# Author        : Dli
# Date          : 27 Oct 2022
# Description   : XAPI Automation for XIQ-4653 - Configure VLAN profile

# Moved to XAPI Location and modified by Subanesh Amarasekaran(samarasekaran)
# Date : 13 NOVEMBER 2022

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
# robot -v ENV:environment.seleniumhub.docker.chrome.yaml -v TOPO:topo.test.g2r1.yaml New_API_7_XIQ-10365.robot
#


*** Variables ***
${VLAN_PROFILE_ID}=                -1

*** Settings ***
Force Tags  testbed_none

Library     common/Xapi.py
Library     common/Cli.py
Library     common/TestFlow.py
Library     common/Utils.py

Resource    Tests/Robot/Libraries/XAPI/XAPI-Authentication-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-VLAN-Keywords.robot

Variables   Environments/Config/waits.yaml
Variables   TestBeds/${TESTBED}
Variables   Environments/${TOPO}

Suite Setup      Pre Condition

*** Keywords ***
Pre Condition
    ${ACCESS_TOKEN}=        generate_access_token    ${tenant_username}      ${tenant_password}      login
    set suite variable     ${ACCESS_TOKEN}
    log  ${ACCESS_TOKEN}
    Log    Checking the Access Token not equal to -1
    skip if     '${ACCESS_TOKEN}' == '-1'
    
*** Test Cases ***

TC-10730: List VLAN Profiles
    [Documentation]         List VLAN Profiles
    [Tags]                  tcxm_10730      development
    ${RESP}=  XAPI List VLAN Profiles
    ${count}=  get json values  ${RESP}  key=total_count
    should be true  ${count} > 0

TC-10732: Create VLAN profile
    [Documentation]         Create VLAN profile
    [Tags]                  tcxm_10732    development
    ${RESP}=  XAPI Create VLAN profile  '{"name" : "vlan-auto-create", "default_vlan_id" : "1", "enable_classification" : false}'
    ${VLAN_PROFILE_ID}=  get json values  ${RESP}  key=id
    log  ${VLAN_PROFILE_ID}
    should be true  ${VLAN_PROFILE_ID}>0
    set global variable     ${VLAN_PROFILE_ID}

TC-10733: Update a VLAN profile by id
    [Documentation]         Update a vlan profile by id
    [Tags]                  tcxm_10733     development
    ${RESP}=  XAPI Update VLAN profile  ${VLAN_PROFILE_ID}   '{"name" : "vlan-auto-update", "default_vlan_id" : 2, "enable_classification" : false}'
    ${default_vlan_id}=  get json values  ${RESP}  key=default_vlan_id
    should be equal as strings  '${default_vlan_id}'   '2'

TC-10731: Get a VLAN profile
    [Documentation]         Get a VLAN profile
    [Tags]                  tcxm_10731     development
    ${RESP}=  XAPI Get VLAN profile  ${VLAN_PROFILE_ID}
    ${RETURNED}=  get json values  ${RESP}  key=id
    should be true  ${RETURNED}==${VLAN_PROFILE_ID}

TC-10734: Delete a VLAN profile by Id
    [Documentation]         Delete a VLAN profile by Id
    [Tags]                  tcxm_10734     development
    ${RECODE}=  XAPI Delete VLAN profile  ${VLAN_PROFILE_ID}
    should be equal as strings     '${RECODE}'     '1'
