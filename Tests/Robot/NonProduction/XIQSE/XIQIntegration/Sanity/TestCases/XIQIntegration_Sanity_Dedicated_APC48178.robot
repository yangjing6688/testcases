# Author        : Heidi S. White
# Description   : Test Suite for sanity testing of XIQSE-XIQ integration where XIQSE contains two devices, is modeled
#                 as an SNMP-managed device, and remains onboarded to XIQ through upgrades:
#                   - confirms XIQSE has expected values in the Devices table
#                   - confirms a pre-existing device has expected values in the Devices table
#                   - confirms new devices added to XIQSE are onboarded to XIQ
#                   - confirms a newly-added device has expected values in the Devices table
#                   - confirms Device360 view can be accessed for newly-added devices
#                   - confirms values of new devices in Device360 view
#                   - confirms Device360 view can be accessed for pre-existing devices
#                   - confirms values of pre-existing devices in Device360 view
#                   - confirms Device360 view can be accessed for XIQSE
#                   - confirms values of XIQSE in Device360 view
#                   - confirms deleting newly-added devices from XIQSE removes them from XIQ
#                   - confirms deleting a pre-existing device from XIQSE removes it from XIQ
#                   - confirms adding back the pre-existing device to XIQSE onboards it to XIQ
#                 This is qTest test case TC-11793 in the CSIT project, and tests Jira APC-48178.

*** Settings ***
Library         Collections
Library         xiq/flows/manage/Device360.py

Resource        ../../Sanity/Resources/AllResources.robot

Force Tags      testbed_2_node

Suite Setup     Log In and Set Up Test
Suite Teardown  Tear Down Test and Close Session


*** Variables ***
# NOTE: The XIQ/XIQSE variables as well as the already-onboarded devices are hard-coded as they test a dedicated setup
#       and have to be specific to this XIQ and XIQSE, with the two already-onboarded devices.
${XIQSE_URL}         https://10.54.142.121:8443
${XIQSE_USER}        root
${XIQSE_PASSWORD}    n7830466
${XIQSE_SERIAL}      XIQSE-50AE2DB5BAF644A487FB9E718C17D22A
${XIQSE_MAC}         000C29CE7BFE
${XIQSE_IP}          10.54.142.121
${XIQSE_NAME}        auto-xiqse-st
${XIQSE_MAKE}        XIQSE
${XIQSE_MODEL}       XIQSE
${XIQSE_PRODUCT}     XIQ_SE
${XIQSE_OS}          XIQSE

${XIQ_URL}           https://g2r1.qa.xcloudiq.com/
${XIQ_USER}          xiqse1+partner@gmail.com
${XIQ_PASSWORD}      Aerohive123

# TWO DEDICATED DEVICES FOR THIS SYSTEM
${DUT1_NAME}         SAPro-x440-235-150
${DUT1_SERIAL}       1532G-235150
${DUT1_IP}           10.57.235.150
${DUT1_PROFILE}      public_v1_Profile
${DUT1_MAC}          00049639EB96
${DUT1_MAKE}         EXOS
${DUT1_MODEL}        X440-G2-24t-G4
${DUT1_PLATFORM}     exos

${DUT2_NAME}         SAPro-x440-235-151
${DUT2_SERIAL}       1532G-235151
${DUT2_IP}           10.57.235.151
${DUT2_PROFILE}      public_v1_Profile
${DUT2_MAC}          00049639EB97
${DUT2_MAKE}         EXOS
${DUT2_MODEL}        X440-G2-24t-G4
${DUT2_PLATFORM}     exos

# Additional devices can be from a test bed
${DUT3_NAME}         ${netelem1.name}
${DUT3_SERIAL}       ${netelem1.serial}
${DUT3_IP}           ${netelem1.ip}
${DUT3_PROFILE}      ${netelem1.profile}
${DUT3_MAC}          ${netelem1.mac}
${DUT3_MAKE}         ${netelem1.make}
${DUT3_MODEL}        ${netelem1.model}
${DUT3_PLATFORM}     ${netelem1.platform}

${DUT4_NAME}         ${netelem2.name}
${DUT4_SERIAL}       ${netelem2.serial}
${DUT4_IP}           ${netelem2.ip}
${DUT4_PROFILE}      ${netelem2.profile}
${DUT4_MAC}          ${netelem2.mac}
${DUT4_MAKE}         ${netelem2.make}
${DUT4_MODEL}        ${netelem2.model}
${DUT4_PLATFORM}     ${netelem2.platform}

@{COLUMNS}           Host Name  Managed By  MGT IP Address  MAC Address  Cloud Config Groups  Serial #  Make  OS  Model
${COLUMN_LABELS}     HOST NAME,MANAGED BY,MGT IP ADDRESS,MAC,CLOUD CONFIG GROUPS,SERIAL,MAKE,OS,MODEL


*** Test Cases ***
Test 1: Confirm XIQ Site Engine Values
    [Documentation]     Confirms the XIQ Site Engine has the expected values in the Devices table
    [Tags]              nightly1    release_testing    csit_tc_11793    apc_48178    development    xiqse    xiq_integration    dedicated_sanity    test1

    Refresh Devices Page

    &{xiqse_info}=     Get Device Row Values  ${XIQSE_SERIAL}  ${COLUMN_LABELS}

    ${serial_result}=   Get From Dictionary  ${xiqse_info}  SERIAL
    ${mgby_result}=     Get From Dictionary  ${xiqse_info}  MANAGED BY
    ${mac_result}=      Get From Dictionary  ${xiqse_info}  MAC
    ${make_result}=     Get From Dictionary  ${xiqse_info}  MAKE
    ${model_result}=    Get From Dictionary  ${xiqse_info}  MODEL
    ${ip_result}=       Get From Dictionary  ${xiqse_info}  MGT IP ADDRESS
    ${os_result}=       Get From Dictionary  ${xiqse_info}  OS
    ${cldcfg_result}=   Get From Dictionary  ${xiqse_info}  CLOUD CONFIG GROUPS

    Should Be Equal     ${serial_result}    ${XIQSE_SERIAL}
    Should Be Equal     ${mgby_result}      XIQ
    Should Be Equal     ${mac_result}       ${XIQSE_MAC}
    Should Be Equal     ${make_result}      ${XIQSE_MAKE}
    Should Be Equal     ${model_result}     ${XIQSE_MODEL}
    Should Be Equal     ${ip_result}        ${XIQSE_IP}
    Should Be Equal     ${os_result}        ${XIQSE_OS}

    Check Cloud Config Result  ${cldcfg_result}

Test 2: Confirm Pre-Existing XIQSE-Managed Device Values
    [Documentation]     Confirms the pre-existing XIQSE-managed device has the expected values in the Devices table
    [Tags]              nightly1    release_testing    csit_tc_11793    apc_48178    development    xiqse    xiq_integration    dedicated_sanity    test2

    Refresh Devices Page

    &{device_info}=     Get Device Row Values  ${DUT1_SERIAL}  ${COLUMN_LABELS}

    ${serial_result}=   Get From Dictionary  ${device_info}  SERIAL
    ${mgby_result}=     Get From Dictionary  ${device_info}  MANAGED BY
    ${mac_result}=      Get From Dictionary  ${device_info}  MAC
    ${make_result}=     Get From Dictionary  ${device_info}  MAKE
    ${model_result}=    Get From Dictionary  ${device_info}  MODEL
    ${ip_result}=       Get From Dictionary  ${device_info}  MGT IP ADDRESS
    ${cldcfg_result}=   Get From Dictionary  ${device_info}  CLOUD CONFIG GROUPS

    Should Be Equal      ${serial_result}    ${DUT1_SERIAL}
    Should Be Equal      ${mgby_result}      ${XIQSE_PRODUCT}
    Should Be Equal      ${mac_result}       ${DUT1_MAC}
    Should Be Equal      ${make_result}      ${DUT1_MAKE}
    Should Be Equal      ${model_result}     ${DUT1_MODEL}

    Check Cloud Config Result  ${cldcfg_result}

Test 3: Confirm Adding New Devices Onboards to XIQ
    [Documentation]     Confirms newly-added devices in XIQSE are onboarded to XIQ
    [Tags]              nightly1    release_testing    csit_tc_11793    apc_48178    development    xiqse    xiq_integration    dedicated_sanity    test3

    # Add new devices to XIQ-SE
    XIQSE Add Device and Confirm Success           ${DUT3_IP}    ${DUT3_PROFILE}
    XIQSE Add Device and Confirm Success           ${DUT4_IP}    ${DUT4_PROFILE}

    # Confirm the new XIQSE-managed devices are automatically onboarded to XIQ
    Confirm XIQSE Device Added to XIQ and Connected   ${DUT3_SERIAL}
    Confirm XIQSE Device Added to XIQ and Connected   ${DUT4_SERIAL}

Test 4: Confirm Newly-Added XIQSE-Managed Device Values
    [Documentation]     Confirms the newly-added XIQSE-managed device has the expected values in the Devices table
    [Tags]              nightly1    release_testing    csit_tc_11793    apc_48178    development    xiqse    xiq_integration    dedicated_sanity    test4

    Refresh Devices Page

    &{device_info}=     Get Device Row Values  ${DUT1_SERIAL}  ${COLUMN_LABELS}

    ${serial_result}=   Get From Dictionary  ${device_info}  SERIAL
    ${mgby_result}=     Get From Dictionary  ${device_info}  MANAGED BY
    ${mac_result}=      Get From Dictionary  ${device_info}  MAC
    ${make_result}=     Get From Dictionary  ${device_info}  MAKE
    ${model_result}=    Get From Dictionary  ${device_info}  MODEL
    ${ip_result}=       Get From Dictionary  ${device_info}  MGT IP ADDRESS
    ${cldcfg_result}=   Get From Dictionary  ${device_info}  CLOUD CONFIG GROUPS

    Should Be Equal      ${serial_result}    ${DUT1_SERIAL}
    Should Be Equal      ${mgby_result}      ${XIQSE_PRODUCT}
    Should Be Equal      ${mac_result}       ${DUT1_MAC}
    Should Be Equal      ${make_result}      ${DUT1_MAKE}
    Should Be Equal      ${model_result}     ${DUT1_MODEL}

    Check Cloud Config Result  ${cldcfg_result}

Test 5: Confirm Device360 View Can Be Opened for New Device
    [Documentation]     Confirms the Device360 view can be opened for a newly-added XIQSE-managed device
    [Tags]              nightly1    release_testing    csit_tc_11793    apc_48178    development    xiqse    xiq_integration    dedicated_sanity    test5

    # Open the Device360 view
    Navigate to Device360 Page with MAC  ${DUT3_MAC}

    [Teardown]  Close Device360 Window

Test 6: Confirm Device360 View Values for New Device
    [Documentation]     Confirms the Device360 view contains correct values for a newly-added XIQSE-managed device
    [Tags]              nightly1    release_testing    csit_tc_11793    apc_48178    development    xiqse    xiq_integration    dedicated_sanity    test6

    Refresh Devices Page
    &{overview_info}=       Get Device360 Overview Information    ${DUT3_MAC}

    ${overview_name}=       Get From Dictionary  ${overview_info}  host_name
    ${overview_mac}=        Get From Dictionary  ${overview_info}  mac_address
    ${overview_serial}=     Get From Dictionary  ${overview_info}  serial_number
    ${overview_make}=       Get From Dictionary  ${overview_info}  device_make
    ${overview_model}=      Get From Dictionary  ${overview_info}  device_model

    Should Be Equal     ${overview_name}    ${DUT3_NAME}
    Should Be Equal     ${overview_mac}     ${DUT3_MAC}
    Should Be Equal     ${overview_serial}  ${DUT3_SERIAL}
# ------- APC-43433
    Log To Console      MAKE value ${overview_make} not checked against ${DUT3_MAKE} until APC-43433 is addressed
#    Should Be Equal    ${overview_make}    ${DUT1_MAKE}
# ------------------
# ------- APC-43840
    Log To Console      MODEL value ${overview_model} not checked against ${DUT3_MODEL} until APC-43840 is addressed
#    Should Be Equal     ${overview_model}   ${DUT1_MODEL}
# ------------------

Test 7: Confirm Device360 View Can Be Opened for Pre-Existing Device
    [Documentation]     Confirms the Device360 view can be opened for a pre-existing XIQSE-managed device
    [Tags]              nightly1    release_testing    csit_tc_11793    apc_48178    development    xiqse    xiq_integration    dedicated_sanity    test7

    # Open the Device360 view
    Navigate to Device360 Page with MAC  ${DUT1_MAC}

    [Teardown]  Close Device360 Window

Test 8: Confirm Device360 View Values for Pre-Existing Device
    [Documentation]     Confirms the Device360 view contains correct values for a pre-existing XIQSE-managed device
    [Tags]              nightly1    release_testing    csit_tc_11793    apc_48178    development    xiqse    xiq_integration    dedicated_sanity    test8

    Refresh Devices Page
    &{overview_info}=       Get Device360 Overview Information    ${DUT1_MAC}

    ${overview_name}=       Get From Dictionary  ${overview_info}  host_name
    ${overview_mac}=        Get From Dictionary  ${overview_info}  mac_address
    ${overview_serial}=     Get From Dictionary  ${overview_info}  serial_number
    ${overview_make}=       Get From Dictionary  ${overview_info}  device_make
    ${overview_model}=      Get From Dictionary  ${overview_info}  device_model

    Should Be Equal     ${overview_name}    ${DUT1_NAME}
    Should Be Equal     ${overview_mac}     ${DUT1_MAC}
    Should Be Equal     ${overview_serial}  ${DUT1_SERIAL}
# ------- APC-43433
    Log To Console      MAKE value ${overview_make} not checked against ${DUT1_MAKE} until APC-43433 is addressed
#    Should Be Equal    ${overview_make}    ${DUT1_MAKE}
# ------------------
# ------- APC-43840
    Log To Console      MODEL value ${overview_model} not checked against ${DUT1_MODEL} until APC-43840 is addressed
#    Should Be Equal     ${overview_model}   ${DUT1_MODEL}
# ------------------

Test 9: Confirm Device360 View Can Be Opened for XIQSE
    [Documentation]     Confirms the Device360 view can be opened for XIQSE
    [Tags]              nightly1    release_testing    csit_tc_11793    apc_48178    development    xiqse    xiq_integration    dedicated_sanity    test9

    # Open the Device360 view
    Navigate to Device360 Page with MAC  ${XIQSE_MAC}

    [Teardown]  Close Device360 Window

Test 10: Confirm Device360 View Values for XIQSE
    [Documentation]     Confirms the Device360 view contains correct values for XIQSE
    [Tags]              nightly1    release_testing    csit_tc_11793    apc_48178    development    xiqse    xiq_integration    dedicated_sanity    test10

    Refresh Devices Page
    &{overview_info}=       Get Device360 Overview Information  ${XIQSE_MAC}

    ${overview_name}=       Get From Dictionary  ${overview_info}  host_name
    ${overview_ip}=         Get From Dictionary  ${overview_info}  ip_address
    ${overview_mac}=        Get From Dictionary  ${overview_info}  mac_address
    ${overview_serial}=     Get From Dictionary  ${overview_info}  serial_number
    ${overview_make}=       Get From Dictionary  ${overview_info}  device_make
    ${overview_model}=      Get From Dictionary  ${overview_info}  device_model

    Should Be Equal     ${overview_name}    ${XIQSE_NAME}
    Should Be Equal     ${overview_ip}      ${XIQSE_IP}
    Should Be Equal     ${overview_mac}     ${XIQSE_MAC}
    Should Be Equal     ${overview_serial}  ${XIQSE_SERIAL}
    Should Be Equal     ${overview_make}    ${XIQSE_MAKE}
# ------- APC-43431
    Log To Console      MODEL value ${overview_model} not checked against ${XIQSE_MODEL} until APC-43431 is addressed
#    Should Be Equal    ${overview_model}   ${XIQSE_MODEL}
# ------------------

Test 11: Confirm Deleting Newly-Added Devices Removes Devices from XIQ
    [Documentation]     Confirms newly-added devices which are deleted from XIQSE are removed from XIQ
    [Tags]              nightly1    release_testing    csit_tc_11793    apc_48178    development    xiqse    xiq_integration    dedicated_sanity    test11

    # Remove newly-added devices from XIQ-SE
    XIQSE Delete Device and Confirm Success           ${DUT3_IP}
    XIQSE Delete Device and Confirm Success           ${DUT4_IP}

    # Confirm the newly-added XIQSE-managed devices which were deleted are also removed from XIQ
    Confirm XIQSE Device Removed From XIQ   ${DUT3_SERIAL}
    Confirm XIQSE Device Removed From XIQ   ${DUT4_SERIAL}

Test 12: Confirm Deleting Pre-Existing Device Removes Device from XIQ
    [Documentation]     Confirms a pre-existing device which is deleted from XIQSE is removed from XIQ
    [Tags]              nightly1    release_testing    csit_tc_11793    apc_48178    development    xiqse    xiq_integration    dedicated_sanity    test12

    # Remove pre-existing device from XIQ-SE
    XIQSE Delete Device and Confirm Success           ${DUT2_IP}

    # Confirm the pre-existing XIQSE-managed device which was deleted is also removed from XIQ
    Confirm XIQSE Device Removed From XIQ   ${DUT2_SERIAL}

Test 13: Confirm Deleted and Re-Created Device is Added Back to XIQ
    [Documentation]     Confirms a pre-existing device which was deleted from and readded to XIQSE is added back to XIQ
    [Tags]              nightly1    release_testing    csit_tc_11793    apc_48178    development    xiqse    xiq_integration    dedicated_sanity    test13

    # Add back the pre-existing device to XIQ-SE
    XIQSE Add Device and Confirm Success           ${DUT2_IP}    ${DUT2_PROFILE}

    # Confirm the XIQSE-managed device is automatically onboarded to XIQ
    Confirm XIQSE Device Added to XIQ and Connected   ${DUT2_SERIAL}


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
    [Documentation]     Logs into XIQ-SE and sets up the components for the test

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    # Confirm the serial number is correct and set the common options needed for automation
    Confirm Serial Number and Set Common Options     ${XIQSE_SERIAL}

    # Navigate to Network> Devices> Devices
    Navigate to Devices and Confirm Success

    # Confirm the expected devices exist and are reported as being onboarded to XIQ
    Confirm IP Address Present in Devices Table     ${XIQSE_IP}
    Confirm IP Address Present in Devices Table     ${DUT1_IP}
    Confirm IP Address Present in Devices Table     ${DUT2_IP}
    Confirm XIQSE Device Onboarded to XIQ           ${XIQSE_IP}
    Confirm XIQSE Device Onboarded to XIQ           ${DUT1_IP}
    Confirm XIQSE Device Onboarded to XIQ           ${DUT2_IP}

Set Up XIQ Components
    [Documentation]     Logs into XIQ and sets up the components for the test

    Switch To Window  ${XIQ_WINDOW_INDEX}

    ${nav_result}=  Navigate to Devices
    Should Be Equal As Integers  ${nav_result}  1

    Column Picker Select       @{COLUMNS}

    # Confirm XIQSE and the XIQSE-managed devices are already onboarded
    Confirm XIQ Site Engine Onboarded to XIQ
    Confirm XIQSE Device Added to XIQ and Connected     ${DUT1_SERIAL}
    Confirm XIQSE Device Added to XIQ and Connected     ${DUT2_SERIAL}

Confirm XIQ Site Engine Onboarded to XIQ
    [Documentation]     Confirms the XIQ Site Engine has been onboarded to XIQ successfully and has connected status

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Confirm Device Serial Present   ${XIQSE_SERIAL}
    Confirm Device Serial Online    ${XIQSE_SERIAL}

Confirm XIQSE Device Added to XIQ and Connected
    [Documentation]     Confirms the specified device is present in XIQ and has connected status
    [Arguments]         ${serial}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Confirm Device Serial Present   ${serial}
    Confirm Device Serial Online    ${serial}

Confirm XIQSE Device Removed From XIQ
    [Documentation]     Confirms the specified device is no longer present in XIQ
    [Arguments]         ${serial}

    Switch To Window  ${XIQ_WINDOW_INDEX}

    Confirm Device Serial Not Present  ${serial}

XIQSE Add Device and Confirm Success
    [Documentation]     Adds the specified device to XIQ-SE
    [Arguments]         ${ip}  ${profile}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Create Device and Confirm Success  ${ip}  ${profile}

XIQSE Delete Device and Confirm Success
    [Documentation]     Deletes the specified device from XIQ-SE
    [Arguments]         ${ip}

    Switch To Window  ${XIQSE_WINDOW_INDEX}

    Delete Device and Confirm Success  ${ip}

Clean Up XIQ Components
    [Documentation]     Cleans up components used in XIQ during the test and logs out

    Switch To Window                        ${XIQ_WINDOW_INDEX}

    Log Out of XIQ and Confirm Success
    Close Window                            ${XIQ_WINDOW_INDEX}

Clean Up XIQSE Components
    [Documentation]     Cleans up components used in XIQ-SE during the test and logs out

    Switch To Window                        ${XIQSE_WINDOW_INDEX}

    Log Out of XIQSE and Confirm Success

Check Cloud Config Result
    [Documentation]     Checks if the cloud config value has the correct information
    [Arguments]         ${cldcfg_result}

    Log To Console  XIQSE VERSION is ${XIQSE_OS_VERSION}
    Run Keyword If  '21.4' in '${XIQSE_OS_VERSION}'
    ...  Should Be True     """${XIQSE_SERIAL}""" in "${cldcfg_result}"
    ...  ELSE
    ...  Should Be True     """XIQSE-${XIQSE_NAME}""" in "${cldcfg_result}"
