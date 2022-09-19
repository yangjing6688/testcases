#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to Global Settings functionality.
#

*** Settings ***
Library          xiq/flows/globalsettings/GlobalSetting.py


*** Keywords ***
Change Device Password and Confirm Success
    [Documentation]     Updates the default device password and confirms the action was successful
    [Arguments]         ${pwd}

    ${result}=  Change Device Password  ${pwd}
    Should Be Equal As Integers         ${result}  1

Enable CoPilot Feature and Confirm Success
    [Documentation]     Enables CoPilot feature in Global Settings -> VIQ Management and verifies success

    ${result_enable}=    Enable CoPilot Feature For This VIQ
    Should Be Equal As Integers     ${result_enable}     1

Disable CoPilot Feature and Confirm Success
    [Documentation]     Disables CoPilot feature in Global Settings -> VIQ Management and verifies success

    ${result_disable}=    Disable CoPilot Feature For This VIQ
    Should Be Equal As Integers     ${result_disable}     1
