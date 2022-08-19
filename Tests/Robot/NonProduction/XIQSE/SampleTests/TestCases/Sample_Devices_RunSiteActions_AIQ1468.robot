#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Dan McCarthy
# Description   : Test Suite for sanity testing of the XIQ-SE 'Add Device > Run Site's Add Actions" functionality.
#                 This is qTest TC-948 in the XIQ-SE project.

*** Settings ***
Resource        ../../SampleTests/Resources/AllResources.robot

Force Tags      testbed_1_node

Suite Setup     Log In and Set Up Test
Suite Teardown  Log Out of XIQSE and Quit Browser


*** Variables ***
${ENV}                   environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                  topo.test.xiqse1.connected.yaml
${TESTBED}               SALEM/Dev/devices-salem-acceptance.yaml

${XIQSE_URL}             ${xiqse.url}
${XIQSE_USER}            ${xiqse.user}
${XIQSE_PASSWORD}        ${xiqse.password}

${DUT1_IP}               ${netelem1.ip}
${DUT1_PROFILE}          ${netelem1.profile}


*** Test Cases ***
Test 1: Add Device And Deselect Run Site Add Actions
    [Documentation]     Confirms a device can be added
    [Tags]              tcxe_948    aiq_1468    development    sample    xiqse    devices    add_actions    test1

    # Clear the Operations panel
    ${action_result}=    XIQSE Clear Operations Panel
    Should Be Equal As Integers                         ${action_result}      1

    ${add_result}=  XIQSE Add Device                    ${DUT1_IP}  ${DUT1_PROFILE}  add_actions=False
    Should Be Equal As Integers                         ${add_result}      1

    # Wait until the Operations panel shows the add operation is completed
    ${wait_result}=  XIQSE Wait Until Device Add Operation Complete   retry_duration=10  retry_count=6
    Should Be Equal As Integers                         ${wait_result}   1

    # Wait until the Operations panel shows the Discover Site Actions operation is completed
    ${wait_result}=  XIQSE Operations Wait Until Operation Complete     Discover Site Actions   retry_duration=10  retry_count=6
    Should Be Equal As Integers                         ${wait_result}   1

    # Verify that the Discover Site Actions operation contains the expected messages
    ${message_result}=  XIQSE Confirm Operations Panel Message For Type     Discover Site Actions   Site Discover Action: Determining Actions By License completed
    Should Be Equal As Integers                         ${message_result}   1

    ${message_result}=  XIQSE Confirm Operations Panel Message For Type     Discover Site Actions   Site Discover Action: Add device completed
    Should Be Equal As Integers                         ${message_result}   1

    # Make sure we didn't get a license limit banner
    Confirm License Limit Warning Message Not Displayed

    # Make sure the device shows up in the Devices table
    ${confirm_result}=  XIQSE Wait Until Device Added   ${DUT1_IP}
    Should Be Equal As Integers                         ${confirm_result}  1

    Navigate and Delete Device  ${DUT1_IP}

    [Teardown]    Navigate and Delete Device  ${DUT1_IP}


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and sets up the components for the test

    # Log into XIQSE and close the banner messages and help panel
    Log Into XIQSE and Close Panels     ${XIQSE_USER}    ${XIQSE_PASSWORD}    url=${XIQSE_URL}

    # Navigate to the Network> Devices> Devices page
    Navigate to Devices and Confirm Success
