#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to SysLog functionality.
#

*** Settings ***


*** Keywords ***
Navigate and Register Syslog Receiver
    [Documentation]     Navigates to the Devices tab and registers the syslog receiver on the specified device, confirming it was registered
    [Arguments]         ${device_ip}

    Navigate to Devices and Confirm Success
    Register Syslog Receiver and Confirm Success                ${device_ip}

Register Syslog Receiver and Confirm Success
    [Documentation]     Navigates to the Devices tab and registers the syslog receiver on the specified device, confirming it was registered
    [Arguments]         ${device_ip}

    ${confirm_result}=  XIQSE Register Syslog Receiver           ${device_ip}
    Should Be Equal As Integers                                 ${confirm_result}     1

    ${wait_result}=  XIQSE Operations Wait Until Operation Complete    Syslog Configuration
    Should Be Equal As Integers         ${wait_result}  1

Navigate and Unregister Syslog Receiver
    [Documentation]     Navigates to the Devices tab and unregisters the syslog receiver on the specified device, confirming it was unregistered
    [Arguments]         ${device_ip}

    Navigate to Devices and Confirm Success
    Unregister Syslog Receiver and Confirm Success              ${device_ip}

Unregister Syslog Receiver and Confirm Success
    [Documentation]     Unregisters the syslog receiver on the specified device, confirming it was unregistered
    [Arguments]         ${device_ip}

    ${confirm_result}=  XIQSE Unregister Syslog Receiver      ${device_ip}
    Should Be Equal As Integers                               ${confirm_result}     1

    ${wait_result}=  XIQSE Operations Wait Until Operation Complete    Syslog Configuration
    Should Be Equal As Integers         ${wait_result}  1
