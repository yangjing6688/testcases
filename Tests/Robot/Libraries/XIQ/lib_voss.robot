#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to VOSS functionality.
#

*** Settings ***
Library          common/Cli.py


*** Keywords ***
Reset VOSS Switch to Factory Defaults
    [Documentation]     Resets the VOSS switch to the factory defaults by remcoving the config.cfg file and resetting the device
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}

    ${spawn}=               Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss

    ${enable_results}=      Send  ${spawn}  enable
    Log To Console          Command results are ${enable_results}
    ${remove_results}=      Send  ${spawn}  remove config.cfg     expect_match=Are you sure (y/n) ?
    Log To Console          Command results are ${remove_results}
    ${confirm_remove}=      Send  ${spawn}  y
    Log To Console          Command results are ${confirm_remove}

    ${reset_results}=       Send  ${spawn}  reset     expect_match=Are you sure you want to reset the switch (y/n) ?
    Log To Console          Command results are ${remove_results}
    ${confirm_reset}=       Send  ${spawn}  y
    Log To Console          Command results are ${confirm_reset}

    sleep                   ${SWITCH_REBOOT_WAIT}

    [Teardown]              Close Spawn  ${spawn}

Configure iqagent for VOSS Switch
    [Documentation]     Configures the iqagent for the VOSS switch
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${iqagent}

    ${spawn}=           Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss

    ${conf_results}=    Send Commands  ${spawn}  enable, configure terminal, application, no iqagent enable, iqagent server ${iqagent}, iqagent enable
    Log To Console      Command results are ${conf_results}
    Should Contain      ${conf_results}  ${iqagent}

    sleep               ${CLIENT_CONNECT_WAIT}

    ${check_results}=   Send  ${spawn}  show application iqagent
    Log To Console      Command results are ${check_results}
    Should Contain      ${check_results}  ${iqagent}

    [Teardown]          Close Spawn  ${spawn}

Disable iqagent for VOSS Switch
    [Documentation]     Disables the iqagent for the VOSS switch
    [Tags]              voss
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}

    ${spawn}=               Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss
    Send Commands           ${spawn}  enable, configure terminal, application, no iqagent enable
    sleep                   ${CLIENT_DISCONNECT_WAIT}

    ${iqagent_results}=     Send                ${spawn}         show application iqagent
    Log To Console          Command results are ${iqagent_results}
    Should Contain          ${iqagent_results}      disconnected

    [Teardown]              Close Spawn  ${spawn}

Enable iqagent for VOSS Switch
    [Documentation]     Enables the iqagent for the VOSS switch
    [Tags]              voss
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}

    ${spawn}=               Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss
    Send Commands           ${spawn}  enable, configure terminal, application, iqagent enable
    sleep                   ${CLIENT_CONNECT_WAIT}

    ${iqagent_results}=     Send                ${spawn}         show application iqagent
    Log To Console          Command results are ${iqagent_results}
    Should Not Contain      ${iqagent_results}      disconnected

    [Teardown]              Close Spawn  ${spawn}

Disable Port for VOSS Switch
    [Documentation]     Disables the specified port for the VOSS switch
    [Tags]              voss
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${test_port}

    ${spawn}=           Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss
    Send Commands       ${spawn}  enable, configure terminal, interface gigabitEthernet ${test_port}, shutdown

    ${results}=         Send Commands  ${spawn}  show interface gigabitEthernet state ${test_port}
    Log To Console      Command results are ${results}
    Should Contain      ${results}  down

    [Teardown]          Close Spawn  ${spawn}

Enable Port for VOSS Switch
    [Documentation]     Enables the specified port for the VOSS switch
    [Tags]              voss
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${test_port}

    ${spawn}=           Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss
    Send Commands       ${spawn}  enable, configure terminal, interface gigabitEthernet ${test_port}, no shutdown

    ${results}=         Send Commands  ${spawn}  show interface gigabitEthernet state ${test_port}
    Log To Console      Command results are ${results}
    Should Contain      ${results}  up

    [Teardown]          Close Spawn  ${spawn}
