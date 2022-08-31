#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to the Digital Twin functionality.
#

*** Settings ***
Library     xiq/flows/common/Login.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/DevicesActions.py
Library     xiq/flows/manage/Device360.py

*** Keywords ***
Confirm Digital Twin Feature Is Enabled
    [Documentation]     Confirm that the Digital Twin option is enabled.

    ${result}=   Is Digital Twin Option Visible
    Should Be Equal As Integers                             ${result}   1

Confirm Digital Twin Feature Is Disabled
    [Documentation]     Confirm if the Digital Twin feature is disabled.

    ${result}=   Is Digital Twin Option Visible
    Should Be Equal As Integers                             ${result}   -1

Enable Digital Twin Feature
    [Documentation]     Use the soft launch URL to enable the Digital Twin feature.
    [Arguments]         ${xiq_url}

    ${result}=   XIQ Soft Launch Feature Url                ${xiq_url}/hm-webapp/?digitalTwin=true#/devices
    Should Be Equal As Integers                             ${result}   1

Disable Digital Twin Feature
    [Documentation]     Use the soft launch URL to disable the Digital Twin feature.
    [Arguments]         ${xiq_url}

    ${result}=   XIQ Soft Launch Feature Url                ${xiq_url}/hm-webapp/?digitalTwin=false#/devices
    Should Be Equal As Integers                             ${result}   1

Confirm Digital Twin Serial Number
    [Documentation]    Check if the Serial Number generated for a Digital Twin device is at least 14 characters.
    [Arguments]        ${serial_number}

    ${result}=  Length Should Be                ${serial_number}    14
    Should Be Equal                             ${result}           ${None}

Confirm Digital Twin MAC Address
    [Documentation]    Determine if the MAC Address assigned to a Digital Twin device is within
    ...                a certain range: C8665D970300 > C8665DB587FF. (See XIQ-6662)
    ...                Currently, just testing that MAC Address starts with "C8665D"
    [Arguments]        ${mac_address}

    ${result}=  Should Start With               ${mac_address}      C8665D
    Should Be Equal                             ${result}           ${None}

Relaunch Digital Twin Device
    [Documentation]    Selects the "Action > Relaunch Digital Twin" menu option

    ${result}=   Actions Relaunch Digital Twin
    Should Be Equal As Integers                              ${result}      1

Confirm Actions Relaunch Digital Twin Option Visible
    [Documentation]     Confirm that the Actions > Relaunch Digital Twin is visible.

    ${action_menu}=  Is Actions Relaunch Digital Twin Visible
    Should Be Equal As Integers                             ${action_menu}   1

Confirm Actions Relaunch Digital Twin Option Hidden
    [Documentation]     Confirm that the Actions > Relaunch Digital Twin is hidden.

    ${action_menu}=  Is Actions Relaunch Digital Twin Visible
    Should Be Equal As Integers                             ${action_menu}   -1

Shutdown Digital Twin Device
    [Documentation]    Selects the "Action > Shutdown Digital Twin" menu option

    ${result}=   Actions Shutdown Digital Twin
    Should Be Equal As Integers                              ${result}      1

Confirm Actions Shutdown Digital Twin Option Visible
    [Documentation]     Confirm that the Actions > Shutdown Digital Twin is visible.

    ${action_menu}=    Is Actions Shutdown Digital Twin Visible
    Should Be Equal As Integers                             ${action_menu}   1

Confirm Actions Shutdown Digital Twin Option Hidden
    [Documentation]     Confirm that the Actions > Shutdown Digital Twin is hidden.

    ${action_menu}=    Is Actions Shutdown Digital Twin Visible
    Should Be Equal As Integers                             ${action_menu}   -1

Confirm D360 Digital Twin Status
    [Documentation]     Confirm that the digital twin device status is disconnected within the Device360 view.
    [Arguments]         ${expected_status}

    ${status}=   Get Device360 Digital Twin Device Status
    Should Be Equal As Strings                              ${status}    ${expected_status}

Confirm D360 Relaunch Digital Twin Option Visible
    [Documentation]     Confirm that the D360 "Relaunch Digital Twin" button is visible.

    ${dt_button}=  Is Device360 Relaunch Digital Twin Button Visible
    Should Be Equal As Integers                             ${dt_button}    1

Confirm D360 Relaunch Digital Twin Option Hidden
    [Documentation]     Confirm that the D360 "Relaunch Digital Twin" button is hidden.

    ${dt_button}=  Is Device360 Relaunch Digital Twin Button Visible
    Should Be Equal As Integers                             ${dt_button}    -1

Confirm D360 Shutdown Digital Twin Option Visible
    [Documentation]     Confirm that the D360 "Shutdown Digital Twin" button is visible.

    ${dt_button}=  Is Device360 Shutdown Digital Twin Button Visible
    Should Be Equal As Integers                             ${dt_button}    1

Confirm D360 Shutdown Digital Twin Button Hidden
    [Documentation]     Confirm that the D360 "Shutdown Digital Twin" button is hidden.

    ${dt_button}=  Is Device360 Shutdown Digital Twin Button Visible
    Should Be Equal As Integers                             ${dt_button}    -1
