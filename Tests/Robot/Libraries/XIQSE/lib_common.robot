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
