# Author        : Barbara Sochor
# Date          : August 10th 2022
# Description   : XIQ-6165 AP5010 Regulatory Support
#
# Topology:
# Host ----- XIQ
#
#  To run using topo and environment:
#  ----------------------------------
#  robot -v TOPO:topology.yaml -v ENV:environment.yaml -v TESTBED:SJ/Dev/xiq_sj_tb0_all.yaml -i tcxm-20828 AP5010xxx.robot
#
#
#  ---------------------
#  This file contains test cases.
#
#  Test Cases:
#  Test1 - TCXM-20804 - Verify: AP Can Be Configured To Albania
#             Verifies that AP can be configured to Country Albania.
#  Test2 - TCXM-20816 - Verify: AP Can Be Configured To Austria
#             Verifies that AP can be configured to Country Austria.
#  Test3 - TCXM-20828 - Verify: AP Can Be Configured To Belgium
#             Verifies that AP can be configured to Country Belgium.
#  Test4 - TCXM-20829 - Verify: AP Can Be Configured To Bulgaria
#             Verifies that AP can be configured to Country Bulgaria.
#  Test5 - TCXM-20830 - Verify: AP Can Be Configured To Bosnia-Herzegovina
#             Verifies that AP can be configured to Country Bosnia-Herzegovina.
#  Test6 - TCXM2-20772 - Verify: AP Can Be Configured To Puerto Rico
#             Verifies that AP can be configured to Country Puerto Rico.
#  Test7 - TCXM-20773 - Verify: AP Can Be Configured To Colombia
#             Verifies that AP can be configured to Country Colombia.
#  Test8 - TCXM-20786 - Verify: AP Can Be Configured To Australia
#             Verifies that AP can be configured to Country Australia.
#  Test9 - TCXM-20798 - Verify: AP Can Be Configured To Italy
#             Verifies that AP can be configured to Country Italy.
#  Test10 - TCXM-20822 - Verify: AP Can Be Configured To Poland
#             Verifies that AP can be configured to Country Poland.
#  Test11 - TCXM-20848 - Verify: AP Can Be Configured To Netherlands
#             Verifies that AP can be configured to Country Netherlands.
#  Test12 - TCXM-20860 - Verify: AP Can Be Configured To Portugal
#             Verifies that AP can be configured to Country Portugal.
#  Test13 - TCXM-20785 - Verify: AP Can Be Configured To Germany
#             Verifies that AP can be configured to Country Germany.
#  Test14 - TCXM-20797 - Verify: AP Can Be Configured To France
#             Verifies that AP can be configured to Country France.
#  Test15 - TCXM-20810 - Verify: AP Can Be Configured To Spain
#             Verifies that AP can be configured to Country Spain.
#  Test16 - TCXM-20836 - Verify: AP Can Be Configured To Finland
#             Verifies that AP can be configured to Country Finland.
#  Test17 - TCXM-20853 - Verify: AP Can Be Configured To Sweden
#             Verifies that AP can be configured to Country Seden.
#  Test18 - TCXM-20849 - Verify: AP Can Be Configured To Romania
#             Verifies that AP can be configured to Country Romania.
#  Test19 - TCXM-20838 - Verify: AP Can Be Configured To Hungary
#             Verifies that AP can be configured to Country Hungry.
#  Test20 - TCXM-20854 - Verify: AP Can Be Configured To Switzerland
#             Verifies that AP can be configured to Country Switzerland.
#  Test21 - TCXM-20769 - Verify: A Country Cannot Be Reconfigured To "United States (840)"
#             Verifies that AP set to World region cannot be configured to United States.
#  Test22 - TCXM-20771 - Verify: A Country Cannot Be Reconfigured To "Canada (124)"
#             Verifies that AP set to World region cannot be configured to Canada.
#  Test23 - TCXM-20768 - Verify: "United States (840)" Country Cannot Be Reconfigured
#             Verifies that AP congigured to US cannot be reconfigured to a different country
#  Test24 - TCXM-20770 - Verify: "Canada (124)" Country Cannot Be Reconfigured
#             Verifies that AP congigured to Canada cannot be reconfigured to a different country
########################################################################################################################

*** Variables ***

*** Settings ***
# import libraries
Library     Collections
Library     xiq/flows/common/Login.py
Library     common/Utils.py
Library     common/Screen.py
Library     common/ImageHandler.py
Library     common/ScreenDiff.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/DeviceConfig.py
Library     common/ImageAnalysis.py
Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/ExpressNetworkPolicies.py
Library     xiq/flows/configure/CommonObjects.py
Library     extauto/common/Cli.py
Library     extauto/common/TestFlow.py
Library     extauto/xiq/flows/common/Login.py
Library     extauto/xiq/flows/common/Navigator.py

Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    TestBeds/${TESTBED}
Variables    Environments/Config/device_commands.yaml
Variables    Environments/Config/waits.yaml
Variables    Tests/Robot/Functional/XIQ/Wireless/Network360Monitor/Resources/n360waits.yaml

Force Tags   testbed_1_node
Suite Setup    InitialSetup

*** Test Cases ***
Test1 - TCXM-20804 - Verify: AP Can Be Configured To Albania
    [Documentation]         AP's country code is changed to Albania and result it verified on UI level
    [Tags]                  tcxm-20804    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Albania
    ${COUNTRY_CODE}     Set Variable    8
    Log                         ${COUNTRY}
    Log to Console              ${COUNTRY}
    ${result}=                  Login User          ${tenant_username}    ${tenant_password}
    ${COUNTRY_STATUS}=          Change Country      ${ap1.serial}         ${COUNTRY}
    Wait Until Device Reboots   ${ap1.serial}
    refresh devices page
    ${AP_STATUS2}=              Get AP Status       ${ap1.serial}
    refresh devices page
    ${AP_COUNTRY}=              Get AP Country      ${ap1.serial}
    refresh devices page
    ${GET_FLAG_STATUS}=         Get AP Flag         ${ap1.serial}
    Save Screen Shot
    ${AP_SPAWN}=                Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=                 Send                ${AP_SPAWN}   ${CMD_BOOT_PARAM}
    Close Spawn                 ${AP_SPAWN}

    Log to Console                      RESTULTS====
    Log to Console                      BOOT_PARAM: ${OUTPUT0}
    Should Contain Any                  ${OUTPUT0}    World   ${COUNTRY_CODE}
    Log to Console                      AP_COUNTRY: ${AP_COUNTRY}
    Should Contain                      ${AP_COUNTRY}           ${COUNTRY}
    Log to Console                      GET_FLAG_STATUS: ${GET_FLAG_STATUS}
    Should Not Be Equal as Integers     ${GET_FLAG_STATUS}      -1
    Log to Console                      COUNTRY_STATUS: ${COUNTRY_STATUS}
    Should Be Equal as Integers         ${COUNTRY_STATUS}       1
    Log to Console                      AP_STATUS2: ${AP_STATUS2}
    Should Be Equal as Strings          '${AP_STATUS2}'         'green'
    Log to Console                      END_RESTULTS====

Test2 - TCXM-20816 - Verify: AP Can Be Configured To Austria
    [Documentation]         AP's country code is changed to Austria and result it verified on UI level
    [Tags]                  tcxm-20816    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Austria
    ${COUNTRY_CODE}     Set Variable    40
    Log                         ${COUNTRY}
    Log to Console              ${COUNTRY}
    ${result}=                  Login User          ${tenant_username}    ${tenant_password}
    ${COUNTRY_STATUS}=          Change Country      ${ap1.serial}         ${COUNTRY}
    Wait Until Device Reboots   ${ap1.serial}
    refresh devices page
    ${AP_STATUS2}=              Get AP Status       ${ap1.serial}
    refresh devices page
    ${AP_COUNTRY}=              Get AP Country      ${ap1.serial}
    refresh devices page
    ${GET_FLAG_STATUS}=         Get AP Flag         ${ap1.serial}
    Save Screen Shot
    ${AP_SPAWN}=                Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=                 Send                ${AP_SPAWN}   ${CMD_BOOT_PARAM}
    Close Spawn                 ${AP_SPAWN}

    Log to Console                      RESTULTS====
    Log to Console                      BOOT_PARAM: ${OUTPUT0}
    Should Contain                      ${OUTPUT0}              ${COUNTRY_CODE}
    Log to Console                      AP_COUNTRY: ${AP_COUNTRY}
    Should Contain                      ${AP_COUNTRY}           ${COUNTRY}
    Log to Console                      GET_FLAG_STATUS: ${GET_FLAG_STATUS}
    Should Not Be Equal as Integers     ${GET_FLAG_STATUS}      -1
    Log to Console                      COUNTRY_STATUS: ${COUNTRY_STATUS}
    Should Be Equal as Integers         ${COUNTRY_STATUS}       1
    Log to Console                      AP_STATUS2: ${AP_STATUS2}
    Should Be Equal as Strings          '${AP_STATUS2}'         'green'
    Log to Console                      END_RESTULTS====

Test3 - TCXM-20828 - Verify: AP Can Be Configured To Belgium
    [Documentation]         AP's country code is changed to Belgium and result it verified on UI level
    [Tags]                  tcxm-20828    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Belgium
    ${COUNTRY_CODE}     Set Variable    56
    Log                         ${COUNTRY}
    Log to Console              ${COUNTRY}
    ${result}=                  Login User          ${tenant_username}    ${tenant_password}
    ${COUNTRY_STATUS}=          Change Country      ${ap1.serial}         ${COUNTRY}
    Wait Until Device Reboots   ${ap1.serial}
    refresh devices page
    ${AP_STATUS2}=              Get AP Status       ${ap1.serial}
    refresh devices page
    ${AP_COUNTRY}=              Get AP Country      ${ap1.serial}
    refresh devices page
    ${GET_FLAG_STATUS}=         Get AP Flag         ${ap1.serial}
    Save Screen Shot
    ${AP_SPAWN}=                Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=                 Send                ${AP_SPAWN}   ${CMD_BOOT_PARAM}
    Close Spawn                 ${AP_SPAWN}

    Log to Console                      RESTULTS====
    Log to Console                      BOOT_PARAM: ${OUTPUT0}
    Should Contain                      ${OUTPUT0}              ${COUNTRY_CODE}
    Log to Console                      AP_COUNTRY: ${AP_COUNTRY}
    Should Contain                      ${AP_COUNTRY}           ${COUNTRY}
    Log to Console                      GET_FLAG_STATUS: ${GET_FLAG_STATUS}
    Should Not Be Equal as Integers     ${GET_FLAG_STATUS}      -1
    Log to Console                      COUNTRY_STATUS: ${COUNTRY_STATUS}
    Should Be Equal as Integers         ${COUNTRY_STATUS}       1
    Log to Console                      AP_STATUS2: ${AP_STATUS2}
    Should Be Equal as Strings          '${AP_STATUS2}'         'green'
    Log to Console                      END_RESTULTS====

Test4 - TCXM-20829 - Verify: AP Can Be Configured To Bulgaria
    [Documentation]         AP's country code is changed to Bulgaria and result it verified on UI level
    [Tags]                  tcxm-20829    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Bulgaria
    ${COUNTRY_CODE}     Set Variable    100
    Log                         ${COUNTRY}
    Log to Console              ${COUNTRY}
    ${result}=                  Login User          ${tenant_username}    ${tenant_password}
    ${COUNTRY_STATUS}=          Change Country      ${ap1.serial}         ${COUNTRY}
    Wait Until Device Reboots   ${ap1.serial}
    refresh devices page
    ${AP_STATUS2}=              Get AP Status       ${ap1.serial}
    refresh devices page
    ${AP_COUNTRY}=              Get AP Country      ${ap1.serial}
    refresh devices page
    ${GET_FLAG_STATUS}=         Get AP Flag         ${ap1.serial}
    Save Screen Shot
    ${AP_SPAWN}=                Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=                 Send                ${AP_SPAWN}   ${CMD_BOOT_PARAM}
    Close Spawn                 ${AP_SPAWN}

    Log to Console                      RESTULTS====
    Log to Console                      BOOT_PARAM: ${OUTPUT0}
    Should Contain                      ${OUTPUT0}              ${COUNTRY_CODE}
    Log to Console                      AP_COUNTRY: ${AP_COUNTRY}
    Should Contain                      ${AP_COUNTRY}           ${COUNTRY}
    Log to Console                      GET_FLAG_STATUS: ${GET_FLAG_STATUS}
    Should Not Be Equal as Integers     ${GET_FLAG_STATUS}      -1
    Log to Console                      COUNTRY_STATUS: ${COUNTRY_STATUS}
    Should Be Equal as Integers         ${COUNTRY_STATUS}       1
    Log to Console                      AP_STATUS2: ${AP_STATUS2}
    Should Be Equal as Strings          '${AP_STATUS2}'         'green'
    Log to Console                      END_RESTULTS====

Test5 - TCXM-20830 - Verify: AP Can Be Configured To Bosnia-Herzegovina
    [Documentation]         AP's country code is changed to Bosnia-Herzegovina and result it verified on UI level
    [Tags]                  tcxm-20830    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Bosnia-Herzegovina
    ${COUNTRY_CODE}     Set Variable    70
    Log                         ${COUNTRY}
    Log to Console              ${COUNTRY}
    ${result}=                  Login User          ${tenant_username}    ${tenant_password}
    ${COUNTRY_STATUS}=          Change Country      ${ap1.serial}         ${COUNTRY}
    Wait Until Device Reboots   ${ap1.serial}
    refresh devices page
    ${AP_STATUS2}=              Get AP Status       ${ap1.serial}
    refresh devices page
    ${AP_COUNTRY}=              Get AP Country      ${ap1.serial}
    refresh devices page
    ${GET_FLAG_STATUS}=         Get AP Flag         ${ap1.serial}
    Save Screen Shot
    ${AP_SPAWN}=                Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=                 Send                ${AP_SPAWN}   ${CMD_BOOT_PARAM}
    Close Spawn                 ${AP_SPAWN}

    Log to Console                      RESTULTS====
    Log to Console                      BOOT_PARAM: ${OUTPUT0}
    Should Contain                      ${OUTPUT0}              ${COUNTRY_CODE}
    Log to Console                      AP_COUNTRY: ${AP_COUNTRY}
    Should Contain                      ${AP_COUNTRY}           ${COUNTRY}
    Log to Console                      GET_FLAG_STATUS: ${GET_FLAG_STATUS}
    Should Not Be Equal as Integers     ${GET_FLAG_STATUS}      -1
    Log to Console                      COUNTRY_STATUS: ${COUNTRY_STATUS}
    Should Be Equal as Integers         ${COUNTRY_STATUS}       1
    Log to Console                      AP_STATUS2: ${AP_STATUS2}
    Should Be Equal as Strings          '${AP_STATUS2}'         'green'
    Log to Console                      END_RESTULTS====

Test6 - TCXM-20772 - Verify: AP Can Be Configured To Puerto Rico
    [Documentation]         AP's country code is changed to Puerto Rico and result it verified on UI level
    [Tags]                  tcxm-20772    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Puerto Rico
    ${COUNTRY_CODE}     Set Variable    630
    ${SHORT_COUNTRY}     Set Variable    Puerto
    Log                         ${COUNTRY}
    Log to Console              ${COUNTRY}
    ${result}=                  Login User          ${tenant_username}    ${tenant_password}
    ${COUNTRY_STATUS}=          Change Country      ${ap1.serial}         ${COUNTRY}
    Wait Until Device Reboots   ${ap1.serial}
    refresh devices page
    ${AP_STATUS2}=              Get AP Status       ${ap1.serial}
    refresh devices page
    ${AP_COUNTRY}=              Get AP Country      ${ap1.serial}
    refresh devices page
    ${GET_FLAG_STATUS}=         Get AP Flag         ${ap1.serial}
    Save Screen Shot
    ${AP_SPAWN}=                Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=                 Send                ${AP_SPAWN}   ${CMD_BOOT_PARAM}
    Close Spawn                 ${AP_SPAWN}

    Log to Console                      RESTULTS====
    Log to Console                      BOOT_PARAM: ${OUTPUT0}
    Should Contain                      ${OUTPUT0}              ${COUNTRY_CODE}
    Log to Console                      AP_COUNTRY: ${AP_COUNTRY}
    Should Contain                      ${AP_COUNTRY}           ${SHORT_COUNTRY}
    Log to Console                      GET_FLAG_STATUS: ${GET_FLAG_STATUS}
    Should Not Be Equal as Integers     ${GET_FLAG_STATUS}      -1
    Log to Console                      COUNTRY_STATUS: ${COUNTRY_STATUS}
    Should Be Equal as Integers         ${COUNTRY_STATUS}       1
    Log to Console                      AP_STATUS2: ${AP_STATUS2}
    Should Be Equal as Strings          '${AP_STATUS2}'         'green'
    Log to Console                      END_RESTULTS====

Test7 - TCXM-20773 - Verify: AP Can Be Configured To Colombia
    [Documentation]         AP's country code is changed to Colombia and result it verified on UI level
    [Tags]                  tcxm-20773    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   170
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Colombia
    ${COUNTRY_CODE}     Set Variable    170
    Log                         ${COUNTRY}
    Log to Console              ${COUNTRY}
    ${result}=                  Login User          ${tenant_username}    ${tenant_password}
    ${COUNTRY_STATUS}=          Change Country      ${ap1.serial}         ${COUNTRY}
    Wait Until Device Reboots   ${ap1.serial}
    refresh devices page
    ${AP_STATUS2}=              Get AP Status       ${ap1.serial}
    refresh devices page
    ${AP_COUNTRY}=              Get AP Country      ${ap1.serial}
    refresh devices page
    ${GET_FLAG_STATUS}=         Get AP Flag         ${ap1.serial}
    Save Screen Shot
    ${AP_SPAWN}=                Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=                 Send                ${AP_SPAWN}   ${CMD_BOOT_PARAM}
    Close Spawn                 ${AP_SPAWN}

    Log to Console                      RESTULTS====
    Log to Console                      BOOT_PARAM: ${OUTPUT0}
    Should Contain                      ${OUTPUT0}              ${COUNTRY_CODE}
    Log to Console                      AP_COUNTRY: ${AP_COUNTRY}
    Should Contain                      ${AP_COUNTRY}           ${COUNTRY}
    Log to Console                      GET_FLAG_STATUS: ${GET_FLAG_STATUS}
    Should Not Be Equal as Integers     ${GET_FLAG_STATUS}      -1
    Log to Console                      COUNTRY_STATUS: ${COUNTRY_STATUS}
    Should Be Equal as Integers         ${COUNTRY_STATUS}       1
    Log to Console                      AP_STATUS2: ${AP_STATUS2}
    Should Be Equal as Strings          '${AP_STATUS2}'         'green'
    Log to Console                      END_RESTULTS====

Test8 - TCXM-20786 - Verify: AP Can Be Configured To Australia
    [Documentation]         AP's country code is changed to Australia and result it verified on UI level
    [Tags]                  tcxm-20786    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Australia
    ${COUNTRY_CODE}     Set Variable    36
    Log                         ${COUNTRY}
    Log to Console              ${COUNTRY}
    ${result}=                  Login User          ${tenant_username}    ${tenant_password}
    ${COUNTRY_STATUS}=          Change Country      ${ap1.serial}         ${COUNTRY}
    Wait Until Device Reboots   ${ap1.serial}
    refresh devices page
    ${AP_STATUS2}=              Get AP Status       ${ap1.serial}
    refresh devices page
    ${AP_COUNTRY}=              Get AP Country      ${ap1.serial}
    refresh devices page
    ${GET_FLAG_STATUS}=         Get AP Flag         ${ap1.serial}
    Save Screen Shot
    ${AP_SPAWN}=                Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=                 Send                ${AP_SPAWN}   ${CMD_BOOT_PARAM}
    Close Spawn                 ${AP_SPAWN}

    Log to Console                      RESTULTS====
    Log to Console                      BOOT_PARAM: ${OUTPUT0}
    Should Contain                      ${OUTPUT0}              ${COUNTRY_CODE}
    Log to Console                      AP_COUNTRY: ${AP_COUNTRY}
    Should Contain                      ${AP_COUNTRY}           ${COUNTRY}
    Log to Console                      GET_FLAG_STATUS: ${GET_FLAG_STATUS}
    Should Not Be Equal as Integers     ${GET_FLAG_STATUS}      -1
    Log to Console                      COUNTRY_STATUS: ${COUNTRY_STATUS}
    Should Be Equal as Integers         ${COUNTRY_STATUS}       1
    Log to Console                      AP_STATUS2: ${AP_STATUS2}
    Should Be Equal as Strings          '${AP_STATUS2}'         'green'
    Log to Console                      END_RESTULTS====

Test9 - TCXM-20798 - Verify: AP Can Be Configured To Italy
    [Documentation]         AP's country code is changed to Italy and result it verified on UI level
    [Tags]                  tcxm-20798    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Italy
    ${COUNTRY_CODE}     Set Variable    380
    Log                         ${COUNTRY}
    Log to Console              ${COUNTRY}
    ${result}=                  Login User          ${tenant_username}    ${tenant_password}
    ${COUNTRY_STATUS}=          Change Country      ${ap1.serial}         ${COUNTRY}
    Wait Until Device Reboots   ${ap1.serial}
    refresh devices page
    ${AP_STATUS2}=              Get AP Status       ${ap1.serial}
    refresh devices page
    ${AP_COUNTRY}=              Get AP Country      ${ap1.serial}
    refresh devices page
    ${GET_FLAG_STATUS}=         Get AP Flag         ${ap1.serial}
    Save Screen Shot
    ${AP_SPAWN}=                Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=                 Send                ${AP_SPAWN}   ${CMD_BOOT_PARAM}
    Close Spawn                 ${AP_SPAWN}

    Log to Console                      RESTULTS====
    Log to Console                      BOOT_PARAM: ${OUTPUT0}
    Should Contain                      ${OUTPUT0}              ${COUNTRY_CODE}
    Log to Console                      AP_COUNTRY: ${AP_COUNTRY}
    Should Contain                      ${AP_COUNTRY}           ${COUNTRY}
    Log to Console                      GET_FLAG_STATUS: ${GET_FLAG_STATUS}
    Should Not Be Equal as Integers     ${GET_FLAG_STATUS}      -1
    Log to Console                      COUNTRY_STATUS: ${COUNTRY_STATUS}
    Should Be Equal as Integers         ${COUNTRY_STATUS}       1
    Log to Console                      AP_STATUS2: ${AP_STATUS2}
    Should Be Equal as Strings          '${AP_STATUS2}'         'green'
    Log to Console                      END_RESTULTS====

Test10 - TCXM-20822 - Verify: AP Can Be Configured To Poland
    [Documentation]         AP's country code is changed to Poland and result it verified on UI level
    [Tags]                  tcxm-20822    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Poland
    ${COUNTRY_CODE}     Set Variable    616
    Log                         ${COUNTRY}
    Log to Console              ${COUNTRY}
    ${result}=                  Login User          ${tenant_username}    ${tenant_password}
    ${COUNTRY_STATUS}=          Change Country      ${ap1.serial}         ${COUNTRY}
    Wait Until Device Reboots   ${ap1.serial}
    refresh devices page
    ${AP_STATUS2}=              Get AP Status       ${ap1.serial}
    refresh devices page
    ${AP_COUNTRY}=              Get AP Country      ${ap1.serial}
    refresh devices page
    ${GET_FLAG_STATUS}=         Get AP Flag         ${ap1.serial}
    Save Screen Shot
    ${AP_SPAWN}=                Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=                 Send                ${AP_SPAWN}   ${CMD_BOOT_PARAM}
    Close Spawn                 ${AP_SPAWN}

    Log to Console                      RESTULTS====
    Log to Console                      BOOT_PARAM: ${OUTPUT0}
    Should Contain                      ${OUTPUT0}              ${COUNTRY_CODE}
    Log to Console                      AP_COUNTRY: ${AP_COUNTRY}
    Should Contain                      ${AP_COUNTRY}           ${COUNTRY}
    Log to Console                      GET_FLAG_STATUS: ${GET_FLAG_STATUS}
    Should Not Be Equal as Integers     ${GET_FLAG_STATUS}      -1
    Log to Console                      COUNTRY_STATUS: ${COUNTRY_STATUS}
    Should Be Equal as Integers         ${COUNTRY_STATUS}       1
    Log to Console                      AP_STATUS2: ${AP_STATUS2}
    Should Be Equal as Strings          '${AP_STATUS2}'         'green'
    Log to Console                      END_RESTULTS====

Test11 - TCXM-20848 - Verify: AP Can Be Configured To Netherlands
    [Documentation]         AP's country code is changed to Netherlands and result it verified on UI level
    [Tags]                  tcxm-20848    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Netherlands
    ${COUNTRY_CODE}     Set Variable    528
    Log                         ${COUNTRY}
    Log to Console              ${COUNTRY}
    ${result}=                  Login User          ${tenant_username}    ${tenant_password}
    ${COUNTRY_STATUS}=          Change Country      ${ap1.serial}         ${COUNTRY}
    Wait Until Device Reboots   ${ap1.serial}
    refresh devices page
    ${AP_STATUS2}=              Get AP Status       ${ap1.serial}
    refresh devices page
    ${AP_COUNTRY}=              Get AP Country      ${ap1.serial}
    refresh devices page
    ${GET_FLAG_STATUS}=         Get AP Flag         ${ap1.serial}
    Save Screen Shot
    ${AP_SPAWN}=                Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=                 Send                ${AP_SPAWN}   ${CMD_BOOT_PARAM}
    Close Spawn                 ${AP_SPAWN}

    Log to Console                      RESTULTS====
    Log to Console                      BOOT_PARAM: ${OUTPUT0}
    Should Contain                      ${OUTPUT0}              ${COUNTRY_CODE}
    Log to Console                      AP_COUNTRY: ${AP_COUNTRY}
    Should Contain                      ${AP_COUNTRY}           ${COUNTRY}
    Log to Console                      GET_FLAG_STATUS: ${GET_FLAG_STATUS}
    Should Not Be Equal as Integers     ${GET_FLAG_STATUS}      -1
    Log to Console                      COUNTRY_STATUS: ${COUNTRY_STATUS}
    Should Be Equal as Integers         ${COUNTRY_STATUS}       1
    Log to Console                      AP_STATUS2: ${AP_STATUS2}
    Should Be Equal as Strings          '${AP_STATUS2}'         'green'
    Log to Console                      END_RESTULTS====

Test12 - TCXM-20860 - Verify: AP Can Be Configured To Portugal
    [Documentation]         AP's country code is changed to Portugal and result it verified on UI level
    [Tags]                  tcxm-20860    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Portugal
    ${COUNTRY_CODE}     Set Variable    620
    Log                         ${COUNTRY}
    Log to Console              ${COUNTRY}
    ${result}=                  Login User          ${tenant_username}    ${tenant_password}
    ${COUNTRY_STATUS}=          Change Country      ${ap1.serial}         ${COUNTRY}
    Wait Until Device Reboots   ${ap1.serial}
    refresh devices page
    ${AP_STATUS2}=              Get AP Status       ${ap1.serial}
    refresh devices page
    ${AP_COUNTRY}=              Get AP Country      ${ap1.serial}
    refresh devices page
    ${GET_FLAG_STATUS}=         Get AP Flag         ${ap1.serial}
    Save Screen Shot
    ${AP_SPAWN}=                Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=                 Send                ${AP_SPAWN}   ${CMD_BOOT_PARAM}
    Close Spawn                 ${AP_SPAWN}

    Log to Console                      RESTULTS====
    Log to Console                      BOOT_PARAM: ${OUTPUT0}
    Should Contain                      ${OUTPUT0}              ${COUNTRY_CODE}
    Log to Console                      AP_COUNTRY: ${AP_COUNTRY}
    Should Contain                      ${AP_COUNTRY}           ${COUNTRY}
    Log to Console                      GET_FLAG_STATUS: ${GET_FLAG_STATUS}
    Should Not Be Equal as Integers     ${GET_FLAG_STATUS}      -1
    Log to Console                      COUNTRY_STATUS: ${COUNTRY_STATUS}
    Should Be Equal as Integers         ${COUNTRY_STATUS}       1
    Log to Console                      AP_STATUS2: ${AP_STATUS2}
    Should Be Equal as Strings          '${AP_STATUS2}'         'green'
    Log to Console                      END_RESTULTS====

Test13 - TCXM-20785 - Verify: AP Can Be Configured To Germany
    [Documentation]         AP's country code is changed to Germany and result it verified on UI level
    [Tags]                  tcxm-20785    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Germany
    ${COUNTRY_CODE}     Set Variable    276
    Log                         ${COUNTRY}
    Log to Console              ${COUNTRY}
    ${result}=                  Login User          ${tenant_username}    ${tenant_password}
    ${COUNTRY_STATUS}=          Change Country      ${ap1.serial}         ${COUNTRY}
    Wait Until Device Reboots   ${ap1.serial}
    refresh devices page
    ${AP_STATUS2}=              Get AP Status       ${ap1.serial}
    refresh devices page
    ${AP_COUNTRY}=              Get AP Country      ${ap1.serial}
    refresh devices page
    ${GET_FLAG_STATUS}=         Get AP Flag         ${ap1.serial}
    Save Screen Shot
    ${AP_SPAWN}=                Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=                 Send                ${AP_SPAWN}   ${CMD_BOOT_PARAM}
    Close Spawn                 ${AP_SPAWN}

    Log to Console                      RESTULTS====
    Log to Console                      BOOT_PARAM: ${OUTPUT0}
    Should Contain                      ${OUTPUT0}              ${COUNTRY_CODE}
    Log to Console                      AP_COUNTRY: ${AP_COUNTRY}
    Should Contain                      ${AP_COUNTRY}           ${COUNTRY}
    Log to Console                      GET_FLAG_STATUS: ${GET_FLAG_STATUS}
    Should Not Be Equal as Integers     ${GET_FLAG_STATUS}      -1
    Log to Console                      COUNTRY_STATUS: ${COUNTRY_STATUS}
    Should Be Equal as Integers         ${COUNTRY_STATUS}       1
    Log to Console                      AP_STATUS2: ${AP_STATUS2}
    Should Be Equal as Strings          '${AP_STATUS2}'         'green'
    Log to Console                      END_RESTULTS====

Test14 - TCXM-20797 - Verify: AP Can Be Configured To France
    [Documentation]         AP's country code is changed to France and result it verified on UI level
    [Tags]                  tcxm-20797    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    France
    ${COUNTRY_CODE}     Set Variable    250
    Log                         ${COUNTRY}
    Log to Console              ${COUNTRY}
    ${result}=                  Login User          ${tenant_username}    ${tenant_password}
    ${COUNTRY_STATUS}=          Change Country      ${ap1.serial}         ${COUNTRY}
    Wait Until Device Reboots   ${ap1.serial}
    refresh devices page
    ${AP_STATUS2}=              Get AP Status       ${ap1.serial}
    refresh devices page
    ${AP_COUNTRY}=              Get AP Country      ${ap1.serial}
    refresh devices page
    ${GET_FLAG_STATUS}=         Get AP Flag         ${ap1.serial}
    Save Screen Shot
    ${AP_SPAWN}=                Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=                 Send                ${AP_SPAWN}   ${CMD_BOOT_PARAM}
    Close Spawn                 ${AP_SPAWN}

    Log to Console                      RESTULTS====
    Log to Console                      BOOT_PARAM: ${OUTPUT0}
    Should Contain                      ${OUTPUT0}              ${COUNTRY_CODE}
    Log to Console                      AP_COUNTRY: ${AP_COUNTRY}
    Should Contain                      ${AP_COUNTRY}           ${COUNTRY}
    Log to Console                      GET_FLAG_STATUS: ${GET_FLAG_STATUS}
    Should Not Be Equal as Integers     ${GET_FLAG_STATUS}      -1
    Log to Console                      COUNTRY_STATUS: ${COUNTRY_STATUS}
    Should Be Equal as Integers         ${COUNTRY_STATUS}       1
    Log to Console                      AP_STATUS2: ${AP_STATUS2}
    Should Be Equal as Strings          '${AP_STATUS2}'         'green'
    Log to Console                      END_RESTULTS====

Test15 - TCXM-20810 - Verify: AP Can Be Configured To Spain
    [Documentation]         AP's country code is changed to Spain and result it verified on UI level
    [Tags]                  tcxm-20810    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Spain
    ${COUNTRY_CODE}     Set Variable    724
    Log                         ${COUNTRY}
    Log to Console              ${COUNTRY}
    ${result}=                  Login User          ${tenant_username}    ${tenant_password}
    ${COUNTRY_STATUS}=          Change Country      ${ap1.serial}         ${COUNTRY}
    Wait Until Device Reboots   ${ap1.serial}
    refresh devices page
    ${AP_STATUS2}=              Get AP Status       ${ap1.serial}
    refresh devices page
    ${AP_COUNTRY}=              Get AP Country      ${ap1.serial}
    refresh devices page
    ${GET_FLAG_STATUS}=         Get AP Flag         ${ap1.serial}
    Save Screen Shot
    ${AP_SPAWN}=                Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=                 Send                ${AP_SPAWN}   ${CMD_BOOT_PARAM}
    Close Spawn                 ${AP_SPAWN}

    Log to Console                      RESTULTS====
    Log to Console                      BOOT_PARAM: ${OUTPUT0}
    Should Contain                      ${OUTPUT0}              ${COUNTRY_CODE}
    Log to Console                      AP_COUNTRY: ${AP_COUNTRY}
    Should Contain                      ${AP_COUNTRY}           ${COUNTRY}
    Log to Console                      GET_FLAG_STATUS: ${GET_FLAG_STATUS}
    Should Not Be Equal as Integers     ${GET_FLAG_STATUS}      -1
    Log to Console                      COUNTRY_STATUS: ${COUNTRY_STATUS}
    Should Be Equal as Integers         ${COUNTRY_STATUS}       1
    Log to Console                      AP_STATUS2: ${AP_STATUS2}
    Should Be Equal as Strings          '${AP_STATUS2}'         'green'
    Log to Console                      END_RESTULTS====

Test16 - TCXM-20836 - Verify: AP Can Be Configured To Finland
    [Documentation]         AP's country code is changed to Finland and result it verified on UI level
    [Tags]                  tcxm-20836    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Finland
    ${COUNTRY_CODE}     Set Variable    246
    Log                         ${COUNTRY}
    Log to Console              ${COUNTRY}
    ${result}=                  Login User          ${tenant_username}    ${tenant_password}
    ${COUNTRY_STATUS}=          Change Country      ${ap1.serial}         ${COUNTRY}
    Wait Until Device Reboots   ${ap1.serial}
    refresh devices page
    ${AP_STATUS2}=              Get AP Status       ${ap1.serial}
    refresh devices page
    ${AP_COUNTRY}=              Get AP Country      ${ap1.serial}
    refresh devices page
    ${GET_FLAG_STATUS}=         Get AP Flag         ${ap1.serial}
    Save Screen Shot
    ${AP_SPAWN}=                Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=                 Send                ${AP_SPAWN}   ${CMD_BOOT_PARAM}
    Close Spawn                 ${AP_SPAWN}

    Log to Console                      RESTULTS====
    Log to Console                      BOOT_PARAM: ${OUTPUT0}
    Should Contain                      ${OUTPUT0}              ${COUNTRY_CODE}
    Log to Console                      AP_COUNTRY: ${AP_COUNTRY}
    Should Contain                      ${AP_COUNTRY}           ${COUNTRY}
    Log to Console                      GET_FLAG_STATUS: ${GET_FLAG_STATUS}
    Should Not Be Equal as Integers     ${GET_FLAG_STATUS}      -1
    Log to Console                      COUNTRY_STATUS: ${COUNTRY_STATUS}
    Should Be Equal as Integers         ${COUNTRY_STATUS}       1
    Log to Console                      AP_STATUS2: ${AP_STATUS2}
    Should Be Equal as Strings          '${AP_STATUS2}'         'green'
    Log to Console                      END_RESTULTS====

Test17 - TCXM-20853 - Verify: AP Can Be Configured To Sweden
    [Documentation]         AP's country code is changed to Sweden and result it verified on UI level
    [Tags]                  tcxm-20853    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Sweden
    ${COUNTRY_CODE}     Set Variable    752
    Log                         ${COUNTRY}
    Log to Console              ${COUNTRY}
    ${result}=                  Login User          ${tenant_username}    ${tenant_password}
    ${COUNTRY_STATUS}=          Change Country      ${ap1.serial}         ${COUNTRY}
    Wait Until Device Reboots   ${ap1.serial}
    refresh devices page
    ${AP_STATUS2}=              Get AP Status       ${ap1.serial}
    refresh devices page
    ${AP_COUNTRY}=              Get AP Country      ${ap1.serial}
    refresh devices page
    ${GET_FLAG_STATUS}=         Get AP Flag         ${ap1.serial}
    Save Screen Shot
    ${AP_SPAWN}=                Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=                 Send                ${AP_SPAWN}   ${CMD_BOOT_PARAM}
    Close Spawn                 ${AP_SPAWN}

    Log to Console                      RESTULTS====
    Log to Console                      BOOT_PARAM: ${OUTPUT0}
    Should Contain                      ${OUTPUT0}              ${COUNTRY_CODE}
    Log to Console                      AP_COUNTRY: ${AP_COUNTRY}
    Should Contain                      ${AP_COUNTRY}           ${COUNTRY}
    Log to Console                      GET_FLAG_STATUS: ${GET_FLAG_STATUS}
    Should Not Be Equal as Integers     ${GET_FLAG_STATUS}      -1
    Log to Console                      COUNTRY_STATUS: ${COUNTRY_STATUS}
    Should Be Equal as Integers         ${COUNTRY_STATUS}       1
    Log to Console                      AP_STATUS2: ${AP_STATUS2}
    Should Be Equal as Strings          '${AP_STATUS2}'         'green'
    Log to Console                      END_RESTULTS====

Test18 - TCXM-20849 - Verify: AP Can Be Configured To Romania
    [Documentation]         AP's country code is changed to Romania and result it verified on UI level
    [Tags]                  tcxm-20849    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Romania
    ${COUNTRY_CODE}     Set Variable    642
    Log                         ${COUNTRY}
    Log to Console              ${COUNTRY}
    ${result}=                  Login User          ${tenant_username}    ${tenant_password}
    ${COUNTRY_STATUS}=          Change Country      ${ap1.serial}         ${COUNTRY}
    Wait Until Device Reboots   ${ap1.serial}
    refresh devices page
    ${AP_STATUS2}=              Get AP Status       ${ap1.serial}
    refresh devices page
    ${AP_COUNTRY}=              Get AP Country      ${ap1.serial}
    refresh devices page
    ${GET_FLAG_STATUS}=         Get AP Flag         ${ap1.serial}
    Save Screen Shot
    ${AP_SPAWN}=                Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=                 Send                ${AP_SPAWN}   ${CMD_BOOT_PARAM}
    Close Spawn                 ${AP_SPAWN}

    Log to Console                      RESTULTS====
    Log to Console                      BOOT_PARAM: ${OUTPUT0}
    Should Contain                      ${OUTPUT0}              ${COUNTRY_CODE}
    Log to Console                      AP_COUNTRY: ${AP_COUNTRY}
    Should Contain                      ${AP_COUNTRY}           ${COUNTRY}
    Log to Console                      GET_FLAG_STATUS: ${GET_FLAG_STATUS}
    Should Not Be Equal as Integers     ${GET_FLAG_STATUS}      -1
    Log to Console                      COUNTRY_STATUS: ${COUNTRY_STATUS}
    Should Be Equal as Integers         ${COUNTRY_STATUS}       1
    Log to Console                      AP_STATUS2: ${AP_STATUS2}
    Should Be Equal as Strings          '${AP_STATUS2}'         'green'
    Log to Console                      END_RESTULTS====

Test19 - TCXM-20838 - Verify: AP Can Be Configured To Hungary
    [Documentation]         AP's country code is changed to Hungary and result it verified on UI level
    [Tags]                  tcxm-20838    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Hungary
    ${COUNTRY_CODE}     Set Variable    348
    Log                         ${COUNTRY}
    Log to Console              ${COUNTRY}
    ${result}=                  Login User          ${tenant_username}    ${tenant_password}
    ${COUNTRY_STATUS}=          Change Country      ${ap1.serial}         ${COUNTRY}
    Wait Until Device Reboots   ${ap1.serial}
    refresh devices page
    ${AP_STATUS2}=              Get AP Status       ${ap1.serial}
    refresh devices page
    ${AP_COUNTRY}=              Get AP Country      ${ap1.serial}
    refresh devices page
    ${GET_FLAG_STATUS}=         Get AP Flag         ${ap1.serial}
    Save Screen Shot
    ${AP_SPAWN}=                Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=                 Send                ${AP_SPAWN}   ${CMD_BOOT_PARAM}
    Close Spawn                 ${AP_SPAWN}

    Log to Console                      RESTULTS====
    Log to Console                      BOOT_PARAM: ${OUTPUT0}
    Should Contain                      ${OUTPUT0}              ${COUNTRY_CODE}
    Log to Console                      AP_COUNTRY: ${AP_COUNTRY}
    Should Contain                      ${AP_COUNTRY}           ${COUNTRY}
    Log to Console                      GET_FLAG_STATUS: ${GET_FLAG_STATUS}
    Should Not Be Equal as Integers     ${GET_FLAG_STATUS}      -1
    Log to Console                      COUNTRY_STATUS: ${COUNTRY_STATUS}
    Should Be Equal as Integers         ${COUNTRY_STATUS}       1
    Log to Console                      AP_STATUS2: ${AP_STATUS2}
    Should Be Equal as Strings          '${AP_STATUS2}'         'green'
    Log to Console                      END_RESTULTS====

Test20 - TCXM-20854 - Verify: AP Can Be Configured To Switzerland
    [Documentation]         AP's country code is changed to Switzerland and result it verified on UI level
    [Tags]                  tcxm-20854    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Switzerland
    ${COUNTRY_CODE}     Set Variable    756
    Log                         ${COUNTRY}
    Log to Console              ${COUNTRY}
    ${result}=                  Login User          ${tenant_username}    ${tenant_password}
    ${COUNTRY_STATUS}=          Change Country      ${ap1.serial}         ${COUNTRY}
    Wait Until Device Reboots   ${ap1.serial}
    refresh devices page
    ${AP_STATUS2}=              Get AP Status       ${ap1.serial}
    refresh devices page
    ${AP_COUNTRY}=              Get AP Country      ${ap1.serial}
    refresh devices page
    ${GET_FLAG_STATUS}=         Get AP Flag         ${ap1.serial}
    Save Screen Shot
    ${AP_SPAWN}=                Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=                 Send                ${AP_SPAWN}   ${CMD_BOOT_PARAM}
    Close Spawn                 ${AP_SPAWN}

    Log to Console                      RESTULTS====
    Log to Console                      BOOT_PARAM: ${OUTPUT0}
    Should Contain                      ${OUTPUT0}              ${COUNTRY_CODE}
    Log to Console                      AP_COUNTRY: ${AP_COUNTRY}
    Should Contain                      ${AP_COUNTRY}           ${COUNTRY}
    Log to Console                      GET_FLAG_STATUS: ${GET_FLAG_STATUS}
    Should Not Be Equal as Integers     ${GET_FLAG_STATUS}      -1
    Log to Console                      COUNTRY_STATUS: ${COUNTRY_STATUS}
    Should Be Equal as Integers         ${COUNTRY_STATUS}       1
    Log to Console                      AP_STATUS2: ${AP_STATUS2}
    Should Be Equal as Strings          '${AP_STATUS2}'         'green'
    Log to Console                      END_RESTULTS====

Test21 - TCXM-20769 - Verify: A Country Cannot Be Reconfigured To "United States (840)"
    [Documentation]    AP, in World region, is attemped to be set to FCC. It should fail.
    [Tags]             tcxm-20769    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${result}=            Login User          ${tenant_username}    ${tenant_password}
    ${NEW_COUNTRYCODE}=   Change Country      ${ap1.serial}   840
    Refresh Devices Page
    ${SPAWN}=             Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT}=            Send Commands       ${SPAWN}      show boot-param
    Log to console        ${OUTPUT}
    Close Spawn           ${SPAWN}
    Should Not Contain Any                    ${OUTPUT}    FCC  840
    should be equal as integers               ${NEW_COUNTRYCODE}      -1

Test22 - TCXM-20771 - Verify: A Country Cannot Be Reconfigured To "Canada (124)"
    [Documentation]    AP, in World region, is attemped to be set to Canada. It should fail.
    [Tags]             tcxm-20771    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${result}=            Login User          ${tenant_username}    ${tenant_password}
    ${NEW_COUNTRYCODE}=   Change Country      ${ap1.serial}   124
    Refresh Devices Page
    ${SPAWN}=             Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT}=            Send Commands       ${SPAWN}      show boot-param
    Log to console        ${OUTPUT}
    Close Spawn           ${SPAWN}
    Should Not Contain Any                    ${OUTPUT}    Canada  124
    should be equal as integers               ${NEW_COUNTRYCODE}      -1

Test23 - TCXM-20768 - Verify: "United States (840)" Country Cannot Be Reconfigured
    [Documentation]    AP is configured to US and cannot be reconfigured to a different country.
    [Tags]             tcxm-20768    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${result}=            Login User          ${tenant_username}    ${tenant_password}
    ${SPAWN0}=            Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT1}=           Send Commands       ${SPAWN0}         mfg-set-region-code #G6L@*Sv^&<W>Cp/ 0 840, save config
    Close Spawn           ${SPAWN0}
    ${REBOOT_STATUS}=     Reboot Device       ${ap1.serial}
    Wait Until Device Reboots                 ${ap1.serial}
    Refresh Devices Page
    ${NEW_COUNTRYCODE}=    Change Country     ${ap1.serial}    356
    Refresh Devices Page
    ${SPAWN}=              Open Spawn         ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT}=            Send Commands       ${SPAWN}      show boot-param
    Log to console                            ${OUTPUT}
    Close Spawn                               ${SPAWN}
    Should Contain Any                        ${OUTPUT}    FCC     840
    should be equal as integers               ${REBOOT_STATUS}        1

Test24 - TCXM-20770 - Verify: "Canada (124)" Country Cannot Be Reconfigured
    [Documentation]    AP is configured to Canada and cannot be reconfigured to a different country.
    [Tags]             tcxm-20770    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${result}=            Login User          ${tenant_username}    ${tenant_password}
    ${SPAWN0}=            Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT1}=           Send Commands       ${SPAWN0}         mfg-set-region-code #G6L@*Sv^&<W>Cp/ 2 124, save config
    Close Spawn           ${SPAWN0}
    ${REBOOT_STATUS}=     Reboot Device       ${ap1.serial}
    Wait Until Device Reboots                 ${ap1.serial}
    Refresh Devices Page
    ${NEW_COUNTRYCODE}=    Change Country     ${ap1.serial}    356
    Refresh Devices Page
    ${SPAWN}=              Open Spawn         ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT}=            Send Commands       ${SPAWN}      show boot-param
    Log to console                            ${OUTPUT}
    Close Spawn                               ${SPAWN}
    Should Contain Any                        ${OUTPUT}    Canada     124
    should be equal as integers               ${REBOOT_STATUS}        1

*** Keywords ***
InitialSetup
    Login User      ${tenant_username}      ${tenant_password}
    delete all aps
    delete all network policies
    delete_all_ssids

    ${onboard_result}=      Onboard Device      ${ap1.serial}         ${ap1.make}       location=${ap1.location}      device_os=${ap1.os}
    ${search_result}=       Search AP Serial    ${ap1.serial}
    should be equal as integers                 ${onboard_result}     1
    should be equal as integers                 ${search_result}      1

    ${AP_SPAWN}=            Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=             Send Commands       ${AP_SPAWN}           mfg-set-region-code #G6L@*Sv^&<W>Cp/ 1 40, capwap client server name ${CAPWAP_URL}, capwap client default-server-name ${CAPWAP_URL}, capwap client server backup name ${CAPWAP_URL}, no capwap client enable, capwap client enable, save config
    ${OUTPUT0}=             Send                ${AP_SPAWN}           ${CMD_CONSOLE_PAGE_0}
    ${OUTPUT0}=             Send                ${AP_SPAWN}           ${CMD_SHOW_VERSION_DETAIL}
    ${OUTPUT0}=             Send                ${AP_SPAWN}           ${CMD_SHOW_CAPWAP_CLIENT}
    ${OUTPUT1}=             Send                ${AP_SPAWN}           ${CMD_CAPWAP_HM_PRIMARY_NAME}
    ${OUTPUT2}=             Send                ${AP_SPAWN}           ${CMD_CAPWAP_SERVER_IP}
    ${OUTPUT3}=             Wait For CLI Output                       ${AP_SPAWN}         ${CMD_CAPWAP_CLIENT_STATE}          ${OUTPUT_CAPWAP_STATUS}
    Close Spawn             ${AP_SPAWN}
    Should Be Equal as Integers                 ${OUTPUT3}            1
    sleep    60
    Wait Until Device Reboots                   ${ap1.serial}
    Log to Console                              WaitUntilCountryDiscovered
    Wait Until Country Discovered               ${ap1.serial}   60    100
    Log to Console                              WaitUntilDeviceReboots
    Wait Until Device Reboots                   ${ap1.serial}
    Sleep   60
    Logout User
    Sleep   10
    Quit Browser
