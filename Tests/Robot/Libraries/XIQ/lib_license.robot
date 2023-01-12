#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to the basic XIQ functionality.
#

*** Settings ***
Library     Collections
Library     xiq/flows/globalsettings/LicenseManagement.py
Library     xiq/flows/common/Navigator.py


*** Keywords ***
Confirm Entitlement Counts for Feature Matches Expected
    [Documentation]     Confirms the specified feature in the Entitlements table has the expected counts
    [Arguments]         ${feature}  ${available}  ${activated}  ${total}  ${retry_interval}=30  ${retry_count}=40

    # Wait until the entitlement counts match what we expect.
    ${result}=  Wait Until Entitlement Counts for Feature Matches  ${feature}  ${available}  ${activated}  ${total}   ${retry_interval}  ${retry_count}
    Should Be Equal As Integers  ${result}  1

Confirm Entitlement Total Count for Feature Matches Expected
    [Documentation]     Confirms the specified feature has the expected number of total devices associated with it
    [Arguments]         ${feature}  ${expected}  ${retry_interval}=30  ${retry_count}=40

    # Wait until the "Device Count" entitlement value matches what we expect.
    ${result}=  Wait Until Entitlement Total Count for Feature Matches  ${expected}  feature=${feature}   ${retry_interval}  ${retry_count}
    Should Be Equal As Integers  ${result}  1

Confirm Entitlement Available Count for Feature Matches Expected
    [Documentation]     Confirms the specified feature has the expected number of available entitlements associated with it
    [Arguments]         ${feature}  ${expected}  ${retry_interval}=30  ${retry_count}=40

    # Wait until the "Available" entitlement value matches what we expect.
    ${result}=  Wait Until Entitlement Available Count for Feature Matches  ${expected}  feature=${feature}   ${retry_interval}  ${retry_count}
    Should Be Equal As Integers  ${result}  1

Confirm Entitlement Activated Count for Feature Matches Expected
    [Documentation]     Confirms the specified feature has the expected number of activated entitlements associated with it
    [Arguments]         ${feature}  ${expected}  ${retry_interval}=30  ${retry_count}=40

    # Wait until the "Activated" entitlement value matches what we expect.
    ${result}=  Wait Until Entitlement Activated Count for Feature Matches  ${expected}  feature=${feature}   ${retry_interval}  ${retry_count}
    Should Be Equal As Integers  ${result}  1

Confirm CoPilot Entitlement Available
    [Documentation]     Confirm that there is at least one available CoPilot entitlement

    &{entitlement}=   Navigate And Get Entitlement Counts For Feature       feature=PRD-XIQ-COPILOT-S-C
    ${feature}=       Get From Dictionary               ${entitlement}      feature
    Should Contain                                      ${feature}          PRD-XIQ-COPILOT-S-C
