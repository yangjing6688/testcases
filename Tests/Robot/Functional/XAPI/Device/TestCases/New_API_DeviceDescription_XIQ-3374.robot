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
# robot -v TOPO:topo.xapi-g2.yaml -v TESTBED:BANGALORE/testbed_all_SubramaniVR.yaml -L DEBUG New_API_5B_XIQ-3374.robot
#


*** Variables ***
${SAMPLE_DEVICE_ID}=  0


*** Settings ***
Force Tags  testbed_1_node

Library     common/TestFlow.py
Library     common/Xapi.py
Library     common/Utils.py
Library     xiq/flows/common/Login.py
Library     xiq/flows/configure/CommonObjects.py
Library      ExtremeAutomation/Imports/CommonObjectUtils.py

Resource    Tests/Robot/Libraries/XAPI/XAPI-Authentication-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-Configuration-Deployment-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-Network-Policy-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-Device-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-Location-Keywords.robot


Variables   Environments/Config/waits.yaml
Variables   TestBeds/${TESTBED}
Variables   Environments/${TOPO}


Suite Setup     Pre Condition
Suite Teardown  Test Suite Clean Up

*** Keywords ***
Pre Condition

    ${ACCESS_TOKEN}=        generate_access_token    ${tenant_username}      ${tenant_password}      login
    log  ${ACCESS_TOKEN}
    set global variable     ${ACCESS_TOKEN}

# Use this method to convert the ap, wing, netelem variable names to a generic device objec
    # device1       => device1
    # wing1     => device1
    # netelem1  => device1 (EXOS / VOSS)
    convert to generic device object   device  index=1
    log to console  ${device1.serial}

#Onboard and Get Sample Device ID
    ${DEVICE_ONBOARD}=               xapi ap device onboard      ${device1.serial}
    Log    Validating the Successful Device Onboard
    Should Be Equal As Integers          ${DEVICE_ONBOARD}       1
    sleep    ${device_onboarding_wait}

    ${SPAWN_CONNECTION}=      Open Spawn    ${device1.ip}     ${device1.port}   ${device1.username}   ${device1.password}    ${device1.cli_type}
    configure_device_to_connect_to_cloud    ${device1.cli_type}       ${capwap_url}      ${SPAWN_CONNECTION}

    ${SAMPLE_DEVICE_ID}=            xapi list and get device id     ${device1.serial}
    skip if   ${SAMPLE_DEVICE_ID}==0
    skip if   ${SAMPLE_DEVICE_ID}==-1
    set suite variable         ${SAMPLE_DEVICE_ID}

#Get-Sample-Device-Description
    skip if   ${SAMPLE_DEVICE_ID}==0
    ${PRE_DESCRIPTION}=   Get Random String
    set suite variable  ${PRE_DESCRIPTION}

#Get-Random-Device-Description
    skip if   ${SAMPLE_DEVICE_ID}==0
    ${DESCRIPTION_FOR_UPDATE}=   Get Random String
    set suite variable  ${DESCRIPTION_FOR_UPDATE}



Test Suite Clean Up

#Delete Device

    ${DELETE_RESP}=              xapi delete device        ${SAMPLE_DEVICE_ID}
    Log    Validating the Successful Delete of Device
    Should Be Equal As Integers      ${DELETE_RESP}       1


*** Test Cases ***

TC-18262: Add Device Description To Device Onboarded
    [Documentation]         Change device description

    [Tags]                  tcxm_18262     development

    skip if   ${SAMPLE_DEVICE_ID}==0
    ${RESP_CODE}=  xapi change device description    ${SAMPLE_DEVICE_ID}    ${PRE_DESCRIPTION}
    should be true  ${RESP_CODE} == 200

    ${UPDATED_DESCRIPTION}=  xapi get device description   ${SAMPLE_DEVICE_ID}
    should be equal   ${UPDATED_DESCRIPTION}        ${PRE_DESCRIPTION}


TC-18277: Update and Check-Device-Description
    [Documentation]         Check device description

    [Tags]                  tcxm_18277     development

    depends on  TC-18262
    skip if   ${SAMPLE_DEVICE_ID}==0
    ${RESP_CODE}=  xapi change device description    ${SAMPLE_DEVICE_ID}    ${DESCRIPTION_FOR_UPDATE}
    should be true  ${RESP_CODE} == 200

    ${UPDATED_DESCRIPTION}=  xapi get device description   ${SAMPLE_DEVICE_ID}
    should be equal   ${UPDATED_DESCRIPTION}        ${DESCRIPTION_FOR_UPDATE}


TC-28015: Set Blank Device-Description
    [Documentation]         Check device description

    [Tags]                  tcxm_28015     development

    depends on  TC-18277
    ${CURRENT_DESCRIPTION_VALUE}=  xapi change device description   ${SAMPLE_DEVICE_ID}    ${EMPTY}
    should contain   ${CURRENT_DESCRIPTION_VALUE}      BAD_REQUEST
    ${CURRENT_DESCRIPTION}=  xapi get device description   ${SAMPLE_DEVICE_ID}
    should contain   ${CURRENT_DESCRIPTION}      ${DESCRIPTION_FOR_UPDATE}
