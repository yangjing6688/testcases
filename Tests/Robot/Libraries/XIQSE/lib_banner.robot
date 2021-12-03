#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to the basic banner message functionality.
#

*** Settings ***
Library     xiqse/flows/common/XIQSE_CommonBanner.py


*** Keywords ***
Confirm License Limit Warning Message Displayed
    [Documentation]     Confirms the License Limit Warning banner message is displayed

    ${result}=  XIQSE Confirm License Limit Warning Message Displayed
    Should Be Equal As Integers  ${result}  1

Confirm License Limit Warning Message Not Displayed
    [Documentation]     Confirms the License Limit Warning banner message is not displayed

    ${result}=  XIQSE Confirm License Limit Warning Message Displayed
    Should Be Equal As Integers  ${result}  -1

Close License Limit Warning Message
    [Documentation]     Closes the License Limit Warning banner message

    ${result}=  XIQSE Close License Limit Warning Message
    Should Be Equal As Integers  ${result}  1

Close All Banner Messages and Confirm Success
    [Documentation]     Closes all banner message panels and confirms the action was successful

    ${result}=  XIQSE Close All Banner Messages
    Should Be Equal As Integers  ${result}  1
