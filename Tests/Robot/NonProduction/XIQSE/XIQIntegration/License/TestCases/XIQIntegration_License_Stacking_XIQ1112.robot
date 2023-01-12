#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Charles Bickford
# Description   : Test Suite for sanity testing of XIQ stack licensing.
#                 This is qTest MD-18624 in the XIQ Mainline (US) project.

*** Settings ***
Library         common/Screen.py
Library         common/Utils.py

Resource        ../../License/Resources/AllResources.robot

Force Tags      testbed_1_node

Suite Setup     Log In and Set Up Test Components
Suite Teardown  Tear Down Test and Close Session

*** Variables ***
${XIQSE_URL}            ${xiqse.url}
${XIQSE_USER}           ${xiqse.user}
${XIQSE_PASSWORD}       ${xiqse.password}
${XIQSE_IP}             ${xiqse.ip}
${XIQSE_PROFILE}        ${xiqse.profile}
${XIQSE_SERIAL}         ${xiqse.serial}
${XIQSE_MAC}            ${xiqse.mac}
${XIQSE_NAME}           ${xiqse.name}
${XIQSE_MAKE}           ${xiqse.make}
${XIQSE_MODEL}          ${xiqse.model}
${XIQSE_PRODUCT}        ${xiqse.product}
${XIQSE_VERSION}        ${xiqse.version}
${INSTALL_MODE}             ${upgrades.install_mode}

${XIQ_URL}                  ${xiq.test_url}
${XIQ_USER}                 ${xiq.tenant_username}
${XIQ_PASSWORD}             ${xiq.tenant_password}

${DUT_IP}                   ${simelem1.ip}
${DUT_PROFILE}              ${simelem1.profile}
${DUT_LICENSE}              ${simelem1.license}

${SNMPSIM_IP}               ${simelem1.snmpsimip}
${SNMPSIM_USER}             ${simelem1.snmpsimloginuser}
${SNMPSIM_PW}               ${simelem1.snmpsimloginpw}
${SNMPSIM_MIB_LOCATION}     ${simelem1.stackmiblocation}
${SNMPSIM_MIB_FILE}         ${simelem1.stackmibfile}
${SNMPSIM_MIB_7SLOT}        ${simelem1.stackprofile7slot}
${SNMPSIM_MIB_8SLOT}        ${simelem1.stackprofile8slot}
${SSH_PORT}                 22

${WORLD_SITE}               World
${TEST_ARCHIVE}             /World
${OPS_DEVICE_DISCOVERY}     Device Discovery - Operation Complete
${OPS_LICENSE_CHECK}        Device License is XIQ_${DUT_LICENSE}

${PILOT_ENTITLEMENT}        ${xiq.pilot_entitlements}
${NAVIGATOR_ENTITLEMENT}    ${xiq.navigator_entitlements}

${PILOT_LICENSE}            XIQ-PIL-S-C
${NAVIGATOR_LICENSE}        XIQ-NAV-S-

*** Test Cases ***
Test 1: Add Device and Confirm Success
    [Documentation]     Confirms a device can be successfuly aded to XIQ-SE
    [Tags]              test1    stacking    tcxm-15241

    # Make sure test starts as 7 slot
    Update SIM Device MIB File  ${SNMPSIM_IP}    ${SNMPSIM_USER}    ${SNMPSIM_PW}    ${SNMPSIM_MIB_LOCATION}
    ...    ${SNMPSIM_MIB_7SLOT}    ${ SNMPSIM_MIB_FILE}    ${SSH_PORT}
    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Navigate and Create Device                          ${DUT_IP}  ${DUT_PROFILE}
    Wait For Operations Panel Operation To Complete     Device Added
    Confirm IP Address Present in Devices Table         ${DUT_IP}

Test 2: Verify Operations Panel Operations Complete Successfully
    [Documentation]     Confirms all operations panel operations completed successfully
    [Tags]              test2    stacking    tcxm-15241

    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Log To Console  >> Confirms Device Poller Completed
    Wait For Operations Panel Operation To Complete     Device Poller

    Log To Console  >> Confirms Device License Check Completed
    Wait For Operations Panel Operation To Complete     Device License Check

    Log To Console  >> Confirms Discover Site Actions Completed
    Wait For Operations Panel Operation To Complete     Discover Site Actions

    Log To Console  >> Confirms Inventory Audit Completed
    Wait For Operations Panel Operation To Complete     Inventory Audit

    Log To Console  >> Confirms operations panel message for device discovery
    Confirm Operations Panel Message For Type           Inventory Audit    ${OPS_DEVICE_DISCOVERY}

    Log To Console  >> Confirms operations panel message for device license check
    Confirm Operations Panel Message For Type           Device License Check    ${OPS_LICENSE_CHECK}

Test 3: Verify Device Assigned Correct License
    [Documentation]     Navigates and verifies the device license on the specified device
    [Tags]              test3    stacking    tcxm-15241

    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Navigate and Confirm Device License                 ${DUT_IP}  ${DUT_LICENSE}

Test 4: Verify Device in XIQ Assigned Correct License Count
    [Documentation]     Navigates to XIQ Devices and verifies the correct consumed licensed.
    [Tags]              test4    stacking     tcxm-15241

    # Confirm a Pilot entitlement is used for this device (1 for XIQSE, and 7 for the device, so a total of 8),
    XIQ Confirm Expected Pilot Licenses Consumed        8


Test 5: Add Stack Unit And Verify in XIQ Assigned Correct License Count
    [Documentation]     Add a stack element and Navigates to XIQ Devices and verifies the correct consumed licensed.
    [Tags]              test5    stacking     tcxm-15241

    Update SIM Device MIB File  ${SNMPSIM_IP}    ${SNMPSIM_USER}    ${SNMPSIM_PW}    ${SNMPSIM_MIB_LOCATION}
    ...    ${SNMPSIM_MIB_8SLOT}    ${ SNMPSIM_MIB_FILE}    ${SSH_PORT}

    XIQSE Rediscover
    # Confirm a Pilot entitlement is used for this device (1 for XIQSE, and 8 for the device, so a total of 9),
    XIQ Confirm Expected Pilot Licenses Consumed        9

Test 6: Delete Stack Unit And Verify in XIQ Assigned Correct License Count
    [Documentation]     Delete a stack unit and Navigates to XIQ Devices and verifies the correct consumed licensed.
    [Tags]              test6    stacking     tcxm-15241

    Update SIM Device MIB File  ${SNMPSIM_IP}    ${SNMPSIM_USER}    ${SNMPSIM_PW}    ${SNMPSIM_MIB_LOCATION}
    ...    ${SNMPSIM_MIB_7SLOT}    ${SNMPSIM_MIB_FILE}    ${SSH_PORT}

    XIQSE Rediscover
    # Confirm a Pilot entitlement is used for this device (1 for XIQSE, and 7 for the device, so a total of 8),
    XIQ Confirm Expected Pilot Licenses Consumed        8

Test 7: Delete Device and Confirm Success
    [Documentation]     Navigates and deletes the specified device from XIQ-SE and confirms it was removed successfully
    [Tags]              test7    stacking     tcxm-15241

    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Navigate to Devices and Confirm Success
    Delete Device and Confirm Success                   ${DUT_IP}
    Wait For Operations Panel Operation To Complete     Device Removed
    Confirm IP Address Not Present in Devices Table     ${DUT_IP}
    # Confirm a Pilot entitlement are freed for this device (1 for XIQSE),
    XIQ Confirm Expected Pilot Licenses Consumed        1

Test 8: Verify Event for Delete Device
    [Documentation]     Navigates and confirms the events view contains the expected event for delete device
    [Tags]              test8    stacking    tcxm-15241

    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Navigate to Events and Confirm Success
    Set Event Time Range and Confirm Success            Last 30 Minutes
    Set Event Type and Confirm Success                  Inventory
    Set Event Search String and Confirm Success         deleted from the database
    Confirm Event Row Contains Text                     ${DUT_IP} and Site Engine data were deleted from the database
    Clear Event Search String and Confirm Success

Test 9: Add Stack Unit And Verify in XIQ Enters Violation State
    [Documentation]     Delete a stack unit and Navigates to XIQ Devices and verifies the correct consumed licensed.
    [Tags]              test9    stacking     tcxm-15241

    Log To Console    "TBD"

Test 10: Verify In XIQ Licenses Are Released
    [Documentation]     Navigates to XIQ and verify licenss have been released.
    [Tags]              test10    stacking    tcxm-15241

    Log To Console    "TBD"

*** Keywords ***
Log In and Set Up Test Components
    [Documentation]     Sets up the components for the test

    XIQSE Log In and Set Window Index
    Set Up XIQSE Components

    XIQ Log In and Set Window Index
    Set Up XIQ Components

    # Onboard the Site Engine to XIQ
    Onboard XIQ Site Engine and Confirm Success

    # Port Information comes in on the update cycle
    Log To Console  Sleeping for 2 minutes to wait for port information to be reported...
    Count Down in Minutes  2

Tear Down Test and Close Session
    [Documentation]     Cleans up XIQ and XIQSE test components

    Clean Up XIQ Components
    Clean Up XIQSE Components
    Quit Browser and Confirm Success

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

    # Store the window index so we can switch between XIQSE and XIQ
    ${xiq_win}=  Get Window Index
    Log To Console  Setting XIQ Window Index to ${xiq_win}
    Set Suite Variable  ${XIQ_WINDOW_INDEX}  ${xiq_win}

Set Up XIQSE Components
    [Documentation]     Sets up the XIQSE components for the test

    Disable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}

    # Enable all columns for event searches
    Set Alarm Event Search Scope    true

    # Confirm the serial number is correct and set the common options needed for automation
    Confirm Serial Number and Set Common Options     ${XIQSE_SERIAL}

Set Up XIQ Components
    [Documentation]     Sets up the XIQ components for the test

    Remove Existing Site Engine from XIQ

    ${date_time}=       Get UTC Time    %Y-%m-%d %H:%M:%S
    Set Suite Variable  ${TEST_TIME}   ${date_time}

Onboard XIQ Site Engine and Confirm Success
    [Documentation]     Confirms the XIQ Site Engine can be onboarded successfully

    Remove Existing Site Engine from XIQ
    Auto Onboard XIQ Site Engine
    Confirm XIQ Site Engine Onboarded to XIQ

Remove Existing Site Engine from XIQ
    [Documentation]     Removes the XIQ Site Engine from XIQ if it exists

    Switch To Window  ${XIQ_WINDOW_INDEX}

    XIQ Navigate to Devices and Confirm Success

    # If the XIQ Site Engine has already been onboarded, delete it
    ${search_result}=  Search Device   ${XIQSE_MAC}
    Run Keyword If  '${search_result}' == '1'    Delete Device  device_mac=${XIQSE_MAC}

Auto Onboard XIQ Site Engine
    [Documentation]     Onboards the specified XIQ Site Engine, deleting it first if it already exists

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Enter XIQ Credentials to Auto Onboard XIQSE     ${XIQ_USER}  ${XIQ_PASSWORD}

Confirm XIQ Site Engine Onboarded to XIQ
    [Documentation]     Confirms the XIQ Site Engine has been onboarded to XIQ successfully

    Switch To Window  ${XIQ_WINDOW_INDEX}

    ${search_result}=  Wait Until Device Added      ${XIQSE_SERIAL}
    Should Be Equal As Integers                     ${search_result}    1

    ${device_status}=  Wait Until Device Online     ${XIQSE_SERIAL}
    Should Be Equal As Integers                     ${device_status}    1

XIQ Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Manage> Devices view in XIQ and confirms the action was successful

    Switch To Window  ${XIQ_WINDOW_INDEX}

    ${nav_result}=  Navigate to Devices
    Should Be Equal As Integers  ${nav_result}  1

Clean Up XIQ Components
    [Documentation]     Cleans up components used in XIQ during the test, logs out, and closes the browser

    Switch To Window  ${XIQ_WINDOW_INDEX}

    XIQ Navigate to Devices and Confirm Success
    ${del_result}=  Delete Device   device_mac=${XIQSE_MAC}
    Should Be Equal As Integers     ${del_result}  1

    # Log out and close the window
    [Teardown]  XIQ Log Out and Close Window

Clean Up XIQSE Components
    [Documentation]     Cleans up components used in XIQSE during the test, logs out, and closes the browser

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Enable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}

    # Disable all columns for event searches
    Set Alarm Event Search Scope    false

    # Make sure XIQ sharing is enabled
    XIQSE Enable XIQ Connection Sharing and Save

    # Log out
    Log Out of XIQSE and Confirm Success

XIQ Log Out and Close Window
    [Documentation]     Logs out of XIQ and closes the window

    Switch To Window    ${XIQ_WINDOW_INDEX}

    Log Out of XIQ and Confirm Success
    Close Window    ${XIQ_WINDOW_INDEX}

XIQ Confirm Expected Pilot Licenses Consumed
    [Documentation]  Confirms the expected number of pilot licenses are consumed based on entitlements
    [Arguments]      ${consumed}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Confirm Expected Pilot Licenses Consumed  ${PILOT_ENTITLEMENT}  ${consumed}  ${PILOT_LICENSE}

XIQSE Rediscover
    [Documentation]     Just a test

    Switch To Window  ${XIQSE_WINDOW_INDEX}
    XIQSE Clear Operations Panel
    Navigate to Devices and Confirm Success
    XIQSE Perform Rediscover Device    ${DUT_IP}
    Wait For Operations Panel Operation To Complete     Device Poller
    # Now wait 2 minutes for XIQSE to Update XIQ after the rediscover
    Sleep    2 minutes
