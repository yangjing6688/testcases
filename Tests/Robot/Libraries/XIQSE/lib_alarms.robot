#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to the Alarms tab functionality.
#

*** Settings ***
Library     xiqse/flows/alarms_events/alarms/XIQSE_AlarmsEventsAlarms.py
Library     xiqse/flows/common/XIQSE_CommonNavigator.py


*** Keywords ***
Navigate to Alarms and Confirm Success
    [Documentation]     Navigates to the Alarms & Events> Events view in XIQ-SE and confirms the action was successful

    ${nav_result}=  XIQSE Navigate to Alarms Tab
    Should Be Equal As Integers         ${nav_result}     1

Set Alarms Search String and Confirm Success
    [Documentation]     Sets the search string on the Alarms tab
    [Arguments]         ${value}

    ${result}=  XIQSE Alarms Perform Search  ${value}
    Should Be Equal As Integers  ${result}      1

Clear Alarms Search String and Confirm Success
    [Documentation]     Clears the search string on the Alarms tab

    ${result}=  XIQSE Alarms Clear Search
    Should Be Equal As Integers  ${result}      1

Confirm Alarms Row Contains Text
    [Documentation]     Confirms the specified text exists within a row of the Alarms tab
    [Arguments]         ${value}

    ${result}=  XIQSE Find Alarm With Text      ${value}
    Should Be Equal As Integers  ${result}      1

Confirm Alarms Row Does Not Contain Text
    [Documentation]     Confirms the specified text exists within a row of the Alarms tab
    [Arguments]         ${value}

    ${result}=  XIQSE Find Alarm With Text      ${value}
    Should Be Equal As Integers  ${result}      -1
