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
Boot Switch To Known Good Configuration
    [Documentation]     Boots the Test Device to a known good configuration
    [Tags]              voss
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${cli_type}

    ${spawn}=               Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  ${cli_type}

    ${enable_results}=      Send  ${spawn}  enable
    Log To Console          Command results are ${enable_results}

    #Please be aware that this keyword should no longer be used and also you should make sure that you have a good configuration on device named 'config_VOSS.cfg'
    #Instead of this keyword try using the following methods:
    #Connect to all network elements
    #reboot_network_element_with_config      ${dut_name}      ${config_file}
    #close_connection_to_all_network_elements
    ${boot_results}=        Send  ${spawn}  boot config config_VOSS.cfg     confirmation_phrases=Are you sure you want to re-boot the switch (y/n) ?    confirmation_args=y
    Log To Console          Command results are ${boot_results}

    sleep                   ${switch_reboot_wait}

#Please be aware that this keyword should no longer be used
#Instead of this keyword try using the following method: configure_device_to_connect_to_cloud
Configure iqagent for Test Device
    [Documentation]     Configures the iqagent for the Test Device
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${iqagent}

    ${spawn}=           Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss

    ${conf_results}=    Send Commands  ${spawn}
    ...  enable, configure terminal, application, no iqagent enable, iqagent server ${iqagent}, iqagent enable
    Log To Console      Configure results are ${conf_results}
    Should Contain      ${conf_results}  ${iqagent}
    ${save_results}=    Send  ${spawn}  save config
    Log To Console      Save results are ${save_results}
    Should Contain      ${save_results}  successful

    sleep               ${CLIENT_CONNECT_WAIT}

    ${check_results}=   Send  ${spawn}  show application iqagent
    Log To Console      Command results are ${check_results}
    Should Contain      ${check_results}  ${iqagent}

    [Teardown]          Close Spawn and Confirm Success  ${spawn}

#Please be aware that this keyword should no longer be used
#Instead of this keyword try using the following method: hostinformation_disable_iqagent
Disable iqagent for Test Device
    [Documentation]     Disables the iqagent for the Test Device
    [Tags]              voss
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}

    ${spawn}=               Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss
    ${results}=             Send Commands  ${spawn}  enable, configure terminal, application, no iqagent enable
    Log To Console          Command results are ${results}
    sleep                   ${CLIENT_DISCONNECT_WAIT}

    ${iqagent_results}=     Send  ${spawn}  show application iqagent
    Log To Console          Command results are ${iqagent_results}
    Should Contain          ${iqagent_results}  disconnected

    [Teardown]              Close Spawn and Confirm Success  ${spawn}

#Please be aware that this keyword should no longer be used
#Instead of this keyword try using the following method: hostinformation_enable_iqagent
Enable iqagent for Test Device
    [Documentation]     Enables the iqagent for the Test Device
    [Tags]              voss
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}

    ${spawn}=               Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss
    ${results}=             Send Commands  ${spawn}  enable, configure terminal, application, iqagent enable
    Log To Console          Command results are ${results}
    ${save_results}=        Send  ${spawn}  save config
    Log To Console          Save results are ${save_results}
    Should Contain          ${save_results}  successful
    sleep                   ${CLIENT_CONNECT_WAIT}

    ${iqagent_results}=     Send  ${spawn}  show application iqagent
    Log To Console          Command results are ${iqagent_results}
    Should Not Contain      ${iqagent_results}  disconnected

    [Teardown]              Close Spawn and Confirm Success  ${spawn}

#Please be aware that this keyword should no longer be used
#Instead of this keyword try using the following method: Upgrade_VOSS_Network_Element
Update NOS Version on Test Device
    [Documentation]     Updates the NOS version on the Test Device to the specified version
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

    Close Spawn and Confirm Success  ${spawn}
    sleep                ${SWITCH_REBOOT_WAIT}

    ${spawn}=            Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss

    # Commit the changes
    ${commit_results}=   Send Commands  ${spawn}  enable, software commit
    Log To Console       Command results are ${commit_results}
    Should Contain Any   ${commit_results}  Software commit successful  has already been committed

    [Teardown]  Close Spawn and Confirm Success  ${spawn}

#Please be aware that this keyword should no longer be used
#Instead of this keyword try using the following method: Downgrade iqagent
Downgrade IQAgent on Test Device
    [Documentation]     Downgrades the IQAgent version on the Test Device to an older version
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}

    ${spawn}=          Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss

    ${results}=        Send Commands  ${spawn}  dbg enable, configure terminal, application, no iqagent enable, software iqagent reinstall, iqagent enable
    Log To Console     Command results are ${results}
    Should Contain     ${results}  Reinstalling IQAgent from VOSS image

    ${check_results}=  Send  ${spawn}  show application iqagent
    Log To Console     Command results are ${check_results}
    Should Contain     ${check_results}  ${IQAGENT_VERSION_OLD}

    [Teardown]  Close Spawn and Confirm Success  ${spawn}

#Please be aware that this keyword should no longer be used
#Instead of this keyword try using the following methods:
#Connect to all network elements
#hostinformation_verify_host_nos_version      ${dut_name}      ${NOS_VERSION_OLD}
#close_connection_to_all_network_elements
Confirm NOS Version on Test Device
    [Documentation]     Confirms the NOS version on the Test Device is at the specified version
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${nos_version}

    ${spawn}=       Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss

    ${results}=     Send  ${spawn}  show sys software | include Version
    Log To Console  Command results are ${results}
    Should Contain  ${results}  ${nos_version}

    [Teardown]  Close Spawn and Confirm Success  ${spawn}

#Please be aware that this keyword should no longer be used
#Instead of this keyword try using the following methods:
#Connect to all network elements
#hostinformation_verify_iqagent_version      ${dut_name}      ${IQAGENT_VERSION_NEW}
#close_connection_to_all_network_elements
Confirm IQAgent Version on Test Device
    [Documentation]     Confirma the IQAgent on the Test Device is at the expected version
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${iqa_version}

    ${spawn}=       Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss

    ${result}=      Send  ${spawn}  show application iqagent
    Log To Console  Command results are ${result}
    Should Contain  ${result}  ${iqa_version}

    [Teardown]  Close Spawn and Confirm Success  ${spawn}

#Please be aware that this keyword should no longer be used
#Instead of this keyword try using the following method: Disable_Port_and_Validate_Port_is_Disabled
Disable Port for Test Device
    [Documentation]     Disables the specified port for the Test Device
    [Tags]              voss
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${test_port}

    ${spawn}=           Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss
    Send Commands       ${spawn}  enable, configure terminal, interface gigabitEthernet ${test_port}, shutdown

    ${results}=         Send Commands  ${spawn}  show interface gigabitEthernet state ${test_port}
    Log To Console      Command results are ${results}
    Should Contain      ${results}  down

    [Teardown]          Close Spawn and Confirm Success  ${spawn}

#Please be aware that this keyword should no longer be used
#Instead of this keyword try using the following method: Enable_Port_and_Validate_Port_is_Enabled
Enable Port for Test Device
    [Documentation]     Enables the specified port for the Test Device
    [Tags]              voss
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${test_port}

    ${spawn}=           Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss
    Send Commands       ${spawn}  enable, configure terminal, interface gigabitEthernet ${test_port}, no shutdown

    ${results}=         Send Commands  ${spawn}  show interface gigabitEthernet state ${test_port}
    Log To Console      Command results are ${results}
    Should Contain      ${results}  up

    [Teardown]          Close Spawn and Confirm Success  ${spawn}

Close Spawn and Confirm Success
    [Documentation]     This is a local keyword to close the test device spawn and confirm the action was successful.
    [Arguments]         ${spawn}

    ${result}=  Close Spawn  ${spawn}
    Should Not Be Equal As Integers  ${result}  -1
