#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to Firmware functionality.
#

*** Settings ***
Library     extauto/common/Cli.py
Library     xiqse/flows/common/XIQSE_CommonNavigator.py
Library     xiqse/flows/network/XIQSE_Network.py
Library     xiqse/flows/network/devices/devices/XIQSE_NetworkDevicesDevices.py
Library     xiqse/flows/network/devices/devices/XIQSE_NetworkDevicesDevicesUpgradeFirmware.py
Library     xiqse/flows/network/devices/devices/XIQSE_NetworkDevicesDevicesFirmwareSelection.py
Library     xiqse/flows/network/devices/devices/XIQSE_NetworkDevicesDevicesInventorySettings.py


*** Keywords ***
Navigate to Firmware and Confirm Success
    [Documentation]     Navigates to the Network> Firmware view in XIQ-SE and confirms the action was successful

    ${net_result}=  XIQSE Navigate to Network Tab
    Should Be Equal As Integers     ${net_result}     1

    ${fw_result}=  XIQSE Network Select Firmware Tab
    Should Be Equal As Integers     ${fw_result}     1

Open Upgrade Firmware Dialog for Device and Confirm Success
    [Documentation]     Opens the Upgrade Firmware dialog for the specified device
    [Arguments]         ${ip}

    ${result}=  XIQSE Open Upgrade Firmware Dialog  ${ip}
    Should Be Equal As Integers     ${result}     1

Close Upgrade Firmware Dialog and Confirm Success
    [Documentation]     Closes the Upgrade Firmware dialog by clicking the Close button

    ${result}=  XIQSE Click Upgrade Firmware Close Button
    Should Be Equal As Integers     ${result}     1

Start Upgrade Firmware and Confirm Success
    [Documentation]     Starts the Upgrade Firmware action by clicking the Start button in the Upgrade Firmware dialog

    ${result}=  XIQSE Click Upgrade Firmware Start Button
    Should Be Equal As Integers     ${result}     1

Open Firmware Selection Dialog and Confirm Success
    [Documentation]     Opens the Firmware Selection dialog by clicking Assign Image in the already-open Upgrade Firmware dialog

    ${result}=  XIQSE Open Assign Firmware Image
    Should Be Equal As Integers     ${result}     1

Refresh Images in Firmware Selection Dialog and Confirm Success
    [Documentation]     Clicks "Refresh Images" in the Firmware Selection dialog

    ${result}=  XIQSE Click Refresh Images
    Should Be Equal As Integers     ${result}     1

Cancel Firmware Selection and Confirm Success
    [Documentation]     Clicks Cancel in the Firmware Selection dialog (accessed by clicking Assign Firmware)

    ${result}=  XIQSE Click Firmware Selection Cancel Button
    Should Be Equal As Integers     ${result}     1

Save Firmware Selection and Confirm Success
    [Documentation]     Clicks OK in the Firmware Selection dialog (accessed by clicking Assign Firmware)

    ${result}=  XIQSE Click Firmware Selection OK Button
    Should Be Equal As Integers     ${result}     1

Open Inventory Settings Dialog and Confirm Success
    [Documentation]     Opens the Inventory Settings dialog from the already-open Upgrade Firmware dialog

    ${result}=  XIQSE Open Inventory Settings
    Should Be Equal As Integers     ${result}     1

Set Inventory Settings File Transfer Mode and Confirm Success
    [Documentation]     Sets the File Transfer Mode in the Inventory Settings dialog
    [Arguments]         ${value}

    ${result}=  XIQSE Inventory Settings Dialog Select File Transfer Mode  ${value}
    Should Be Equal As Integers     ${result}     1

Set Inventory Settings Firmware Download MIB and Confirm Success
    [Documentation]     Sets the Firmware Download MIB in the Inventory Settings dialog
    [Arguments]         ${value}

    ${result}=  XIQSE Inventory Settings Dialog Select Firmware Download MIB  ${value}
    Should Be Equal As Integers     ${result}     1

Set Inventory Settings Configuration Download MIB and Confirm Success
    [Documentation]     Sets the Configuration Download MIB in the Inventory Settings dialog
    [Arguments]         ${value}

    ${result}=  XIQSE Inventory Settings Dialog Select Configuration Download MIB  ${value}
    Should Be Equal As Integers     ${result}     1

Set Inventory Settings Device Family Definition Filename and Confirm Success
    [Documentation]     Sets the Device Family Definition Filename in the Inventory Settings dialog
    [Arguments]         ${value}

    ${result}=  XIQSE Inventory Settings Dialog Select Device Family Definition Filename  ${value}
    Should Be Equal As Integers     ${result}     1

Cancel Inventory Settings and Confirm Success
    [Documentation]     Closes the Inventory Settings dialog by clicking the Cancel button

    ${result}=  XIQSE Click Inventory Settings Cancel Button
    Should Be Equal As Integers     ${result}     1

Save Inventory Settings and Confirm Success
    [Documentation]     Clicks OK in the Inventory Settings dialog

    ${result}=  XIQSE Click Inventory Settings OK Button
    Should Be Equal As Integers     ${result}     1

Wait Until Device Upgraded and Confirm Success
    [Documentation]     Waits for the device to show as being upgraded to the upgrade version in the devices table
    [Arguments]         ${ip}    ${firmware_version}    ${retry_duration}=30    ${retry_count}=10

    ${result}=  XIQSE Wait Until Device Upgraded        ${ip}    ${firmware_version}    ${retry_duration}   ${retry_count}
    Should Be Equal As Integers                         ${result}     1

Perform Firmware Upgrade and Confirm Success
    [Documentation]    Performs a firmware upgrade and confirms the actions are successful
    [Arguments]        ${ip}    ${transfer_mode}    ${filename}    ${upgrade_release}    ${firmware_version}

    Select Device and Confirm Success  ${ip}
    Open Upgrade Firmware Dialog for Device and Confirm Success    ${ip}
    Open Inventory Settings Dialog and Confirm Success
    Select File Transfer Mode and Confirm Success      ${transfer_mode}
    Set Inventory Settings Device Family Definition Filename and Confirm Success   ${filename}
    Save Inventory Settings and Confirm Success
    Open Assign Images, Refresh Images and Confirm Success
    Select Firmware Image, Start Upgrade and Confirm Success    ${upgrade_release}
    Wait Until Device Upgraded and Confirm Success  ${ip}  ${firmware_version}  retry_duration=10  retry_count=30

Download Firmware to XIQ-SE and Confirm Success
    [Documentation]     Downloads firmware upgrade image from internal servers to XIQ-SE directory
    [Arguments]   	    ${ip}  ${user}  ${password}  ${fw_dir}  ${src_loc}  ${dest_loc}  ${timeout_val}

    ${ssh_session} =    open_paramiko_ssh_spawn  ${ip}  ${user}  ${password}  ${SSH_PORT}

    #Delete Existing Firmware Files
    ${output} =  Send Paramiko CMD        ${ssh_session}  rm ${fw_dir}/*
    log to console  ${output}
    #Download firmware
    ${output}=  Send Paramiko Cmd  ${ssh_session}  curl ${src_loc} > ${dest_loc}  ${timeout_val}
    log to console  ${output}

    #close paramiko session
    ${close_result} =  Close Paramiko Spawn  ${ssh_session}

Delete Firmware from XIQ-SE and Confirm Success
    [Documentation]     Deletes firmware upgrade image from XIQ-SE directory
    [Arguments]   	    ${ip}  ${user}  ${password}  ${fw_dir}

    ${ssh_session} =    open_paramiko_ssh_spawn  ${ip}  ${user}  ${password}  ${SSH_PORT}

    #Delete Existing Firmware Images
    ${output} =  Send Paramiko CMD        ${ssh_session}  rm ${fw_dir}/*
    log to console  ${output}

    #close paramiko session
    ${close_result} =  Close Paramiko Spawn  ${ssh_session}

Open Assign Images, Refresh Images and Confirm Success
    [Documentation]     Clicks on the "Assign Image..." button within the Upgrade Firmware panel

    ${result}=  XIQSE Open Assign Firmware Image
    Should Be Equal As Integers             ${result}     1

    Refresh Images in Firmware Selection Dialog and Confirm Success

Select Device and Confirm Success
    [Documentation]     Selects the specified device
    [Arguments]         ${ip}

    ${result}=  XIQSE Select Device         ${ip}
    Should Be Equal As Integers             ${result}     1

Select File Transfer Mode and Confirm Success
    [Documentation]     Selects the File Transfer Mode in the Inventory Settings dialog
    [Arguments]         ${mode}

    ${result}=  XIQSE Inventory Settings Dialog Select File Transfer Mode      ${mode}
    Should Be Equal As Integers             ${result}     1

Select Firmware Image, Start Upgrade and Confirm Success
    [Documentation]     Selects the specified firmware, clicks OK then Start to perform upgrade, clicks Close to exit upgrade dialog and confirms success
    [Arguments]         ${image}

    ${result}=  XIQSE Select Firmware Image       ${image}
    Should Be Equal As Integers             ${result}     1

    Save Firmware Selection and Confirm Success
    Start Upgrade Firmware and Confirm Success
    Click Begin Downloading Firmware Yes Button and Confirm Success
    Wait For Upgrade To Complete and Confirm Success
    Wait For Restart Device To Complete and Confirm Success
    Close Upgrade Firmware Dialog and Confirm Success

Click Begin Downloading Firmware Yes Button and Confirm Success
    [Documentation]     Clicks the Yes button on the Begin Downloading Firmware Dialog

    ${result}=  XIQSE Click Begin Downloading Firmware Yes Button
    Should Be Equal As Integers             ${result}     1

Wait For Upgrade To Complete and Confirm Success
    [Documentation]     Institutes a loop waiting for "Processed 1 of 1 devices with 0 failures" text to appear in the Upgrade Firmware dialog

    Log To Console  >> Waiting for Upgrade Firmware dialog Summary to show "Processed 1 of 1 devices with 0 failures"
    ${result}=  XIQSE Wait For Processed No Failures Text
    Should Be Equal As Integers             ${result}     1
    Sleep  10 seconds

Wait For Restart Device To Complete and Confirm Success
    [Documentation]     Institutes a loop waiting for "Processed 1 of 1 devices with 0 failures" text to appear in the Restart Device dialog

    Log To Console  >> Waiting for Restart Device dialog Summary to show "Processed 1 of 1 devices with 0 failures"
    ${result}=  XIQSE Wait For Processed No Failures Text
    Should Be Equal As Integers             ${result}     1
