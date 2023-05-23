#########################################################################################################
# Author        : Binh Nguyen
# Date          : Feb 22nd 2023
# Description   : TCXM-8440 - Verify the AP reset feature for the new pop-up message
#                 TCXM-8441 - Verify the AP reset feature resets the device successfully
#########################################################################################################

*** Settings ***
# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/DevicesActions.py

Variables    Environments/${TOPO}
Variables    Environments/${ENV}

Force Tags  testbed_none

*** Test Cases ***
Step0: Reset devices to default and remove devices from XIQ
    [Documentation]    Reset devices to default and remove devices from XIQ
    [Tags]             tcxm-8440   tcxm-8441    development     step0   steps
    ${STATUS}                           Login User    ${tenant_username}   ${tenant_password}
    should be equal as strings          '${STATUS}'   '1'
    reset devices to default
    delete all devices
    Quit Browser