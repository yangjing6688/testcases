# Author        : Heidi S. White
# Description   : Test Suite for sanity testing of the VOSS switch:
#                   - resets VOSS switch to factory defaults
#                   - configures iqagent for VOSS switch
#                   - onboards VOSS switch with policy and location specified
#                   - confirms correct column values in the Devices view
#                   - confirms VOSS switch is successully connected to iqagent
#                   - performs a device update
#                   - confirms Device 360 view has correct data
#                   - enables SSH proxy to the VOSS switch
#                   - confirms connecting to the VOSS switch via SSH is successful
#                 This is qTest test case TC-51558.

*** Settings ***
Library     Collections
Library     common/Cli.py
Library     xiq/flows/common/Login.py
Library     xiq/flows/common/Navigator.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/configure/ExpressNetworkPolicies.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/SwitchTemplate.py
Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/manage/Device360.py
Library     xiq/flows/manage/Devices.py
Library     common/TestFlow.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml

Force Tags   testbed_1_node

Suite Setup      Log Into XIQ and Set Up Test
Suite Teardown   Tear Down Test and Close Session


*** Variables ***
${TESTBED}                  slm_tb_1
${TOPO}                     topo-1
${DEVICE}                   ${netelem1.model}
${ENTRY_TYPE}               Manual
# Please do not change the DUT variables - if you have AP1/SW1-prefixed variables in your device file,
# just edit your device file, copy/paste those AP1/SW1 variables, and change the prefix to DEVICE.
${DUT_SERIAL}               ${netelem1.serial}
${DUT_NAME}                 ${netelem1.name}
${DUT_MODEL}                ${netelem1.model}
${DUT_MAC}                  ${netelem1.mac}
${DUT_CONSOLE_IP}           ${netelem1.ip}
${DUT_CONSOLE_PORT}         ${netelem1.port}
${DUT_USERNAME}             ${netelem1.username}
${DUT_PASSWORD}             ${netelem1.password}
${DUT_PLATFORM}             ${netelem1.platform}
${DUT_TYPE}                 ${netelem1.make}
${DUT_CONNECTION_METHOD}    ${netelem1.connection_method}

${STATUS_BEFORE_UPDATE}     config audit mismatch
${STATUS_AFTER_UPDATE}      green
${LOCATION}                 auto_location_01, Santa Clara, building_02, floor_04
${LOCATION_DISPLAY}         auto_location_01 >> Santa Clara >> building_02 >> floor_04
${FLOOR}                    floor_04
${POLICY_NAME}              VOSS_POLICY_AUTO
${SSID_NAME}                VOSS_SSID_AUTO
${TEMPLATE_NAME}            VOSS_TEMPLATE_AUTO


*** Test Cases ***
TCCS-7299_Step1: Configure VOSS Switch
    [Documentation]     Resets the VOSS switch to the factory defaults and configures the IQ agent on he VOSS switch

    [Tags]              production      tccs_7299       tccs_7299_step1

    Reset VOSS Switch to Factory Defaults       ${DUT_CONSOLE_IP}  ${DUT_CONSOLE_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}  ${DUT_CONNECTION_METHOD}
    Configure iqagent for VOSS Switch           ${DUT_CONSOLE_IP}  ${DUT_CONSOLE_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}  ${sw_capwap_url}   ${DUT_CONNECTION_METHOD}

TCCS-7299_Step2: Onboard VOSS Device With Policy and Location Set Using Quick Add
    [Documentation]     Confirms a VOSS switch can be onboarded with policy and location set via the Quick Add workflow

    [Tags]              production      tccs_7299       tccs_7299_step2

    Depends On          TCCS-7299_Step1
    Onboard New Test Device                     ${DUT_SERIAL}  ${POLICY_NAME}  ${LOCATION}

TCCS-7299_Step3: Confirm VOSS Device Values After Onboard
    [Documentation]     Confirms the VOSS switch has the expected values in the Devices table after onboard

    [Tags]              production      tccs_7299       tccs_7299_step3

    Navigate to Devices and Confirm Success
    Refresh Devices Page

    Depends On          TCCS-7299_Step2

    &{device_info}=     Get Device Row Values  ${DUT_SERIAL}  POLICY,LOCATION,SERIAL,MODEL
    ${policy_result}=   Get From Dictionary     ${device_info}  POLICY
    Should Be Equal     ${policy_result}        ${POLICY_NAME}

    ${loc_result}=      Get From Dictionary     ${device_info}  LOCATION
    Should Be Equal     ${loc_result}           ${LOCATION_DISPLAY}

    ${serial_result}=   Get From Dictionary     ${device_info}  SERIAL
    Should Be Equal     ${serial_result}        ${DUT_SERIAL}

    ${model_result}=    Get From Dictionary     ${device_info}  MODEL
    Should Be Equal     ${model_result}         ${DUT_MODEL}

TCCS-7299_Step4: Confirm iqagent for VOSS Switch is Connected to XIQ After Onboard
    [Documentation]     Confirms the iqagent for the VOSS switch is connected to XIQ

    [Tags]              production      tccs_7299       tccs_7299_step4

    Depends On          TCCS-7299_Step3

    Confirm iqagent for VOSS Switch is Connected to XIQ     ${DUT_CONSOLE_IP}  ${DUT_CONSOLE_PORT}
    ...                                                     ${DUT_USERNAME}  ${DUT_PASSWORD}  ${sw_capwap_url}  ${DUT_CONNECTION_METHOD}

TCCS-7299_Step5: Perform Device Update on VOSS Switch
    [Documentation]     Performs a device update on the VOSS switch
    [Tags]              production      tccs_7299       tccs_7299_step5

    Depends On          TCCS-7299_Step4

    ${result}=  Update Switch Policy and Configuration    ${DUT_SERIAL}
    Should Be Equal As Integers     ${result}     1

TCCS-7299_Step6: Confirm VOSS Device Values After Update
    [Documentation]     Confirms the device table contains expected values for the VOSS switch after an update

    [Tags]              production      tccs_7299       tccs_7299_step6

    Depends On          TCCS-7299_Step5

    Refresh Devices Page
    Confirm Device Status   ${DUT_SERIAL}  ${STATUS_AFTER_UPDATE}

    &{device_info}=     Get Device Row Values  ${DUT_SERIAL}  POLICY,LOCATION,SERIAL,MODEL

    ${policy_result}=   Get From Dictionary     ${device_info}  POLICY
    Should Be Equal     ${policy_result}        ${POLICY_NAME}

    ${loc_result}=      Get From Dictionary     ${device_info}  LOCATION
    Should Be Equal     ${loc_result}           ${LOCATION_DISPLAY}

    ${serial_result}=   Get From Dictionary     ${device_info}  SERIAL
    Should Be Equal     ${serial_result}        ${DUT_SERIAL}

    ${model_result}=    Get From Dictionary     ${device_info}  MODEL
    Should Be Equal     ${model_result}         ${DUT_MODEL}

TCCS-7299_Step7: Confirm Device360 View Values for VOSS Switch
    [Documentation]     Confirms the Device360 view contains correct values for the VOSS Switch

    [Tags]              production      tccs_7299       tccs_7299_step7

    Depends On          TCCS-7299_Step6

    Refresh Devices Page
    &{overview_info}=           Get VOSS Device360 Overview Information                 ${DUT_MAC}

    Refresh Devices Page
    &{device_config_info}=      Get VOSS Device360 Device Configuration Information     ${DUT_MAC}

    ${overview_serial}=         Get From Dictionary  ${overview_info}  serial_number
    Should Be Equal             ${overview_serial}  ${DUT_SERIAL}

    ${overview_model}=          Get From Dictionary  ${overview_info}  device_model
    Should Be Equal             ${overview_model}  ${DUT_MODEL}

    ${overview_policy}=         Get From Dictionary  ${overview_info}  network_policy
    Should Be Equal             ${overview_policy}  ${POLICY_NAME}

    ${config_policy}=           Get From Dictionary  ${device_config_info}  network_policy
    Should Be Equal             ${config_policy}  ${POLICY_NAME}

    ${config_template}=         Get From Dictionary  ${device_config_info}  device_template
    Should Be Equal             ${config_template}  ${TEMPLATE_NAME}

TCCS-7299_Step8: Enable SSH on VOSS Switch and Confirm SSH Session Can Be Established
    [Documentation]     Enables SSH for the VOSS Switch

    [Tags]              production      tccs_7299       tccs_7299_step8

    Depends On          TCCS-7299_Step7

    &{ip_port_info}=                    Device360 Enable SSH CLI Connectivity   ${DUT_MAC}

    ${ip}=                              Get From Dictionary  ${ip_port_info}  ip
    ${port}=                            Get From Dictionary  ${ip_port_info}  port

    ${ssh_spawn}=                       Open pxssh Spawn    ${ip}  ${DUT_USERNAME}  ${DUT_PASSWORD}  ${port}
    Should Not Be Equal As strings      '${ssh_spawn}'      '-1'

    ${cmd_result}=                      Send pxssh  ${ssh_spawn}  show sys-info | include Serial
    Log To Console                      SSH Command Result Is ${cmd_result}

    ${close_result}=                    Close pxssh Spawn  ${ssh_spawn}
    Should Not Be Equal As strings      '${close_result}'    '-1'

    [Teardown]  Disable SSH and Close Device360 Window

*** Keywords ***
Log Into XIQ and Set Up Test
    [Documentation]     Logs into XIQ and sets up the elements necessary to complete this test suite

    Log Into XIQ and Confirm Success
    ${ENABLE_SSH}=                      Enable SSH Availability
    Should Be Equal As Integers         ${ENABLE_SSH}       1

    # If the test device has already been onboarded, delete it
    Navigate to Devices and Confirm Success

    ${search_result}=  Search Device Serial   ${DUT_SERIAL}
    Run Keyword If  '${search_result}' == '1'    Delete Device  ${DUT_SERIAL}

    # Create the policy for the test
    Create Open Policy For Switch           ${POLICY_NAME}  ${SSID_NAME}  ${DUT_MODEL}  ${TEMPLATE_NAME}

Tear Down Test and Close Session
    [Documentation]     Cleans up test data, logs out of XIQ, and closes the browser

    Clean Up Test Device and Confirm Success    ${DUT_SERIAL}
    Clean Up Open Policy For Switch             ${POLICY_NAME}  ${SSID_NAME}  ${TEMPLATE_NAME}
    Log Out of XIQ and Confirm Success
    [Teardown]   run keywords       quit browser

Disable SSH and Close Device360 Window
    ${DISABLE_SSH}=                     Device360 Disable SSH Connectivity
    Should Be Equal As Integers         ${DISABLE_SSH}     1

    ${CLOSE_DEVICE360_WINDOW}=          Close Device360 Window
    Should Be Equal As Integers         ${CLOSE_DEVICE360_WINDOW}     1

# The following keywords are helper keywords for this test
## common keywords
Log Into XIQ and Confirm Success
    [Documentation]     Logs into XIQ and confirms the login was successful

    ${LOGIN_STATUS}=              Login User          ${tenant_username}      ${tenant_password}     check_warning_msg=True
    should be equal as integers             ${LOGIN_STATUS}               1

Log Out of XIQ and Confirm Success
    [Documentation]     Logs out of XIQ and confirms the logout was successful

    ${LOGOUT_STATUS}=      Logout User
    Should Be Equal As Integers     ${LOGOUT_STATUS}     1

Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Manage> Devices view and confirms the action was successful

    ${nav_result}=  Navigate to Devices
    Should Be Equal As Integers  ${nav_result}  1

Onboard New Test Device
    [Documentation]     Onboards the specified test device, deleting it first if it already exists
    [Arguments]         ${serial}  ${policy}  ${location}

    Navigate to Devices and Confirm Success

    # If the device has already been onboarded, delete it first
    ${search_result}=  Search Device Serial   ${serial}
    Run Keyword If  '${search_result}' == '1'    Delete Device  ${serial}

    ${search_result}=  Search Device Serial   ${serial}

    # Onboard the device
    ${ONBOARD_RESULT}=      Onboard Device          ${serial}         device_make=${DUT_TYPE}       location=${location}
    Should Be Equal As Integers                     ${ONBOARD_RESULT}           1

    ${voss_result}=  Wait Until Device Online        ${serial}
    Should Be Equal As Integers                     ${voss_result}       1

    ${device_managed_result}=    WAIT UNTIL DEVICE MANAGED       ${serial}           MANAGED
    Should Be Equal As Integers                 ${device_managed_result}       1

    Confirm Device Status   ${serial}  ${STATUS_AFTER_UPDATE}

    # Confirm the device was added successfully
    ${search_result}=  Search Device Serial  ${serial}
    Should Be Equal As Integers  ${search_result}  1

Confirm Device Status
    [Documentation]     Checks the status of the specified device and confirms it matches the expected value
    [Arguments]         ${serial}  ${expected_status}

    ${device_status}=       Get Device Status       device_serial=${serial}
    Should Contain          ${device_status}   ${expected_status}

Clean Up Test Device and Confirm Success
    [Documentation]     Deletes the specified device and confirms the action was successful
    [Arguments]         ${serial}

    Navigate to Devices and Confirm Success
    ${del_result}=  Delete Device   ${serial}
    Should Be Equal As Integers     ${del_result}  1

## switch keywords
Reset VOSS Switch to Factory Defaults
    [Documentation]     Resets the VOSS switch to the factory defaults by remcoving the config.cfg file and resetting the device
    [Tags]              voss
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${connection_method}

    ${spawn}=               Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss   ${connection_method}

    ${remove_results}=                  Send  ${spawn}  remove config.cfg     confirmation_phrases=Are you sure (y/n) ?    confirmation_arg=y
    Log To Console                      Command results are ${remove_results}

    ${reset_results}=                   Send  ${spawn}  reset     confirmation_phrases=Are you sure you want to reset the switch (y/n) ?   confirmation_arg=y
    Log To Console                      Command results are ${remove_results}

    sleep                   ${switch_reboot_wait}

    [Teardown]              Close Spawn  ${spawn}

Configure iqagent for VOSS Switch
    [Documentation]     Configures the iqagent for the VOSS switch
    [Tags]              voss
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${iqagent}  ${connection_method}


    ${spawn}=               Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss  ${connection_method}

    ${reset_iq_agent}=      Send Commands  ${spawn}  enable, configure terminal, show application iqagent, application, no iqagent enable, software iqagent reinstall , iqagent enable, show application iqagent , end
    Log To Console          Command results are ${reset_iq_agent}

    ${conf_results}=        Send Commands  ${spawn}  enable, configure terminal, application, no iqagent enable, iqagent server ${iqagent}, iqagent enable
        Log To Console          Command results are ${conf_results}

    Should Contain          ${conf_results}  ${iqagent}
    sleep                   ${client_connect_wait}

    ${check_results}=       Send  ${spawn}  show application iqagent
    Log To Console          Command results are ${check_results}
    Should Contain          ${check_results}  ${iqagent}

    [Teardown]              Close Spawn  ${spawn}

Confirm iqagent for VOSS Switch is Connected to XIQ
    [Documentation]     Confirms the iqagent for the VOSS switch is connected to XIQ
    [Tags]              voss
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${iqagent}  ${connection_method}

    ${spawn}=               Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  voss  ${connection_method}

    ${iqagent_results}=     Send                ${spawn}         show application iqagent
    Log To Console          Command results are ${iqagent_results}
    Should Contain          ${iqagent_results}      connected

    [Teardown]              Close Spawn  ${spawn}

Create Open Policy For Switch
    [Documentation]     Creates an open policy using the express method, and attaches a switch template
    [Tags]              switch  voss
    [Arguments]         ${policy}  ${ssid}  ${template_model}  ${template_name}

    # If the policy has already been created, delete it first
    Clean Up Open Policy For Switch                             ${POLICY_NAME}  ${SSID_NAME}  ${TEMPLATE_NAME}

    ${create_result}=  Create Open Auth Express Network Policy  ${policy}  ${ssid}
    Should Be Equal As Integers                                 ${create_result}  1

    ${tpl_result}=  Add Sw Template                             ${policy}  ${template_model}  ${template_name}
    Should Be Equal As Integers                                 ${tpl_result}  1

Clean Up Open Policy For Switch
    [Documentation]     Deletes the policy, SSID, and switch template
    [Tags]              switch  voss
    [Arguments]         ${policy}  ${ssid}  ${switch_template}

    ${DLT_NW_POLICY}=               Delete Network Policy                   ${policy}
    should be equal as integers     ${DLT_NW_POLICY}            1

    ${DELETE_SSID}=                 Delete SSID                             ${ssid}
    should be equal as integers     ${DELETE_SSID}              1

    ${DELETE_SWITCH_TEMPLATE}=      Delete Switch Template                  ${switch_template}
    should be equal as integers     ${DELETE_SWITCH_TEMPLATE}   1

