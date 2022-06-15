# Author        : Heidi S. White
# Description   : Test Suite for testing device status when XIQ-SE is disconnected.
#                 This is story APC-42459 - Provide contextual information for "device disconnected" status
#                 This is qTest test case TC-10316 in project CSIT:
#                   TC-10316: XIQSE Disconnected: Device Status

*** Settings ***
Library         Collections
Library         common/Cli.py
Library         common/Utils.py

Resource        ../../DeviceStatus/Resources/AllResources.robot

Force Tags      testbed_2_node


*** Variables ***
# Defaults
${ENV}                  environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                 topo.test.xiqse1.connected.yaml
${TESTBED}              SALEM/Dev/devices-salem-acceptance.yaml

${XIQSE_URL}            ${xiqse.url}
${XIQSE_USER}           ${xiqse.user}
${XIQSE_PASSWORD}       ${xiqse.password}
${XIQSE_IP}             ${xiqse.ip}
${XIQSE_SERIAL}         ${xiqse.serial}
${XIQSE_MAC}            ${xiqse.mac}

${XIQ_URL}              ${xiq.test_url}
${XIQ_USER}             ${xiq.tenant_username}
${XIQ_PASSWORD}         ${xiq.tenant_password}

${DUT1_SERIAL}          ${netelem1.serial}
${DUT1_IP}              ${netelem1.ip}
${DUT1_PROFILE}         ${netelem1.profile}

${DUT2_SERIAL}          ${netelem2.serial}
${DUT2_IP}              ${netelem2.ip}
${DUT2_PROFILE}         ${netelem2.profile}


*** Test Cases ***
Configure Test Requirements
    [Documentation]     Sets up the components needed for the test
    [Tags]              nightly2    release_testing    csit_tc_10316    apc_42459    development    xiqse    xiq_integration    device_status    xiqse_disconnect    test0

    [Setup]    Log Into XIQSE and XIQ and Confirm Success

    Set Up XIQSE Components
    Set Up XIQ Components

    # Onboard XIQ Site Engine
    Auto Onboard XIQ Site Engine
    Confirm XIQ Site Engine Onboarded to XIQ

    # Add the test devices to XIQ-SE
    Add Device to XIQSE and Confirm Success     ${DUT1_IP}    ${DUT1_PROFILE}
    Add Device to XIQSE and Confirm Success     ${DUT2_IP}    ${DUT2_PROFILE}

    # Confirm the test devices are onboarded to XIQ with connected status
    Confirm XIQSE Device Added to XIQ           ${DUT1_SERIAL}
    Confirm XIQSE Device Added to XIQ           ${DUT2_SERIAL}

    [Teardown]    Log Out of XIQ and XIQSE and Quit Browser

Test 1: Confirm Connected Devices Have Correct Status in XIQSE and XIQ
    [Documentation]     Confirms devices with connected status in XIQ-SE show as connected in XIQ
    [Tags]              nightly2    release_testing    csit_tc_10316    apc_42459    development    xiqse    xiq_integration    device_status    xiqse_disconnect    test1

    [Setup]    Log Into XIQSE and XIQ and Confirm Success

    # Confirm Device Status in XIQ-SE
    Switch To Window                ${XIQSE_WINDOW_INDEX}
    XIQSE Navigate to Devices and Confirm Success
    Confirm Device Status Up        ${DUT1_IP}
    Confirm Device Status Up        ${DUT2_IP}

    # Confirm Device Status in XIQ
    Switch To Window                ${XIQ_WINDOW_INDEX}
    Confirm Device Serial Online    ${DUT1_SERIAL}
    Confirm Device Serial Online    ${DUT2_SERIAL}

    [Teardown]    Log Out of XIQ and XIQSE and Quit Browser

Test 2: Confirm Disconnected Device Has Correct Status in XIQSE and XIQ
    [Documentation]     Confirms a device with disconnected status in XIQ-SE shows as disconnected in XIQ
    [Tags]              nightly2    release_testing    csit_tc_10316    apc_42459    development    xiqse    xiq_integration    device_status    xiqse_disconnect    test2

    [Setup]    Log Into XIQSE and XIQ and Confirm Success

    # Disconnect the device in XIQ-SE
    Disconnect XIQSE Test Device and Confirm Success    ${DUT1_IP}    BAD_PROFILE

    # Confirm the XIQSE-managed device reported in XIQ shows the correct status (disconnected)
    Switch To Window                ${XIQ_WINDOW_INDEX}
    Confirm Device Serial Offline   ${DUT1_SERIAL}

    [Teardown]    Log Out of XIQ and XIQSE and Quit Browser

Test 3: Confirm Disconnected XIQ-SE Results in Correct Status in XIQ
    [Documentation]     Confirms when XIQ-SE is disconnected, XIQSE-managed devices will have Unknown status in XIQ.
    [Tags]              nightly2    release_testing    csit_tc_10316    apc_42459    development    xiqse    xiq_integration    device_status    xiqse_disconnect    test3

    [Setup]  XIQ Log In and Set Window Index

    # Shut down the XIQSE server and confirm XIQ shows the correct disconnected status
    Stop XIQSE Server                   ${XIQSE_IP}  ${XIQSE_USER}  ${XIQSE_PASSWORD}
    Confirm XIQSE Disconnected

    # Confirm test devices have status Unknown
    Confirm Device Status with Serial   ${DUT1_SERIAL}    unknown
    Confirm Device Status with Serial   ${DUT2_SERIAL}    unknown

    [Teardown]  Log Out of XIQ and Quit Browser

Test 4: Confirm Reconnected XIQ-SE Results in Correct Status in XIQ
    [Documentation]     Confirms when XIQ-SE is reconnected, XIQSE-managed devices will have correct status in XIQ.
    [Tags]              nightly2    release_testing    csit_tc_10316    apc_42459    development    xiqse    xiq_integration    device_status    xiqse_disconnect    test4

    [Setup]  XIQ Log In and Set Window Index

    # Restart the XIQSE server and confirm XIQ shows the correct connected status
    Start XIQSE Server                  ${XIQSE_IP}  ${XIQSE_USER}  ${XIQSE_PASSWORD}
    Confirm XIQSE Connected

    # Confirm test devices have correct status
    Confirm Device Status with Serial   ${DUT1_SERIAL}    disconnected
    Confirm Device Status with Serial   ${DUT2_SERIAL}    green

    [Teardown]  Log Out of XIQ and Quit Browser

Test 5: Confirm Re-connected Device Has Correct Status in XIQ
    [Documentation]     Confirms a device which re-establishes connection in XIQ-SE shows as connected in XIQ
    [Tags]              nightly2    release_testing    csit_tc_10316    apc_42459    development    xiqse    xiq_integration    device_status    xiqse_disconnect    test5

    [Setup]    Log Into XIQSE and XIQ and Confirm Success

    # Reconnect the device in XNC
    Reconnect XIQSE Test Device and Confirm Success     ${DUT1_IP}    ${DUT1_PROFILE}

    # Confirm the XIQSE-managed device reported in XIQ shows the correct status (connected)
    Switch To Window                ${XIQ_WINDOW_INDEX}
    Confirm Device Serial Online    ${DUT1_SERIAL}

    [Teardown]    Log Out of XIQ and XIQSE and Quit Browser

Tear Down Test and Close Session
    [Documentation]     Cleans up XIQ and XIQ-SE test components
    [Tags]              nightly2    release_testing    csit_tc_10316    apc_42459    development    xiqse    xiq_integration    device_status    xiqse_disconnect    test6

    [Setup]    Log Into XIQSE and XIQ and Confirm Success

    Clean Up XIQ Components
    Clean Up XIQSE Components

    [Teardown]    XIQSE Quit Browser


*** Keywords ***
Log Into XIQSE and XIQ and Confirm Success
    [Documentation]     Logs into XIQ-SE and XIQ, and confirms the logins were successful

    XIQSE Log In and Set Window Index
    XIQ Log In and Set Window Index

XIQSE Log In and Set Window Index
    [Documentation]     Logs into XIQSE and sets the window index

    Log Into XIQSE and Confirm Success              ${XIQSE_USER}  ${XIQSE_PASSWORD}  url=${XIQSE_URL}
    Handle License Agreement If Displayed           ${XIQ_USER}  ${XIQ_PASSWORD}

    # Close any banner messages (Connection Lost with XIQ, License Expiration, etc.) and the Help panel, if displayed
    Close Panels on Login If Displayed

    # Store the window index so we can switch between XIQSE and XIQ
    ${xiqse_win}=  XIQSE Get Window Index
    Log To Console  Setting XIQSE Window Index to ${xiqse_win}
    Set Suite Variable  ${XIQSE_WINDOW_INDEX}  ${xiqse_win}

XIQ Log In and Set Window Index
    [Documentation]     Logs into XIQ and sets the window index

    Log Into XIQ and Confirm Success    ${XIQ_USER}  ${XIQ_PASSWORD}  url=${XIQ_URL}

    ${xiq_win}=  Get Window Index
    Log To Console  Setting XIQ Window Index to ${xiq_win}
    Set Suite Variable  ${XIQ_WINDOW_INDEX}  ${xiq_win}

Set Up XIQSE Components
    [Documentation]     Sets up the XIQ-SE components for the test

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Confirm Serial Number and Set Common Options  ${XIQSE_SERIAL}

    # Create an invalid profile for causing a device disconnect
    XIQSE Create Invalid Profile

Set Up XIQ Components
    [Documentation]     Sets up the XIQ components for the test

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate and Remove Device by MAC From XIQ  ${XIQSE_MAC}

Log Out of XIQ and XIQSE and Quit Browser
    [Documentation]     Logs into XIQ-SE and XIQ, and confirms the logins were successful

    Switch To Window  ${XIQ_WINDOW_INDEX}
    Log Out of XIQ and Confirm Success

    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Log Out of XIQSE and Confirm Success
    Quit Browser and Confirm Success

Auto Onboard XIQ Site Engine
    [Documentation]     Onboards the specified XIQ Site Engine using the Auto Onboard button

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Enter XIQ Credentials to Auto Onboard XIQSE  ${XIQ_USER}  ${XIQ_PASSWORD}

Confirm XIQ Site Engine Onboarded to XIQ
    [Documentation]     Confirms the XIQ Site Engine has been onboarded to XIQ successfully

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Confirm Device Serial Present   ${XIQSE_SERIAL}
    Confirm Device Serial Online    ${XIQSE_SERIAL}

XIQ Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Manage> Devices view in XIQ and confirms the action was successful

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate to XIQ Devices and Confirm Success

XIQSE Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Network> Devices> Devices view in XIQ-SE and confirms the action was successful

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate to Devices and Confirm Success

XIQSE Create Invalid Profile
    [Documentation]     Creates an SNMP credential and profile in XIQ-SE which will cause a device to disconnect

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # Create Invalid SNMP Credential
    Navigate and Create SNMP Credential     BAD_CRED  SNMPv2  junk

    # Create Invalid Profile (uses the invalid SNMP credential)
    Create Profile and Confirm Success      BAD_PROFILE  SNMPv2  BAD_CRED

Confirm Device Status with Serial
    [Documentation]     Checks the status of the specified device using Serial Number and confirms it matches the expected value
    [Arguments]         ${serial}  ${expected_status}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    ${device_status}=  Get Device Status   device_serial=${serial}
    Should Contain     ${device_status}    ${expected_status}

Confirm Device Status with MAC
    [Documentation]     Checks the status of the specified device using MAC address and confirms it matches the expected value
    [Arguments]         ${mac}  ${expected_status}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    ${device_status}=  Get Device Status   device_mac=${mac}
    Should Contain     ${device_status}    ${expected_status}

Add Device to XIQSE and Confirm Success
    [Documentation]     Adds the specified device to XIQ-SE
    [Arguments]         ${ip}  ${profile}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate and Create Device  ${ip}  ${profile}

Confirm XIQSE Device Added to XIQ
    [Documentation]     Confirms the specified device is present in XIQ
    [Arguments]         ${serial}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Confirm Device Serial Present  ${serial}

Disconnect XIQSE Test Device and Confirm Success
    [Documentation]     Updates the specified device to lose contact in XIQ-SE by changing the profile
    [Arguments]         ${ip}  ${profile}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    XIQSE Navigate to Devices and Confirm Success
    Set Device Profile and Confirm Success          ${ip}    BAD_PROFILE
    Confirm Device Status Down                      ${ip}

Reconnect XIQSE Test Device and Confirm Success
    [Documentation]     Updates the specified device to regain contact in XIQ-SE by changing the profile
    [Arguments]         ${ip}    ${profile}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    XIQSE Navigate to Devices and Confirm Success
    Set Device Profile and Confirm Success          ${ip}    ${profile}
    Confirm Device Status Up                        ${ip}

Confirm XIQSE Disconnected
    [Documentation]     Confirms the device status is displayed correctly in XIQ when XIQSE is disconnected

    Switch To Window  ${XIQ_WINDOW_INDEX}

    # Confirm XIQ-SE has status Disconnected
    Wait Until Device Offline           device_mac=${XIQSE_MAC}  retry_duration=30  retry_count=22
    Confirm Device Status with MAC      ${XIQSE_MAC}     disconnected

Confirm XIQSE Connected
    [Documentation]     Confirms the device status is displayed correctly in XIQ when XIQSE is connected

    # Confirm connection status in XIQ
    Switch To Window  ${XIQ_WINDOW_INDEX}

    ##   Confirm XIQ-SE has status Connected (green)
    Wait Until Device Online            device_mac=${XIQSE_MAC}  retry_duration=30  retry_count=22
    Confirm Device Status with MAC      ${XIQSE_MAC}     green

Delete XIQSE Test Device and Confirm Success
    [Documentation]     Deletes the specified device from XIQSE and confirms the action was successful
    [Arguments]         ${ip}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate and Delete Device  ${ip}

XIQSE Delete SNMP Credential and Confirm Success
    [Documentation]     Deletes the SNMP credential from XIQ-SE
    [Arguments]         ${name}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate and Delete SNMP Credential  ${name}

XIQSE Delete Profile and Confirm Success
    [Documentation]     Deletes the profile from XIQ-SE
    [Arguments]         ${name}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate and Delete Profile  ${name}

Clean Up XIQ Components
    [Documentation]     Cleans up components used in XIQ during the test, logs out, and closes the browser

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate and Remove Device by MAC From XIQ  ${XIQSE_MAC}

    Log Out of XIQ and Confirm Success

Clean Up XIQSE Components
    [Documentation]     Cleans up components used in XIQ-SE during the test, logs out, and closes the browser

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # Delete the test devices
    Delete XIQSE Test Device and Confirm Success          ${DUT1_IP}
    Delete XIQSE Test Device and Confirm Success          ${DUT2_IP}

    # Delete the profile and SNMP credential
    XIQSE Delete Profile and Confirm Success              BAD_PROFILE
    XIQSE Delete SNMP Credential and Confirm Success      BAD_CRED

    Log Out of XIQSE and Confirm Success
