# Author        : Rameswar
# Date          : January 15th 2020
# Description   : Basic Login Test Cases
#
# Modified by   : Shreen Banu
# Date          : Oct 4 2022

# Topology      :
# Host ----- Cloud

*** Variables ***
${LOCATION}                 auto_location_01, Santa Clara, building_02, floor_04

*** Settings ***
Library     extauto/xiq/flows/common/Login.py
Library     extauto/xiq/flows/manage/Devices.py

Variables    Environments/${TOPO}
Variables    Environments/${ENV}

Force Tags   testbed_none

*** Keywords ***

*** Test Cases ***
TCCS-13211: Quick Add Onboard Simulated Device
    [Documentation]         Quick Onboarding - Add Simulated Devices
    [Tags]                  production      tccs_7651       tccs_13211
    ${LOGIN_STATUS}=                Login User          ${tenant_username}          ${tenant_password}
    should be equal as integers     ${LOGIN_STATUS}               1

    ${SIM_SERIAL}=                  Onboard Simulated Device                AP460C             location=${LOCATION}
    Should not be Empty             ${SIM_SERIAL}

    ${DELETE_AP}=                   Delete Devices              ${SIM_SERIAL}
    should be equal as integers     ${DELETE_AP}               1

    [Teardown]  Run Keywords    Logout User   Quit Browser