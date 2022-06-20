#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for testing XIQSE-XIQ Integration for the Device 360 view functionality
#                 when the Site Engine is modeled as an SNMP-managed device.
#                 This is qTest test case (CSIT project):
#                   TC-9009: D360 View:XIQ Site Engine - managed device

*** Settings ***
Library         common/Screen.py
Library         common/Utils.py

Resource        ../../D360/Resources/AllResources.robot

Force Tags      testbed_1_node

Suite Setup     Log In and Set Up Test Components
Suite Teardown  Tear Down Test and Close Session


*** Variables ***
# Defaults
${ENV}                  environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                 topo.test.xiqse1.connected.yaml
${TESTBED}              SALEM/Dev/devices-salem-acceptance.yaml

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

${XIQ_URL}              ${xiq.test_url}
${XIQ_USER}             ${xiq.tenant_username}
${XIQ_PASSWORD}         ${xiq.tenant_password}

${WORLD_SITE}           World

*** Test Cases ***
Test 1: Confirm Basic Device360 Values
    [Documentation]     Confirms basic Device360 values for an XIQ Site Engine which is SNMP-managed
    [Tags]              nightly2    release_testing    staging_testing    csit_tc_9009   xmc_3196    development    known_issue    xiqse    xiq_integration    d360    managed    test1

    Log To Console  KNOWN ISSUE: APC-45291 (Active Since Time is not always matching)

    # Confirm XIQSE is shown as onboarded within XIQSE
    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Navigate to Devices and Confirm Success
    Confirm XIQSE Device Onboarded to XIQ    ${XIQSE_IP}

    # Confirm Values in D360 View
    Switch To Window  ${XIQ_WINDOW_INDEX}
    ${nav_result}=  Navigate to Device360 Page with MAC  ${XIQSE_MAC}
    Should Be Equal As Integers  ${nav_result}  1
    Confirm Device360 Title for XIQ Site Engine
    Confirm Device360 Side Bar Information for XIQ Site Engine
    Confirm Device360 Top Bar Information for XIQ Site Engine
    Confirm Device360 CPU Usage Information for XIQ Site Engine
    Confirm Device360 Memory Usage Information for XIQ Site Engine
    Confirm Device360 Ports Information Is Displayed

    [Teardown]  Run Keywords
    ...  Switch To Window  ${XIQ_WINDOW_INDEX}
    ...  AND
    ...  Close Device360 Window

Test 2: Confirm Alarm and Event Device360 Values
    [Documentation]     Confirms Device360 Alarm and Event values for an XIQ Site Engine which is SNMP-managed
    [Tags]              nightly2    release_testing    staging_testing    csit_tc_9009   xmc_3196    development    known_issue    xiqse    xiq_integration    d360    managed    test2

    Log To Console  UNDER INVESTIGATION: Active Alarms panel is not updating until next sync on some systems

    # Make sure the Device360 window is closed from the previous test
    Close Device360 Window

    # Generate the alarm and event
    Generate Alarm and Event for XIQ Site Engine

    # Confirm Values in D360 View
    Switch To Window  ${XIQ_WINDOW_INDEX}
    ${nav_result}=  Navigate to Device360 Page with MAC  ${XIQSE_MAC}
    Should Be Equal As Integers  ${nav_result}  1
    Save Screen Shot

    Confirm Device360 Alarms
    Confirm Device360 Events

    [Teardown]  Run Keywords
    ...  Switch To Window  ${XIQ_WINDOW_INDEX}
    ...  AND
    ...  Close Device360 Window
    ...  AND
    ...  Switch To Window  ${XIQSE_WINDOW_INDEX}
    ...  AND
    ...  Enable XIQ Connection Sharing and Confirm Success


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

Log Out of XIQ and Confirm Success
    [Documentation]     Logs out of XIQ and confirms the logout was successful

    Switch To Window  ${XIQ_WINDOW_INDEX}

    ${result}=  Logout User
    Should Be Equal As Integers     ${result}     1

Set Up XIQSE Components
    [Documentation]     Sets up the XIQSE components for the test

    Disable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}

    # Confirm the serial number is correct and set the common options needed for automation
    Confirm Serial Number and Set Common Options     ${XIQSE_SERIAL}

    # Add XIQSE as an SNMP-managed device
    Add Device to XIQSE and Confirm Success    ${XIQSE_IP}    ${XIQSE_PROFILE}

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
    ${search_result}=  Search Device Mac   ${XIQSE_MAC}
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

XIQSE Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Network> Devices> Devices view in XIQSE and confirms the action was successful

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate to Devices and Confirm Success

XIQ Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Manage> Devices view in XIQ and confirms the action was successful

    Switch To Window  ${XIQ_WINDOW_INDEX}

    ${nav_result}=  Navigate to Devices
    Should Be Equal As Integers  ${nav_result}  1

Add Device to XIQSE and Confirm Success
    [Documentation]     Adds the specified device to XIQSE
    [Arguments]         ${ip}  ${profile}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate and Create Device  ${ip}  ${profile}
    Confirm Device Status Up    ${ip}

Delete XIQSE Test Device and Confirm Success
    [Documentation]     Deletes the specified device from XIQSE and confirms the action was successful
    [Arguments]         ${ip}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate and Delete Device   ${ip}

Clean Up XIQ Components
    [Documentation]     Cleans up components used in XIQ during the test, logs out, and closes the browser

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Close Device360 Window

    XIQ Navigate to Devices and Confirm Success
    ${del_result}=  Delete Device   device_mac=${XIQSE_MAC}
    Should Be Equal As Integers     ${del_result}  1

    # Log out and close the window
    [Teardown]  XIQ Log Out and Close Window

Clean Up XIQSE Components
    [Documentation]     Cleans up components used in XIQSE during the test, logs out, and closes the browser

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Enable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}

    # Delete the test device
    Delete XIQSE Test Device and Confirm Success    ${XIQSE_IP}

    # Make sure XIQ sharing is enabled
    XIQSE Enable XIQ Connection Sharing and Save

    # Log out
    Log Out of XIQSE and Confirm Success

XIQ Log Out and Close Window
    [Documentation]     Logs out of XIQ and closes the window

    Switch To Window    ${XIQ_WINDOW_INDEX}

    Log Out of XIQ and Confirm Success
    Close Window    ${XIQ_WINDOW_INDEX}

Confirm Device360 Title for XIQ Site Engine
    [Documentation]     Confirms the Device360 view contains the correct title for the XIQ Site Engine

    Switch To Window  ${XIQ_WINDOW_INDEX}

    ${title}=  Device360 Get Device Title
    Log To Console  Got Title ${title}
    Should Be Equal  ${title}  ${XIQSE_PRODUCT} - ${XIQSE_NAME}

Confirm Device360 Side Bar Information for XIQ Site Engine
    [Documentation]     Confirms the sidebar of the Device360 view contains correct values for the XIQ Site Engine

    Switch To Window  ${XIQ_WINDOW_INDEX}

    # Get the data displayed in the left sidebar
    Device360 Refresh Page
    &{sidebar_info}=  Device360 Get Side Bar Information

    ${sidebar_model}=           Get From Dictionary  ${sidebar_info}  device_model
    ${sidebar_image}=           Get From Dictionary  ${sidebar_info}  device_image
    ${sidebar_name}=            Get From Dictionary  ${sidebar_info}  host_name
    ${sidebar_enabled_ports}=   Get From Dictionary  ${sidebar_info}  enabled_ports
    ${sidebar_disabled_ports}=  Get From Dictionary  ${sidebar_info}  disabled_ports
    ${sidebar_connected}=       Get From Dictionary  ${sidebar_info}  connected_state
    ${sidebar_alarms}=          Get From Dictionary  ${sidebar_info}  active_alarms

    # Compare the values
    Should Be Equal     ${sidebar_model}            ${XIQSE_MODEL}
    Should Contain      ${sidebar_image}            VirtualAppliance.png
    Should Be Equal     ${sidebar_name}             ${XIQSE_NAME}
    Should Be Equal     ${sidebar_enabled_ports}    1
    Should Be Equal     ${sidebar_disabled_ports}   0
    Should Be Equal     ${sidebar_connected}        Connected
    Should Be Equal     ${sidebar_alarms}           0

    # Since the time keeps updating, we need to check several times so the automation doesn't
    # keep chasing the time and never match (we ignore the seconds value for this reason, but the
    # minute value may flip).
    # APC-45291 - D360: "Active Since" field sometimes updates to be 1-2 minutes earlier than the last displayed time
    Wait Until Keyword Succeeds  16x  8 sec  Compare Active Since Times

Confirm Device360 Top Bar Information for XIQ Site Engine
    [Documentation]     Confirms the topbar of the Device360 view contains correct values for the XIQ Site Engine

    Switch To Window  ${XIQ_WINDOW_INDEX}

    # Get the data displayed in the top bar
    Device360 Refresh Page
    &{topbar_info}=  Device360 Get Top Bar Information

    ${topbar_mac_use}=  Get From Dictionary  ${topbar_info}  mac_usage
    ${topbar_ip}=       Get From Dictionary  ${topbar_info}  ip_address
    ${topbar_mac}=      Get From Dictionary  ${topbar_info}  mac_address
    ${topbar_version}=  Get From Dictionary  ${topbar_info}  software_version
    ${topbar_model}=    Get From Dictionary  ${topbar_info}  device_model
    ${topbar_serial}=   Get From Dictionary  ${topbar_info}  serial_number
    ${topbar_make}=     Get From Dictionary  ${topbar_info}  device_make

    Should Be Equal                 ${topbar_mac_use}   0%
    Should Be Equal                 ${topbar_ip}        ${XIQSE_IP}
    Should Be Equal                 ${topbar_mac}       ${XIQSE_MAC}
    Should Contain                  ${topbar_version}   ${XIQSE_VERSION}
# ------- APC-43431
    Log To Console      MODEL value ${topbar_model} not checked against ${XIQSE_MODEL} until APC-43431 is addressed
#    Should Be Equal                ${topbar_model}     ${XIQSE_MODEL}
# ------------------
    Should Be Equal                 ${topbar_serial}    ${XIQSE_SERIAL}
    Should Be Equal                 ${topbar_make}      ${XIQSE_MAKE}

#    # Keep checking every 10 seconds for 2.5 minutes to see if the last update times are the same.
#    # Since updates come in every 2 minutes, we need to check several times so the automation doesn't
#    # keep chasing the update time and never match.
#    # XMC-3467 - Diagnostics: need column to show last time XIQ was updated
#    Wait Until Keyword Succeeds  15x  10 sec  Compare Last Update Times

    # Check the Temperature value a few times in case there is a change between getting the values from XIQSE vs XIQ
    Wait Until Keyword Succeeds  3x  5 sec  Compare Temperature Values

Confirm Device360 CPU Usage Information for XIQ Site Engine
    [Documentation]     Compares the CPU Usage values between XIQSE Diagnostics and XIQ D360 (left sidebar and top bar)

    # Check the CPU value a few times in case there is a change between getting the values from XIQSE vs XIQ
    Wait Until Keyword Succeeds  3x  5 sec  Compare CPU Usage Values

Confirm Device360 Memory Usage Information for XIQ Site Engine
    [Documentation]     Compares the Memory Usage values between XIQSE Diagnostics and XIQ D360 (left sidebar and top bar)

    # Check the Memory value a few times in case there is a change between getting the values from XIQSE vs XIQ
    Wait Until Keyword Succeeds  3x  5 sec  Compare Memory Usage Values

Compare CPU Usage Values
    [Documentation]     Compares the CPU Usage value between XIQSE Diagnostics and XIQ D360

    # Obtain the expected CPU Usage value from the Administration> Diagnostics view
    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Navigate to XIQ Device Message Details and Confirm Success
    ${cpu_msg}=  XIQSE XIQ Device Message Details Get Metric From Device    ${XIQSE_IP}  ${XIQSE_PRODUCT}  cpuTotal
    ${xiqse_cpu}=  Evaluate  int(${cpu_msg})
    Log To Console  CPU VALUE FROM XIQSE IS ${xiqse_cpu}

    # Obtain the CPU Usage value from the Device360 view
    Switch To Window  ${XIQ_WINDOW_INDEX}
    Device360 Refresh Page

    ## Get the data displayed in the left sidebar
    ${sidebar_cpu}=  Device360 Get Side Bar CPU Usage
    Log To Console  CPU VALUE FROM D360 SIDE BAR IS ${sidebar_cpu}

    ## Get the data displayed in the left sidebar
    ${topbar_cpu}=  Device360 Get Top Bar CPU Usage
    Log To Console  CPU VALUE FROM D360 TOP BAR IS ${topbar_cpu}

    Should Be Equal     ${sidebar_cpu}    ${topbar_cpu}
    Should Be Equal     ${sidebar_cpu}    ${xiqse_cpu}%

Compare Memory Usage Values
    [Documentation]     Compares the Memory Usage value between XIQSE Diagnostics and XIQ D360

    # Obtain the expected Memory Usage value from the Administration> Diagnostics view
    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Navigate to XIQ Device Message Details and Confirm Success
    ${mem_msg}=  XIQSE XIQ Device Message Details Get Metric From Device    ${XIQSE_IP}  ${XIQSE_PRODUCT}  memoryUsed
    ${xiqse_mem}=  Evaluate  int(${mem_msg})
    Log To Console  MEMORY VALUE FROM XIQSE IS ${xiqse_mem}

    # Obtain the Memory Usage value from the Device360 view
    Switch To Window  ${XIQ_WINDOW_INDEX}
    Device360 Refresh Page

    ## Get the data displayed in the left sidebar
    ${sidebar_mem}=  Device360 Get Side Bar Memory Usage
    Log To Console  MEMORY VALUE FROM D360 SIDE BAR IS ${sidebar_mem}

    ## Get the data displayed in the left sidebar
    ${topbar_mem}=  Device360 Get Top Bar Memory Usage
    Log To Console  MEMORY VALUE FROM D360 TOP BAR IS ${topbar_mem}

    Should Be Equal     ${sidebar_mem}    ${topbar_mem}
    Should Be Equal     ${sidebar_mem}    ${xiqse_mem}%

Compare Active Since Times
    [Documentation]     Compares the Active Since times between XIQSE Diagnostics and XIQ D360 views

    # Obtain the uptime value from the Device360 view
    Switch To Window  ${XIQ_WINDOW_INDEX}
    Device360 Refresh Page
    &{d360_active}=  Device360 Get Side Bar Active Since Information
    ${d360_days}=   Get From Dictionary  ${d360_active}  days
    ${d360_hours}=  Get From Dictionary  ${d360_active}  hours
    ${d360_mins}=   Get From Dictionary  ${d360_active}  minutes

    # Obtain the expected Active Since value from the Administration> Diagnostics view
    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Navigate to XIQ Device Message Details and Confirm Success
    ${xiqse_msg}=    XIQSE XIQ Device Message Details Get Metric From Device    ${XIQSE_IP}  ${XIQSE_PRODUCT}  upTime
    Log To Console   Up Time Value From XIQ Device Message Details: '${xiqse_msg}'
    &{xiqse_info}=   Convert MS To Time  ${xiqse_msg}
    ${xiqse_days}=   Get From Dictionary  ${xiqse_info}  days
    ${xiqse_hours}=  Get From Dictionary  ${xiqse_info}  hours
    ${xiqse_mins}=   Get From Dictionary  ${xiqse_info}  minutes

    Log To Console  Comparing D360 Days ${d360_days} with XIQSE Days ${xiqse_days}
    Should Be True  ${d360_days} == ${xiqse_days}
    Log To Console  Comparing D360 Hours ${d360_hours} with XIQSE Hours ${xiqse_hours}
    Should Be True  ${d360_hours} == ${xiqse_hours}
    Log To Console  Comparing D360 Minutes ${d360_mins} with XIQSE Minutes ${xiqse_mins}
    Should Be True  ${d360_mins} == ${xiqse_mins}

Compare Last Update Times
    [Documentation]     Compares the Last Update Time between XIQSE Diagnostics and XIQ D360 views

    # Obtain the expected Last Update Time value from the Administration> Diagnostics view
    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Navigate to XIQ Device Message Details and Confirm Success
    ${xiqse_val}=  XIQSE XIQ Device Message Details Get Last Update Time    ${XIQSE_IP}  ${XIQSE_PRODUCT}

    # Obtain the uptime value from the Device360 view
    Switch To Window  ${XIQ_WINDOW_INDEX}
    Device360 Refresh Page
    ${topbar_uptime}=  Device360 Get Top Bar Last Update Time

    # Need to do a special comparison of the two date/time strings as the diagnostics view has two digits
    # for the month and hour values, but the D360 view only has one digit for the month and hour values
    ${result}=  Compare Date Time Strings  ${topbar_uptime}  ${xiqse_val}
    Should Be Equal As Integers     ${result}   1

Compare Temperature Values
    [Documentation]     Compares the Temperature value between XIQSE Diagnostics and XIQ D360 views

    # Obtain the expected Temperature value from the Administration> Diagnostics view
    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Navigate to XIQ Device Message Details and Confirm Success
    ${xiqse_val}=  XIQSE XIQ Device Message Details Get Metric From Device    ${XIQSE_IP}  ${XIQSE_PRODUCT}  unitTemperature

    # Obtain the Temperature value from the Device360 view
    Switch To Window  ${XIQ_WINDOW_INDEX}
    Device360 Refresh Page
    ${d360_temp}=  Device360 Get Top Bar Temperature

    Should Be Equal    ${d360_temp}    ${xiqse_val}

Confirm Device360 Ports Information Is Displayed
    [Documentation]     Confirms the ports table area of the Device360 view contains data

    ${port_count}=  Device360 Get Port Icon Count
    Should Be Equal As Integers     ${port_count}    1

    ${table_displayed}=  Device360 Is Port Details Table Displayed
    Should Be Equal As Integers     ${table_displayed}    1

Generate Alarm and Event for XIQ Site Engine
    [Documentation]     Disables and re-enables XIQ Connection sharing to generate a Disconnected alarm and event

    # Disable Sharing to generate a Device Down event and an alarm
    Switch To Window  ${XIQSE_WINDOW_INDEX}
    ${disable_result}=  XIQSE Disable XIQ Connection Sharing and Save
    Should Be Equal As Integers         ${disable_result}     1

    # Wait until XIQSE goes offline
    Switch To Window  ${XIQ_WINDOW_INDEX}
    Wait Until Device Offline           device_mac=${XIQSE_MAC}  retry_duration=30  retry_count=22

    # Confirm the XIQ Site Engine reported in XIQ shows the correct status (disconnected)
    Confirm Device Status with MAC   ${XIQSE_MAC}    disconnected

    # Re-enable Sharing to generate a Device Up event
    Switch To Window  ${XIQSE_WINDOW_INDEX}
    ${enable_result}=  XIQSE Enable XIQ Connection Sharing and Save
    Should Be Equal As Integers         ${enable_result}     1

    # Confirm the XIQ Site Engine reported in XIQ shows the correct status (green/connected)
    Switch To Window  ${XIQ_WINDOW_INDEX}
    Wait Until Device Online            device_mac=${XIQSE_MAC}  retry_duration=30  retry_count=22
    Confirm Device Status with MAC      ${XIQSE_MAC}    green

    # The values update after 2 minutes
    Log To Console  Sleeping for 2 minutes to wait for the next update to come in
    Count Down in Minutes  2

Confirm Device Status with MAC
    [Documentation]     Checks the status of the specified device using MAC address and confirms it matches the expected value
    [Arguments]         ${mac}  ${expected_status}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    ${device_status}=       Get Device Status   device_mac=${mac}
    Should Contain          ${device_status}    ${expected_status}

Confirm Device360 Alarms
    [Documentation]     Confirms the alarms information is correct

    # Confirm left sidebar shows one active alarm
    &{sidebar_info}=  Device360 Get Side Bar Information
    ${sidebar_alarms}=  Get From Dictionary  ${sidebar_info}  active_alarms
    Should Be Equal     ${sidebar_alarms}           1

    # Confirm overview Active Alarms panel shows one active alarm
    ${alarm_count}=  Device360 Get Total Active Alarms Count
    Should Be Equal As Integers     ${alarm_count}    1

    # Confirm Alarms view displays alarm
    Device360 Select Alarms View
# ------- APC-41429
    Log To Console                  NOTE: ignoring time stamp (${TEST_TIME}) until APC-41429 is fixed
#    Confirm Alarm Exists           Device Disconnected  ${TEST_TIME}
    Confirm Alarm Exists            Device Disconnected  ${EMPTY}
# ------------------

Confirm Device360 Events
    [Documentation]     Confirms the events information is correct

    # Confirm Events view displays events
    Device360 Select Events View
# ------- APC-41429
    Log To Console                  NOTE: ignoring time stamp (${TEST_TIME}) until APC-41429 is fixed
#    Confirm Event Exists           Disconnect message from HiveAgent  ${TEST_TIME}
    Confirm Event Exists            Disconnect message from HiveAgent  ${EMPTY}
# ------------------

Confirm Alarm Exists
    [Documentation]     Confirms the specified alarm exists after the specified time
    [Arguments]         ${alarm_cat}  ${after_time}

    ${alarm_found}=                 Device360 Confirm Alarm Category Exists  ${alarm_cat}  ${after_time}
    Should Be Equal As Integers     ${alarm_found}  1

Confirm Event Exists
    [Documentation]     Confirms the specified event exists after the specified time
    [Arguments]         ${event_str}  ${after_time}

    # Search for the event string first in case the view contains a lot of events
    d360Event Search                ${event_str}

    # Confirm the event exists in the view
    ${event_found}=                 Device360 Confirm Event Description Contains  ${event_str}  ${after_time}
    Should Be Equal As Integers     ${event_found}  1
