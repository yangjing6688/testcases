#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to Device360 functionality.
#

*** Settings ***
Library     xiq/flows/common/Login.py
Library     xiq/flows/common/Navigator.py
Library     xiq/flows/manage/Device360.py

*** Keywords ***
Open Device360 Using MAC And Confirm Success
    [Documentation]     Open the Device360 view for the specified device MAC Address.
    [Arguments]         ${mac_address}

    ${nav_result}=  Navigate To Device360 Page With MAC     ${mac_address}
    Should Be Equal As Integers  ${nav_result}  1

Close Device360 And Refresh Devices Page
    [Documentation]     Close the Device360 panel and Refresh the Manage > Devices page.

    Close Device360 Window

    Refresh Page
