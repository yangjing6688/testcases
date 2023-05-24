*** Settings ***
Library     String
Library     Collections
Library     extauto/xiq/flows/common/Login.py
Library     extauto/xiq/flows/globalsettings/GlobalSetting.py
Library     extauto/xiq/flows/manage/Devices.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/device_commands.yaml

Force Tags       testbed_none
Suite Setup      Pre_condition
Suite Teardown   Post_condition

*** Variables ***
# change the variables valuse as per the AP
${MAKE}            Extreme - Aerohive
${MODEl}           AP5010
${SERIAL}          WM052223W-30097
${MANAGED}         Managed
${MANAGED_BY}      XIQ
${MGT_IP_ADDRESS}  10.16.187.115
${MGT_VLAN}        N/A

*** Keywords ***
Pre Condition
    [Documentation]   AP Should be onboarded  and it is online.
    ${STATUS}                           Login User    ${tenant_username}   ${tenant_password}
    should be equal as strings          '${STATUS}'   '1'

Post_condition
    Logout User
    Quit Browser

*** Test Cases ***
TCXM-19405: Verify Manage - device: Make, Model, Serial#, Managed, Managed By, Mgt IP Address, Mgt Vlan
    [Documentation]    Validating multiple Fields of an AP
    [Tags]    tcxm-19405    regression

    &{DEVICE}   create dictionary    make=get    model=get   serial=get  managed=get     managed_by=get    mgt_ip_address=get   mgt_vlan=get
    &{MANAGE_DEVICE_INFO}   create dictionary    device=&{DEVICE}

    ${OUTP}=  Get Device Details      ${ap1.serial}  ${MANAGE_DEVICE_INFO}  False
    Should Be Equal As Strings   '${OUTP}[device][make]'              '${MAKE}'
    Should Be Equal As Strings   '${OUTP}[device][model]'             '${MODEL}'
    Should Be Equal As Strings   '${OUTP}[device][serial]'            '${SERIAL}'
    Should Be Equal As Strings   '${OUTP}[device][managed]'           '${MANAGED}'
    Should Be Equal As Strings   '${OUTP}[device][managed_by]'        '${MANAGED_BY}'
    Should Be Equal As Strings   '${OUTP}[device][mgt_ip_address]'    '${MGT_IP_ADDRESS}'
    Should Be Equal As Strings   '${OUTP}[device][mgt_vlan]'          '${MGT_VLAN}'