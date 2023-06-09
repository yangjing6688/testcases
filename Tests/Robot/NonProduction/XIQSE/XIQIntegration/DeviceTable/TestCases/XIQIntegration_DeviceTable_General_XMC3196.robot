# Author        : Heidi S. White
# Description   : Test Suite for testing XIQSE-XIQ Integration for the Device table functionality.
#                 This encompasses the following qTest test cases in the CSIT project:
#                   TC-9519: Add XIQ Site Engine Using Auto Onboard Button
#                   TC-9070: Add Device to XIQ-SE - Unique Serial Number
#                   [TC-9051: Add Device to XIQ-SE - No Serial Number] - this test is currently commented out
#                   TC-9035: Add XIQ Site Engine device to XIQ-SE
#                   TC-9025: Delete XIQ Site Engine Device from XIQ-SE (already onboarded to XIQ)
#                   TC-9012: Delete Device from XIQ-SE (already onboarded to XIQ)

*** Settings ***
Library         common/TestFlow.py
Library         common/Utils.py

Resource        ../../DeviceTable/Resources/AllResources.robot

Force Tags      testbed_2_node

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
${XIQSE_IP}             ${xiqse.ip}
${XIQSE_PROFILE}        ${xiqse.profile}
${XIQSE_NAME}           ${xiqse.name}
${XIQSE_MAKE}           ${xiqse.make}
${XIQSE_MODEL}          ${xiqse.model}
${XIQSE_OS}             ${xiqse.xiq_os}
${XIQSE_VERSION}        ${xiqse.version}
${XIQSE_PRODUCT}        ${xiqse.product}

${XIQ_URL}              ${xiq.test_url}
${XIQ_USER}             ${xiq.tenant_username}
${XIQ_PASSWORD}         ${xiq.tenant_password}

${DUT1_SERIAL}          ${netelem1.serial}
${DUT1_IP}              ${netelem1.ip}
${DUT1_PROFILE}         ${netelem1.profile}
${DUT1_MAC}             ${netelem1.mac}
${DUT1_NAME}            ${netelem1.name}
${DUT1_MODEL}           ${netelem1.model}
${DUT1_MAKE}            ${netelem1.make}
${DUT1_OS}              ${netelem1.xiq_os}

#${DUT2_SERIAL}          ${ap1.serial}
#${DUT2_IP}              ${ap1.ip}
#${DUT2_PROFILE}         ${ap1.profile}
#${DUT2_MODEL}           ${ap1.model}
#${DUT2_MAKE}            ${ap1.make}

@{COLUMNS}          Host Name  Managed By  Uptime  MGT IP Address  MAC Address  Cloud Config Groups  Serial #  Make  OS  OS Version  Model
${COLUMN_LABELS}    HOST NAME,MANAGED BY,UPTIME,MGT IP ADDRESS,MAC,CLOUD CONFIG GROUPS,SERIAL,MAKE,OS,OS VERSION,MODEL

${WORLD_SITE}           World


*** Test Cases ***
TC-53136: Add XIQ Site Engine Using Auto Onboard Button
    [Documentation]     Confirms the XIQ Site Engine can be onboarded via the Auto Onboard workflow
    [Tags]              nightly2    release_testing    tccs_9519    xmc_3196    development    xiqse    xiq_integration    onboard    test1

    # Onboard XIQ Site Engine
    Remove Existing Site Engine from XIQ
    Auto Onboard XIQ Site Engine

    # Confirm XIQ Site Engine establishes connection with XIQ
    Confirm XIQ Site Engine Establishes Connection with XIQ

    # Confirm the device table values for the XIQ Site Engine
    Switch To Window  ${XIQ_WINDOW_INDEX}
    Wait Until Device Data Present  ${XIQSE_SERIAL}  MGT IP ADDRESS
    Confirm XIQ Site Engine Values

TC-52225: Add Device to XIQSE - Unique Serial Number
    [Documentation]     Confirms a device with a unique serial number in XIQ-SE is automatically added to XIQ
    [Tags]              nightly2    release_testing    tccs_9070    xmc_3196    development    xiqse    xiq_integration     test2
    Depends On          test1

    # Add a device to XIQ-SE which has a unique serial number
    Add Device to XIQSE and Confirm Success           ${DUT1_IP}    ${DUT1_PROFILE}

    # Confirm the XIQSE-managed device is automatically onboarded to XIQ and has correct values
    Confirm XIQSE Device Added to XIQ and Connected   ${DUT1_SERIAL}
    Log To Console  Sleeping for 2 minutes to wait for the next update to come in
    Count Down in Minutes  2
    Confirm XIQSE-Managed Device Values

#TC-52226: Add Device to XIQSE - No Serial Number - Serial Auto-Generated by XIQ-SE
#    [Documentation]     Confirms a device without a serial number modeled in XIQ-SE will have a serial number generated
#    [Tags]              nightly2    release_testing    tccs_9051    xmc_3196    development    xiqse    xiq_integration     test3
#    Depends On          test1
#
#    Switch To Window  ${XIQSE_WINDOW_INDEX}
#    XIQSE Navigate to Devices and Confirm Success
#
#    # Make sure the XIQ Onboarded column is being displayed
#    ${col}=  XIQSE Devices Show Columns     XIQ Onboarded
#    Should Be Equal As Integers             ${col}     1
#
#    # Add a device to XIQ-SE which does not have a serial number but which will have one auto-generated due to
#    # having a correct profile and NOT having a Vendor Profile set to "Do not onboard to XIQ"
#    Add Device to XIQSE and Confirm Success                     ${DUT2_IP}    ${DUT2_PROFILE}
#
#    # Wait until the device shows it has been onboarded to XIQ
#    ${onboarded}=  XIQSE Wait Until Device Onboarded to XIQ     ${DUT2_IP}
#    Should Be Equal As Integers                                 ${onboarded}     1
#
#    # Wait until the serial number and base MAC are populated for the device
#    ${has_serial}=  XIQSE Wait Until Device Has Serial Number   ${DUT2_IP}
#    Should Be Equal As Integers                                 ${has_serial}     1
#    ${has_mac}=  XIQSE Wait Until Device Has Base MAC           ${DUT2_IP}
#    Should Be Equal As Integers                                 ${has_mac}     1
#
#    # Serial number and base MAC are auto-generated by XIQ-SE - obtain the values
#    ${device_serial}=  XIQSE Get Device Serial Number   ${DUT2_IP}
#    ${device_mac}=  XIQSE Get Device Base MAC           ${DUT2_IP}
#
#    # Confirm the device is added to XIQ
#    Confirm Device Serial Present in XIQ                ${device_serial}
#    Confirm Device MAC Present in XIQ                   ${device_mac}

TC-52227: Add XIQ Site Engine device to XIQSE
    [Documentation]     Confirms when the XIQ Site Engine is modeled as an SNMP device, it is correctly reported in XIQ
    [Tags]              nightly2    release_testing    tccs_9035    xmc_3196    development    xiqse    xiq_integration     test4
    Depends On          test1

    # Add the XIQ Site Engine as an SNMP-managed device in XIQ-SE
    Add Device to XIQSE and Confirm Success         ${XIQSE_IP}    ${XIQSE_PROFILE}

    # Confirm the XIQ-SE device is not added as a second entry in XIQ
    Log To Console  Sleeping for 3 minutes to wait for the next update to come in
    Count Down in Minutes  3
    Confirm Device MAC Present in XIQ               ${XIQSE_MAC}
    Confirm MAC Not Duplicated in XIQ               ${XIQSE_MAC}

    # Confirm the device values are correct
    Confirm XIQ Site Engine as Managed Device Values

TC-52427: Delete XIQ Site Engine Device from XIQSE (already onboarded to XIQ)
    [Documentation]     Confirms when a device is deleted in XIQ-SE, it is removed from XIQ
    [Tags]              nightly2    release_testing    tccs_9025    xmc_3196    development    xiqse    xiq_integration     test5
    Depends On          test1   test4

    # Delete the XIQ Site Engine SNMP-managed device
    Delete XIQSE Test Device and Confirm Success  ${XIQSE_IP}

    # Confirm the XIQ Site Engine entry is still present in XIQ
    Log To Console  Sleeping for 3 minutes to wait for the next update to come in
    Count Down in Minutes  3
    Confirm Device MAC Present in XIQ             ${XIQSE_MAC}

    # Confirm the XIQ Site Engine entry reverts back to its original values
    Confirm XIQ Site Engine Values

TC-52228: Delete Device from XIQSE (already onboarded to XIQ)
    [Documentation]     Confirms when a device is deleted in XIQ-SE, it is removed from XIQ
    [Tags]              nightly2    release_testing    tccs_9012    xmc_3196    development    xiqse    xiq_integration     test6
    Depends On          test1   test2

    # Delete a device from XIQ-SE which is already onboarded in XIQ
    Delete XIQSE Test Device and Confirm Success    ${DUT1_IP}

    # Confirm the XIQSE-managed device is automatically removed from XIQ
    Switch To Window  ${XIQ_WINDOW_INDEX}
    ${search_result}=  Wait Until Device Removed    device_serial=${DUT1_SERIAL}
    Should Be Equal As Integers                     ${search_result}    1


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Sets up the components for the test

    XIQSE Log In and Set Window Index
    Set Up XIQSE Components

    XIQ Log In and Set Window Index
    Set Up XIQ Components

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
    [Documentation]     Sets up the XIQ-SE components for the test

    Disable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}

    # Disable all columns for event searches
    Set Alarm Event Search Scope    true

    # Confirm the serial number is correct and set the common options needed for automation
    Confirm Serial Number and Set Common Options     ${XIQSE_SERIAL}

    # Clear the current contents of the server.log on the Diagnostics tab
    Clear XIQSE Diagnostics Server Log

Set Up XIQ Components
    [Documentation]     Sets up the XIQ components for the test

    XIQ Navigate to Devices and Confirm Success

    Remove Existing Site Engine from XIQ

    Column Picker Select        @{COLUMNS}

Clear XIQSE Diagnostics Server Log
    [Documentation]     Clears the current contents of the server.log on the Diagnostics tab

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    XIQSE Navigate to Admin Diagnostics Tab
    XIQSE Select Server Log Tree Node
    ${result}=  XIQSE Server Log Clear
    Should Be Equal As Integers     ${result}     1

Refresh XIQSE Diagnostics Server Log
    [Documentation]     Refreshes the current contents of the server.log on the Diagnostics tab

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    XIQSE Navigate to Admin Diagnostics Tab
    XIQSE Select Server Log Tree Node
    ${result}=  XIQSE Server Log Refresh
    Should Be Equal As Integers     ${result}     1

XIQSE Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Network> Devices> Devices view in XIQSE and confirms the action was successful

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate to Devices and Confirm Success

XIQ Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Manage> Devices view in XIQ and confirms the action was successful

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate to XIQ Devices and Confirm Success

Remove Existing Site Engine from XIQ
    [Documentation]     Removes the XIQ Site Engine from XIQ if it exists

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Navigate and Remove Device by MAC From XIQ   ${XIQSE_MAC}

Auto Onboard XIQ Site Engine
    [Documentation]     Onboards the specified XIQ Site Engine, deleting it first if it already exists

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Enter XIQ Credentials to Auto Onboard XIQSE  ${XIQ_USER}  ${XIQ_PASSWORD}

Confirm XIQ Site Engine Establishes Connection with XIQ
    [Documentation]     Confirms the XIQ Site Engine establishes connection with XIQ

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Confirm Device Serial Present   ${XIQSE_SERIAL}
    Confirm Device Serial Online    ${XIQSE_SERIAL}

    # Refresh the server.log page and confirm the expected server association message is present
    Refresh XIQSE Diagnostics Server Log
    ${log_result}=  XIQSE Confirm Server Log Contents Contains String   Server Association is successful
    Should Be Equal As Integers                                         ${log_result}    1

Add Device to XIQSE and Confirm Success
    [Documentation]     Adds the specified device to XIQSE
    [Arguments]         ${ip}  ${profile}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate and Create Device  ${ip}  ${profile}

Confirm Device Status
    [Documentation]     Checks the status of the specified device and confirms it matches the expected value
    [Arguments]         ${serial}  ${expected_status}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    ${device_status}=  Get Device Status   device_serial=${serial}
    Should Contain     ${device_status}    ${expected_status}

Confirm XIQSE Device Added to XIQ and Connected
    [Documentation]     Confirms the specified device is present in XIQ and has connected status
    [Arguments]         ${serial}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Confirm Device Serial Present   ${serial}
    Confirm Device Serial Online    ${serial}

Confirm Device Serial Present in XIQ
    [Documentation]     Confirms the specified device by SERIAL NUMBER is present in XIQ
    [Arguments]         ${serial}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Confirm Device Serial Present   ${serial}

Confirm Device MAC Present in XIQ
    [Documentation]     Confirms the specified device by MAC ADDRESS is present in XIQ
    [Arguments]         ${mac}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Confirm Device MAC Address Present  ${mac}

Confirm Device MAC Not Present in XIQ
    [Documentation]     Confirms the specified device by MAC ADDRESS is not present in XIQ
    [Arguments]         ${mac}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Confirm Device MAC Address Not Present      ${mac}

Confirm MAC Not Duplicated in XIQ
    [Documentation]     Confirms the specified MAC Address is not present in multiple rows in XIQ
    [Arguments]         ${mac}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Refresh Devices Page

    ${search_result}=  Confirm No Duplicate Rows    ${mac}
    Should Be Equal As Integers                     ${search_result}     1

Confirm XIQ Site Engine Values
    [Documentation]     Confirms the XIQ Site Engine has the expected values in the Devices table

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Refresh Devices Page

    &{xiqse_info}=     Get Device Row Values  ${XIQSE_MAC}  ${COLUMN_LABELS}

    ${name_result}=     Get From Dictionary  ${xiqse_info}  HOST NAME
    ${mgby_result}=     Get From Dictionary  ${xiqse_info}  MANAGED BY
    ${uptime_result}=   Get From Dictionary  ${xiqse_info}  UPTIME
    ${ip_result}=       Get From Dictionary  ${xiqse_info}  MGT IP ADDRESS
    ${mac_result}=      Get From Dictionary  ${xiqse_info}  MAC
    ${cldcfg_result}=   Get From Dictionary  ${xiqse_info}  CLOUD CONFIG GROUPS
    ${serial_result}=   Get From Dictionary  ${xiqse_info}  SERIAL
    ${make_result}=     Get From Dictionary  ${xiqse_info}  MAKE
    ${os_result}=       Get From Dictionary  ${xiqse_info}  OS
    ${version_result}=  Get From Dictionary  ${xiqse_info}  OS VERSION
    ${model_result}=    Get From Dictionary  ${xiqse_info}  MODEL

    Should Be Equal         ${name_result}      ${XIQSE_IP}
    Should Be Equal         ${mgby_result}      XIQ
    Should Not Be Equal     ${uptime_result}    N/A
    Should Be Equal         ${ip_result}        ${XIQSE_IP}
    Should Be Equal         ${mac_result}       ${XIQSE_MAC}
    Should Be Equal         ${serial_result}    ${XIQSE_SERIAL}
    Should Be Equal         ${make_result}      ${XIQSE_MAKE}
    Should Be Equal         ${os_result}        ${XIQSE_OS}
    Should Contain          ${version_result}   ${XIQSE_VERSION}
    Should Be Equal         ${model_result}     ${XIQSE_MODEL}
    Run Keyword If  '21.4' in '${XIQSE_VERSION}'  Should Be Equal     ${cldcfg_result}    ${XIQSE_SERIAL}
    ...  ELSE  Should Be Equal     ${cldcfg_result}    XIQSE-${XIQSE_NAME}

Confirm XIQ Site Engine as Managed Device Values
    [Documentation]     Confirms the XIQ Site Engine as an SNMP-managed device has the expected values in the Devices table

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Refresh Devices Page

    &{xiqse_info}=        Get Device Row Values  ${XIQSE_MAC}  ${COLUMN_LABELS}

    ${name_result}=     Get From Dictionary  ${xiqse_info}  HOST NAME
    ${mgby_result}=     Get From Dictionary  ${xiqse_info}  MANAGED BY
    ${uptime_result}=   Get From Dictionary  ${xiqse_info}  UPTIME
    ${ip_result}=       Get From Dictionary  ${xiqse_info}  MGT IP ADDRESS
    ${mac_result}=      Get From Dictionary  ${xiqse_info}  MAC
    ${cldcfg_result}=   Get From Dictionary  ${xiqse_info}  CLOUD CONFIG GROUPS
    ${serial_result}=   Get From Dictionary  ${xiqse_info}  SERIAL
    ${make_result}=     Get From Dictionary  ${xiqse_info}  MAKE
    ${os_result}=       Get From Dictionary  ${xiqse_info}  OS
    ${version_result}=  Get From Dictionary  ${xiqse_info}  OS VERSION
    ${model_result}=    Get From Dictionary  ${xiqse_info}  MODEL

    Should Be Equal         ${name_result}      ${XIQSE_NAME}
    Should Be Equal         ${mgby_result}      XIQ
    Should Not Be Equal     ${uptime_result}    N/A
    Should Be Equal         ${ip_result}        ${XIQSE_IP}
    Should Be Equal         ${mac_result}       ${XIQSE_MAC}
    Should Be Equal         ${serial_result}    ${XIQSE_SERIAL}
    Should Be Equal         ${make_result}      ${XIQSE_MAKE}
    Should Be Equal         ${os_result}        ${XIQSE_OS}
    Should Contain          ${version_result}   ${XIQSE_VERSION}
    Should Be Equal         ${model_result}     ${XIQSE_MODEL}
    Run Keyword If  '21.4' in '${XIQSE_VERSION}'  Should Be Equal     ${cldcfg_result}    ${XIQSE_SERIAL}
    ...  ELSE  Should Be Equal     ${cldcfg_result}    XIQSE-${XIQSE_NAME}

Confirm XIQSE-Managed Device Values
    [Documentation]     Confirms the test device has the expected values in the Devices table

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Refresh Devices Page

    Confirm Device Status   ${DUT1_SERIAL}  green

    &{device_info}=         Get Device Row Values  ${DUT1_SERIAL}  ${COLUMN_LABELS}
    ${name_result}=         Get From Dictionary  ${device_info}  HOST NAME
    ${serial_result}=       Get From Dictionary  ${device_info}  SERIAL
    ${mgby_result}=         Get From Dictionary  ${device_info}  MANAGED BY
    ${ip_result}=           Get From Dictionary  ${device_info}  MGT IP ADDRESS
    ${mac_result}=          Get From Dictionary  ${device_info}  MAC
    ${make_result}=         Get From Dictionary  ${device_info}  MAKE
    ${model_result}=        Get From Dictionary  ${device_info}  MODEL
    ${os_result}=           Get From Dictionary  ${device_info}  OS
    ${cldcfg_result}=       Get From Dictionary  ${device_info}  CLOUD CONFIG GROUPS
    ${uptime_result}=       Get From Dictionary  ${device_info}  UPTIME

    Should Be Equal         ${name_result}      ${DUT1_NAME}
    Should Be Equal         ${serial_result}    ${DUT1_SERIAL}
    Should Be Equal         ${mgby_result}      ${XIQSE_PRODUCT}
    Should Be Equal         ${ip_result}        ${DUT1_IP}
    Should Be Equal         ${mac_result}       ${DUT1_MAC}
    Should Be Equal         ${make_result}      ${DUT1_MAKE}
    Should Be Equal         ${model_result}     ${DUT1_MODEL}
    Should Be Equal         ${os_result}        ${DUT1_OS}
    Should Not Be Equal     ${uptime_result}    N/A
    Run Keyword If  '21.4' in '${XIQSE_VERSION}'  Should Be Equal     ${cldcfg_result}    ${XIQSE_SERIAL}
    ...  ELSE  Should Be Equal     ${cldcfg_result}    XIQSE-${XIQSE_NAME}

Delete XIQSE Test Device and Confirm Success
    [Documentation]     Deletes the specified device from XIQSE and confirms the action was successful
    [Arguments]         ${ip}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Navigate and Delete Device   ${ip}

Clean Up XIQ Components
    [Documentation]     Cleans up components used in XIQ during the test, logs out, and closes the browser

    Switch To Window  ${XIQ_WINDOW_INDEX}

    # Remove XIQSE from XIQ
    Navigate and Remove Device by MAC From XIQ  ${XIQSE_MAC}

    # Log out
    Log Out of XIQ and Confirm Success

Clean Up XIQSE Components
    [Documentation]     Cleans up components used in XIQ-SE during the test, logs out, and closes the browser

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Enable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}

    # Enable all columns for event searches
    Set Alarm Event Search Scope    false

    # Reset the options
    ${options_result}=  XIQSE Restore Default XIQ Connection Options and Save
    Should Be Equal As Integers         ${options_result}     1

#    # Delete the remaining test device
#    Delete XIQSE Test Device and Confirm Success    ${DUT2_IP}

    # Log out
    Log Out of XIQSE and Confirm Success
