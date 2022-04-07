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


Resource    ../../XAPI_PHASE_5A/Resources/AllResources.robot

Variables   Environments/Config/waits.yaml


*** Keywords ***

#####  Get default device password Keywords   #####
Get Default Device Password
    [Documentation]  get the default device password
    ${RESP}=  rest api get  ${DEVICE_PASSWORD_URI}
    ${PASSWORD}=  get json values  ${RESP}  key=password
    log  ${PASSWORD}
    [Return]  ${PASSWORD}

#####  Change default device password Keywords   #####
Change Default Device Password
    [Documentation]  change device password
    [Arguments]  ${PASSWORD}
    ${RESPCODE}=  rest api put v1  ${DEVICE_PASSWORD_URI}    ${PASSWORD}
    [Return]  ${RESPCODE}

*** Test Cases ***

# generate the key once per suite
Pre Condition-User-Login
    [Documentation]  XAPI User login successful
    [Tags]                  xim_tcxm_16480     development
    ${ACCESS_TOKEN}=        generate_access_token    ${tenant_username}      ${tenant_password}      login
    log  ${ACCESS_TOKEN}
    set global variable     ${ACCESS_TOKEN}

# Get the current device default password
Pre Condition-Get-Current-Device-Password
    [Documentation]  XAPI Get current device password successful
    [Tags]                  xim_tcxm_18342     development
    ${CUR_PASSWORD}=        get default device password
    log  ${CUR_PASSWORD}
    Set Suite Variable     ${CUR_PASSWORD}


# Change the current device default password
TC-18333: change default device password
    [Documentation]         change default device password
    [Tags]                  xim_tcxm_18333     development
    ${RESP_CODE}=   change default device password    ${NEW_DEVICE_PASSWORD}
    should be true  ${RESP_CODE}==200


# Get the changed device default password
TC-18342: get default device password
    [Documentation]         get the default device password
    [Tags]                  xim_tcxm_18342     development
    ${PASSWORD}=   get default device password
    Should Be Equal As Strings    '${PASSWORD}'      '${NEW_DEVICE_PASSWORD}'

    [Teardown]
    Change Default Device Password   ${CUR_PASSWORD}
