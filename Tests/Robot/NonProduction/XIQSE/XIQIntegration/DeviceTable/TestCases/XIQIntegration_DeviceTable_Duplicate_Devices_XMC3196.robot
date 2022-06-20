#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for testing XIQSE-XIQ Integration for the Duplicate Devices functionality.
#                 This encompasses the following qTest test cases in the CSIT project:
#                   TC-52234: Device Onboarded to XIQ & Subsequently Onboarded to XIQSE
#                   TC-52235: Device Onboarded to XIQSE & Subsequently Onboarded to XIQ
#                   TC-52236: Device in XIQ and XIQSE then Deleted from XIQ

*** Settings ***
Library         Collections
Library         common/Utils.py

Resource        ../../DeviceTable/Resources/AllResources.robot

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

${DUT_SERIAL}           ${netelem2.serial}
${DUT_IP}               ${netelem2.ip}
${DUT_PROFILE}          ${netelem2.profile}
${DUT_MODEL}            ${netelem2.model}
${DUT_MAKE}             ${netelem2.make}

${LOCATION}             San Jose, building_01, floor_02
${WORLD_SITE}           World


*** Test Cases ***
Test 1: TC-52234 - Device Onboarded to XIQ & Subsequently Onboarded to XIQSE
    [Documentation]     Confirms if a device is managed by XIQ it is not added as XIQSE-managed device when added to XIQSE
    [Tags]              nightly2    release_testing    csit_tc_52234    xmc_3196    development    xiqse    xiq_integration    device_table    test1

    # Onboard Device to XIQ
    Switch To Window  ${XIQ_WINDOW_INDEX}
    Navigate and Onboard Switch to XIQ   ${DUT_SERIAL}  ${DUT_MAKE}  ${LOCATION}

    # Add Device to XIQSE and make sure a system message appears that it is already onboarded
    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Add Device to XIQSE and Confirm Success  ${DUT_IP}  ${DUT_PROFILE}
    Navigate to XIQ Device Message Details and Confirm Success
    Confirm Device Has Expected Onboard Status  ${DUT_IP}  ${DUT_MODEL}  DEVICE_ALREADY_ONBOARDED

    [Teardown]  Delete Test Device From XIQSE and XIQ  ${DUT_IP}  ${DUT_SERIAL}

Test 2: TC-52235 - Device Onboarded to XIQSE & Subsequently Onboarded to XIQ
    [Documentation]     Confirms an XIQSE-managed device onbaorded to XIQ cannot be onboarded directly into XIQ
    [Tags]              nightly2    release_testing    csit_tc_52235    xmc_3196    development    xiqse    xiq_integration    device_table    test2

    # Add device to XIQSE
    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Add Device to XIQSE and Confirm Success  ${DUT_IP}  ${DUT_PROFILE}

    # Wait until the device has been added to XIQ
    Switch To Window  ${XIQ_WINDOW_INDEX}
    Confirm Device Serial Present   ${DUT_SERIAL}

    # Attempt to onboard the same device to XIQ - should report error
    Switch To Window  ${XIQ_WINDOW_INDEX}
    ${xiq_result}=  Confirm XIQSE Managed Device Not Onboarded by XIQ   ${DUT_SERIAL}  ${DUT_MAKE}  ${LOCATION}
    Should Be Equal As Integers  ${xiq_result}  1

    [Teardown]  Delete XIQSE Test Device and Confirm Success  ${DUT_IP}

Test 3: TC-52236 - Device in XIQ and XIQSE then Deleted from XIQ
    [Documentation]     Confirms a device which has been onboarded in XIQ and also exists in XIQSE is onboarded as an XIQSE-managed device when deleted from XIQ
    [Tags]              nightly2    release_testing    known_issue    csit_tc_52236    xmc_3196    development    xiqse    xiq_integration    device_table    test3

    Log To Console  KNOWN ISSUE: APC-44759

    # Onboard Device to XIQ
    Switch To Window  ${XIQ_WINDOW_INDEX}
    Refresh Devices Page
    Onboard Switch to XIQ and Confirm Success   ${DUT_SERIAL}  ${DUT_MAKE}  ${LOCATION}

    # Add Same Device to XIQSE
    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Add Device to XIQSE and Confirm Success         ${DUT_IP}  ${DUT_PROFILE}

    # Delete Device from XIQ and confirm device is re-added automatically to XIQ as an XIQSE-managed device
    Switch To Window  ${XIQ_WINDOW_INDEX}
    ${managed_by_xiq}=  Get Device Details          ${DUT_SERIAL}  MANAGED BY
    Should Be Equal                                 ${managed_by_xiq}     XIQ
    Delete XIQ Test Device and Confirm Success      ${DUT_SERIAL}

    Log To Console  Sleeping for 2 minutes to wait for the next update to come in
    Count Down in Minutes  2
    Refresh Devices Page
    Confirm Device Serial Present                   ${DUT_SERIAL}
    ${managed_by_xiqse}=  Get Device Details        ${DUT_SERIAL}  MANAGED BY
    Should Be Equal                                 ${managed_by_xiqse}     XIQ_SE

    # Delete the Device from XIQSE
    [Teardown]  Delete XIQSE Test Device and Confirm Success      ${DUT_IP}


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Sets up the components for the test

    XIQSE Log In and Set Window Index
    Set Up XIQSE Components

    XIQ Log In and Set Window Index

    # Onboard the Site Engine to XIQ
    Onboard XIQ Site Engine and Confirm Success

Tear Down Test and Close Session
    [Documentation]     Cleans up XIQ and XIQSE test components

    Clean Up XIQ Components
    Clean Up XIQSE Components
    XIQSE Quit Browser

XIQSE Log In and Set Window Index
    [Documentation]     Logs into XIQSE and confirms the login was successful

    Log Into XIQSE and Confirm Success              ${XIQSE_USER}  ${XIQSE_PASSWORD}  url=${XIQSE_URL}
    Handle License Agreement If Displayed           ${XIQ_USER}  ${XIQ_PASSWORD}

    # Close any banner messages (Connection Lost with XIQ, License Expiration, etc.) and the Help panel, if displayed
    Close Panels on Login If Displayed

    # Store the window index so we can switch between XIQSE and XIQ
    ${xiqse_win}=  XIQSE Get Window Index
    Log To Console  Setting XIQSE Window Index to ${xiqse_win}
    Set Suite Variable  ${XIQSE_WINDOW_INDEX}  ${xiqse_win}

XIQ Log In and Set Window Index
    [Documentation]     Logs into XIQ and confirms the login was successful

    Log Into XIQ and Confirm Success    ${XIQ_USER}  ${XIQ_PASSWORD}  url=${XIQ_URL}

    ${xiq_win}=  Get Window Index
    Log To Console  Setting XIQ Window Index to ${xiq_win}
    Set Suite Variable  ${XIQ_WINDOW_INDEX}  ${xiq_win}

Set Up XIQSE Components
    [Documentation]     Sets up the XIQSE components for the test

    Disable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}

    # Confirm the serial number is correct and set the common options needed for automation
    Confirm Serial Number and Set Common Options     ${XIQSE_SERIAL}

XIQSE Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Network> Devices> Devices view in XIQSE and confirms the action was successful

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate to Devices and Confirm Success

XIQ Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Manage> Devices view in XIQ and confirms the action was successful

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate to XIQ Devices and Confirm Success

Onboard XIQ Site Engine and Confirm Success
    [Documentation]     Confirms the XIQ Site Engine can be onboarded successfully

    Remove Existing Site Engine from XIQ
    Auto Onboard XIQ Site Engine
    Confirm XIQ Site Engine Onboarded to XIQ

Remove Existing Site Engine from XIQ
    [Documentation]     Removes the XIQ Site Engine from XIQ if it exists

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate and Remove Device by MAC From XIQ  ${XIQSE_MAC}

Auto Onboard XIQ Site Engine
    [Documentation]     Onboards the specified XIQ Site Engine, deleting it first if it already exists

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Enter XIQ Credentials to Auto Onboard XIQSE  ${XIQ_USER}  ${XIQ_PASSWORD}

Confirm XIQ Site Engine Onboarded to XIQ
    [Documentation]     Confirms the XIQ Site Engine has been onboarded to XIQ successfully

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Confirm Device Serial Present   ${XIQSE_SERIAL}
    Confirm Device Serial Online    ${XIQSE_SERIAL}

Add Device to XIQSE and Confirm Success
    [Documentation]     Adds the specified device to XIQSE
    [Arguments]         ${ip}  ${profile}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate and Create Device  ${ip}  ${profile}

Delete XIQSE Test Device and Confirm Success
    [Documentation]     Deletes the specified device from XIQSE and confirms the action was successful
    [Arguments]         ${ip}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate and Delete Device   ${ip}

Delete XIQ Test Device and Confirm Success
    [Documentation]     Deletes the specified device from XIQ and confirms the action was successful
    [Arguments]         ${serial}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate and Remove Device by Serial From XIQ  ${serial}

Delete Test Device From XIQSE and XIQ
    [Documentation]     Deletes the test device from both XIQSE and XIQ
    [Arguments]         ${ip}  ${serial}

    # Delete the Device from XIQSE
    Delete XIQSE Test Device and Confirm Success  ${DUT_IP}

    # Delete the Device from XIQ
    Delete XIQ Test Device and Confirm Success    ${DUT_SERIAL}

Clean Up XIQ Components
    [Documentation]     Cleans up components used in XIQ during the test, logs out, and closes the browser

    Switch To Window  ${XIQ_WINDOW_INDEX}

    # Remove XIQSE from XIQ
    Navigate and Remove Device by MAC From XIQ  ${XIQSE_MAC}

    # Log out
    Log Out of XIQ and Confirm Success

Clean Up XIQSE Components
    [Documentation]     Cleans up components used in XIQSE during the test, logs out, and closes the browser

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Enable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}

    # Delete the test device
    Delete XIQSE Test Device and Confirm Success    ${DUT_IP}

    # Log out
    Log Out of XIQSE and Confirm Success
