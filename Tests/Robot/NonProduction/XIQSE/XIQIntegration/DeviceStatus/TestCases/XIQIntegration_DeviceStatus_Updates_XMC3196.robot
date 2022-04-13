# Author        : Heidi S. White
# Description   : Test Suite for testing XIQSE-XIQ Integration for device status updates functionality.
#                 This is CSIT qTest test case:
#                   TC-8995: XIQ-SE Device Status Updates

*** Settings ***
Library         common/Utils.py

Resource        ../../DeviceStatus/Resources/AllResources.robot

Force Tags      testbed_1_node

Suite Setup     Log In and Set Up Test
Suite Teardown  Tear Down Test and Close Session


*** Variables ***
# Defaults
${ENV}                  environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                 topo.test.xiqse1.connected.yaml
${TESTBED}              SALEM/Dev/devices-salem-acceptance.yaml

${XIQSE_URL}            ${xiqse.url}
${XIQSE_USER}           ${xiqse.user}
${XIQSE_PASSWORD}       ${xiqse.password}
${XIQSE_SERIAL}         ${xiqse.serial}
${XIQSE_MAC}            ${xiqse.mac}

${XIQ_URL}              ${xiq.test_url}
${XIQ_USER}             ${xiq.tenant_username}
${XIQ_PASSWORD}         ${xiq.tenant_password}

${DUT_SERIAL}           ${netelem1.serial}
${DUT_MAC}              ${netelem1.mac}
${DUT_IP}               ${netelem1.ip}
${DUT_PROFILE}          ${netelem1.profile}
${DUT_MODEL}            ${netelem1.model}
${DUT_MAKE}             ${netelem1.make}


*** Test Cases ***
Test 1: Confirm Connected Device Has Correct Status In XIQSE and XIQ
    [Documentation]     Confirms a device with connected status in XIQSE shows as connected in XIQ
    [Tags]              nightly1    release_testing    csit_tc_8995    xmc_3196    development    xiqse    xiq_integration    device_status    updates    test1

    # Confirm Device Status in XIQ
    Switch To Window  ${XIQ_WINDOW_INDEX}
    ${xiq_result}=  Wait Until Device Online        ${DUT_SERIAL}
    Should Be Equal As Integers                     ${xiq_result}       1

    # Confirm Device Status in XIQSE
    Switch To Window  ${XIQSE_WINDOW_INDEX}
    XIQSE Navigate to Devices and Confirm Success
    Confirm Device Status Up                        ${DUT_IP}

Test 2: Confirm Disconnected Device Has Correct Status In XIQSE and XIQ
    [Documentation]     Confirms a device with disconnected status in XIQSE shows as disconnected in XIQ
    [Tags]              nightly1    release_testing    csit_tc_8995    xmc_3196    development    xiqse    xiq_integration    device_status    updates    test2

    # Disconnect the device in XIQSE
    Disconnect XIQSE Test Device and Confirm Success    ${DUT_IP}    BAD_PROFILE

    # Confirm the XIQSE-managed device reported in XIQ shows the correct status (disconnected)
    Switch To Window  ${XIQ_WINDOW_INDEX}
    ${disconnect_result}=  Wait Until Device Offline    ${DUT_SERIAL}
    Should Be Equal As Integers                         ${disconnect_result}       1

Test 3: Confirm Re-connected Device Has Correct Status In XIQSE and XIQ
    [Documentation]     Confirms a device which re-establishes connection in XIQSE shows as connected in XIQ
    [Tags]              nightly1    release_testing    csit_tc_8995    xmc_3196    development    xiqse    xiq_integration    device_status    updates    test3

    # Reconnect the device in XNC
    Reconnect XIQSE Test Device and Confirm Success     ${DUT_IP}    ${DUT_PROFILE}

    # Confirm the XIQSE-managed device reported in XIQ shows the correct status (connected)
    Switch To Window  ${XIQ_WINDOW_INDEX}
    ${reconnect_result}=  Wait Until Device Online      ${DUT_SERIAL}
    Should Be Equal As Integers                         ${reconnect_result}       1

Test 4: Confirm XIQ Site Engine and XIQSE-Managed Device Status When Sharing Disabled
    [Documentation]     Confirms XIQ displays unknown status for XIQSE-managed devices when XIQSE has disconnected status
    [Tags]              nightly1    release_testing    csit_tc_8995    xmc_3196    development    xiqse    xiq_integration    device_status    updates    test4

    # Disable sharing
    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Disable XIQ Connection Sharing and Confirm Success

    # Confirm the XIQ Site Engine reported in XIQ shows the correct status (disconnected)
    Switch To Window  ${XIQ_WINDOW_INDEX}
    Wait Until Device Offline   device_mac=${XIQSE_MAC}
    Confirm Device Status       ${XIQSE_MAC}    disconnected

    # Confirm the XIQSE-managed device reported in XIQ shows the correct status (unknown)
    Confirm Device Status  ${DUT_MAC}  unknown

Test 5: Confirm XIQ Site Engine and XIQSE-Managed Device Status When Sharing Re-enabled - Device Down
    [Documentation]     Confirms XIQ displays correct status for XIQ Site Engine and XIQSE-managed devices when sharing is re-enabled and test device is down
    [Tags]              nightly1    release_testing    csit_tc_8995    xmc_3196    development    xiqse    xiq_integration    device_status    updates    test5

    # Disable sharing
    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Disable XIQ Connection Sharing and Confirm Success

    # Confirm the XIQ Site Engine reported in XIQ shows the correct status (disconnected)
    Switch To Window  ${XIQ_WINDOW_INDEX}
    Wait Until Device Offline   device_mac=${XIQSE_MAC}
    Confirm Device Status       ${XIQSE_MAC}    disconnected

    # Disconnect Test Device
    Disconnect XIQSE Test Device and Confirm Success    ${DUT_IP}    BAD_PROFILE

    # Enable sharing
    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Enable XIQ Connection Sharing and Confirm Success

    # Confirm the XIQ Site Engine reported in XIQ shows the correct status (connected)
    Switch To Window  ${XIQ_WINDOW_INDEX}
    Wait Until Device Online    device_mac=${XIQSE_MAC}
    Confirm Device Status       ${XIQSE_MAC}    green

    # Confirm the XIQSE-managed device reported in XIQ shows the correct status (disconnected)
    Confirm Device Status   ${DUT_MAC}    disconnected

Test 6: Confirm XIQ Site Engine and XIQSE-Managed Device Status When Sharing Re-enabled - Device Up
    [Documentation]     Confirms XIQ displays correct status for XIQ Site Engine and XIQSE-managed devices when sharing is re-enabled and test device is up
    [Tags]              nightly1    release_testing    csit_tc_8995    xmc_3196    development    xiqse    xiq_integration    device_status    updates    test6

    # Disable sharing
    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Disable XIQ Connection Sharing and Confirm Success

    # Confirm the XIQ Site Engine reported in XIQ shows the correct status (disconnected)
    Switch To Window  ${XIQ_WINDOW_INDEX}
    Wait Until Device Offline  device_mac=${XIQSE_MAC}
    Confirm Device Status       ${XIQSE_MAC}    disconnected

    # Reconnect the device in XNC
    Reconnect XIQSE Test Device and Confirm Success     ${DUT_IP}    ${DUT_PROFILE}

    # Enable sharing
    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Enable XIQ Connection Sharing and Confirm Success

    # Confirm the XIQ Site Engine reported in XIQ shows the correct status (connected)
    Switch To Window  ${XIQ_WINDOW_INDEX}
    Wait Until Device Online    device_mac=${XIQSE_MAC}
    Confirm Device Status       ${XIQSE_MAC}    green

    # Confirm the XIQSE-managed device reported in XIQ shows the correct status (connected)
    Confirm Device Status       ${DUT_MAC}    green


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and sets up the test

    XIQSE Log In and Set Window Index
    Set Up XIQSE Components

    XIQ Log In and Set Window Index

    # Onboard XIQ Site Engine
    Onboard XIQ Site Engine and Confirm Success

    # Add the test device to XIQSE, deleting it first if it is already present
    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Navigate and Delete Device          ${DUT_IP}
    Create Device and Confirm Success   ${DUT_IP}    ${DUT_PROFILE}

    # Confirm the test device is onboarded to XIQ with connected status
    Confirm XIQSE Device Added to XIQ   ${DUT_SERIAL}

Tear Down Test and Close Session
    [Documentation]     Cleans up XIQ and XIQSE test components

    Clean Up XIQ Components
    Clean Up XIQSE Components
    XIQSE Quit Browser

XIQSE Log In and Set Window Index
    [Documentation]     Logs into XIQSE and confirms the login was successful

    Log Into XIQSE and Confirm Success    ${XIQSE_USER}    ${XIQSE_PASSWORD}    url=${XIQSE_URL}

    # Close any banner messages (Connection Lost with XIQ, License Expiration, etc.) and the Help panel, if displayed
    Close Panels on Login If Displayed

    # Store the window index so we can switch between XIQSE and XIQ
    ${xiqse_win}=  XIQSE Get Window Index
    Log To Console  Setting XIQSE Window Index to ${xiqse_win}
    Set Suite Variable  ${XIQSE_WINDOW_INDEX}  ${xiqse_win}

XIQ Log In and Set Window Index
    [Documentation]     Logs into XIQ and confirms the login was successful

    ${result}=  Login User          ${XIQ_USER}  ${XIQ_PASSWORD}  url=${XIQ_URL}
    Should Be Equal As Integers     ${result}     1

    ${xiq_win}=  Get Window Index
    Log To Console  Setting XIQ Window Index to ${xiq_win}
    Set Suite Variable  ${XIQ_WINDOW_INDEX}  ${xiq_win}

Set Up XIQSE Components
    [Documentation]     Sets up the XIQSE components for the test

    # Confirm the serial number is correct and set the common options needed for automation
    Confirm Serial Number and Set Common Options     ${XIQSE_SERIAL}

    # Create an invalid profile for causing a device disconnect
    XIQSE Create Invalid Profile

Onboard XIQ Site Engine and Confirm Success
    [Documentation]     Confirms the XIQ Site Engine can be onboarded successfully

    Remove Existing Site Engine from XIQ
    Auto Onboard XIQ Site Engine
    Confirm XIQ Site Engine Onboarded to XIQ

Remove Existing Site Engine from XIQ
    [Documentation]     Removes the XIQ Site Engine from XIQ if it exists

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate and Remove Device by MAC From XIQ   ${XIQSE_MAC}

Auto Onboard XIQ Site Engine
    [Documentation]     Onboards the specified XIQ Site Engine, deleting it first if it already exists

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Enter XIQ Credentials to Auto Onboard XIQSE  ${XIQ_USER}  ${XIQ_PASSWORD}

Confirm XIQ Site Engine Onboarded to XIQ
    [Documentation]     Confirms the XIQ Site Engine has been onboarded to XIQ successfully

    Switch To Window  ${XIQ_WINDOW_INDEX}

    ${search_result}=  Wait Until Device Added      ${XIQSE_SERIAL}
    Should Be Equal As Integers                     ${search_result}    1

    ${device_status}=  Wait Until Device Online     device_mac=${XIQSE_MAC}
    Should Be Equal As Integers                     ${device_status}    1

XIQ Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Manage> Devices view in XIQ and confirms the action was successful

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate to XIQ Devices and Confirm Success

XIQSE Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Network> Devices> Devices view in XIQSE and confirms the action was successful

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate to Devices and Confirm Success

XIQSE Create Invalid Profile
    [Documentation]     Creates an SNMP credential and profile in XIQSE which will cause a device to disconnect

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # Create SNMP Credential and Confirm Success
    Navigate and Create SNMP Credential     BAD_CRED  SNMPv2  junk

    # Create Profile and Confirm Success
    Navigate and Create Profile             BAD_PROFILE  version=SNMPv2  read=BAD_CRED

Confirm Device Status
    [Documentation]     Checks the status of the specified device and confirms it matches the expected value
    [Arguments]         ${mac}  ${expected_status}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    ${device_status}=  Get Device Status   device_mac=${mac}
    Should Contain     ${device_status}    ${expected_status}

Confirm XIQSE Device Added to XIQ
    [Documentation]     Confirms the specified device is present in XIQ
    [Arguments]         ${serial}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    ${search_result}=  Wait Until Device Added      ${serial}
    Should Be Equal As Integers                     ${search_result}    1

Disconnect XIQSE Test Device and Confirm Success
    [Documentation]     Updates the specified device to lose contact in XIQSE by changing the profile
    [Arguments]         ${ip}  ${profile}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    XIQSE Navigate to Devices and Confirm Success
    Set Device Profile and Confirm Success      ${ip}  BAD_PROFILE

    Confirm Device Status Down                  ${ip}

Reconnect XIQSE Test Device and Confirm Success
    [Documentation]     Updates the specified device to regain contact in XIQSE by changing the profile
    [Arguments]         ${ip}    ${profile}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    XIQSE Navigate to Devices and Confirm Success
    Set Device Profile and Confirm Success          ${ip}  ${profile}

    Confirm Device Status Up                        ${ip}

Clean Up XIQ Components
    [Documentation]     Cleans up components used in XIQ during the test, logs out, and closes the browser

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate and Remove Device by MAC From XIQ  ${XIQSE_MAC}

    Log Out of XIQ and Confirm Success

Clean Up XIQSE Components
    [Documentation]     Cleans up components used in XIQSE during the test, logs out, and closes the browser

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # Make sure sharing with XIQ is enabled
    Enable XIQ Connection Sharing and Confirm Success

    # Delete the test device
    Navigate and Delete Device              ${DUT_IP}

    # Delete the profile and SNMP credential
    Navigate and Delete Profile              BAD_PROFILE
    Navigate and Delete SNMP Credential      BAD_CRED

    # Log out
    Log Out of XIQSE and Confirm Success
