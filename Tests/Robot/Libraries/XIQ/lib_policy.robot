#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to Policy functionality.
#

*** Settings ***
Library          xiq/flows/configure/CommonObjects.py
Library          xiq/flows/configure/ExpressNetworkPolicies.py
Library          xiq/flows/configure/NetworkPolicy.py
Library          xiq/flows/configure/SwitchTemplate.py


*** Keywords ***
Create Open Express Policy and Confirm Success
    [Documentation]     Creates an open policy using the express method and confirms the action was successful
    [Arguments]         ${policy}  ${ssid}

    ${result}=  Create Open Auth Express Network Policy  ${policy}  ${ssid}
    Should Be Equal As Integers  ${result}  1

Create Open Express Policy With Switch Template and Confirm Success
    [Documentation]     Creates an open policy using the express method, and attaches a switch template
    [Arguments]         ${policy}  ${ssid}  ${template_name}

    Create Open Express Policy and Confirm Success  ${policy}  ${ssid}

    ${result}=  Assign Switch Template  ${policy}  ${template_name}
    Should Be Equal As Integers         ${result}  1

Assign Policy to Device and Confirm Success
    [Documentation]     Updates the network policy to the device and confirms the action was successful
    [Arguments]         ${policy}  ${serial}

    ${update_result}=               Update Network Policy To AP  policy_name=${policy}  ap_serial=${serial}
    Should Be Equal As Integers     ${update_result}  1

Delete Policy and Confirm Success
    [Documentation]     Deletes the policy and confirms the action was successful
    [Arguments]         ${policy}

    ${result}=  Delete Network Policy    ${policy}
    Should Be Equal As Integers          ${result}  1

Delete SSID and Confirm Success
    [Documentation]     Deletes the SSID and confirms the action was successful
    [Arguments]         ${ssid}

    ${result}=  Delete SSID      ${ssid}
    Should Be Equal As Integers  ${result}  1
