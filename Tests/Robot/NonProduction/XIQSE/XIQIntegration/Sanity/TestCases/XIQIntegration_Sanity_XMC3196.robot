#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for sanity testing of the XIQSE to XIQ integration:
#                   - onboards XIQ Site Engine
#                   - confirms XIQSE-managed devices added to Devices view
#                   - confirms XIQ Site Engine values in Devices view
#                   - confirms values of XIQSE-managed devices in Devices view
#                   - confirms XIQ Site Engine values in Device 360 view
#                   - confirms values of XIQSE-managed devices in Device 360 view
#                   - confirms XIQSE-managed devices deleted from Devices view when XIQ Site Engine deleted
#                 This is qTest test case TC-10786 in the CSIT project, and Jira story XMC-3196.

*** Settings ***
Library         xiq/flows/manage/FilterManageDevices.py

Resource        ../../Sanity/Resources/AllResources.robot

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
${XIQSE_IP}             ${xiqse.ip}
${XIQSE_MAC}            ${xiqse.mac}
${XIQSE_NAME}           ${xiqse.name}
${XIQSE_MAKE}           ${xiqse.make}
${XIQSE_MODEL}          ${xiqse.model}
${XIQSE_OS}             ${xiqse.xiq_os}
${XIQSE_VERSION}        ${xiqse.version}
${XIQSE_PRODUCT}        ${xiqse.product}

${XIQ_URL}              ${xiq.test_url}
${XIQ_USER}             ${xiq.tenant_username}
${XIQ_PASSWORD}         ${xiq.tenant_password}

${DUT_SERIAL}           ${netelem1.serial}
${DUT_MAC}              ${netelem1.mac}
${DUT_IP}               ${netelem1.ip}
${DUT_PROFILE}          ${netelem1.profile}
${DUT_NAME}             ${netelem1.name}
${DUT_MODEL}            ${netelem1.model}
${DUT_MAKE}             ${netelem1.make}
${DUT_OS}               ${netelem1.xiq_os}

@{COLUMNS}          Serial #  Managed By  MAC Address  Make  Model  MGT IP Address  OS  OS Version  Cloud Config Groups
${COLUMN_LABELS}    SERIAL,MANAGED BY,MAC,MAKE,MODEL,MGT IP ADDRESS,OS,OS VERSION,CLOUD CONFIG GROUPS
${WORLD_SITE}       World


*** Test Cases ***
Test 1: Confirm Site Engine Onboarded
    [Documentation]     Confirms the XIQ Site Engine can be onboarded successfully
    [Tags]              nightly2    release_testing    staging_testing    tccs_10796    xmc_3196    development    xiqse    xiq_integration    test1

    # Onboard XIQSE to XIQ
    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Enter XIQ Credentials to Auto Onboard XIQSE  ${XIQ_USER}  ${XIQ_PASSWORD}

    # Confirm XIQSE is present in XIQ
    Confirm XIQ Site Engine Onboarded to XIQ

    # Filter to only show devices with the XIQ Site Engine's cloud config group
    Filter on XIQSE CCG Group

Test 2: Confirm Devices Managed by XIQSE are Automatically Onboarded and Connected
    [Documentation]     Confirms the test device managed by XIQSE is automatically onboarded into XIQ
    [Tags]              nightly2    release_testing    staging_testing    tccs_10796    xmc_3196    development    xiqse    xiq_integration    test2

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Confirm Device Serial Present   ${DUT_SERIAL}
    Confirm Device Serial Online    ${DUT_SERIAL}

Test 3: Confirm XIQ Site Engine Values After Onboard
    [Documentation]     Confirms the XIQ Site Engine has the expected values in the Devices table after onboard
    [Tags]              nightly2    release_testing    staging_testing    tccs_10796    xmc_3196    development    xiqse    xiq_integration    test3

    Switch To Window  ${XIQ_WINDOW_INDEX}

    sleep  5 seconds
    Refresh Devices Page

    &{xiqse_info}=     Get Device Row Values  ${XIQSE_MAC}  ${COLUMN_LABELS}

    ${serial_result}=   Get From Dictionary  ${xiqse_info}  SERIAL
    ${mgby_result}=     Get From Dictionary  ${xiqse_info}  MANAGED BY
    ${mac_result}=      Get From Dictionary  ${xiqse_info}  MAC
    ${make_result}=     Get From Dictionary  ${xiqse_info}  MAKE
    ${model_result}=    Get From Dictionary  ${xiqse_info}  MODEL
    ${ip_result}=       Get From Dictionary  ${xiqse_info}  MGT IP ADDRESS
    ${os_result}=       Get From Dictionary  ${xiqse_info}  OS
    ${osver_result}=    Get From Dictionary  ${xiqse_info}  OS VERSION
    ${cldcfg_result}=   Get From Dictionary  ${xiqse_info}  CLOUD CONFIG GROUPS

    Should Be Equal     ${serial_result}    ${XIQSE_SERIAL}
    Should Be Equal     ${mgby_result}      XIQ
    Should Be Equal     ${mac_result}       ${XIQSE_MAC}
    Should Be Equal     ${make_result}      ${XIQSE_MAKE}
    Should Be Equal     ${model_result}     ${XIQSE_MODEL}
    Should Be Equal     ${ip_result}        ${XIQSE_IP}
    Should Be Equal     ${os_result}        ${XIQSE_OS}
    Should Contain      ${osver_result}     ${XIQSE_VERSION}
    Run Keyword If  '21.4' in '${XIQSE_VERSION}'  Should Be Equal     ${cldcfg_result}    ${XIQSE_SERIAL}
    ...  ELSE  Should Be Equal     ${cldcfg_result}    XIQSE-${XIQSE_NAME}

Test 4: Confirm XIQSE-Managed Device Values After Onboard
    [Documentation]     Confirms the test device managed by XIQSE has the expected values in the Devices table after onboard
    [Tags]              nightly2    release_testing    staging_testing    tccs_10796    xmc_3196    development    xiqse    xiq_integration    test4

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Refresh Devices Page

    &{device_info}=     Get Device Row Values  ${DUT_SERIAL}  ${COLUMN_LABELS}

    ${serial_result}=   Get From Dictionary  ${device_info}  SERIAL
    ${mgby_result}=     Get From Dictionary  ${device_info}  MANAGED BY
    ${mac_result}=      Get From Dictionary  ${device_info}  MAC
    ${make_result}=     Get From Dictionary  ${device_info}  MAKE
    ${model_result}=    Get From Dictionary  ${device_info}  MODEL
    ${ip_result}=       Get From Dictionary  ${device_info}  MGT IP ADDRESS
    ${os_result}=       Get From Dictionary  ${device_info}  OS
    ${osver_result}=    Get From Dictionary  ${device_info}  OS VERSION
    ${cldcfg_result}=   Get From Dictionary  ${device_info}  CLOUD CONFIG GROUPS

    Should Be Equal      ${serial_result}    ${DUT_SERIAL}
    Should Be Equal      ${mgby_result}      ${XIQSE_PRODUCT}
    Should Be Equal      ${mac_result}       ${DUT_MAC}
    Should Be Equal      ${make_result}      ${DUT_MAKE}
    Should Be Equal      ${model_result}     ${DUT_MODEL}
    Should Be Equal      ${os_result}        ${DUT_OS}
    Run Keyword If  '21.4' in '${XIQSE_VERSION}'  Should Be Equal     ${cldcfg_result}    ${XIQSE_SERIAL}
    ...  ELSE  Should Be Equal     ${cldcfg_result}    XIQSE-${XIQSE_NAME}

Test 5: Confirm Device360 View Values for XIQ Site Engine
    [Documentation]     Confirms the Device360 view contains correct values for the XIQ Site Engine
    [Tags]              known_issue    nightly2    release_testing    staging_testing    tccs_10796    xmc_3196    development    xiqse    xiq_integration    test5

    Log To Console      "KNOWN ISSUE: XIQ-8873    Potential fix in 22r7"
    Switch To Window  ${XIQ_WINDOW_INDEX}

    Refresh Devices Page
    &{overview_info}=       Get Device360 Overview Information  ${XIQSE_MAC}

    ${overview_name}=       Get From Dictionary  ${overview_info}  host_name
    ${overview_ip}=         Get From Dictionary  ${overview_info}  ip_address
    ${overview_mac}=        Get From Dictionary  ${overview_info}  mac_address
    ${overview_serial}=     Get From Dictionary  ${overview_info}  serial_number
    ${overview_model}=      Get From Dictionary  ${overview_info}  device_model
    ${overview_make}=       Get From Dictionary  ${overview_info}  device_make
    ${overview_ver}=        Get From Dictionary  ${overview_info}  software_version

    Should Be Equal     ${overview_name}    ${XIQSE_IP}
    Should Be Equal     ${overview_ip}      ${XIQSE_IP}
    Should Be Equal     ${overview_mac}     ${XIQSE_MAC}
    Should Be Equal     ${overview_serial}  ${XIQSE_SERIAL}
# ------- APC-43431
    Log To Console      MODEL value ${overview_model} not checked against ${XIQSE_MODEL} until APC-43431 is addressed
#    Should Be Equal    ${overview_model}   ${XIQSE_MODEL}
# ------------------
    Should Be Equal     ${overview_make}    ${XIQSE_MAKE}
    Should Contain      ${overview_ver}     ${XIQSE_VERSION}

Test 6: Confirm Device360 View Values for XIQSE-Managed Device
    [Documentation]     Confirms the Device360 view contains correct values for the XIQSE-managed test device
    [Tags]              nightly2    release_testing    staging_testing    tccs_10796    xmc_3196    development    xiqse    xiq_integration    test6

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Refresh Devices Page
    &{overview_info}=       Get Device360 Overview Information    ${DUT_MAC}

    ${overview_name}=       Get From Dictionary  ${overview_info}  host_name
    ${overview_mac}=        Get From Dictionary  ${overview_info}  mac_address
    ${overview_serial}=     Get From Dictionary  ${overview_info}  serial_number
    ${overview_model}=      Get From Dictionary  ${overview_info}  device_model
    ${overview_make}=       Get From Dictionary  ${overview_info}  device_make

    Should Be Equal     ${overview_name}    ${DUT_NAME}
    Should Be Equal     ${overview_mac}     ${DUT_MAC}
    Should Be Equal     ${overview_serial}  ${DUT_SERIAL}
# ------- APC-43840
    Log To Console      MODEL value ${overview_model} not checked against ${DUT_MODEL} until APC-43840 is addressed
#    Should Be Equal     ${overview_model}   ${DUT_MODEL}
# ------------------
# ------- APC-43433
    Log To Console      MAKE value ${overview_make} not checked against ${DUT_MAKE} until APC-43433 is addressed
#    Should Be Equal    ${overview_make}    ${DUT_MAKE}
# ------------------

Test 7: Confirm Deleting XIQ Site Engine Removes XIQSE-Managed Devices
    [Documentation]     Confirms the test device managed by XIQSE is removed when the XIQ Site Engine is deleted from XIQ
    [Tags]              nightly2    release_testing    staging_testing    tccs_10796    xmc_3196    development    xiqse    xiq_integration    test7

    Switch To Window  ${XIQ_WINDOW_INDEX}

    # Remove XIQSE from XIQ
    Navigate and Remove Device by MAC From XIQ  ${XIQSE_MAC}

    # Confirm the XIQSE-managed test device is removed from XIQ
    Confirm Device Serial Not Present           ${DUT_SERIAL}


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and sets up the components for the test

    XIQSE Log In and Set Window Index
    Set Up XIQSE Components

    XIQ Log In and Set Window Index
    Set Up XIQ Components

Tear Down Test and Close Session
    [Documentation]     Cleans up XIQ and XIQSE test components and closes the browser

    Clean Up XIQ Components
    Clean Up XIQSE Components
    Quit Browser and Confirm Success

XIQSE Log In and Set Window Index
    [Documentation]     Logs into XIQSE and sets the window index

    Log Into XIQSE and Confirm Success              ${XIQSE_USER}  ${XIQSE_PASSWORD}  url=${XIQSE_URL}
    Handle License Agreement If Displayed           ${XIQ_USER}  ${XIQ_PASSWORD}

    # Close any banner messages (Connection Lost with XIQ, License Expiration, etc.) and the Help panel, if displayed
    Close Panels on Login If Displayed

    Onboard XIQSE To XIQ If In Connected Mode    "CONNECTED"    ${XIQSE_IP}  ${XIQ_USER}  ${XIQ_PASSWORD}

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

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Disable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}

    # Enable all columns for event searches
    Set Alarm Event Search Scope    true

    # Confirm the serial number is correct and set the common options needed for automation
    Confirm Serial Number and Set Common Options     ${XIQSE_SERIAL}

    # Create the test device
    Navigate and Create Device      ${DUT_IP}  ${DUT_PROFILE}

Set Up XIQ Components
    [Documentation]     Sets up the XIQ components for the test

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate to XIQ Devices and Confirm Success

    Column Picker Select  @{COLUMNS}

Confirm XIQ Site Engine Onboarded to XIQ
    [Documentation]     Confirms the XIQ Site Engine has been onboarded to XIQ successfully and has connected status

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Confirm Device Serial Present   ${XIQSE_SERIAL}
    Confirm Device Serial Online    ${XIQSE_SERIAL}

Filter on XIQSE CCG Group
    [Documentation]     Filters by the XIQSE CCG group to make sure the test has just our devices displayed

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Log To Console  >> Navigating away from and back to the Devices page until APC-44605 is fixed <<
    Navigate Configure Network Policies
    Navigate to XIQ Devices and Confirm Success
    Run Keyword If  '21.4' in '${XIQSE_VERSION}'  Set CCG Group Filter For Older XIQSE
    ...  ELSE  Set CCG Group Filter For Current XIQSE

Set CCG Group Filter For Older XIQSE
    [Documentation]     Filters by the XIQSE CCG group using XIQSE Serial Number

    ${filter_result}=  Set Cloud Config Groups Filter   ${XIQSE_SERIAL}  true
    Should Be Equal As Integers                         ${filter_result}  1

Set CCG Group Filter For Current XIQSE
    [Documentation]     Filters by the XIQSE CCG group using XIQSE Host Name

    ${filter_result}=  Set Cloud Config Groups Filter   XIQSE-${XIQSE_NAME}  true
    Should Be Equal As Integers                         ${filter_result}  1

Clean Up XIQ Components
    [Documentation]     Cleans up components used in XIQ during the test and logs out

    Switch To Window                            ${XIQ_WINDOW_INDEX}

    # Make sure XIQSE has been removed
    Navigate and Remove Device by MAC From XIQ  ${XIQSE_MAC}

    Log Out of XIQ and Confirm Success
    Close Window                                ${XIQ_WINDOW_INDEX}

Clean Up XIQSE Components
    [Documentation]     Cleans up components used in XIQSE during the test and logs out

    Switch To Window                        ${XIQSE_WINDOW_INDEX}

    Enable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}

    # Disable all columns for event searches
    Set Alarm Event Search Scope    false

    Navigate and Delete Device              ${DUT_IP}
    Log Out of XIQSE and Confirm Success
