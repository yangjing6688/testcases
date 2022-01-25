#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for sanity testing of basic XIQ-SE firmware functionality.
#                 This is qTest TC-892 in the XIQ-SE project.

*** Settings ***
Resource        ../../SampleTests/Resources/AllResources.robot

Force Tags      testbed_1_node

Suite Setup     Log In and Set Up Test
Suite Teardown  Tear Down Test and Close Session


*** Variables ***
${ENV}                  environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                 topo.test.xiqse1.connected.yaml
${TESTBED}              SALEM/Dev/devices-salem-acceptance.yaml

${XIQSE_URL}            ${xiqse.url}
${XIQSE_USER}           ${xiqse.user}
${XIQSE_PASSWORD}       ${xiqse.password}

${DUT1_IP}              ${netelem1.ip}
${DUT1_PROFILE}         ${netelem1.profile}


*** Test Cases ***
Test 1: Open and Close Upgrade Firmware dialog
    [Documentation]     Confirms the Upgrade Firmware dialog can be opened and closed
    [Tags]              xiqse_tc_892    aiq_1332    development    sample    xiqse    firmware    test1

    Navigate to Devices and Confirm Success

    # Open the Upgrade Firmware dialog
    Open Upgrade Firmware Dialog for Device and Confirm Success  ${DUT1_IP}

    # Close the Upgrade Firmware dialog
    Close Upgrade Firmware Dialog and Confirm Success

Test 2: Confirm Firmware Selection Dialog Components
    [Documentation]     Confirms the components of the Firmware Selection dialog (Assign Image))
    [Tags]              xiqse_tc_892    aiq_1332    development    sample    xiqse    firmware    test2

    Navigate to Devices and Confirm Success

    # Open the Upgrade Firmware dialog
    Open Upgrade Firmware Dialog for Device and Confirm Success  ${DUT1_IP}

    # Open the Inventory Settings dialog
    Open Firmware Selection Dialog and Confirm Success

    # Refresh Images
    Refresh Images in Firmware Selection Dialog and Confirm Success

    # Close the Inventory Settings dialog
    Cancel Firmware Selection and Confirm Success

    # Close the Upgrade Firmware dialog
    Close Upgrade Firmware Dialog and Confirm Success

Test 3: Confirm Inventory Settings Dialog Components
    [Documentation]     Confirms the components of the Inventory Settings dialog
    [Tags]              xiqse_tc_892    aiq_1332    development    sample    xiqse    firmware    test3

    Navigate to Devices and Confirm Success

    # Open the Upgrade Firmware dialog
    Open Upgrade Firmware Dialog for Device and Confirm Success  ${DUT1_IP}

    # Open the Inventory Settings dialog
    Open Inventory Settings Dialog and Confirm Success

    # Set File Transfer Mode
    Set Inventory Settings File Transfer Mode and Confirm Success  SCP

    # Set Firmware Download MIB
    Set Inventory Settings Firmware Download MIB and Confirm Success  Script

    # Set Configuration Download MIB
    Set Inventory Settings Configuration Download MIB and Confirm Success  Script

    # Set Device Family Definition Filename
    Set Inventory Settings Device Family Definition Filename and Confirm Success  ExtremeXOS - SCP (VR-Default)

    # Close the Inventory Settings dialog
    Cancel Inventory Settings and Confirm Success

    # Close the Upgrade Firmware dialog
    Close Upgrade Firmware Dialog and Confirm Success

Test 4: Navigate to Firmware Tab
    [Documentation]     Confirms the Firmware tab can be navugated to
    [Tags]              xiqse_tc_892    aiq_1332    development    sample    xiqse    firmware    test4

    Navigate to Firmware and Confirm Success


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and sets up the components for the test

    # Log into XIQSE and close any banner messages and help panel, if displayed
    Log Into XIQSE and Confirm Success  ${XIQSE_USER}  ${XIQSE_PASSWORD}  url=${XIQSE_URL}
    Close Panels on Login If Displayed

    # Create the test device
    Navigate and Create Device  ${DUT1_IP}  ${DUT1_PROFILE}
    Confirm Device Status Up    ${DUT1_IP}

Tear Down Test and Close Session
    [Documentation]     Cleans up XIQSE test components and closes the browser

    # Clean up the test device
    Navigate and Delete Device  ${DUT1_IP}

    # Log out and close the browser
    Log Out of XIQSE and Quit Browser
