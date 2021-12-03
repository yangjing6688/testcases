#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to the Events tab functionality.
#

*** Settings ***
Library     xiqse/flows/alarms_events/events/XIQSE_AlarmsEventsEvents.py
Library     xiqse/flows/common/XIQSE_CommonNavigator.py


*** Keywords ***
Navigate to Events and Confirm Success
    [Documentation]     Navigates to the Alarms & Events> Events view in XIQ-SE and confirms the action was successful

    ${nav_result}=  XIQSE Navigate to Events Tab
    Should Be Equal As Integers         ${nav_result}     1

Navigate and Set Event Time Range
    [Documentation]     Navigates to the Events tab and sets the time range
    [Arguments]         ${value}

    Navigate to Events and Confirm Success
    Set Event Time Range and Confirm Success  ${value}

Navigate and Set Event Type
    [Documentation]     Navigates to the Events tab and sets the event type(s) to display
    [Arguments]         ${value}

    Navigate to Events and Confirm Success
    Set Event Type and Confirm Success  ${value}

Set Event Time Range and Confirm Success
    [Documentation]     Sets the time range used on the Events tab (e.g., All, Last Hour, Yesterday, etc.)
    [Arguments]         ${value}

    ${result}=  XIQSE Events Select Time Range  ${value}
    Should Be Equal As Integers  ${result}      1

Set Event Type and Confirm Success
    [Documentation]     Sets the event type(s) to display on the Events tab (comma-separated list of values to select)
    [Arguments]         ${value}

    ${result}=  XIQSE Events Select Type  ${value}
    Should Be Equal As Integers  ${result}      1

Set Event Search String and Confirm Success
    [Documentation]     Sets the search string on the Events tab
    [Arguments]         ${value}

    ${result}=  XIQSE Events Perform Search  ${value}
    Should Be Equal As Integers  ${result}      1

Clear Event Search String and Confirm Success
    [Documentation]     Clears the search string on the Events tab

    ${result}=  XIQSE Events Clear Search
    Should Be Equal As Integers  ${result}      1

Confirm Event Row Contains Text
    [Documentation]     Confirms the specified text exists within a row of the Events tab
    [Arguments]         ${value}

    ${result}=  XIQSE Find Event With Text      ${value}
    Should Be Equal As Integers  ${result}      1

Set Event Filter String and Confirm Success
    [Documentation]     Set a filter for a column on the Events tab
    [Arguments]         ${column}    ${value}

    IF    '${column}' == 'Severity'
    ${set_result}=  XIQSE Table Set Column Filter  ${column}  ${value}    filter_type=Checkbox
    Should Be Equal As Integers  ${set_result}    1
    ELSE
    ${set_result}=  XIQSE Table Set Column Filter    ${column}    ${value}
    Should Be Equal As Integers  ${set_result}    1
    END
    sleep    2 seconds

Clear Event Filter String and Confirm Success
    [Documentation]     Clear a filter for a column on the Events tab
    [Arguments]         ${column}

    ${remove_result}=  XIQSE Table Remove Column Filter  ${column}
    Should Be Equal As Integers  ${remove_result}      1
    sleep    2 seconds
