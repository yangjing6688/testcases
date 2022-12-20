#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Dan McCarthy
# Description   : Sanity tests to verify basic Digital Twin functionality for the XIQ 22R6 release.
#               : These test cases require that the CoPilot feature can be enabled.
#               : The 'user' account will need to have either an active CoPilot license
#               :  or use the 30-Day Trial license.
#               : qTest test cases in the CSIT project.
#                 - TCCS-13497: Test 1: Enable the Digital Twin feature
#                 - TCCS-13498: Test 2: Onboard Digital Twin Device
#                 - TCCS-13499: Test 3: Digital Twin Device D360 Overview panel
#                 - TCCS-13500: Test 4: Disable the Digital Twin Feature

*** Settings ***
Library         Collections
Library         common/TestFlow.py
Library         xiq/flows/common/Login.py
Library         xiq/flows/common/Navigator.py
Library         xiq/flows/globalsettings/GlobalSetting.py
Library         xiq/flows/globalsettings/LicenseManagement.py
Library         xiq/flows/manage/Devices.py
Library         xiq/flows/manage/DevicesActions.py
Library         xiq/flows/manage/Device360.py

Force Tags      testbed_none

Variables       Environments/${ENV}
Variables       Environments/${TOPO}
Variables       TestBeds/${TESTBED}
Variables       Environments/Config/waits.yaml

Suite Setup     Log In and Set Up Test
Suite Teardown  Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}                  ${test_url}
${XIQ_USER}                 ${tenant_username}
${XIQ_PASSWORD}             ${tenant_password}

${DT_PERSONA}               ${netelem1.digital_twin_persona}
${DT_MODEL}                 ${netelem1.model}
${DT_VERSION}               ${netelem1.digital_twin_version}
${DT_IP_ADDRESS}            ${netelem1.ip}
${LOCATION}                 ${netelem1.location}
${DT_IQAGENT}

*** Test Cases ***
TCCS-13497: Enable Digital Twin Feature
    [Documentation]     Enables the "Digital Twin" feature by enabling CoPilot. (Required for 22R6)
    [Tags]      tccs-13497      development    xiq    digital_twin    sanity

    ${result}=  Navigate to Devices
    Should Be Equal As Integers                             ${result}       1

    ${result}=  Is Digital Twin Option Visible
    Should Be Equal As Strings                              ${result}       False

    ${result}=  Enable CoPilot Feature For This VIQ
    Should Be Equal As Integers                             ${result}       1

    ${result}=  Navigate to Devices
    Should Be Equal As Integers                             ${result}       1

    ${result}=  Is Digital Twin Option Visible
    Should Be Equal As Strings                              ${result}       True

    [Teardown]    Refresh Page

TCCS-13498: Onboard Digital Twin Device
    [Documentation]     Onboard "Digital Twin" device.
    [Tags]      tccs-13498      development    xiq    digital_twin    sanity

    Depends On      TCCS-13497

    ${result}=  Navigate to Devices
    Should Be Equal As Integers                             ${result}       1

    ${ONBOARD_RESULT}=      onboard device quick            ${netelem1}
    Should Be Equal As Strings                              ${ONBOARD_RESULT}     1

    ${dt_serial}=           set variable                    ${${netelem1.name}.serial}
    Set Suite Variable                                      ${DT_SERIAL}    ${dt_serial}

    ${result}=  Length Should Be                            ${DT_SERIAL}    14
    Should Be Equal                                         ${result}       ${None}

    ${status_icon}=    Get Device Status Icon               ${DT_SERIAL}
    Should Be Equal As Strings                              ${status_icon}  digital_twin

    Select Device                                           ${DT_SERIAL}

    ${action_menu}=  Is Actions Relaunch Digital Twin Visible
    Should Be Equal As Strings                              ${action_menu}  True

    ${action_menu}=    Is Actions Shutdown Digital Twin Visible
    Should Be Equal As Strings                              ${action_menu}  False

    ${result}=  Wait Until Device Online                    ${DT_SERIAL}    retry_duration=5    retry_count=60
    Should Be Equal As Integers                             ${result}       1

    ${result}=    Wait Until Device Managed                 ${DT_SERIAL}    retry_duration=5    retry_count=60
    Should Be Equal As Integers                             ${result}       1

    ${status}=  Get Device Status                           device_serial=${DT_SERIAL}
    Should Contain                                          ${status}       green

    ${dt_mac}=   Get Device Details                         ${DT_SERIAL}    MAC
    Set Suite Variable                                      ${DT_MAC}       ${dt_mac}

    ${result}=  Should Start With                           ${DT_MAC}       C8665D
    Should Be Equal                                         ${result}       ${None}

    ${dt_iqagent}=   Get Device Details                     ${DT_SERIAL}    IQAGENT
    Set Suite Variable                                      ${DT_IQAGENT}   ${dt_iqagent}

    [Teardown]    Refresh Page

TCCS-13499: Digital Twin Device D360 Overview panel
    [Documentation]     Open D360 view.  Verify the device specific information is displayed.
    [Tags]      tccs-13499      development    xiq    digital_twin    sanity

    Depends On      TCCS-13498

    ${result}=  Navigate to Devices
    Should Be Equal As Integers                             ${result}       1

    ${nav_result}=  Navigate To Device360 Page With MAC     ${DT_MAC}
    Should Be Equal As Integers                             ${nav_result}   1

    ${status}=   Get Device360 Digital Twin Device Status
    Should Be Equal As Strings                              ${status}       connected

    ${dt_button}=  Is Device360 Shutdown Digital Twin Button Visible
    Should Be Equal As Strings                              ${dt_button}    True

    Confirm Device360 Top Bar Information for Digital Twin Device

    [Teardown]    Run Keywords          Refresh Page

TCCS-13500: Disable Digital Twin Feature
    [Documentation]     Disables the "Digital Twin" feature by disabling CoPilot. (Required for 22R6)
    [Tags]      tccs-13500      development    xiq    digital_twin    sanity

    ${result}=  Navigate to Devices
    Should Be Equal As Integers                             ${result}       1

    ${result}=   Is Digital Twin Option Visible
    Should Be Equal As Strings                              ${result}       True

    ${result}=    Disable CoPilot Feature For This VIQ
    Should Be Equal As Integers                             ${result}       1

    ${result}=  Navigate to Devices
    Should Be Equal As Integers                             ${result}       1

    ${result}=   Is Digital Twin Option Visible
    Should Be Equal As Strings                              ${result}       False

    Depends On      TCCS-13498

    ${status}=  Get Device Status                           device_serial=${DT_SERIAL}
    Should Contain                                          ${status}       disconnected

    Select Device                                           ${DT_SERIAL}

    ${result}=    Is Actions Button Enabled
    Should Be Equal As Strings                              ${result}       False

    [Teardown]    Refresh Page

*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs into XIQ and configures pre-requisites for the test

    ${result}=  Login User                                  ${XIQ_USER}     ${XIQ_PASSWORD}     url=${XIQ_URL}
    Should Be Equal As Integers                             ${result}       1

    &{entitlement}=   Navigate And Get Entitlement Counts For Feature       feature=PRD-XIQ-COPILOT-S-C
    ${feature}=       Get From Dictionary                   ${entitlement}  feature
    Should Contain                                          ${feature}      PRD-XIQ-COPILOT-S-C

    ${result}=    Disable CoPilot Feature For This VIQ
    Should Be Equal As Integers                             ${result}       1

    # Refresh Page

Tear Down Test and Close Session
    [Documentation]     Cleans up the components created during the test and ends the test

    ${result}=  Delete Device                               ${DT_SERIAL}
    Should Be Equal As Integers                             ${result}       1

    ${result}=  Logout User
    Should Be Equal As Integers                             ${result}       1

    ${result}=  Quit Browser
    Should Be Equal As Integers                             ${result}       1

Confirm Device360 Top Bar Information for Digital Twin Device
    [Documentation]     Confirms the topbar of the Device360 view contains correct values for the Digital Twin device.

    # Obtain the data displayed along the top bar in the Device360 > Overview panel.
    &{topbar_info}=  Get Switch Information

    ${topbar_ip}=       Get From Dictionary  ${topbar_info}  ip_address
    ${topbar_mac}=      Get From Dictionary  ${topbar_info}  mac_address
    ${topbar_version}=  Get From Dictionary  ${topbar_info}  software_version
    ${topbar_model}=    Get From Dictionary  ${topbar_info}  device_model
    ${topbar_serial}=   Get From Dictionary  ${topbar_info}  serial_number
    ${topbar_iqagent}=  get from dictionary  ${topbar_info}  IQAgent_version

    Should Be Equal                 ${topbar_ip}        ${DT_IP_ADDRESS}
    Should Be Equal                 ${topbar_mac}       ${DT_MAC}
    Should Be Equal                 ${topbar_version}   ${DT_VERSION}
    Should Contain                  ${topbar_model}     ${DT_MODEL}
    Should Be Equal                 ${topbar_serial}    ${DT_SERIAL}
    Should Be Equal                 ${topbar_iqagent}   ${DT_IQAGENT}
