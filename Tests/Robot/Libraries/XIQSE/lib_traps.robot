#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to Traps functionality.
#

*** Settings ***


*** Keywords ***
Navigate and Register Trap Receiver
    [Documentation]     Navigates to the Devices tab and registers the trap receiver on the specified device, confirming it was registered
    [Arguments]         ${device_ip}

    Navigate to Devices and Confirm Success
    Register Trap Receiver and Confirm Success              ${device_ip}

Register Trap Receiver and Confirm Success
    [Documentation]     Navigates to the Devices tab and registers the trap receiver on the specified device, confirming it was registered
    [Arguments]         ${device_ip}

    ${confirm_result}=  XIQSE Register Trap Receiver             ${device_ip}
    Should Be Equal As Integers                                 ${confirm_result}     1

    ${wait_result}=  XIQSE Operations Wait Until Operation Complete    Trap Configuration
    Should Be Equal As Integers         ${wait_result}  1

Navigate and Unregister Trap Receiver
    [Documentation]     Navigates to the Devices tab and unregisters the trap receiver on the specified device, confirming it was unregistered
    [Arguments]         ${device_ip}

    Navigate to Devices and Confirm Success
    Unregister Trap Receiver and Confirm Success                ${device_ip}

Unregister Trap Receiver and Confirm Success
    [Documentation]     Unregisters the trap receiver on the specified device, confirming it was unregistered
    [Arguments]         ${device_ip}

    ${confirm_result}=  XIQSE Unregister Trap Receiver        ${device_ip}
    Should Be Equal As Integers                               ${confirm_result}     1

    ${wait_result}=  XIQSE Operations Wait Until Operation Complete    Trap Configuration
    Should Be Equal As Integers         ${wait_result}  1
