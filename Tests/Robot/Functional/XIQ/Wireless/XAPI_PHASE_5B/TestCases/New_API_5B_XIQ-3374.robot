# Author        : Yuhua Cao
# Date          : 25 Mar 2022
# Description   : XAPI - Device description

# Topology:
# ---------
#    ScriptHost
#      |________
#      |        |
#     Cloud     AP
# Pre-config:
# -----------
#Ensure the device under test has description, shoud not be null
#

# Execution Command:
# ------------------
# robot  -v TOPO:topo.test.cp1r1.yaml New_API_5B_XIQ-3374.robot
#
#


*** Variables ***
${LIST_DEVICES_URI}=  /devices?page=1&limit=10
${SAMPLE_DEVICE_ID}=  0

*** Settings ***
Force Tags  testbed_1_node

Library     common/TestFlow.py
Library     common/Xapi.py
Library     common/Utils.py
Library     xiq/flows/common/Login.py
Library     xiq/flows/configure/CommonObjects.py


Resource    ../../XAPI_PHASE_5A/Resources/AllResources.robot

Variables   Environments/Config/waits.yaml


*** Keywords ***
#####  Get sample id from devices Keywords   #####
Get Sample ID From Devices
    [Documentation]  get a sample device id from device list
    ${RESP}=  rest api get  ${LIST_DEVICES_URI}
    ${DATA}=  get json values  ${RESP}  key=data
    ${ID}=   get random id from list json  ${DATA}
    log  ${ID}
    [Return]  ${ID}

#####  Get device description Keywords   #####
Get Device Description
    [Documentation]  get device description
    [Arguments]  ${ID}
    ${RESP}=  rest api get  /devices/${ID}
    ${DESCRIPTION}=  get json values  ${RESP}  key=description
    log  ${DESCRIPTION}
    [Return]  ${DESCRIPTION}

#####  Change device description Keywords   #####
Change Device Description
    [Documentation]  change device description
    [Arguments]  ${ID}  ${DESCRIPTION}
    ${RESPCODE}=  rest api put v1  /devices/${ID}/description    ${DESCRIPTION}
    log  ${RESPCODE}
    [Return]  ${RESPCODE}




*** Test Cases ***
Pre Condition-User-Login
    [Documentation]  XAPI User login successful
    [Tags]                  xim_tc_16480     development

    ${ACCESS_TOKEN}=        generate_access_token    ${tenant_username}      ${tenant_password}      login
    log  ${ACCESS_TOKEN}
    set global variable     ${ACCESS_TOKEN}

Pre Condition-Get-Sample-Device-ID
    [Documentation]         Get a sample device ID from device list
    [Tags]                  xim_tc_18262     development

    ${SAMPLE_DEVICE_ID}=   Get Sample ID From Devices
    skip if   ${SAMPLE_DEVICE_ID}==0
    set suite variable      ${SAMPLE_DEVICE_ID}

Pre Condition-Get-Sample-Device-Description
    [Documentation]         Get a sample device description from given device ID
    [Tags]                  xim_tc_18262     development

    skip if   ${SAMPLE_DEVICE_ID}==0
    ${PRE_DESCRIPTION}=   Get Device Description   ${SAMPLE_DEVICE_ID}
    set suite variable  ${PRE_DESCRIPTION}

Pre Condition-Get-Random-Device-Description
    [Documentation]         Generate random description for update
    [Tags]                  xim_tc_18262     development

    skip if   ${SAMPLE_DEVICE_ID}==0
    ${DESCRIPTION_FOR_UPDATE}=   Get Random String
    set suite variable  ${DESCRIPTION_FOR_UPDATE}

TC-18262: Update-Device-Description
    [Documentation]         Change device description
    [Tags]                  xim_tc_18262     development

    skip if   ${SAMPLE_DEVICE_ID}==0
    ${RESP_CODE}=  Change Device Description    ${SAMPLE_DEVICE_ID}    ${DESCRIPTION_FOR_UPDATE}
    should be true  ${RESP_CODE} == 200

TC-18277: Check-Device-Description
    [Documentation]         Check device description
    [Tags]                  xim_tc_18277     development

    skip if   ${SAMPLE_DEVICE_ID}==0
    ${UPDATED_DESCRIPTION}=  Get Device Description   ${SAMPLE_DEVICE_ID}
    should be equal   ${UPDATED_DESCRIPTION}      ${DESCRIPTION_FOR_UPDATE}

    [Teardown]
    Change Device Description   ${SAMPLE_DEVICE_ID}    ${PRE_DESCRIPTION}
    ${CURRENT_DESCRIPTION}=  Get Device Description   ${SAMPLE_DEVICE_ID}
    should be equal   ${CURRENT_DESCRIPTION}      ${PRE_DESCRIPTION}
