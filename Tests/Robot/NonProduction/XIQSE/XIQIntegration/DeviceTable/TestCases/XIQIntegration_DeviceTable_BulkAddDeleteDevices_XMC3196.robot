#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for testing XIQSE-XIQ Integration for the Bulk Add/Delete functionality.
#                     A discovery is performed in XIQ-SE which results in a large number of devices.
#                     XIQ is checked to confirm the devices are successfully added.
#                     XIQ-SE's Diagnostic view is checked for a SUCCESS onboard status.
#                     The devices are then multi-selected and deleted in bulk from XIQ-SE.
#                     XIQ is then checked again to confirm the devices are removed.
#                 This is qTest test case TC-8968 in the CSIT project.

*** Settings ***
Library         Collections
Library         common/TestFlow.py

Resource        ../../DeviceTable/Resources/AllResources.robot

Force Tags      testbed_license_node

Suite Setup     Log In and Set Up Test Components
Suite Teardown  Tear Down Test and Close Session


*** Variables ***
# Defaults
${ENV}                    environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                   topo.test.xiqse1.connected.yaml
${TESTBED}                RDU/Prod/rdu_xiqse_license1.yaml

${XIQSE_URL}              ${xiqse.url}
${XIQSE_USER}             ${xiqse.user}
${XIQSE_PASSWORD}         ${xiqse.password}
${XIQSE_SERIAL}           ${xiqse.serial}
${XIQSE_MAC}              ${xiqse.mac}

${XIQ_URL}                ${xiq.test_url}
${XIQ_USER}               ${xiq.tenant_username}
${XIQ_PASSWORD}           ${xiq.tenant_password}

${DISCOVER_IP_START}      ${netelem7.ip}
${DISCOVER_IP_END}        ${netelem8.ip}
${DISCOVER_PROFILE}       ${netelem7.profile}

${DISCOVER_SUBNET}        ${netelem7.ip}/24

${TEST_SITE}              AutomationSite
${DISCOVERY_TYPE}         RANGE
${WORLD_SITE}             World


*** Test Cases ***
Test 1: Bulk Add
    [Documentation]     Confirms a bulk add in XIQ-SE adds all devices to XIQ
    [Tags]              staging_testing    release_testing    license_testing    tccs_8968    xmc_3196    development    xiqse    xiq_integration    bulk    test1

    # Obtain the number of devices in XIQ before the discovery
    Switch To Window  ${XIQ_WINDOW_INDEX}
    Refresh Devices Page
    ${xiq_before}=    Get Total Device Count
    Log To Console  XIQ Device Count Before Discovery Is ${xiq_before}

    # Obtain the number of rows in the XIQ Device Message Details table before the discovery
    XIQSE Navigate to XIQ Device Message Details View and Confirm Success
    XIQSE XIQ Device Message Details Refresh Table
    Refresh Device Message Details Using Navigation
    ${diag_before}=  XIQSE Get XIQ Device Message Details Row Count
    Log To Console  XIQ-SE Diagnostics XIQ Device Message Details Row Count Before Delete Is ${diag_before}

    # Obtain the number of successfully onboarded devices in the XIQ Device Message Details table before the discovery
    XIQSE Navigate to XIQ Device Message Details View and Confirm Success
    XIQSE XIQ Device Message Details Show Columns  Onboard Status  Onboard
    XIQSE XIQ Device Message Details Refresh Table
    Refresh Device Message Details Using Navigation
    Filter XIQ Device Message Details Table and Confirm Success  SUCCESS
    ${diag_success_before}=  XIQSE Get XIQ Device Message Details Row Count
    Clear XIQ Device Message Details Table Filter and Confirm Success

    ${diag_before}=  XIQSE Get XIQ Device Message Details Row Count
    Log To Console  XIQ-SE Diagnostics XIQ Device Message Details Row Count Before Delete Is ${diag_before}

    # Clear the current contents of the operations panel
    Clear Operations Panel and Confirm Success

    # Perform discovery and confirm devices are added to XIQ-SE
    XIQSE Navigate to Site and Confirm Success            ${TEST_SITE}
    Run Keyword If  '${DISCOVERY_TYPE}' == 'RANGE'
    ...  XIQSE Perform IP Range Discovery and Confirm Success    ${DISCOVER_IP_START}  ${DISCOVER_IP_END}  ${DISCOVER_PROFILE}
    Run Keyword If  '${DISCOVERY_TYPE}' == 'SUBNET'
    ...  XIQSE Perform Subnet Discovery and Confirm Success    ${DISCOVER_SUBNET}  ${DISCOVER_PROFILE}

    # Confirm devices are all added to XIQ
    Wait Until Keyword Succeeds  10 min  30 sec  Confirm XIQ Device Count Increase  ${xiq_before}  ${DEVICE_COUNT}

    # Confirm the Diagnostics view shows the devices onboarded with SUCCESS
    XIQSE Confirm Diagnostics Shows Devices Onboarded Successfully  ${diag_before}  ${diag_success_before}  ${DEVICE_COUNT}

Test 2: Bulk Delete
    [Documentation]     Confirms a bulk delete in XIQ-SE removes all devices from XIQ
    [Tags]              staging_testing    release_testing    license_testing    tccs_8968    xmc_3196    development    xiqse    xiq_integration    bulk    test2
    Depends On          test1

    # Obtain the number of rows in the XIQ Device Message Details table before the delete
    XIQSE Navigate to XIQ Device Message Details View and Confirm Success
    XIQSE XIQ Device Message Details Refresh Table
    Refresh Device Message Details Using Navigation
    ${diag_before}=  XIQSE Get XIQ Device Message Details Row Count
    Log To Console  XIQ-SE Diagnostics XIQ Device Message Details Row Count Before Delete Is ${diag_before}

    # Obtain the number of devices in XIQ before the delete
    Switch To Window  ${XIQ_WINDOW_INDEX}
    Refresh Devices Page
    ${xiq_before}=    Get Total Device Count
    Log To Console  XIQ Device Count Before Discovery Is ${xiq_before}

    # Delete all the discovered devices from XIQ-SE
    XIQSE Delete All Site Devices and Confirm Success    ${TEST_SITE}

    # Confirm all devices are removed from XIQ
    Wait Until Keyword Succeeds  10 min  30 sec  Confirm XIQ Device Count Decrease  ${xiq_before}  ${DEVICE_COUNT}

    # Confirm the Diagnostics view removes the onboarded devices
    XIQSE Confirm Diagnostics Removes Onboarded Devices  ${diag_before}  ${DEVICE_COUNT}


*** Keywords ***
Log In and Set Up Test Components
    [Documentation]     Sets up the components for the test

    XIQSE Log In and Set Window Index
    Set Up XIQSE Components

    XIQ Log In and Set Window Index
    Set Up XIQ Components

    Onboard XIQ Site Engine and Confirm Success

Tear Down Test and Close Session
    [Documentation]     Cleans up XIQ and XIQ-SE test components

    Clean Up XIQSE Components
    Clean Up XIQ Components

    Quit Browser and Confirm Success

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
    [Documentation]     Sets up the XIQSE components for the test

    Disable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}

    # Enable all columns for event searches
    Set Alarm Event Search Scope    true

    # Confirm the serial number is correct and set the common options needed for automation
    Confirm Serial Number and Set Common Options     ${XIQSE_SERIAL}

    # Create the test site
    XIQSE Create Site and Confirm Success  ${TEST_SITE}

Set Up XIQ Components
    [Documentation]     Sets up the XIQ components for the test

    # Remove XIQSE if it is already present
    Navigate and Remove Device by MAC From XIQ  ${XIQSE_MAC}

Onboard XIQ Site Engine and Confirm Success
    [Documentation]     Confirms the XIQ Site Engine can be onboarded successfully

    Auto Onboard XIQ Site Engine
    Confirm XIQ Site Engine Onboarded to XIQ

Auto Onboard XIQ Site Engine
    [Documentation]     Onboards the specified XIQ Site Engine, deleting it first if it already exists

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Enter XIQ Credentials to Auto Onboard XIQSE  ${XIQ_USER}  ${XIQ_PASSWORD}

Confirm XIQ Site Engine Onboarded to XIQ
    [Documentation]     Confirms the XIQ Site Engine has been onboarded to XIQ successfully

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Confirm Device Serial Present   ${XIQSE_SERIAL}
    Confirm Device Serial Online    ${XIQSE_SERIAL}

XIQSE Create Site and Confirm Success
    [Documentation]     Creates the specified site under the World node
    [Arguments]  ${site}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # Navigate to the Devices tab for the World node
    XIQSE Navigate to Site Devices and Confirm Success  World

    # Create the specified site
    Create Site and Confirm Success  ${site}

XIQSE Delete Site and Confirm Success
    [Documentation]     Deletes the specified site
    [Arguments]  ${site}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # Navigate to the Devices tab for the World node
    XIQSE Navigate to Site Devices and Confirm Success  World

    # Delete the specified site
    Delete Site and Confirm Success  ${site}

XIQSE Navigate to Site and Confirm Success
    [Documentation]     Navigates to the specified site in XIQ-SE and confirms the action was successful
    [Arguments]         ${site}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # Navigate to the Devices view
    Navigate to Devices and Confirm Success

    # Select the site in the tree
    Navigate to Site Tree Node and Confirm Success  ${site}

    # Navigate to the site context
    Navigate to Site Tab and Confirm Success  ${site}

XIQSE Navigate to Site Devices and Confirm Success
    [Documentation]     Navigates to the Devices tab for the specified site in XIQ-SE and confirms the action was successful
    [Arguments]         ${site}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # Navigate to the Devices view
    Navigate to Devices and Confirm Success

    # Select the site in the tree
    Select Site and Confirm Success  ${site}

    # Select the Devices tab
    ${sel_tab}=  XIQSE Devices Select Devices Tab
    Should Be Equal As Integers     ${sel_tab}     1

XIQSE Perform Subnet Discovery and Confirm Success
    [Documentation]     Performs a subnet discovery in XIQ-SE and confirms the action was successful
    [Arguments]         ${subnet_mask}  ${profile}

    Perform Subnet Discovery and Confirm Success  ${subnet_mask}  ${profile}  auto_add=true  trap=false  syslog=false  archive=false

    ${DEVICE_COUNT}=  XIQSE Operations Get Discovered Device Count
    Log To Console  DISCOVERED DEVICE COUNT IS ${DEVICE_COUNT}
    Set Suite Variable  ${DEVICE_COUNT}

    ${result}=  XIQSE Devices Select Devices Tab
    Should Be Equal As Integers  ${result}  1

    ${result}=  XIQSE Wait Until Devices Present  ${DEVICE_COUNT}
    Should Be Equal As Integers  ${result}  1

XIQSE Perform IP Range Discovery and Confirm Success
    [Documentation]     Performs an IP Range discovery in XIQ-SE and confirms the action was successful
    [Arguments]         ${ip_start}  ${ip_end}  ${profile}

    Perform IP Range Discovery and Confirm Success  ${ip_start}  ${ip_end}  ${profile}  auto_add=true  trap=false  syslog=false  archive=false

    ${DEVICE_COUNT}=  XIQSE Operations Get Discovered Device Count
    Log To Console  DISCOVERED DEVICE COUNT IS ${DEVICE_COUNT}
    Set Suite Variable  ${DEVICE_COUNT}

    ${result}=  XIQSE Devices Select Devices Tab
    Should Be Equal As Integers  ${result}  1

    ${result}=  XIQSE Wait Until Devices Present  ${DEVICE_COUNT}
    Should Be Equal As Integers  ${result}  1

    Wait For Operations Panel Operation To Complete     Discover Site Actions

XIQSE Delete All Site Devices and Confirm Success
    [Documentation]     Deletes all devices in the specified site and confirms the action is successful
    [Arguments]         ${site}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # Navigate to the Devices tab for the site
    XIQSE Navigate to Site Devices and Confirm Success  ${site}

    # Delete all devices within the site
    ${del_result}=  XIQSE Delete All Devices
    Should Be Equal As Integers  ${del_result}  1

    # Confirm the device count is zero
    ${count_result}=  XIQSE Get Device Total Count
    Should Be Equal As Integers  ${count_result}  0

XIQSE Navigate to XIQ Device Message Details View and Confirm Success
    [Documentation]     Navigates to the XIQ Device Message Details view and confirms the action was successful.

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate to XIQ Device Message Details and Confirm Success

XIQSE Confirm Diagnostics Shows Devices Onboarded Successfully
    [Documentation]     Confirms the specified number of devices show an onboard status of SUCCESS
    [Arguments]  ${before_count}  ${success_before_count}  ${added_count}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # Navigate to the Diagnostics XIQ Device Message Details view
    Navigate to XIQ Device Message Details and Confirm Success

    # Make sure the Onboard Status column is visible
    XIQSE XIQ Device Message Details Show Columns  Onboard Status
    sleep  2 seconds

    # Confirm the number of rows in the view, plus the number of rows existing before,
    # is equal to the number of devices added
    XIQSE XIQ Device Message Details Refresh Table
    Refresh Device Message Details Using Navigation
    ${current_count}=  XIQSE Get XIQ Device Message Details Row Count
    Should Be True  ${before_count} + ${added_count} == ${current_count}

    # Perform a search for "SUCCESS" and confirm the number of rows matches the number of devices added
    Filter XIQ Device Message Details Table and Confirm Success  SUCCESS
    ${success_count}=  XIQSE Get XIQ Device Message Details Row Count
    Should Be True  ${success_before_count} + ${added_count} == ${success_count}
    Clear XIQ Device Message Details Table Filter and Confirm Success

XIQSE Confirm Diagnostics Removes Onboarded Devices
    [Documentation]     Confirms the specified number of devices have been removed from the view
    [Arguments]  ${before_count}  ${removed_count}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # Navigate to the Diagnostics XIQ Device Message Details view
    Navigate to XIQ Device Message Details and Confirm Success

    # Confirm the number of rows in the view, plus one more to account for the XIQ-SE server, is greater than or equal to
    # the number of devices discovered
    XIQSE XIQ Device Message Details Refresh Table
    Refresh Device Message Details Using Navigation
    ${current_count}=  XIQSE Get XIQ Device Message Details Row Count
    Should Be True  ${before_count} - ${removed_count} == ${current_count}

Filter XIQ Device Message Details Table and Confirm Success
    [Documentation]     Sets a filter on the XIQ Device Message Details table and confirms the action was successful.
    [Arguments]  ${value}

    ${result}=  XIQSE XIQ Device Message Details Filter Table  ${value}
    Should Be Equal As Integers  ${result}  1

Clear XIQ Device Message Details Table Filter and Confirm Success
    [Documentation]     Clears the filter on the XIQ Device Message Details table and confirms the action was successful.

    ${result}=  XIQSE XIQ Device Message Details Clear Filter
    Should Be Equal As Integers  ${result}  1

Confirm XIQ Device Count Increase
    [Documentation]     Confirms the device count in XIQ increases by the specified amount
    [Arguments]  ${before}  ${added_devices}

    # Obtain the current number of devices in XIQ
    Switch To Window  ${XIQ_WINDOW_INDEX}
    Refresh Devices Page
    ${current_count}=    Get Total Device Count
    Log To Console  Current XIQ Device Count Is ${current_count}

    # Check if the current count is the expected value
    Should Be True  ${before} + ${added_devices} == ${current_count}

Confirm XIQ Device Count Decrease
    [Documentation]     Confirms the device count in XIQ decreases by the specified amount
    [Arguments]  ${before}  ${removed_devices}

    # Obtain the current number of devices in XIQ
    Switch To Window  ${XIQ_WINDOW_INDEX}
    Refresh Devices Page
    ${current_count}=    Get Total Device Count
    Log To Console  Current XIQ Device Count Is ${current_count}

    # Check if the current count is the expected value
    Should Be True  ${before} - ${removed_devices} == ${current_count}

Clean Up XIQ Components
    [Documentation]     Cleans up components used in XIQ during the test, logs out, and closes the browser

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate and Remove Device by MAC From XIQ  ${XIQSE_MAC}

    Log Out of XIQ and Confirm Success

Clean Up XIQSE Components
    [Documentation]     Cleans up components used in XIQ-SE during the test, logs out, and closes the browser

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Enable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}

    # Disable all columns for event searches
    Set Alarm Event Search Scope    false

    # Clean up the Discover tab
    XIQSE Navigate to Site and Confirm Success    ${TEST_SITE}
    Run Keyword If  '${DISCOVERY_TYPE}' == 'RANGE'
    ...    Clean Up IP Range Discovery Settings and Confirm Success  ${DISCOVER_IP_START}  ${DISCOVER_IP_END}  ${DISCOVER_PROFILE}
    Run Keyword If  '${DISCOVERY_TYPE}' == 'SUBNET'
    ...    Clean Up Subnet Discovery Settings and Confirm Success  ${DISCOVER_SUBNET}  ${DISCOVER_PROFILE}

    # Delete the Site
    XIQSE Delete Site and Confirm Success  ${TEST_SITE}

    # Reset the options
    ${options_result}=  XIQSE Restore Default XIQ Connection Options and Save
    Should Be Equal As Integers  ${options_result}     1

    # Clear the current contents of the operations panel
    Clear Operations Panel and Confirm Success

    # Log out
    Log Out of XIQSE and Confirm Success
