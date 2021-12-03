#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to the basic Operations panel functionality.
#

*** Settings ***
Library     xiqse/flows/common/XIQSE_CommonOperationsPanel.py


*** Keywords ***
Open Operations Panel and Confirm Success
    [Documentation]     Opens the Operations panel and confirms the action was successful

    ${result}=  XIQSE Open Operations Panel
    Should Be Equal As Integers  ${result}  1

Close Operations Panel and Confirm Success
    [Documentation]     Closes the Operations panel and confirms the action was successful

    ${result}=  XIQSE Close Operations Panel
    Should Be Equal As Integers  ${result}  1

Clear Operations Panel and Confirm Success
    [Documentation]     Clears the contents of the Operations panel and confirms the action was successful

    Wait Until Keyword Succeeds  5x  2s  Clear Operations Panel and Check Result

Clear Operations Panel and Check Result
    [Documentation]     Clears the contents of the Operations panel and checks for success

    ${result}=  XIQSE Clear Operations Panel
    Should Be Equal As Integers  ${result}  1

Get Discovered Device Count From Operations Panel
    [Documentation]     Returns the number of discovered devices

    ${device_count}=  XIQSE Operations Get Discovered Device Count

    [Return]  ${device_count}

Confirm Discovered Device Count From Operations Panel
    [Documentation]     Confirms the number of discovered devices reported in the Operations paenl is the expected value
    [Arguments]         ${expected}

    ${device_count}=  Get Discovered Device Count From Operations Panel
    Should Be Equal As Integers  ${device_count}  ${expected}

Wait For Operations Panel Operation To Complete
    [Documentation]     Waits until the specified operation in the Operations Panel is marked as completed
    [Arguments]         ${op_type}

    ${results}=  XIQSE Operations Wait Until Operation Complete     ${op_type}
    Should Be Equal As Integers        ${results}    1

Confirm Operations Panel Message For Type
    [Documentation]     Confirms the message for the specified type in the Operations Panel contains the expected text
    [Arguments]         ${op_type}  ${the_message}

    ${results}=  XIQSE Confirm Operations Panel Message For Type      ${op_type}  ${the_message}
    Should Be Equal As Integers        ${results}    1

Confirm Operations Panel is Empty
    [Documentation]     Confirms the Operations Panel is empty

    ${result}=  XIQSE Confirm Operations Panel is Empty
    Should Be Equal As Integers  ${result}  1
