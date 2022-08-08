
*** Variables ***
${LOCATION}                 auto_location_01, Santa Clara, building_02, floor_04

*** Settings ***
Library     Collections
Library     extauto/common/Utils.py
Library     extauto/common/Cli.py
Library     extauto/xiq/flows/common/Login.py
Library     extauto/xiq/flows/manage/Devices.py
Library     extauto/xiq/flows/manage/Device360.py
Library     extauto/xiq/flows/manage/Switch.py
Library     extauto/xiq/flows/manage/Tools.py
Library     extauto/xiq/flows/configure/NetworkPolicy.py
Library     extauto/xiq/flows/globalsettings/GlobalSetting.py
Library     extauto/common/TestFlow.py
Library     ./utils.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Force Tags   testbed_1_node
Suite Setup     Test Suite Setup
Suite Teardown  Test Suite Teardown

*** Keywords ***
Test Suite Setup
    convert to generic device object   device  index=1
    Login User      ${tenant_username}      ${tenant_password}

Test Suite Teardown
    Logout User
    Quit Browser

delete device action
    ${DELETE_RESULT}=          Delete Device  ${device1.serial}
    Should Be Equal As Integers                ${DELETE_RESULT}     1


*** Test Cases ***
Deboard_device_Step1: Deboard device on XIQ
    [Documentation]         Checks for device deboarding on XIQ

     [Tags]                  simple_deboard      development

    # If the device has already been onboarded, delete it first
    ${search_result}=  Search Device    serial=${device1.serial}  ignore_cli_feedback=true
    Run Keyword If  '${search_result}' == '1'       delete device action

