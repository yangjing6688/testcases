#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to Firmware functionality.
#

*** Settings ***
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
    Should Be Equal As Integers         ${net_result}     1

    ${fw_result}=  XIQSE Network Select Firmware Tab
    Should Be Equal As Integers         ${fw_result}     1

Open Upgrade Firmware Dialog for Device and Confirm Success
    [Documentation]     Opens the Upgrade Firmware dialog for the specified device
    [Arguments]         ${ip}

    ${result}=  XIQSE Open Upgrade Firmware Dialog  ${ip}
    Should Be Equal As Integers  ${result}     1

Close Upgrade Firmware Dialog and Confirm Success
    [Documentation]     Closes the Upgrade Firmware dialog by clicking the Close button

    ${result}=  XIQSE Click Upgrade Firmware Close Button
    Should Be Equal As Integers  ${result}     1

Start Upgrade Firmware and Confirm Success
    [Documentation]     Starts the Upgrade Firmware action by clicking the Start button in the Upgrade Firmware dialog

    ${result}=  XIQSE Click Upgrade Firmware Start Button
    Should Be Equal As Integers  ${result}     1

Open Firmware Selection Dialog and Confirm Success
    [Documentation]     Opens the Firmware Selection dialog by clicking Assign Image in the already-open Upgrade Firmware dialog

    ${result}=  XIQSE Open Assign Firmware Image
    Should Be Equal As Integers  ${result}     1

Refresh Images in Firmware Selection Dialog and Confirm Success
    [Documentation]     Clicks "Refresh Images" in the Firmware Selection dialog

    ${result}=  XIQSE Click Refresh Images
    Should Be Equal As Integers  ${result}     1

Cancel Firmware Selection and Confirm Success
    [Documentation]     Clicks Cancel in the Firmware Selection dialog (accessed by clicking Assign Firmare)

    ${result}=  XIQSE Click Firmware Selection Cancel Button
    Should Be Equal As Integers  ${result}     1

Save Firmware Selection and Confirm Success
    [Documentation]     Clicks OK in the Firmware Selection dialog (accessed by clicking Assign Firmare)

    ${result}=  XIQSE Click Firmware Selection OK Button
    Should Be Equal As Integers  ${result}     1

Open Inventory Settings Dialog and Confirm Success
    [Documentation]     Opens the Inventory Settings dialog from the already-open Upgrade Firmware dialog

    ${result}=  XIQSE Open Inventory Settings
    Should Be Equal As Integers  ${result}     1

Set Inventory Settings File Transfer Mode and Confirm Success
    [Documentation]     Sets the File Transfer Mode in the Inventory Settings dialog
    [Arguments]         ${value}

    ${result}=  XIQSE Inventory Settings Dialog Select File Transfer Mode  ${value}
    Should Be Equal As Integers  ${result}     1

Set Inventory Settings Firmware Download MIB and Confirm Success
    [Documentation]     Sets the Firmware Download MIB in the Inventory Settings dialog
    [Arguments]         ${value}

    ${result}=  XIQSE Inventory Settings Dialog Select Firmware Download MIB  ${value}
    Should Be Equal As Integers  ${result}     1

Set Inventory Settings Configuration Download MIB and Confirm Success
    [Documentation]     Sets the Configuration Download MIB in the Inventory Settings dialog
    [Arguments]         ${value}

    ${result}=  XIQSE Inventory Settings Dialog Select Configuration Download MIB  ${value}
    Should Be Equal As Integers  ${result}     1

Set Inventory Settings Device Family Definition Filename and Confirm Success
    [Documentation]     Sets the Device Family Definition Filename in the Inventory Settings dialog
    [Arguments]         ${value}

    ${result}=  XIQSE Inventory Settings Dialog Select Device Family Definition Filename  ${value}
    Should Be Equal As Integers  ${result}     1

Cancel Inventory Settings and Confirm Success
    [Documentation]     Closes the Inventory Settings dialog by clicking the Cancel button

    ${result}=  XIQSE Click Inventory Settings Cancel Button
    Should Be Equal As Integers  ${result}     1

Save Inventory Settings and Confirm Success
    [Documentation]     Clicks OK in the Inventory Settings dialog

    ${result}=  XIQSE Click Inventory Settings OK Button
    Should Be Equal As Integers  ${result}     1
