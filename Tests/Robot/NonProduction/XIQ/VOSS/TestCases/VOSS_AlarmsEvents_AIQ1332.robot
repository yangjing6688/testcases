#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for testing Alarm and Event functionality of the VOSS switch.
#                 This is qTest test case TC-8384 in the CSIT project.

*** Settings ***
Library          Collections
Library          common/Utils.py
Library          xiq/flows/manage/Device360.py

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
${DUT_MAC}                  ${netelem3.mac}
${DUT_NAME}                 ${netelem3.name}
${DUT_TEMPLATE}             ${netelem3.template}
${DUT_IP}                   ${netelem3.ip}
${DUT_PORT}                 ${netelem3.port}
${DUT_USERNAME}             ${netelem3.username}
${DUT_PASSWORD}             ${netelem3.password}
${DUT_PLATFORM}             ${netelem3.platform}
${DUT_TEST_PORT}            ${netelem3.test_port}
${DUT_MAKE}                 ${netelem3.make}
${DUT_CLI_TYPE}             ${netelem3.cli_type}

${LOCATION}                 San Jose, building_01, floor_02


*** Test Cases ***
Test1: Confirm Link Down Event
    [Documentation]     Disables a port on the test device and confirms a Link Down event is generated
    [Tags]              csit_tc_8384    aiq_1332    development    xiq    voss    alarms_events    test1

    Disable Port for Test Device            ${DUT_IP}  ${DUT_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}  ${DUT_TEST_PORT}

    Refresh Devices Page
    Navigate to Device360 Page with MAC     ${DUT_MAC}
    Device360 Select Events View
#    Confirm Event Exists                    Link down detected on interface ${DUT_TEST_PORT}  ${TEST_TIME}
    Log To Console                          NOTE: ignoring time stamp (${TEST_TIME}) until APC-41429 is fixed
    Confirm Event Exists                    Link down detected on interface ${DUT_TEST_PORT}  ${EMPTY}

    [Teardown]                              Close Device360 Window

Test2: Confirm Link Up Event
    [Documentation]     Enables a port on the test device and confirms a Link Up event is generated
    [Tags]              csit_tc_8384    aiq_1332    development    xiq    voss    alarms_events    test2

    Enable Port for Test Device             ${DUT_IP}  ${DUT_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}  ${DUT_TEST_PORT}

    Refresh Devices Page
    Navigate to Device360 Page with MAC     ${DUT_MAC}
    Device360 Select Events View
#    Confirm Event Exists                    Link up detected on interface ${DUT_TEST_PORT}  ${TEST_TIME}
    Log To Console                          NOTE: ignoring time stamp (${TEST_TIME}) until APC-41429 is fixed
    Confirm Event Exists                    Link up detected on interface ${DUT_TEST_PORT}  ${EMPTY}

    [Teardown]                              Close Device360 Window

Test3: Confirm Device Disconnected Alarm
    [Documentation]     Disconnect the test device from the IQ agent and confirms a Device Disconnected alarm is generated
    [Tags]              csit_tc_8384    aiq_1332    development    xiq    voss    alarms_events    test3

    Disable iqagent for Test Device         ${DUT_IP}  ${DUT_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}

    Refresh Devices Page
    Navigate to Device360 Page with MAC     ${DUT_MAC}
    Device360 Select Alarms View
#    Confirm Alarm Exists                    Device Disconnected  ${TEST_TIME}
    Log To Console                          NOTE: ignoring time stamp (${TEST_TIME}) until APC-41429 is fixed
    Confirm Alarm Exists                    Device Disconnected  ${EMPTY}

    [Teardown]                              Clear Alarm Condition and Close Device360 Window


*** Keywords ***
Log Into XIQ and Set Up Test
    [Documentation]     Logs into XIQ and sets up the elements necessary to complete this test suite

    Log Into XIQ and Confirm Success            ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}
    Change XIQ Account Time Zone                (GMT) UTC

    Configure Test Device                       ${DUT_IP}  ${DUT_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}  ${DUT_CLI_TYPE}  ${IQAGENT}

    Enable Port for Test Device                 ${DUT_IP}  ${DUT_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}  ${DUT_TEST_PORT}

    Onboard New Test Device                     ${DUT_SERIAL}  ${DUT_MAKE}  ${LOCATION}
    Wait Until Device Online                    ${DUT_SERIAL}

    ${date_time}=                               Get UTC Time    %Y-%m-%d %H:%M:%S
    Set Suite Variable                          ${TEST_TIME}   ${date_time}

Tear Down Test and Close Session
    [Documentation]     Cleans up test data, logs out of XIQ, and closes the browser

    Clean Up Test Device and Confirm Success    ${DUT_SERIAL}
    Log Out of XIQ and Quit Browser

Configure Test Device
    [Documentation]     Configures the specified test device by rebooting a known good configuration file and then configuring the iqagent
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${cli_type}  ${agent}

    Boot Switch To Known Good Configuration     ${ip}  ${port}  ${user}  ${pwd}  ${cli_type}
    Configure Device To Connect To Cloud        ${cli_type}  ${ip}  ${port}  ${user}  ${pwd}  ${agent}

Confirm Event Exists
    [Documentation]     Confirms the specified event exists after the specified time
    [Arguments]         ${event_str}  ${after_time}

    ${event_found}=                 Device360 Confirm Event Description Contains  ${event_str}  ${after_time}
    Should Be Equal As Integers     ${event_found}  1

Confirm Alarm Exists
    [Documentation]     Confirms the specified alarm exists after the specified time
    [Arguments]         ${alarm_cat}  ${after_time}

    ${alarm_found}=                 Device360 Confirm Alarm Category Exists  ${alarm_cat}  ${after_time}
    Should Be Equal As Integers     ${alarm_found}  1

Clear Alarm Condition and Close Device360 Window
    [Documentation]     Re-enables the iqagent to clear the alarm condition, and closes the Device360 window

    Enable iqagent for Test Device  ${DUT_IP}  ${DUT_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}
    Close Device360 Window

Onboard New Test Device
    [Documentation]     Onboards the specified test device, deleting it first if it already exists
    [Arguments]         ${serial}  ${make}  ${location}

    Navigate to Devices and Confirm Success

    # If the device has already been onboarded, delete it first
    Delete Device and Confirm Success  ${serial}
    Confirm Device Serial Not Present  ${serial}

    # Onboard the device
    Onboard Device    ${serial}  ${make}  location=${location}
    sleep   ${DEVICE_ONBOARDING_WAIT}
    Confirm Device Serial Present  ${serial}

Clean Up Test Device and Confirm Success
    [Documentation]     Deletes the specified device and confirms the action was successful
    [Arguments]         ${serial}

    Navigate to Devices and Confirm Success

    Delete Device and Confirm Success  ${serial}
    Confirm Device Serial Not Present  ${serial}
