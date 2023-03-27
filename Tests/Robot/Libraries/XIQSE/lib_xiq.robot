#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to the basic XIQ functionality.
#

*** Settings ***
Library     Collections
Library     xiq/flows/common/Login.py
Library     xiq/flows/common/Navigator.py
Library     xiq/flows/copilot/Copilot.py
Library     xiq/flows/globalsettings/LicenseManagement.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Device360.py
Library     xiq/flows/manage/Switch.py


*** Keywords ***
Log Into XIQ and Confirm Success
    [Documentation]     Logs into XIQ and confirms the action was successful
    [Arguments]         ${user}  ${pwd}  ${url}

    ${result}=  Login User          ${user}  ${pwd}  url=${url}
    Should Be Equal As Integers     ${result}     1

Log Out of XIQ and Confirm Success
    [Documentation]     Logs out of XIQ and confirms the action was successful

    ${result}=  Logout User
    Should Be Equal As Integers     ${result}     1

Quit XIQ Browser and Confirm Success
    [Documentation]     Closes the browser and confirms the action was successful

    ${result}=  Quit Browser
    Should Be Equal As Integers     ${result}     1

Log Out of XIQ and Quit Browser
    [Documentation]     Logs out of XIQ, confirms the action was successful, and closes the browser

    Log Out of XIQ and Confirm Success
    Quit XIQ Browser and Confirm Success

Navigate to XIQ Devices and Confirm Success
    [Documentation]     Navigates to the Manage> Devices view in XIQ and confirms the action was successful

    ${result}=  Navigate to Devices
    Should Be Equal As Integers  ${result}  1

Navigate and Remove Device by MAC From XIQ
    [Documentation]     Navigates to XIQ Devices and removes the specified device by MAC address from XIQ
    [Arguments]         ${mac}

    Navigate to XIQ Devices and Confirm Success
    Remove Device By MAC From XIQ and Confirm Success  ${mac}

Navigate and Remove Device by Serial From XIQ
    [Documentation]     Navigates to XIQ Devices and removes the specified device by serial number from XIQ
    [Arguments]         ${serial}

    Navigate to XIQ Devices and Confirm Success
    Remove Device By Serial From XIQ and Confirm Success  ${serial}

Navigate and Onboard Device to XIQ
    [Documentation]     Navigates to XIQ Devices, onboards the specified switch to XIQ and confirms it was added
    [Arguments]         ${netelem}  ${serial}

    Navigate to XIQ Devices and Confirm Success
    ${onboard_result}=  Onboard Device Quick  ${netelem}
    Should Be Equal As Integers         ${onboard_result}  1

    Confirm Device Serial Present       ${serial}

Onboard Device to XIQ and Confirm Success
    [Documentation]     Onboards the specified switch to XIQ and confirms it was added
    [Arguments]         ${netelem}  ${serial}

    ${onboard_result}=  Onboard Device Quick  ${netelem}
    Should Be Equal As Integers         ${onboard_result}  1

    Confirm Device Serial Present       ${serial}

Remove Device By MAC From XIQ and Confirm Success
    [Documentation]     Removes the device specified by its MAC address from XIQ and confirms the action was successful
    [Arguments]         ${mac}

    ${result}=  Delete Device  device_mac=${mac}
    Should Be Equal As Integers  ${result}  1

Remove Device By Serial From XIQ and Confirm Success
    [Documentation]     Removes the device specified by its serial number from XIQ and confirms the action was successful
    [Arguments]         ${serial}

    ${result}=  Delete Device  device_serial=${serial}
    Should Be Equal As Integers  ${result}  1

Confirm Device Serial Present
    [Documentation]     Confirms the device with the specified serial number is present in the Devices table
    [Arguments]         ${serial}

    ${result}=  Wait Until Device Added    device_serial=${serial}
    Should Be Equal As Integers            ${result}    1

Confirm Device Name Present
    [Documentation]     Confirms the device with the specified host name is present in the Devices table
    [Arguments]         ${name}

    ${result}=  Wait Until Device Added    device_name=${name}
    Should Be Equal As Integers            ${result}    1

Confirm Device MAC Address Present
    [Documentation]     Confirms the device with the specified MAC address is present in the Devices table
    [Arguments]         ${mac}

    ${result}=  Wait Until Device Added    device_mac=${mac}
    Should Be Equal As Integers            ${result}    1

Confirm Device OS Version Present
    [Documentation]     Confirms the "OS Version" field is populated for the device in the Devices table
    [Arguments]         ${serial}

    ${result}=  Wait Until Device Data Present  ${serial}   OS VERSION
    Should Be Equal As Integers                 ${result}   1

Confirm Device Serial Not Present
    [Documentation]     Confirms the device with the specified serial number is not present in the Devices table
    [Arguments]         ${serial}

    ${result}=  Wait Until Device Removed    device_serial=${serial}
    Should Be Equal As Integers              ${result}    1

Confirm Device Name Not Present
    [Documentation]     Confirms the device with the specified host name is not present in the Devices table
    [Arguments]         ${name}

    ${result}=  Wait Until Device Removed    device_name=${name}
    Should Be Equal As Integers              ${result}    1

Confirm Device MAC Address Not Present
    [Documentation]     Confirms the device with the specified MAC address is not present in the Devices table
    [Arguments]         ${mac}

    ${result}=  Wait Until Device Removed    device_mac=${mac}
    Should Be Equal As Integers              ${result}    1

Confirm Device Serial Online
    [Documentation]     Confirms the specified serial number has a connected/online status in XIQ
    [Arguments]         ${serial}

    ${result}=  Wait Until Device Online     ${serial}
    Should Be Equal As Integers              ${result}    1

Confirm Device Serial Offline
    [Documentation]     Confirms the specified serial number has a disconnected/offline status in XIQ
    [Arguments]         ${serial}

    ${result}=  Wait Until Device Offline   ${serial}
    Should Be Equal As Integers             ${result}    1

Navigate Filter and Confirm Device Serial Present
    [Documentation]     Navigates, filters, and confirms the specified device serial is present in the table
    [Arguments]         ${serial}

    Navigate to XIQ Devices and Confirm Success
    Search XIQ Devices Table and Confirm Success  ${serial}
    Confirm Device Serial Present  ${serial}
    Clear Search on XIQ Devices Table and Confirm Success

Navigate Filter and Confirm Device MAC Present
    [Documentation]     Navigates, filters, and confirms the specified device MAC is present in the table
    [Arguments]         ${mac}

    Navigate to XIQ Devices and Confirm Success
    Search XIQ Devices Table and Confirm Success  ${mac}
    Confirm Device MAC Address Present  ${mac}
    Clear Search on XIQ Devices Table and Confirm Success

Navigate Filter and Confirm Device Serial Not Present
    [Documentation]     Navigates, filters, and confirms the specified device serial is not present in the table
    [Arguments]         ${serial}

    Navigate to XIQ Devices and Confirm Success
    Search XIQ Devices Table and Confirm Success  ${serial}
    Confirm Device Serial Not Present  ${serial}
    Clear Search on XIQ Devices Table and Confirm Success

Navigate Filter and Confirm Device MAC Not Present
    [Documentation]     Navigates, filters, and confirms the specified device MAC is not present in the table
    [Arguments]         ${mac}

    Navigate to XIQ Devices and Confirm Success
    Search XIQ Devices Table and Confirm Success  ${mac}
    Confirm Device MAC Address Not Present  ${mac}
    Clear Search on XIQ Devices Table and Confirm Success

Confirm Entitlement Counts for Feature Matches Expected
    [Documentation]     Confirms the specified feature in the Entitlements table has the expected counts
    [Arguments]         ${feature}  ${available}  ${activated}  ${total}

    # Wait until the entitlement counts match what we expect.
    ${result}=  Wait Until Entitlement Counts for Feature Matches  ${feature}  ${available}  ${activated}  ${total}
    Should Be Equal As Integers  ${result}  1

Confirm Entitlement Total Count for Feature Matches Expected
    [Documentation]     Confirms the specified feature has the expected number of total devices associated with it
    [Arguments]         ${feature}  ${expected}

    # Wait until the "Total" entitlement value matches what we expect.
    ${result}=  Wait Until Entitlement Total Count for Feature Matches  ${expected}  feature=${feature}
    Should Be Equal As Integers  ${result}  1

Confirm Entitlement Available Count for Feature Matches Expected
    [Documentation]     Confirms the specified feature has the expected number of available entitlements associated with it
    [Arguments]         ${feature}  ${expected}

    # Wait until the "Available" entitlement value matches what we expect.
    ${result}=  Wait Until Entitlement Available Count for Feature Matches  ${expected}  feature=${feature}
    Should Be Equal As Integers  ${result}  1

Confirm Entitlement Activated Count for Feature Matches Expected
    [Documentation]     Confirms the specified feature has the expected number of activated entitlements associated with it
    [Arguments]         ${feature}  ${expected}

    # Wait until the "Activated" entitlement value matches what we expect.
    ${result}=  Wait Until Entitlement Activated Count for Feature Matches  ${expected}  feature=${feature}
    Should Be Equal As Integers  ${result}  1

Confirm Expected Pilot Licenses Consumed
    [Documentation]  Confirms the expected number of pilot licenses are consumed based on the entitlements
    [Arguments]      ${entitlements}  ${consumed}  ${feature}=XIQ-PIL-S-C

    ${available}=  Evaluate  ${entitlements} - ${consumed}

    # Confirm counts on License Management page
    Confirm Entitlement Counts for Feature Matches Expected  ${feature}  ${available}  ${consumed}  ${entitlements}

Confirm Expected Navigator Licenses Consumed
    [Documentation]  Confirms the expected number of navigator licenses are consumed based on the entitlements
    [Arguments]      ${entitlements}  ${consumed}  ${feature}=XIQ-NAV-S-C

    ${available}=  Evaluate  ${entitlements} - ${consumed}

    # Confirm counts on License Management page
    Confirm Entitlement Counts for Feature Matches Expected  ${feature}  ${available}  ${consumed}  ${entitlements}

Search XIQ Devices Table and Confirm Success
    [Documentation]     Performs a search on the Devices table in XIQ and confirms success.
    ...                 Note the search parameter will only match on Serial Number, Host Name, or MAC Address.
    [Arguments]         ${value}

    ${result}=  Perform Search on Devices Table  ${value}
    Should Be Equal As Integers  ${result}  1

Clear Search on XIQ Devices Table and Confirm Success
    [Documentation]     Clears the current search on the Devices table in XIQ and confirms success.

    ${result}=  Clear Search on Devices Table
    Should Be Equal As Integers  ${result}  1

Close XIQ Device360 Window and Confirm Success
    [Documentation]     Closes the Device360 window in XIQ and confirms the action was successful.

    ${result}=  Close Device360 Window
    Should Be Equal As Integers  ${result}  1
