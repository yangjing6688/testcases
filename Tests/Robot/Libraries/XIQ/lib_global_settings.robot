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
