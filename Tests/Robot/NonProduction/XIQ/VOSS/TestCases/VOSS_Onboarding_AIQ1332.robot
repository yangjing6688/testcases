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
Resource         ExtremeAutomation/Resources/Libraries/DefaultLibraries.robot

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
${DUT_IP}                   ${netelem3.ip}
${DUT_PORT}                 ${netelem3.port}
${DUT_USERNAME}             ${netelem3.username}
${DUT_PASSWORD}             ${netelem3.password}
${DUT_PLATFORM}             ${netelem3.platform}
${NOS_DIR_OLD}              ${netelem3.nos.dir.old}
${NOS_DIR_NEW}              ${netelem3.nos.dir.new}
${NOS_VERSION_OLD}          ${netelem3.nos.version.old}
${NOS_VERSION_NEW}          ${netelem3.nos.version.new}
${IQAGENT_VERSION_OLD}      ${netelem3.iqagent_version.old}
${IQAGENT_VERSION_NEW}      ${netelem3.iqagent_version.new}
${DUT_MAKE}                 ${netelem3.make}
${DUT_CLI_TYPE}             ${netelem3.cli_type}
${DUT_NAME}                 ${netelem3.name}

#Please be aware that you should make sure that you have a good configuration on device named 'config_VOSS.cfg', if not the test will fail
${CONFIG_FILE}              "config_VOSS"
${DUT_CSV_FILE}             onboard.csv
${STATUS_UP}                green
${LOCATION}                 San Jose, building_01, floor_02


*** Test Cases ***
Test 1: Test Device Onboarding - CSV Entry Type
    [Documentation]     Confirms a VOSS device can be onboarded via the Quick Add workflow using a CSV file and has the expected status
    [Tags]              tccs_8405    aiq_1332    development    xiq    voss    onboarding    csv    test1

    [Setup]  Delete Device and Confirm Success  ${DUT_SERIAL}

    ${onboard_result}=  onboard device quick     ${netelem3}
    Should Be Equal As Integers                 ${onboard_result}       1

    Confirm Device Serial Online                ${DUT_SERIAL}
    Confirm Device Serial Has Expected Status   ${DUT_SERIAL}  ${STATUS_UP}

Test 2: Test Device Onboarding - No IQAgent Upgrade Required
    [Documentation]     Confirms a VOSS device can be onboarded successfully when IQAgent is at latest version
    [Tags]              tccs_8429    aiq_1332    development    xiq    voss    onboarding    no_upgrade    test2

    [Setup]  Delete Device and Confirm Success  ${DUT_SERIAL}

    # Confirm the IQAgent is already at the latest version
    Confirm IQAgent Version on Test Device      ${DUT_IP}  ${DUT_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}  ${IQAGENT_VERSION_NEW}

    # Onboard the device and confirm it appears in the list
    Onboard VOSS Device and Confirm Success     ${DUT_SERIAL}  ${DUT_MAKE}    ${netelem3}

    # Confirm the device connects successfully
    Confirm Device Serial Online                ${DUT_SERIAL}
    Confirm Device Serial Has Expected Status   ${DUT_SERIAL}  ${STATUS_UP}

    # Confirm the IQAgent column shows the new version immediately after onboarding
    Confirm IQAgent Version in XIQ              ${IQAGENT_VERSION_NEW}

    # Confirm the IQAgent is still at the latest version after onboarding
    Count Down in Minutes  2
    Confirm IQAgent Version on Test Device      ${DUT_IP}  ${DUT_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}  ${IQAGENT_VERSION_NEW}
    Confirm IQAgent Version in XIQ              ${IQAGENT_VERSION_NEW}

Test 3: Test Device Onboarding - IQAgent Upgrade Required
    [Documentation]     Confirms a VOSS device can be onboarded successfully and the IQAgent is upgraded automatically
    [Tags]              known_issue    tccs_8459    aiq_1332    development    xiq    voss    onboarding    upgrade    test3

    [Setup]  Delete Device and Confirm Success  ${DUT_SERIAL}

    Log To Console  KNOWN ISSUE: XIQ-686

    # Downgrade the NOS and IQAgent versions
    Downgrade NOS Version on Test Device        ${DUT_IP}  ${DUT_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}
    Downgrade IQAgent on Test Device            ${DUT_IP}  ${DUT_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}

    ${SW_SPAWN}=                        Open Spawn          ${DUT_IP}       ${DUT_PORT}      ${DUT_USERNAME}       ${DUT_PASSWORD}        ${DUT_CLI_TYPE}
    ${DOWNGRADE_IQAGENT}=               Downgrade iqagent      ${DUT_CLI_TYPE}     ${SW_SPAWN}
    Should Be Equal As Integers         ${DOWNGRADE_IQAGENT}       1
    Close Spawn     ${SW_SPAWN}

    # Confirm the IQAgent is at an older version
    Confirm IQAgent Version on Test Device      ${DUT_IP}  ${DUT_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}  ${IQAGENT_VERSION_OLD}

    # Onboard the device and confirm it appears in the list
    Onboard VOSS Device and Confirm Success     ${DUT_SERIAL}  ${DUT_MAKE}   ${netelem3}

    # Confirm the device connects successfully
    Confirm Device Serial Online                ${DUT_SERIAL}
    Confirm Device Serial Has Expected Status   ${DUT_SERIAL}  ${STATUS_UP}

    # Confirm the IQAgent is automatically upgraded shortly after onboarding
    Count Down in Minutes  2
    Confirm IQAgent Version on Test Device      ${DUT_IP}  ${DUT_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}  ${IQAGENT_VERSION_NEW}
    Confirm IQAgent Version in XIQ              ${IQAGENT_VERSION_NEW}

    # Confirm the NOS is not automatically upgraded
    Confirm NOS Version on Test Device          ${DUT_IP}  ${DUT_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}  ${NOS_VERSION_OLD}
    Refresh Devices Page
    Confirm NOS Version in XIQ                  ${NOS_VERSION_OLD}

    # Reset the NOS version to the latest
    [Teardown]  Upgrade NOS Version on Test Device   ${DUT_IP}  ${DUT_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}


*** Keywords ***
Log Into XIQ and Set Up Test
    [Documentation]     Logs into XIQ and sets up the elements necessary to complete this test suite

    Create CSV File and Confirm Success     ${DUT_CSV_FILE}  ${DUT_SERIAL}
    Configure Test Device                   ${DUT_IP}  ${DUT_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}  ${DUT_CLI_TYPE}  ${IQAGENT}    ${DUT_NAME}    ${CONFIG_FILE}

    Log Into XIQ and Confirm Success        ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}

Tear Down Test and Close Session
    [Documentation]     Cleans up test data, logs out of XIQ, closes the browser, and resets the NOS version

    Delete CSV File and Confirm Success       ${DUT_CSV_FILE}
    Clean Up Test Device and Confirm Success  ${DUT_SERIAL}

    Log Out of XIQ and Quit Browser

Configure Test Device
    [Documentation]     Configures the specified test device by rebooting a known good configuration file and then configuring the iqagent
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${cli_type}  ${agent}    ${dut_name}    ${config_file}

    #Boot the Test Device to a known good configuration
    Connect to all network elements
    reboot_network_element_with_config      ${dut_name}      ${config_file}
    close_connection_to_all_network_elements

    ${SPAWN_CONNECTION}=      Open Spawn       ${ip}  ${port}  ${user}  ${pwd}  ${cli_type}
    # Downgrade the device's iqagent if needed
    ${DOWNGRADE_IQAGENT}=     Downgrade Iqagent        ${cli_type}      ${SPAWN_CONNECTION}
    Should Be Equal As Integers                 ${DOWNGRADE_IQAGENT}        1

    ${CONF_STATUS_RESULT}=    Configure Device To Connect To Cloud    ${cli_type}      ${agent}     ${SPAWN_CONNECTION}
    Should Be Equal As Strings                  ${CONF_STATUS_RESULT}       1

    Close Spawn       ${SPAWN_CONNECTION}

Onboard Device and Confirm Success
    [Documentation]     Onboards the specified device and confirms the action was successful
    [Arguments]         ${serial}  ${location}  ${csv_file}    ${device}

    ${onboard_result}=  onboard device quick    ${device}
    Should Be Equal As Integers  ${onboard_result}       1

Onboard VOSS Device and Confirm Success
    [Documentation]     Onboards the specified device and confirms the action was successful
    [Arguments]         ${serial}  ${make}    ${device}

    ${onboard_result}=  onboard device quick    ${device}
    Should Be Equal As Integers  ${onboard_result}       1

Clean Up Test Device and Confirm Success
    [Documentation]     Deletes the specified device and confirms the action was successful
    [Arguments]         ${serial}

    Navigate to Devices and Confirm Success

    Delete Device and Confirm Success  ${serial}
    Confirm Device Serial Not Present  ${serial}

Downgrade NOS Version on Test Device
    [Documentation]     Downgrades the NOS version on the VOSS switch to an older version
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}

    Update NOS Version on Test Device    ${ip}  ${port}  ${user}  ${pwd}  ${NOS_DIR_OLD}
    Confirm NOS Version on Test Device   ${ip}  ${port}  ${user}  ${pwd}  ${NOS_VERSION_OLD}

Upgrade NOS Version on Test Device
    [Documentation]     Upgrades the NOS version on the VOSS switch to the latest version
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}

    Update NOS Version on Test Device   ${ip}  ${port}  ${user}  ${pwd}  ${NOS_DIR_NEW}
    Confirm NOS Version on Test Device  ${ip}  ${port}  ${user}  ${pwd}  ${NOS_VERSION_NEW}

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
