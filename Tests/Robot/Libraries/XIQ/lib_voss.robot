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
    Log To Console          Command results are ${reset_results}
    ${confirm_reset}=       Send  ${spawn}  y
    Log To Console          Command results are ${confirm_reset}

    sleep                   ${SWITCH_REBOOT_WAIT}

    [Teardown]              Close VOSS Spawn and Confirm Success  ${spawn}

Configure iqagent for VOSS Switch
    [Documentation]     Configures the iqagent for the VOSS switch
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${iqagent}

    ${spawn}=           Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss

    ${conf_results}=    Send Commands  ${spawn}
    ...  enable, configure terminal, application, no iqagent enable, iqagent server ${iqagent}, iqagent enable
    Log To Console      Configure results are ${conf_results}
    Should Contain      ${conf_results}  ${iqagent}
    ${save_results}=    Send  ${spawn}  save config
    Log To Console      Save results are ${save_results}
    Should Contain      ${save_results}  Save config successful

    sleep               ${CLIENT_CONNECT_WAIT}

    ${check_results}=   Send  ${spawn}  show application iqagent
    Log To Console      Command results are ${check_results}
    Should Contain      ${check_results}  ${iqagent}

    [Teardown]          Close VOSS Spawn and Confirm Success  ${spawn}

Disable iqagent for VOSS Switch
    [Documentation]     Disables the iqagent for the VOSS switch
    [Tags]              voss
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}

    ${spawn}=               Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss
    ${results}=             Send Commands  ${spawn}  enable, configure terminal, application, no iqagent enable
    Log To Console          Command results are ${results}
    sleep                   ${CLIENT_DISCONNECT_WAIT}

    ${iqagent_results}=     Send  ${spawn}  show application iqagent
    Log To Console          Command results are ${iqagent_results}
    Should Contain          ${iqagent_results}  disconnected

    [Teardown]              Close VOSS Spawn and Confirm Success  ${spawn}

Enable iqagent for VOSS Switch
    [Documentation]     Enables the iqagent for the VOSS switch
    [Tags]              voss
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}

    ${spawn}=               Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss
    ${results}=             Send Commands  ${spawn}  enable, configure terminal, application, iqagent enable
    Log To Console          Command results are ${results}
    ${save_results}=        Send  ${spawn}  save config
    Log To Console          Save results are ${save_results}
    Should Contain          ${save_results}  Save config successful

    sleep                   ${CLIENT_CONNECT_WAIT}

    ${iqagent_results}=     Send  ${spawn}  show application iqagent
    Log To Console          Command results are ${iqagent_results}
    Should Not Contain      ${iqagent_results}  disconnected

    [Teardown]              Close VOSS Spawn and Confirm Success  ${spawn}

Update NOS Version on VOSS Switch
    [Documentation]     Updates the NOS version on the VOSS switch to the specified version
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${nos_dir}

    ${spawn}=            Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss

    # Confirm the version we want to activate is present
    ${results}=          Send Commands  ${spawn}  enable, cd release, ls
    Log To Console       Command results are ${results}
    Should Contain       ${results}  ${nos_dir}

    # Activate the NOS version
    ${update_results}=   Send  ${spawn}  software activate ${nos_dir}
    Log To Console       Command results are ${update_results}

    # Reboot the switch
    ${reset_results}=    Send  ${spawn}  reset -Y
    Log To Console       Command results are ${reset_results}

    Close VOSS Spawn and Confirm Success  ${spawn}
    sleep                ${SWITCH_REBOOT_WAIT}

    ${spawn}=            Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss

    # Commit the changes
    ${commit_results}=   Send Commands  ${spawn}  enable, software commit
    Log To Console       Command results are ${commit_results}
    Should Contain Any   ${commit_results}  Software commit successful  has already been committed

    [Teardown]  Close VOSS Spawn and Confirm Success  ${spawn}

Downgrade IQAgent on VOSS Switch
    [Documentation]     Downgrades the IQAgent version on the VOSS switch to an older version
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}

    ${spawn}=          Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss

    ${results}=        Send Commands  ${spawn}  dbg enable, configure terminal, application, no iqagent enable, software iqagent reinstall, iqagent enable
    Log To Console     Command results are ${results}
    Should Contain     ${results}  Reinstalling IQAgent from VOSS image

    ${check_results}=  Send  ${spawn}  show application iqagent
    Log To Console     Command results are ${check_results}
    Should Contain     ${check_results}  ${IQAGENT_VERSION_OLD}

    [Teardown]  Close VOSS Spawn and Confirm Success  ${spawn}

Confirm NOS Version on VOSS Switch
    [Documentation]     Confirms the NOS version on the VOSS switch is at the specified version
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${nos_version}

    ${spawn}=       Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss

    ${results}=     Send  ${spawn}  show sys software
    Log To Console  Command results are ${results}
    Should Contain  ${results}  ${nos_version}

    [Teardown]  Close VOSS Spawn and Confirm Success  ${spawn}

Confirm IQAgent Version on VOSS Switch
    [Documentation]     Confirma the IQAgent on the VOSS switch is at the expected version
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${iqa_version}

    ${spawn}=       Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss

    ${result}=      Send  ${spawn}  show application iqagent
    Log To Console  Command results are ${result}
    Should Contain  ${result}  ${iqa_version}

    [Teardown]  Close VOSS Spawn and Confirm Success  ${spawn}

Disable Port for VOSS Switch
    [Documentation]     Disables the specified port for the VOSS switch
    [Tags]              voss
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${test_port}

    ${spawn}=           Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss
    Send Commands       ${spawn}  enable, configure terminal, interface gigabitEthernet ${test_port}, shutdown

    ${results}=         Send Commands  ${spawn}  show interface gigabitEthernet state ${test_port}
    Log To Console      Command results are ${results}
    Should Contain      ${results}  down

    [Teardown]          Close VOSS Spawn and Confirm Success  ${spawn}

Enable Port for VOSS Switch
    [Documentation]     Enables the specified port for the VOSS switch
    [Tags]              voss
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${test_port}

    ${spawn}=           Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss
    Send Commands       ${spawn}  enable, configure terminal, interface gigabitEthernet ${test_port}, no shutdown

    ${results}=         Send Commands  ${spawn}  show interface gigabitEthernet state ${test_port}
    Log To Console      Command results are ${results}
    Should Contain      ${results}  up

    [Teardown]          Close VOSS Spawn and Confirm Success  ${spawn}

Close VOSS Spawn and Confirm Success
    [Documentation]     This is a local keyword to close the VOSS spawn and confirm the action was successful.
    [Arguments]         ${spawn}

    ${result}=  Close Spawn  ${spawn}
    Should Not Be Equal As Integers  ${result}  -1
