# Author        : Shreen
# Date          : May 2022
# Description   : Resets VIQ and deletes all devices and existing configuration

*** Variables ***

*** Settings ***
# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     xiq/flows/globalsettings/GlobalSetting.py

Variables    Environments/${TOPO}
Variables    Environments/${ENV}

Force Tags   testbed_none

*** Keywords ***

*** Test Cases ***
TCCS-13205: Perform Backup/Reset VIQ , Add default login password for devices
    [Documentation]    Takes backup of VIQ and Resets the VIQ,  Add default login password for devices

    [Tags]             production       tccs_13205

    ${LOGIN_STATUS}=                Login User              ${TENANT_USERNAME}     ${TENANT_PASSWORD}
    should be equal as integers         ${LOGIN_STATUS}               1

    #Perform Backup VIQ
    ${BACKUP_VIQ_DATA}=             Backup VIQ Data
    Should Be Equal As Strings      '${BACKUP_VIQ_DATA}'              '1'

    ${QUIT_BROWSER_RESULT}=         Quit Browser
    Should Be Equal As Integers     ${QUIT_BROWSER_RESULT}          1

    Sleep    3 minutes

    #Perform Reset VIQ
    ${LOGIN_STATUS}=                   Login User          ${tenant_username}     ${tenant_password}
    should be equal as integers         ${LOGIN_STATUS}               1

    ${RESET_VIQ_DATA}=              Reset VIQ Data
    Should Be Equal As Strings      '${RESET_VIQ_DATA}'              '1'

    ${QUIT_BROWSER_RESULT}=         Quit Browser
    Should Be Equal As Integers     ${QUIT_BROWSER_RESULT}          1

    Sleep    3 minutes

    # Add default login password for devices
    ${LOGIN_STATUS}=                   Login User          ${tenant_username}     ${tenant_password}       check_warning_msg=True
    should be equal as integers         ${LOGIN_STATUS}               1

    ${CHANGE_PASSWORD_STATUS}=      Change Device Password                  Aerohive123
    should be equal as integers     ${CHANGE_PASSWORD_STATUS}               1

    ${LOGOUT_RESULT}=               Logout User
    Should Be Equal As Integers     ${LOGOUT_RESULT}                1

    ${QUIT_BROWSER_RESULT}=         Quit Browser
    Should Be Equal As Integers     ${QUIT_BROWSER_RESULT}          1