# Author        : Junjie Ma
# Date          : March 26th 2022
# Description   : XAPI - change device global default password

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
# robot  -v TOPO:topo.xapi.yaml New_API_5_XIQ-3368.robot
#
#


*** Variables ***

${NEW_DEVICE_PASSWORD}=  automation123


*** Settings ***
Force Tags  testbed_none

Library     common/TestFlow.py
Library     common/Xapi.py
Library     common/Utils.py


Resource    Tests/Robot/Libraries/XAPI/XAPI-Account-Keywords.robot

Variables   Environments/Config/waits.yaml

Suite Setup      Pre Condition

*** Keywords ***
Pre Condition
    ${ACCESS_TOKEN}=        generate_access_token    ${tenant_username}      ${tenant_password}      login
    set suite variable     ${ACCESS_TOKEN}
    log  ${ACCESS_TOKEN}
    Log    Checking the Access Token not equal to -1
    skip if     '${ACCESS_TOKEN}' == '-1'
    
*** Test Cases ***

# Get the current device default password
Pre Condition-Get-Current-Device-Password
    [Documentation]  XAPI Get current device password 
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
