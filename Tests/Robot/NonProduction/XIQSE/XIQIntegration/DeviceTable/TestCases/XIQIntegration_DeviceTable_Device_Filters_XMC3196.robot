# Author        : Heidi S. White
# Description   : Test Suite for testing XIQSE-XIQ Integration for device filtering functionality.
#                   - Device Type
#                   - Device Connection State
#                   - Device Management State
#                   - Device Function
#                   - Device Software Version
#                   - Cloud Config Groups
#                   - Device Product Type (this test case is commented out for now due to an automation bug)
#                 This is CSIT qTest test case:
#                   TC-8984: XIQ-SE Device View Filters

*** Settings ***
Library         common/Cli.py
Library         common/Utils.py
Library         xiq/flows/manage/FilterManageDevices.py

Resource        ../../DeviceTable/Resources/AllResources.robot

Force Tags      testbed_1_node

Suite Setup     Log In and Set Up Test
Suite Teardown  Tear Down Test and Close Session


*** Variables ***
# Defaults
${ENV}                      environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                     topo.test.xiqse1.connected.yaml
${TESTBED}                  SALEM/Dev/devices-salem-acceptance.yaml

${LOCATION}                 Santa Clara, building_02, floor_04

${XIQSE_URL}                ${xiqse.url}
${XIQSE_USER}               ${xiqse.user}
${XIQSE_PASSWORD}           ${xiqse.password}
${XIQSE_SERIAL}             ${xiqse.serial}
${XIQSE_MAC}                ${xiqse.mac}
${XIQSE_NAME}               ${xiqse.name}
${XIQSE_OS_VERSION}         ${xiqse.version}
${XIQSE_FUNCTION}           ${xiqse.function}
${XIQSE_PRODUCT}            ${xiqse.product}

${XIQ_URL}                  ${xiq.test_url}
${XIQ_USER}                 ${xiq.tenant_username}
${XIQ_PASSWORD}             ${xiq.tenant_password}
${XIQ_CAPWAP_URL}           ${xiq.capwap_url}

${XIQ_DUT_SERIAL}           ${ap1.serial}
${XIQ_DUT_NAME}             ${ap1.name}
${XIQ_DUT_MODEL}            ${ap1.model}
${XIQ_DUT_MAKE}             ${ap1.make}
${XIQ_DUT_CLI_TYPE}         ${ap1.cli_type}
${XIQ_DUT_CCG}              ${ap1.ccg}
${XIQ_DUT_IP}               ${ap1.ip}
${XIQ_DUT_PORT}             ${ap1.port}
${XIQ_DUT_USERNAME}         ${ap1.username}
${XIQ_DUT_PASSWORD}         ${ap1.password}
${XIQ_DUT_PLATFORM}         ${ap1.platform}
${IQAGENT}                  ${xiq.sw_connection_host}

${XIQSE_DUT_IP}             ${netelem1.ip}
${XIQSE_DUT_PROFILE}        ${netelem1.profile}
${XIQSE_DUT_SERIAL}         ${netelem1.serial}
${XIQSE_DUT_MAC}            ${netelem1.mac}
${XIQSE_DUT_PRODUCT}        ${netelem1.product}
${XIQSE_DUT_FUNCTION}       ${netelem1.function}

${WORLD_SITE}               World


*** Test Cases ***
Test 1: Confirm Device Type Filter
    [Documentation]     Tests the Device Type Filter functionality
    [Tags]              nightly2    release_testing    tccs_8984    xmc_3196    development    xiqse    xiq_integration    device_table    filters    test1

    Switch To Window  ${XIQ_WINDOW_INDEX}
    Clear All Filters
    Log To Console  >> Navigating away from and back to the Devices page until APC-51254 is fixed <<
    Navigate Configure Network Policies
    XIQ Navigate to Devices and Confirm Success

    # Filter to only show Real devices
    ${set_real_status}=  Set Device Type Filter     Real Devices  true
    Should Be Equal As Integers                     ${set_real_status}  1
    sleep  5 seconds
    Confirm Device MAC Present in XIQ               ${XIQSE_MAC}
    Confirm Device MAC Present in XIQ               ${XIQSE_DUT_MAC}
    Confirm Device Serial Present in XIQ            ${XIQ_DUT_SERIAL}
    ${reset_real_status}=  Set Device Type Filter   Real Devices  false
    Should Be Equal As Integers                     ${reset_real_status}  1

    # Filter to only show Simulated devices
    ${set_sim_status}=     Set Device Type Filter   Simulated Devices  true
    Should Be Equal As Integers                     ${set_sim_status}  1
    sleep  5 seconds
    Confirm Device MAC Not Present in XIQ           ${XIQSE_MAC}
    Confirm Device MAC Not Present in XIQ           ${XIQSE_DUT_MAC}
    Confirm Device Serial Not Present in XIQ        ${XIQ_DUT_SERIAL}
    ${reset_sim_status}=  Set Device Type Filter    Simulated Devices  false
    Should Be Equal As Integers                     ${reset_sim_status}  1

Test 2: Confirm Device Connection State Filter
    [Documentation]     Tests the Device Connection State Filter functionality
    [Tags]              nightly2    release_testing    tccs_8984    xmc_3196    development    xiqse    xiq_integration    device_table    filters    test2

    # Disconnect a device in XNC
    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Disconnect XIQSE Test Device and Confirm Success            ${XIQSE_DUT_IP}    BAD_PROFILE

    # Confirm the XIQSE-managed device reported in XIQ shows the correct status (disconnected)
    Switch To Window  ${XIQ_WINDOW_INDEX}
    Clear All Filters
    Log To Console  >> Navigating away from and back to the Devices page until APC-51254 is fixed <<
    Navigate Configure Network Policies
    XIQ Navigate to Devices and Confirm Success

    ${disconnect_result}=  Wait Until Device Offline            ${XIQSE_DUT_SERIAL}
    Should Be Equal As Integers                                 ${disconnect_result}       1

    # Filter to only show Connected devices
    ${set_conn_status}=  Set Device Connection State Filter     Connected  true
    Should Be Equal As Integers                                 ${set_conn_status}  1
    sleep  5 seconds
    Confirm Device MAC Present in XIQ                           ${XIQSE_MAC}
    Confirm Device MAC Not Present in XIQ                       ${XIQSE_DUT_MAC}
    Confirm Device Serial Present in XIQ                        ${XIQ_DUT_SERIAL}
    ${reset_conn_status}=  Set Device Connection State Filter   Connected  false
    Should Be Equal As Integers                                 ${reset_conn_status}  1

    # Filter to only show Disconnected devices
    ${set_disc_status}=  Set Device Connection State Filter     Disconnected  true
    Should Be Equal As Integers                                 ${set_disc_status}  1
    sleep  5 seconds
    Confirm Device MAC Not Present in XIQ                       ${XIQSE_MAC}
    Confirm Device MAC Present in XIQ                           ${XIQSE_DUT_MAC}
    Confirm Device Serial Not Present in XIQ                    ${XIQ_DUT_SERIAL}
    ${reset_disc_status}=  Set Device Connection State Filter   Disconnected  false
    Should Be Equal As Integers                                 ${reset_disc_status}  1

    # Filter to show All devices
    ${set_all_status}=  Set Device Connection State Filter      All  true
    Should Be Equal As Integers                                 ${set_all_status}  1
    sleep  5 seconds
    Confirm Device MAC Present in XIQ                           ${XIQSE_MAC}
    Confirm Device MAC Present in XIQ                           ${XIQSE_DUT_MAC}
    Confirm Device Serial Present in XIQ                        ${XIQ_DUT_SERIAL}
    ${reset_all_status}=  Set Device Connection State Filter    All  false
    Should Be Equal As Integers                                 ${reset_all_status}  1

    # Reconnect the device in XIQ-SE
    Switch To Window  ${XIQSE_WINDOW_INDEX}
    Reconnect XIQSE Test Device and Confirm Success  ${XIQSE_DUT_IP}  ${XIQSE_DUT_PROFILE}

    # Confirm the XIQSE-managed device reported in XIQ shows the correct status (connected)
    Switch To Window  ${XIQ_WINDOW_INDEX}
    ${reconnect_result}=  Wait Until Device Online  ${XIQSE_DUT_SERIAL}
    Should Be Equal As Integers                     ${reconnect_result}       1

Test 3: Confirm Device Management State Filter
    [Documentation]     Tests the Device Management State Filter functionality
    [Tags]              nightly2    release_testing    tccs_8984    xmc_3196    development    xiqse    xiq_integration    device_table    filters    test3

    Switch To Window  ${XIQ_WINDOW_INDEX}
    Clear All Filters
    Log To Console  >> Navigating away from and back to the Devices page until APC-51254 is fixed <<
    Navigate Configure Network Policies
    XIQ Navigate to Devices and Confirm Success

    # Filter to only show Managed devices
    ${set_managed_status}=  Set Device Management State Filter      Managed  true
    Should Be Equal As Integers                                     ${set_managed_status}  1
    sleep  5 seconds
    Confirm Device MAC Present in XIQ                               ${XIQSE_MAC}
    Confirm Device MAC Present in XIQ                               ${XIQSE_DUT_MAC}
    Confirm Device Serial Present in XIQ                            ${XIQ_DUT_SERIAL}
    ${reset_managed_status}=  Set Device Management State Filter    Managed  false
    Should Be Equal As Integers                                     ${reset_managed_status}  1

    # Filter to only show Unmanaged devices
    ${set_unmanaged_status}=  Set Device Management State Filter    Unmanaged  true
    Should Be Equal As Integers                                     ${set_unmanaged_status}  1
    sleep  5 seconds
    Confirm Device MAC Not Present in XIQ                           ${XIQSE_MAC}
    Confirm Device MAC Not Present in XIQ                           ${XIQSE_DUT_MAC}
    Confirm Device Serial Not Present in XIQ                        ${XIQ_DUT_SERIAL}
    ${reset_unmanaged_status}=  Set Device Management State Filter  Unmanaged  false
    Should Be Equal As Integers                                     ${reset_unmanaged_status}  1

Test 4: Confirm Device Function Filter
    [Documentation]     Tests the Device Function Filter functionality
    [Tags]              nightly2    release_testing    tccs_8984    xmc_3196    development    xiqse    xiq_integration    device_table    filters    test4

    Switch To Window  ${XIQ_WINDOW_INDEX}
    Clear All Filters
    Log To Console  >> Navigating away from and back to the Devices page until APC-51254 is fixed <<
    Navigate Configure Network Policies
    XIQ Navigate to Devices and Confirm Success

    # Filter to only show devices with XIQSE function
    ${set_xiqse_status}=  Set Device Function Filter        ${XIQSE_FUNCTION}  true
    Should Be Equal As Integers                             ${set_xiqse_status}  1
    sleep  5 seconds
    Confirm Device MAC Present in XIQ                       ${XIQSE_MAC}
    Confirm Device MAC Not Present in XIQ                   ${XIQSE_DUT_MAC}
    Confirm Device Serial Not Present in XIQ                ${XIQ_DUT_SERIAL}
    ${reset_xiqse_status}=  Set Device Function Filter      ${XIQSE_FUNCTION}  false
    Should Be Equal As Integers                             ${reset_xiqse_status}  1

    # Filter to only show devices with Switch function
    ${set_switch_status}=  Set Device Function Filter       ${XIQSE_DUT_FUNCTION}  true
    Should Be Equal As Integers                             ${set_switch_status}  1
    sleep  5 seconds
    Confirm Device MAC Not Present in XIQ                   ${XIQSE_MAC}
    Confirm Device MAC Present in XIQ                       ${XIQSE_DUT_MAC}
    Confirm Device Serial Not Present in XIQ                ${XIQ_DUT_SERIAL}
    ${reset_switch_status}=  Set Device Function Filter     ${XIQSE_DUT_FUNCTION}  false
    Should Be Equal As Integers                             ${reset_switch_status}  1

Test 5: Confirm Device Software Version Filter
    [Documentation]     Tests the Device Software Version Filter functionality
    [Tags]              nightly2    release_testing    tccs_8984    xmc_3196    development    xiqse    xiq_integration    device_table    filters    test5

    Switch To Window  ${XIQ_WINDOW_INDEX}
    Clear All Filters
    Log To Console  >> Navigating away from and back to the Devices page until APC-51254 is fixed <<
    Navigate Configure Network Policies
    XIQ Navigate to Devices and Confirm Success

    # Filter to only show devices with the XIQ Site Engine's software version
    ${set_xiqse_status}=  Set Device Software Version Filter    ${XIQSE_OS_VERSION}  true  exact_match=false
    Should Be Equal As Integers                                 ${set_xiqse_status}  1
    sleep  5 seconds
    Confirm Device MAC Present in XIQ                           ${XIQSE_MAC}
    Confirm Device MAC Not Present in XIQ                       ${XIQSE_DUT_MAC}
    Confirm Device Serial Not Present in XIQ                    ${XIQ_DUT_SERIAL}
    ${reset_xiqse_status}=  Set Device Software Version Filter  ${XIQSE_OS_VERSION}  false  exact_match=false
    Should Be Equal As Integers                                 ${reset_xiqse_status}  1

    # Filter to show devices with all software versions
    ${set_all_status}=  Set Device Software Version Filter      All  true
    Should Be Equal As Integers                                 ${set_all_status}  1
    sleep  5 seconds
    Confirm Device MAC Present in XIQ                           ${XIQSE_MAC}
    Confirm Device MAC Present in XIQ                           ${XIQSE_DUT_MAC}
    Confirm Device Serial Present in XIQ                        ${XIQ_DUT_SERIAL}
    ${reset_all_status}=  Set Device Software Version Filter    All  false
    Should Be Equal As Integers                                 ${reset_all_status}  1

Test 6: Confirm Cloud Config Groups Filter
    [Documentation]     Tests the Cloud Config Groups Filter functionality
    [Tags]              nightly2    release_testing    tccs_8984    xmc_3196    development    xiqse    xiq_integration    device_table    filters    test6

    Switch To Window  ${XIQ_WINDOW_INDEX}
    Clear All Filters
    Log To Console  >> Navigating away from and back to the Devices page until APC-51254 is fixed <<
    Navigate Configure Network Policies
    XIQ Navigate to Devices and Confirm Success

    # Filter to only show devices with the XIQ Site Engine's cloud config group
    Run Keyword If  '21.4' in '${XIQSE_OS_VERSION}'  Set CCG Group Filter  ${XIQSE_SERIAL}  true
    ...  ELSE  Set CCG Group Filter  XIQSE-${XIQSE_NAME}  true
    sleep  5 seconds
    Confirm Device MAC Present in XIQ                           ${XIQSE_MAC}
    Confirm Device MAC Present in XIQ                           ${XIQSE_DUT_MAC}
    Confirm Device Serial Not Present in XIQ                    ${XIQ_DUT_SERIAL}
    Run Keyword If  '21.4' in '${XIQSE_OS_VERSION}'  Set CCG Group Filter  ${XIQSE_SERIAL}  false
    ...  ELSE  Set CCG Group Filter  XIQSE-${XIQSE_NAME}  false

    # Filter to show devices with all cloud config groups
    Set CCG Group Filter                                        All  true
    sleep  5 seconds
    Confirm Device MAC Present in XIQ                           ${XIQSE_MAC}
    Confirm Device MAC Present in XIQ                           ${XIQSE_DUT_MAC}
    Confirm Device Serial Not Present in XIQ                    ${XIQ_DUT_SERIAL}
    Set CCG Group Filter                                        All  false

# This test is commented out as there is an automation bug where the incorrect element is being identified
#Test 7: Confirm Device Product Type Filter
#    [Documentation]     Tests the Device Product Type Filter functionality
#    [Tags]              nightly2    release_testing    tccs_8984    xmc_3196    development    xiqse    xiq_integration    device_table    filters    test7
#
#    Switch To Window  ${XIQ_WINDOW_INDEX}
#    Clear All Filters
#    Log To Console  >> Navigating away from and back to the Devices page until APC-51254 is fixed <<
#    Navigate Configure Network Policies
#    XIQ Navigate to Devices and Confirm Success
#
#    # Filter to only show devices with the XIQ Site Engine's product type
#    ${set_xiqse_status}=  Set Device Product Type Filter        ${XIQSE_PRODUCT}  true
#    Should Be Equal As Integers                                 ${set_xiqse_status}  1
#    sleep  5 seconds
#    Confirm Device MAC Present in XIQ                           ${XIQSE_MAC}
#    Confirm Device MAC Not Present in XIQ                       ${XIQSE_DUT_MAC}
#    Confirm Device Serial Not Present in XIQ                    ${XIQ_DUT_SERIAL}
#    ${reset_xiqse_status}=  Set Device Product Type Filter      ${XIQSE_PRODUCT}  false
#    Should Be Equal As Integers                                 ${reset_xiqse_status}  1
#
#    # Filter to only show devices with the test device's product type
#    ${set_device_status}=  Set Device Product Type Filter       ${XIQSE_DUT_PRODUCT}  true
#    Should Be Equal As Integers                                 ${set_device_status}  1
#    sleep  5 seconds
#    Confirm Device MAC Not Present in XIQ                       ${XIQSE_MAC}
#    Confirm Device MAC Present in XIQ                           ${XIQSE_DUT_MAC}
#    Confirm Device Serial Not Present in XIQ                    ${XIQ_DUT_SERIAL}
#    ${reset_device_status}=  Set Device Product Type Filter     ${XIQSE_DUT_PRODUCT}  false
#    Should Be Equal As Integers                                 ${reset_device_status}  1
#
#    # Filter to show devices with all product types
#    ${set_all_status}=  Set Device Product Type Filter          All  true
#    Should Be Equal As Integers                                 ${set_all_status}  1
#    sleep  5 seconds
#    Confirm Device MAC Present in XIQ                           ${XIQSE_MAC}
#    Confirm Device MAC Present in XIQ                           ${XIQSE_DUT_MAC}
#    Confirm Device Serial Present in XIQ                        ${XIQ_DUT_SERIAL}
#    ${reset_all_status}=  Set Device Product Type Filter        All  false
#    Should Be Equal As Integers                                 ${reset_all_status}  1


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Sets up the components for the test

    XIQSE Log In and Set Window Index
    Set Up XIQSE Components

    XIQ Log In and Set Window Index
    Set Up XIQ Components

    Onboard XIQ Site Engine and Confirm Success

    # Confirm the test device managed by XIQSE is onboarded to XIQ with connected status
    Confirm XIQSE Device Added to XIQ and Connected   ${XIQSE_DUT_SERIAL}

    # Set up to test filtering
    Log To Console  Sleeping for 3 minutes to wait for the next update to come in
    Count Down in Minutes  3
    Log To Console  >> Navigating away from and back to the Devices page until APC-48603 is fixed <<
    Navigate Configure Network Policies
    XIQ Navigate to Devices and Confirm Success
    Open Filter Panel
    Clear All Filters
    Log To Console  >> Navigating away from and back to the Devices page until APC-51254 is fixed <<
    Navigate Configure Network Policies
    XIQ Navigate to Devices and Confirm Success

Tear Down Test and Close Session
    [Documentation]     Cleans up XIQ and XIQ-SE test components

    Clean Up XIQ Components
    Clean Up XIQSE Components
    XIQSE Quit Browser

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

    Confirm Serial Number and Set Common Options    ${XIQSE_SERIAL}

    # Create an invalid profile for causing a device disconnect
    XIQSE Create Invalid Profile

    # Add a test device to XIQSE
    Add Device to XIQSE and Confirm Success         ${XIQSE_DUT_IP}    ${XIQSE_DUT_PROFILE}

Set Up XIQ Components
    [Documentation]     Sets up the XIQ components for the test

    XIQ Navigate to Devices and Confirm Success

    # Clear any filters which may be applied to the view
    Clear All Filters
    Log To Console  >> Navigating away from and back to the Devices page until APC-51254 is fixed <<
    Navigate Configure Network Policies
    XIQ Navigate to Devices and Confirm Success

    # Remove XIQSE if it is already present
    Remove Device By MAC From XIQ and Confirm Success  ${XIQSE_MAC}

    # Onboard a test device managed by XIQ
    Onboard New XIQ Device                                      ${XIQ_DUT_SERIAL}  ${XIQ_DUT_MAKE}  ${LOCATION}    ${ap1}

    ${SPAWN_CONNECTION}=      Open Spawn       ${XIQ_DUT_IP}  ${XIQ_DUT_PORT}  ${XIQ_DUT_USERNAME}  ${XIQ_DUT_PASSWORD}  ${XIQ_DUT_CLI_TYPE}

    ${CONF_STATUS_RESULT}=      Configure Device To Connect To Cloud    ${XIQ_DUT_CLI_TYPE}      ${XIQ_CAPWAP_URL}    ${SPAWN_CONNECTION}
    Should Be Equal As Strings                  ${CONF_STATUS_RESULT}       1

    Close Spawn       ${SPAWN_CONNECTION}

    ${conn_result}=  Wait Until Device Online   ${XIQ_DUT_SERIAL}
    Should Be Equal As Integers                 ${conn_result}     1

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

Onboard New XIQ Device
    [Documentation]     Onboards the specified test device to XIQ, deleting it first if it already exists
    [Arguments]         ${serial}  ${make}  ${loc}   ${device}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    XIQ Navigate to Devices and Confirm Success

    # If the device has already been onboarded, delete it first
    ${search_result}=  Search Device   ${serial}

    # Onboard the device
    Run Keyword If  '${search_result}' != '1'    onboard device quick    ${device}
    Run Keyword If  '${search_result}' != '1'    Sleep   ${device_onboarding_wait}

    # Confirm the device was added successfully
    ${added_result}=  Wait Until Device Added  ${serial}
    Should Be Equal As Integers  ${added_result}  1

XIQ Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Manage> Devices view in XIQ and confirms the action was successful

    Switch To Window  ${XIQ_WINDOW_INDEX}

    ${nav_result}=  Navigate to Devices
    Should Be Equal As Integers  ${nav_result}  1

XIQSE Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Network> Devices> Devices view in XIQ-SE and confirms the action was successful

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    ${nav_result}=  XIQSE Navigate to Network Devices Tab
    Should Be Equal As Integers         ${nav_result}     1

    ${sel_result}=  XIQSE Devices Select Devices Tab
    Should Be Equal As Integers         ${sel_result}     1

XIQSE Create Invalid Profile
    [Documentation]     Creates an SNMP credential and profile in XIQSE which will cause a device to disconnect

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # Create SNMP Credential and Confirm Success
    ${add_cred_result}=  XIQSE Navigate and Create SNMP Credential    BAD_CRED  SNMPv2  junk
    Should Be Equal As Integers                                       ${add_cred_result}     1
    ${find_cred_result}=  XIQSE Find SNMP Credential                  BAD_CRED
    Should Be Equal As Integers                                       ${find_cred_result}     1

    # Create Profile and Confirm Success
    ${add_profile_result}=  XIQSE Create Profile                      BAD_PROFILE  SNMPv2  BAD_CRED
    Should Be Equal As Integers                                       ${add_profile_result}     1
    ${find_profile_result}=  XIQSE Find Profile                       BAD_PROFILE
    Should Be Equal As Integers                                       ${find_profile_result}     1

Confirm Device Status
    [Documentation]     Checks the status of the specified device and confirms it matches the expected value
    [Arguments]         ${serial}  ${expected_status}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    ${device_status}=       Get Device Status   device_serial=${serial}
    Should Contain          ${device_status}    ${expected_status}

Add Device to XIQSE and Confirm Success
    [Documentation]     Adds the specified device to XIQ-SE
    [Arguments]         ${ip}  ${profile}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    XIQSE Navigate to Devices and Confirm Success

    ${add_result}=  XIQSE Add Device      ${ip}  ${profile}
    Should Be Equal As Integers         ${add_result}     1

Confirm XIQSE Device Added to XIQ and Connected
    [Documentation]     Confirms the specified device is present in XIQ and has connected status
    [Arguments]         ${serial}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    ${search_result}=  Wait Until Device Added      ${serial}
    Should Be Equal As Integers                     ${search_result}    1

    ${device_status}=  Wait Until Device Online     ${serial}
    Should Be Equal As Integers                     ${device_status}    1

Confirm Device Serial Present in XIQ
    [Documentation]     Confirms the specified device by SERIAL NUMBER is present in XIQ
    [Arguments]         ${serial}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Refresh Devices Page

    ${search_result}=  Search Device     ${serial}
    Should Be Equal As Integers                 ${search_result}    1

Confirm Device Serial Not Present in XIQ
    [Documentation]     Confirms the specified device by SERIAL NUMBER is not present in XIQ
    [Arguments]         ${serial}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Refresh Devices Page

    ${search_result}=  Search Device     ${serial}
    Should Not Be Equal As Strings              '${search_result}'    '1'

Confirm Device MAC Present in XIQ
    [Documentation]     Confirms the specified device by MAC ADDRESS is present in XIQ
    [Arguments]         ${mac}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Refresh Devices Page

    ${search_result}=  Search Device     ${mac}
    Should Be Equal As Integers              ${search_result}    1

Confirm Device MAC Not Present in XIQ
    [Documentation]     Confirms the specified device by MAC ADDRESS is not present in XIQ
    [Arguments]         ${mac}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Refresh Devices Page

    ${search_result}=  Search Device      ${mac}
    Should Be Equal As Integers               ${search_result}    -1

Disconnect XIQSE Test Device and Confirm Success
    [Documentation]     Updates the specified device to lose contact in XIQ-SE by changing the profile
    [Arguments]         ${ip}  ${profile}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    XIQSE Navigate to Devices and Confirm Success

    ${set_result}=  XIQSE Device Set Profile                  ${ip}    BAD_PROFILE
    Should Be Equal As Integers                               ${set_result}       1
    ${status_result}=  XIQSE Wait Until Device Status Down    ${ip}
    Should Be Equal As Integers                               ${status_result}    1

Reconnect XIQSE Test Device and Confirm Success
    [Documentation]     Updates the specified device to regain contact in XIQ-SE by changing the profile
    [Arguments]         ${ip}    ${profile}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    XIQSE Navigate to Devices and Confirm Success

    ${set_result}=  XIQSE Device Set Profile                  ${ip}    ${profile}
    Should Be Equal As Integers                               ${set_result}       1
    ${status_result}=  XIQSE Wait Until Device Status Up      ${ip}
    Should Be Equal As Integers                               ${status_result}    1

Set CCG Group Filter
    [Documentation]     Filters by the XIQSE CCG group
    [Arguments]         ${filter}  ${value}

    ${result}=  Set Cloud Config Groups Filter   ${filter}  ${value}
    Should Be Equal As Integers                  ${result}  1

Delete XIQ Test Device and Confirm Success
    [Documentation]     Deletes the specified device and confirms the action was successful.
    [Arguments]         ${mac}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    XIQ Navigate to Devices and Confirm Success

    ${del_result}=  Delete Device   device_mac=${mac}
    Should Be Equal As Integers     ${del_result}  1

Delete XIQSE Test Device and Confirm Success
    [Documentation]     Deletes the specified device from XIQ-SE and confirms the action was successful
    [Arguments]         ${ip}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    XIQSE Navigate to Devices and Confirm Success

    ${del_result}=  XIQSE Delete Device   ${ip}
    Should Be Equal As Integers         ${del_result}     1

XIQSE Delete SNMP Credential and Confirm Success
    [Documentation]     Deletes the SNMP credential from XIQ-SE
    [Arguments]         ${name}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    ${del_result}=  XIQSE Navigate and Delete SNMP Credential   ${name}
    Should Be Equal As Integers                                 ${del_result}     1
    ${find_result}=  XIQSE Find SNMP Credential                 ${name}
    Should Be Equal As Integers                                 ${find_result}    -1

XIQSE Delete Profile and Confirm Success
    [Documentation]     Deletes the profile from XIQ-SE
    [Arguments]         ${name}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    ${del_result}=  XIQSE Navigate and Delete Profile           ${name}
    Should Be Equal As Integers                                 ${del_result}     1
    ${find_result}=  XIQSE Find Profile                         ${name}
    Should Be Equal As Integers                                 ${find_result}    -1

Clean Up XIQ Components
    [Documentation]     Cleans up components used in XIQ during the test, logs out, and closes the browser

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Clear All Filters
    Log To Console  >> Navigating away from and back to the Devices page until APC-51254 is fixed <<
    Navigate Configure Network Policies
    XIQ Navigate to Devices and Confirm Success

    Close Filter Panel

    Delete XIQ Test Device and Confirm Success    ${XIQSE_MAC}
    Delete XIQ Test Device and Confirm Success    ${XIQ_DUT_SERIAL}

    # Log out and close the window
    [Teardown]  Run Keywords
    ...  Log Out of XIQ and Confirm Success
    ...  AND
    ...  Close Window    ${XIQ_WINDOW_INDEX}

Clean Up XIQSE Components
    [Documentation]     Cleans up components used in XIQ-SE during the test, logs out, and closes the browser

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Enable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}

    # Disable all columns for event searches
    Set Alarm Event Search Scope    false

    # Handle Connection Lost
    XIQSE Handle Connection Lost Error    ${XIQSE_USER}    ${XIQSE_PASSWORD}

    # Reset the options
    ${options_result}=  XIQSE Restore Default XIQ Connection Options and Save
    Should Be Equal As Integers         ${options_result}     1

    # Delete the test device
    Delete XIQSE Test Device and Confirm Success          ${XIQSE_DUT_IP}

    # Delete the profile and SNMP credential
    XIQSE Delete Profile and Confirm Success              BAD_PROFILE
    XIQSE Delete SNMP Credential and Confirm Success      BAD_CRED

    # Log out
    Log Out of XIQSE and Confirm Success
