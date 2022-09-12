# Author        : Abhinith
# Date          : April 14th 2022
# Description   : Backup and Reset VIQ Data
# Host ----- Cloud

*** Variables ***

*** Settings ***
Force Tags  testbed_1_node
Variables   Environments/${TOPO}
Variables   Environments/${ENV}
Resource    Tests/Robot/Functional/XIQ/Wireless/Extreme_Guest/Resources/settings.robot

*** Test Cases ***
TCCS-13022 Step1: Perform BackUp VIQ
    [Documentation]         BackUp Customer Account Data
    [Tags]                  development    tccs_13022

    ${LOGIN_XIQ}=                   Login User          ${tenant_username}      ${tenant_password}      url=${test_url}
    Should Be Equal As Strings      '${LOGIN_XIQ}'              '1'

    ${BACKUP_VIQ_DATA}=             Backup VIQ Data
    Should Be Equal As Strings      '${BACKUP_VIQ_DATA}'              '1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TCCS-13022 Step2: Perform Reset VIQ
    [Documentation]         Reset Customer Account Data
    [Tags]                  development    tccs_13022
    Depends On              TCCS-13022 Step1

    BuiltIn.Sleep  30 seconds
    ${LOGIN_XIQ}=                   Login User          ${tenant_username}      ${tenant_password}      url=${test_url}
    Should Be Equal As Strings      '${LOGIN_XIQ}'              '1'

    ${RESET_VIQ_DATA}=              Reset VIQ Data
    Should Be Equal As Strings      '${RESET_VIQ_DATA}'              '1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser
