#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords which perform common workflows (that is, putting together groups of common keywords to
# perform multiple common steps).
#

*** Settings ***


*** Keywords ***
Confirm Serial Number and Set Common Options
    [Documentation]     Confirms the serial number is correct and sets up common options used for XIQSE automation tests
    [Arguments]  ${serial}

    # Make sure the expected Serial Number is being reported
    Confirm XIQSE Serial Number     ${serial}

    # Make sure sharing with XIQ is enabled
    Enable XIQ Connection Sharing and Confirm Success

    # Set the HTTP session timeout
    Set Option Web Server Session Timeout and Confirm Success  7  day(s)

    # Set the Device Tree to display by IP Address
    Set Option Device Tree Name Format and Confirm Success   IP Address

Onboard XIQSE To XIQ If In Connected Mode
    [Documentation]     If XIQSE is running in connected mode, it is onboarded to XIQ
    [Arguments]         ${xiqse_mode}  ${xiqse_ip}  ${xiq_email}  ${xiq_password}

    Run Keyword If  'CONNECTED' in '${xiqse_mode}'
    ...     Run Keywords
    ...         Navigate to XIQ Device Message Details and Confirm Success
    ...         AND
    ...         Onboard XIQSE if Not Onboarded    ${xiqse_ip}  ${xiq_email}  ${xiq_password}
    ...         AND
    ...         Confirm XIQSE Onboarded Successfully    ${xiqse_ip}
    ...     ELSE
    ...     Log To Console  This is an AirGap deployment so no need to onboard XIQSE to XIQ

Remove XIQSE From XIQ If In Connected Mode
    [Documentation]     If XIQSE is runing in connected mode, it is removed from XIQ
    [Arguments]         ${xiqse_mode}  ${xiq_email}  ${xiq_password}  ${xiq_url}  ${xiqse_mac}

    Run Keyword If  'CONNECTED' in '${xiqse_mode}'
    ...     Run Keywords
    ...         Log Into XIQ and Confirm Success  ${xiq_email}  ${xiq_password}  url=${xiq_url}
    ...         AND
    ...         Navigate and Remove Device by MAC From XIQ    ${xiqse_mac}
    ...         AND
    ...         Log Out of XIQ and Quit Browser
    ...     ELSE
    ...     Log To Console  This is an AirGap deployment so no need to remove XIQSE from XIQ