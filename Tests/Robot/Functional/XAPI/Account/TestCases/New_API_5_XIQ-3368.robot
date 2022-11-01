# Author        : Junjie Ma
# Date          : March 26th 2022
# Description   : XAPI - change device global default password

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
# robot  -v TOPO:topo.xapi.yaml New_API_5_XIQ-3368.robot
#
#


*** Variables ***
${DEVICE_PASSWORD_URI}=  /account/viq/default-device-password
${NEW_DEVICE_PASSWORD}=  automation123


*** Settings ***
Force Tags  testbed_3_node

Library     common/TestFlow.py
Library     common/Xapi.py
Library     common/Utils.py
Library     xiq/flows/common/Login.py
Library     xiq/flows/configure/CommonObjects.py

Resource    Tests/Robot/Libraries/XAPI/XAPI-Account-Keywords.robot

Variables   Environments/Config/waits.yaml


*** Keywords ***


*** Test Cases ***

# generate the key once per suite
Pre Condition-User-Login
    [Documentation]  XAPI User login successful
    [Tags]                  tcxm_16480     development
    ${ACCESS_TOKEN}=        generate_access_token    ${tenant_username}      ${tenant_password}      login
    log  ${ACCESS_TOKEN}
    set global variable     ${ACCESS_TOKEN}

# Get the current device default password
Pre Condition-Get-Current-Device-Password
    [Documentation]  XAPI Get current device password successful
    [Tags]                  tcxm_18342     development
    ${CUR_PASSWORD}=        xapi get default device password
    log  ${CUR_PASSWORD}
    Set Suite Variable     ${CUR_PASSWORD}


# Change the current device default password
TC-18333: change default device password
    [Documentation]         change default device password
    [Tags]                  tcxm_18333     development
    ${RESP_CODE}=   xapi change default device password    ${NEW_DEVICE_PASSWORD}
    should be true  ${RESP_CODE}==200


# Get the changed device default password
TC-18342: get default device password
    [Documentation]         get the default device password
    [Tags]                  tcxm_18342     development
    ${PASSWORD}=   xapi get default device password
    Should Be Equal As Strings    '${PASSWORD}'      '${NEW_DEVICE_PASSWORD}'

    [Teardown]
    Change Default Device Password   ${CUR_PASSWORD}
