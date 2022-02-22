#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for testing the onboarding of VOSS devices under various circumstances:
#                   - Using CSV file (qTest test case TC-8405 in the CSIT project)
#                   - IQAgent upgrade not required (qTest test case TC-8429 in the CSIT project)
#                   - IQAgent upgrade required (qTest test case TC-8459 in the CSIT project)

*** Settings ***
Library          OperatingSystem
Library          common/Utils.py

Resource         ../../VOSS/Resources/AllResources.robot

Force Tags       testbed_voss_node

Suite Setup      Log Into XIQ and Set Up Test
Suite Teardown   Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}                  ${xiq.test_url}
${XIQ_USER}                 ${xiq.tenant_username}
${XIQ_PASSWORD}             ${xiq.tenant_password}
${IQAGENT}                  ${xiq.sw_connection_host}

${DUT_SERIAL}               ${netelem3.serial}
${DUT_TEMPLATE}             ${netelem3.template}
${DUT_CONSOLE_IP}           ${netelem3.console_ip}
${DUT_CONSOLE_PORT}         ${netelem3.console_port}
${DUT_USERNAME}             ${netelem3.username}
${DUT_PASSWORD}             ${netelem3.password}
${DUT_PLATFORM}             ${netelem3.platform}
${NOS_DIR_OLD}              ${netelem3.nos.dir.old}
${NOS_DIR_NEW}              ${netelem3.nos.dir.new}
${NOS_VERSION_OLD}          ${netelem3.nos.version.old}
${NOS_VERSION_NEW}          ${netelem3.nos.version.new}
${IQAGENT_VERSION_OLD}      ${netelem3.iqagent_version.old}
${IQAGENT_VERSION_NEW}      ${netelem3.iqagent_version.new}

${DUT_CSV_FILE}             onboard.csv
${STATUS_UP}                green
${LOCATION}                 San Jose, building_01, floor_02


*** Test Cases ***
Test 1: VOSS Onboarding - CSV Entry Type
    [Documentation]     Confirms a VOSS device can be onboarded via the Quick Add workflow using a CSV file and has the expected status
    [Tags]              csit_tc_8405    aiq_1332    development    xiq    voss    onboarding    csv    test1

    [Setup]  Delete Device and Confirm Success  ${DUT_SERIAL}

    ${onboard_result}=  Onboard VOSS Device     ${DUT_SERIAL}  entry_type=CSV  csv_location=${DUT_CSV_FILE}  loc_name=${LOCATION}
    Should Be Equal As Integers                 ${onboard_result}       1
    Confirm Device Serial Online                ${DUT_SERIAL}
    Confirm Device Serial Has Expected Status   ${DUT_SERIAL}  ${STATUS_UP}

Test 2: VOSS Onboarding - No IQAgent Upgrade Required
    [Documentation]     Confirms a VOSS device can be onboarded successfully when IQAgent is at latest version
    [Tags]              csit_tc_8429    aiq_1332    development    xiq    voss    onboarding    no_upgrade    test2

    [Setup]  Delete Device and Confirm Success  ${DUT_SERIAL}

    # Confirm the IQAgent is already at the latest version
    Confirm IQAgent Version on VOSS Switch      ${DUT_CONSOLE_IP}  ${DUT_CONSOLE_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}  ${IQAGENT_VERSION_NEW}

    # Onboard the device and confirm it appears in the list
    Onboard VOSS Device and Confirm Success     ${DUT_SERIAL}  ${DUT_PLATFORM}

    # Confirm the device connects successfully
    Confirm Device Serial Online                ${DUT_SERIAL}
    Confirm Device Serial Has Expected Status   ${DUT_SERIAL}  ${STATUS_UP}

    # Confirm the IQAgent column shows the new version immediately after onboarding
    Confirm IQAgent Version in XIQ              ${IQAGENT_VERSION_NEW}

    # Confirm the IQAgent is still at the latest version after onboarding
    Count Down in Minutes  2
    Confirm IQAgent Version on VOSS Switch      ${DUT_CONSOLE_IP}  ${DUT_CONSOLE_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}  ${IQAGENT_VERSION_NEW}
    Confirm IQAgent Version in XIQ              ${IQAGENT_VERSION_NEW}

Test 3: VOSS Onboarding - IQAgent Upgrade Required
    [Documentation]     Confirms a VOSS device can be onboarded successfully and the IQAgent is upgraded automatically
    [Tags]              known_issue    csit_tc_8459    aiq_1332    development    xiq    voss    onboarding    upgrade    test3

    [Setup]  Delete Device and Confirm Success  ${DUT_SERIAL}

    Log To Console  KNOWN ISSUE: XIQ-686

    # Downgrade the NOS and IQAgent versions
    Downgrade NOS Version on VOSS Switch  ${DUT_CONSOLE_IP}  ${DUT_CONSOLE_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}
    Downgrade IQAgent on VOSS Switch      ${DUT_CONSOLE_IP}  ${DUT_CONSOLE_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}

    # Confirm the IQAgent is at an older version
    Confirm IQAgent Version on VOSS Switch      ${DUT_CONSOLE_IP}  ${DUT_CONSOLE_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}  ${IQAGENT_VERSION_OLD}

    # Onboard the device and confirm it appears in the list
    Onboard VOSS Device and Confirm Success     ${DUT_SERIAL}  ${DUT_PLATFORM}

    # Confirm the device connects successfully
    Confirm Device Serial Online                ${DUT_SERIAL}
    Confirm Device Serial Has Expected Status   ${DUT_SERIAL}  ${STATUS_UP}

    # Confirm the IQAgent is automatically upgraded shortly after onboarding
    Count Down in Minutes  2
    Confirm IQAgent Version on VOSS Switch      ${DUT_CONSOLE_IP}  ${DUT_CONSOLE_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}  ${IQAGENT_VERSION_NEW}
    Confirm IQAgent Version in XIQ              ${IQAGENT_VERSION_NEW}

    # Confirm the NOS is not automatically upgraded
    Confirm NOS Version on VOSS Switch          ${DUT_CONSOLE_IP}  ${DUT_CONSOLE_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}  ${NOS_VERSION_OLD}
    Refresh Devices Page
    Confirm NOS Version in XIQ                  ${NOS_VERSION_OLD}

    # Reset the NOS version to the latest
    [Teardown]  Upgrade NOS Version on VOSS Switch  ${DUT_CONSOLE_IP}  ${DUT_CONSOLE_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}


*** Keywords ***
Log Into XIQ and Set Up Test
    [Documentation]     Logs into XIQ and sets up the elements necessary to complete this test suite

    Create CSV File and Confirm Success  ${DUT_CSV_FILE}  ${DUT_SERIAL}

    Reset VOSS Switch to Factory Defaults  ${DUT_CONSOLE_IP}  ${DUT_CONSOLE_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}
    Configure IQAgent for VOSS Switch      ${DUT_CONSOLE_IP}  ${DUT_CONSOLE_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}  ${IQAGENT}

    Log Into XIQ and Confirm Success  ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}

Tear Down Test and Close Session
    [Documentation]     Cleans up test data, logs out of XIQ, closes the browser, and resets the NOS version

    Delete CSV File and Confirm Success       ${DUT_CSV_FILE}
    Clean Up Test Device and Confirm Success  ${DUT_SERIAL}

    Log Out of XIQ and Quit Browser

Onboard VOSS Device and Confirm Success
    [Documentation]     Onboards the specified device and confirms the action was successful
    [Arguments]         ${serial}  ${device_make}

    ${onboard_result}=  Onboard VOSS Device  ${serial}  ${device_make}  loc_name=${LOCATION}
    Should Be Equal As Integers  ${onboard_result}       1

Clean Up Test Device and Confirm Success
    [Documentation]     Deletes the specified device and confirms the action was successful
    [Arguments]         ${serial}

    Navigate to Devices and Confirm Success

    Delete Device and Confirm Success  ${serial}
    Confirm Device Serial Not Present  ${serial}

Downgrade NOS Version on VOSS Switch
    [Documentation]     Downgrades the NOS version on the VOSS switch to an older version
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}

    Update NOS Version on VOSS Switch   ${ip}  ${port}  ${user}  ${pwd}  ${NOS_DIR_OLD}
    Confirm NOS Version on VOSS Switch  ${ip}  ${port}  ${user}  ${pwd}  ${NOS_VERSION_OLD}

Upgrade NOS Version on VOSS Switch
    [Documentation]     Upgrades the NOS version on the VOSS switch to the latest version
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}

    Update NOS Version on VOSS SWITCH   ${ip}  ${port}  ${user}  ${pwd}  ${NOS_DIR_NEW}
    Confirm NOS Version on VOSS Switch  ${ip}  ${port}  ${user}  ${pwd}  ${NOS_VERSION_NEW}

Confirm NOS Version in XIQ
    [Documentation]     Confirms XIQ displays the specified NOS version for the VOSS switch
    [Arguments]         ${nos_version}

    ${result}=  Get Device Details  ${DUT_SERIAL}  OS VERSION
    Should Contain                  ${result}  ${nos_version}

Confirm IQAgent Version in XIQ
    [Documentation]     Confirms XIQ displays the specified IQAgent version for the VOSS switch
    [Arguments]         ${iqa_version}

    ${result}=  Get Device Details  ${DUT_SERIAL}  IQAGENT
    Should Contain                  ${result}  ${iqa_version}

Create CSV File and Confirm Success
    [Documentation]     Creates a file with the specified name and containing the specified serial number
    [Arguments]         ${file_name}  ${serial}

    File Should Not Exist     ${file_name}
    Append To File            ${file_name}  ${serial}
    File Should Exist         ${file_name}
    File Should Not Be Empty  ${file_name}

Delete CSV File and Confirm Success
    [Documentation]     Creates a file with the specified name and containing the specified serial number
    [Arguments]         ${file_name}

    Remove File            ${file_name}
    File Should Not Exist  ${file_name}
