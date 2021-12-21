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

Navigate and Onboard Switch to XIQ
    [Documentation]     Navigates to XIQ Devices and onboards the specified switch to XIQ
    [Arguments]         ${serial}  ${make}  ${location}

    Navigate to XIQ Devices and Confirm Success
    Onboard Switch to XIQ and Confirm Success  ${serial}  ${make}  ${location}

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

Onboard Switch to XIQ and Confirm Success
    [Documentation]     Onboards the specified switch to XIQ and confirms it was added
    [Arguments]         ${serial}  ${make}  ${location}

    ${onboard_result}=  Onboard Switch  ${serial}  ${make}  location=${location}
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

Confirm Entitlement Device Count for Feature Matches Expected
    [Documentation]     Confirms the specified feature has the expected number of devices associated with it
    [Arguments]         ${feature}  ${expected}

    # Wait until the entitlement count matches what we expect.  This could take 2-3 minutes for the counts to "settle".
    ${result}=  Wait Until Entitlement Device Count for Feature Matches  ${expected}  feature=${feature}
    Should Be Equal As Integers  ${result}  1

Log License Information From CoPilot Dashboard
    [Documentation]     Obtains the license information from the CoPilot Dashboard and logs the results

    ${result}=  Get CoPilot Licenses
    Log         ${result}

Get Total Pilot License Entitlements From CoPilot Dashboard
    [Documentation]     Returns the number of Pilot license entitlements, as displayed on the CoPilot Dashboard

    ${retval}=  Set Variable  -1

    ${licenses}=    Get CoPilot Licenses
    FOR  ${row}  IN  @{licenses}
        ${license_type}=  Get From Dictionary  ${row}  license_type
        IF  "${license_type}" == "PILOT"
            ${consumed}=  Get From Dictionary   ${row}  consumed
            ${available}=  Get From Dictionary  ${row}  available
            ${total}=  Evaluate  ${consumed} + ${available}
            ${retval}=  Set Variable  ${total}
            Exit For Loop If  "${license_type}" == "PILOT"
        END
    END

    [Return]  ${retval}

Get Total Navigator License Entitlements From CoPilot Dashboard
    [Documentation]     Returns the number of Navigator license entitlements, as displayed on the CoPilot Dashboard

    ${retval}=  Set Variable  -1

    ${licenses}=    Get CoPilot Licenses
    FOR  ${row}  IN  @{licenses}
        ${license_type}=  Get From Dictionary  ${row}  license_type
        IF  "${license_type}" == "NAVIGATOR"
            ${consumed}=  Get From Dictionary   ${row}  consumed
            ${available}=  Get From Dictionary  ${row}  available
            ${total}=  Evaluate  ${consumed} + ${available}
            ${retval}=  Set Variable  ${total}
            Exit For Loop If  "${license_type}" == "NAVIGATOR"
        END
    END

    [Return]  ${retval}

Get Pilot License Available Count From CoPilot Dashboard
    [Documentation]     Returns the number of Pilot licenses available, as displayed on the CoPilot Dashboard

    ${retval}=  Set Variable  -1

    ${licenses}=    Get CoPilot Licenses
    FOR  ${row}  IN  @{licenses}
        ${license_type}=  Get From Dictionary  ${row}  license_type
        IF  "${license_type}" == "PILOT"
            ${value}=  Get From Dictionary  ${row}  available
            ${retval}=  Set Variable  ${value}
            Exit For Loop If  "${license_type}" == "PILOT"
        END
    END

    [Return]  ${retval}

Get Pilot License Consumed Count From CoPilot Dashboard
    [Documentation]     Returns the number of Pilot licenses consumed, as displayed on the CoPilot Dashboard

    ${retval}=  Set Variable  -1

    ${licenses}=    Get CoPilot Licenses
    FOR  ${row}  IN  @{licenses}
        ${license_type}=  Get From Dictionary  ${row}  license_type
        IF  "${license_type}" == "PILOT"
            ${value}=  Get From Dictionary  ${row}  consumed
            ${retval}=  Set Variable  ${value}
            Exit For Loop If  "${license_type}" == "PILOT"
        END
    END

    [Return]  ${retval}

Get Navigator License Available Count From CoPilot Dashboard
    [Documentation]     Returns the number of Navigator licenses available, as displayed on the CoPilot Dashboard

    ${retval}=  Set Variable  -1

    ${licenses}=    Get CoPilot Licenses
    FOR  ${row}  IN  @{licenses}
        ${license_type}=  Get From Dictionary  ${row}  license_type
        IF  "${license_type}" == "NAVIGATOR"
            ${value}=  Get From Dictionary  ${row}  available
            ${retval}=  Set Variable  ${value}
            Exit For Loop If  "${license_type}" == "NAVIGATOR"
        END
    END

    [Return]  ${retval}

Get Navigator License Consumed Count From CoPilot Dashboard
    [Documentation]     Returns the number of Navigator licenses consumed, as displayed on the CoPilot Dashboard

    ${retval}=  Set Variable  -1

    ${licenses}=    Get CoPilot Licenses
    FOR  ${row}  IN  @{licenses}
        ${license_type}=  Get From Dictionary  ${row}  license_type
        IF  "${license_type}" == "NAVIGATOR"
            ${value}=  Get From Dictionary  ${row}  consumed
            ${retval}=  Set Variable  ${value}
            Exit For Loop If  "${license_type}" == "NAVIGATOR"
        END
    END

    [Return]  ${retval}

Confirm Total License Entitlements
    [Documentation]     Confirms the expected number of Pilot and Navigator license entitlements matches
    ...                 what is displayed on the CoPilot Dashboard
    [Arguments]         ${expected_pilots}  ${expected_navigators}

    ${total_pilots}=        Set Variable  -1
    ${total_navigators}=    Set Variable  -1

    # Do a new loop here instead of calling the individual keywords as we can speed things up since all data is returned
    # in the Get CoPilot Licenses call, and calling the individual keywords would make two calls to get the data
    ${licenses}=    Get CoPilot Licenses
    FOR  ${row}  IN  @{licenses}
        ${license_type}=  Get From Dictionary  ${row}  license_type
        IF  "${license_type}" == "PILOT"
            ${consumed}=  Get From Dictionary   ${row}  consumed
            ${available}=  Get From Dictionary  ${row}  available
            ${total}=  Evaluate  ${consumed} + ${available}
            ${total_pilots}=  Set Variable  ${total}
        ELSE IF  "${license_type}" == "NAVIGATOR"
            ${consumed}=  Get From Dictionary   ${row}  consumed
            ${available}=  Get From Dictionary  ${row}  available
            ${total}=  Evaluate  ${consumed} + ${available}
            ${total_navigators}=  Set Variable  ${total}
        END
    END

    Should Be Equal As Integers  ${total_pilots}      ${expected_pilots}
    Should Be Equal As Integers  ${total_navigators}  ${expected_navigators}

Confirm Total Pilot License Entitlements
    [Documentation]     Confirms the expected number of Pilot license entitlements matches
    ...                 what is displayed on the CoPilot Dashboard
    [Arguments]         ${expected_pilots}

    ${total_pilots}=  Get Total Pilot License Entitlements From CoPilot Dashboard
    Should Be Equal As Integers  ${total_pilots}      ${expected_pilots}

Confirm Total Navigator License Entitlements
    [Documentation]     Confirms the expected number of Navigator license entitlements matches
    ...                 what is displayed on the CoPilot Dashboard
    [Arguments]         ${expected_navigators}

    ${total_navigators}=  Get Total Navigator License Entitlements From CoPilot Dashboard
    Should Be Equal As Integers  ${total_navigators}  ${expected_navigators}

Confirm Number of Licenses Consumed
    [Documentation]     Confirms the number of Pilot and Navigator licenses expected to be consumed matches
    ...                 what is displayed on the CoPilot Dashboard
    [Arguments]         ${expected_pilots}  ${expected_navigators}

    ${pilots_consumed}=         Set Variable  -1
    ${navigators_consumed}=     Set Variable  -1

    # Do a new loop here instead of calling the individual keywords as we can speed things up since all data is returned
    # in the Get CoPilot Licenses call, and calling the individual keywords would make two calls to get the data
    ${licenses}=    Get CoPilot Licenses
    FOR  ${row}  IN  @{licenses}
        ${license_type}=  Get From Dictionary  ${row}  license_type
        IF  "${license_type}" == "PILOT"
            ${value}=  Get From Dictionary  ${row}  consumed
            ${pilots_consumed}=  Set Variable  ${value}
        ELSE IF  "${license_type}" == "NAVIGATOR"
            ${value}=  Get From Dictionary  ${row}  consumed
            ${navigators_consumed}=  Set Variable  ${value}
        END
    END

    Should Be Equal As Integers  ${pilots_consumed}      ${expected_pilots}
    Should Be Equal As Integers  ${navigators_consumed}  ${expected_navigators}

Confirm Number of Pilot Licenses Consumed
    [Documentation]     Confirms the number of Pilot licenses expected to be consumed matches
    ...                 what is displayed on the CoPilot Dashboard
    [Arguments]         ${expected_pilots}

    ${pilots_consumed}=  Get Pilot License Consumed Count From CoPilot Dashboard
    Should Be Equal As Integers  ${pilots_consumed}  ${expected_pilots}

Confirm Number of Navigator Licenses Consumed
    [Documentation]     Confirms the number of Navigator licenses expected to be consumed matches
    ...                 what is displayed on the CoPilot Dashboard
    [Arguments]         ${expected_navigators}

    ${navigators_consumed}=  Get Navigator License Consumed Count From CoPilot Dashboard
    Should Be Equal As Integers  ${navigators_consumed}  ${expected_navigators}

Confirm Number of Licenses Available
    [Documentation]     Confirms the number of Pilot and Navigator licenses expected to be available matches
    ...                 what is displayed on the CoPilot Dashboard
    [Arguments]         ${expected_pilots}  ${expected_navigators}

    ${pilots_available}=         Set Variable  -1
    ${navigators_available}=     Set Variable  -1

    # Do a new loop here instead of calling the individual keywords as we can speed things up since all data is returned
    # in the Get CoPilot Licenses call, and calling the individual keywords would make two calls to get the data
    ${licenses}=    Get CoPilot Licenses
    FOR  ${row}  IN  @{licenses}
        ${license_type}=  Get From Dictionary  ${row}  license_type
        IF  "${license_type}" == "PILOT"
            ${value}=  Get From Dictionary  ${row}  available
            ${pilots_available}=  Set Variable  ${value}
        ELSE IF  "${license_type}" == "NAVIGATOR"
            ${value}=  Get From Dictionary  ${row}  available
            ${navigators_available}=  Set Variable  ${value}
        END
    END

    Should Be Equal As Integers  ${pilots_available}      ${expected_pilots}
    Should Be Equal As Integers  ${navigators_available}  ${expected_navigators}

Confirm Number of Pilot Licenses Available
    [Documentation]     Confirms the number of Pilot licenses expected to be available matches
    ...                 what is displayed on the CoPilot Dashboard
    [Arguments]         ${expected_pilots}

    ${pilots_available}=  Get Pilot License Available Count From CoPilot Dashboard
    Should Be Equal As Integers  ${pilots_available}  ${expected_pilots}

Confirm Number of Navigator Licenses Available
    [Documentation]     Confirms the number of Navigator licenses expected to be available matches
    ...                 what is displayed on the CoPilot Dashboard
    [Arguments]         ${expected_navigators}

    ${navigators_available}=  Get Navigator License Available Count From CoPilot Dashboard
    Should Be Equal As Integers  ${navigators_available}  ${expected_navigators}

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
