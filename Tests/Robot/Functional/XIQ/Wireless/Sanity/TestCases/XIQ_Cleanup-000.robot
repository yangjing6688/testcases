# Author        : Shreen
# Date          : May 2022
# Description   : Resets VIQ and deletes all devices and existing configuration

*** Variables ***
${MAP_FILE_NAME}            auto_location_01_1595321828282.tar.gz

*** Settings ***
Library     xiq/flows/common/Login.py
Library     xiq/flows/globalsettings/GlobalSetting.py

Library     common/Cli.py
Library     xiq/flows/mlinsights/Network360Plan.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}

Force Tags   testbed_1_node

*** Keywords ***

*** Test Cases ***
TCCS-13205_Step1: Perform Backup VIQ 
    [Documentation]    Takes backup of VIQ
    [Tags]             production       tccs_13205_step1

    ${LOGIN_STATUS}=                Login User              ${TENANT_USERNAME}     ${TENANT_PASSWORD}

    ${BACKUP_VIQ_DATA}=             Backup VIQ Data
    Should Be Equal As Strings      '${BACKUP_VIQ_DATA}'              '1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TCCS-13205_Step2: Perform Reset VIQ
    [Documentation]         Resets VIQ
    [Tags]                  production  tccs_13205_step2

    Sleep    3 minutes
    ${LOGIN_XIQ}=                   Login User          ${tenant_username}     ${tenant_password}

    ${RESET_VIQ_DATA}=              Reset VIQ Data
    Should Be Equal As Strings      '${RESET_VIQ_DATA}'              '1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TCCS-13205_Step3: Import Map
    [Documentation]         Imports map
    [Tags]                  production  tccs_13205_step3

    Sleep    3 minutes
    ${LOGIN_XIQ}=                   Login User          ${tenant_username}     ${tenant_password}       check_warning_msg=True

    ${IMPORT_MAP}=                  Import Map In Network360Plan  ${MAP_FILE_NAME}
    Should Be Equal As Strings      '${IMPORT_MAP}'              '1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser