# Author        : Philip Do
# Date          : December 2021
# Description   : APC-45525 - WiFi 6E - d360 Device configuration for AP4000/AP4000U & APC-44617 - WiFi 6E - radio profile for AP4000/AP4000U

# Pre-Condtion
# 1. AP4000 should be onboarded and online, wireless policy "AP1-policy" should be assigned to AP4000. AP CLI should be reachable by console.

*** Settings ***

Library     extauto/common/Cli.py
Library     extauto/common/TestFlow.py
Library     extauto/xiq/flows/common/Login.py
Library     extauto/xiq/flows/configure/NetworkPolicy.py
Library     extauto/xiq/flows/common/Navigator.py
Library     extauto/xiq/flows/manage/Client.py
Library     extauto/xiq/flows/manage/Devices.py
Library     extauto/xiq/flows/manage/DeviceConfig.py
Library     extauto/xiq/flows/globalsettings/GlobalSetting.py

Library     extauto/xiq/flows/configure/RadioProfile.py
Library     Collections
Library     String

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/device_commands.yaml

Force Tags   testbed_none

Test Setup       Login User        ${tenant_username}      ${tenant_password}
Test Teardown    Quit Browser

*** Variables ***

${DEVICE_TYPE}          Real
${ENTRY_TYPE}           Manual
${LOCATION}                 auto_location_01, Santa Clara, building_02, floor_04
${POLICY_01}        AP1-policy
${profile_name_2}       radio_ng_11ax-6g
${profile_name_1}       radio_ng_11ax-5g
${profile_name_0}       radio_ng_11ax-2g

@{wifi2-80-mhz-channels}     7  23  39  55  71  87  103  119  135  151  167  183  199   215
@{wifi1-20-mhz-channels}     36  40  44  48  149  153  157  161  165
@{wifi1-20-mhz-disabled-DFS-channels}     52  56  60  64  100  104  108  112  116  120  124  128  132  136  140  144
@{wifi0-20-mhz-channels}     1  2  3  4  5  6  7  8  9  10  11

@{wifi2-excluded_channels}   7  55
${wifi2-excluded_channels-CLI-1}     1
${wifi2-excluded_channels-CLI-2}     5
${wifi2-excluded_channels-CLI-3}     9
${wifi2-excluded_channels-CLI-4}     13
${wifi2-excluded_channels-CLI-5}     49
${wifi2-excluded_channels-CLI-6}     53
${wifi2-excluded_channels-CLI-7}     57
${wifi2-excluded_channels-CLI-8}     61

@{wifi1-excluded_channels}   36  48
${wifi1-excluded_channels-CLI-1}     36
${wifi1-excluded_channels-CLI-2}     48

@{wifi0-excluded_channels}   1  5  10
${wifi0-excluded_channels-CLI-1}     1
${wifi0-excluded_channels-CLI-2}     5
${wifi0-excluded_channels-CLI-3}     10

@{20mhz-unni-1-channels}     36  40  44  48
@{20mhz-unni-3-channels}     149  153  157  161  165

@{40mhz-unni-1-channels}     38  46
@{40mhz-unni-3-channels}     151  159

@{80mhz-unni-1-channels}     42
@{80mhz-unni-3-channels}     155

@{20mhz-unni-5-channels}     1  5  9  13  17  21  25  29  33  37  41  45  49  53  57  61  65  69  73  77  81  85  89  93
@{20mhz-unni-6-channels}     97  101  105  109  113
@{20mhz-unni-7-channels}     117  121  125  129  133  137  141  145  149  153  157  161  165  169  173  181  185
@{20mhz-unni-8-channels}     189  193  197  201  205  209  213  217  221  225  229

@{40mhz-unni-5-channels}     3  11  19  27  35  43  51  59  67  75  83  91
@{40mhz-unni-6-channels}     99  107
@{40mhz-unni-7-channels}     115  123  131  139  147  155  163  171  179
@{40mhz-unni-8-channels}     187  195  203  211  219  227

@{80mhz-unni-5-channels}     7  23  39  55  71  87
@{80mhz-unni-6-channels}     103
@{80mhz-unni-7-channels}     119  135  151  167  183
@{80mhz-unni-8-channels}     199  215


*** Keywords ***
Navigate To Device Config Wireless wifi2
    [teardown]     Quit Browser
    [Arguments]    ${device_mac}


*** Test Cases ***

TCXM-17044: Precondition - Setting default radio profiles on AP4000 at d360 configuration page on AP4000
   [Documentation]      Setting default radio profiles on AP4000 at d360 configuration page on AP4000
   [Tags]              tcxm_17044     tcxm-17044      development    xiq-mainline   precondition    t1

    navigate_to_device_config_interface_wireless   ${ap1.mac}
    ${rc2}   configure_custom_radio_profile         profile_name=${profile_name_2}   interface=wifi2
    Should Be Equal    '${rc2}'     '1'

    close_d360_configuration_page

    navigate_to_device_config_interface_wireless   ${ap1.mac}   interface=wifi1
    ${rc1}   configure_custom_radio_profile         profile_name=${profile_name_1}   interface=wifi1
    Should Be Equal    '${rc1}'     '1'

    close_d360_configuration_page

    navigate_to_device_config_interface_wireless   ${ap1.mac}   interface=wifi0
    ${rc0}   configure_custom_radio_profile         profile_name=${profile_name_0}   interface=wifi0
    Should Be Equal    '${rc0}'     '1'

    close_d360_configuration_page

    update_override_configuration_to_device  device_serial=${ap1.serial}
    sleep  60s


TCXM-17044: APC-45525: wifi2: Verify Default d360 Config Interface settings
    [Documentation]     To verify default config values for wifi2 interface settings at d360 page.
    [Tags]              tcxm_17044    development    xiq-mainline   tcxm-17044    t2     apc-45525    d360   wifi2

    &{fields_to_check}=   Create Dictionary   radio_profile=radio_ng_11ax-6g    client_access=ON   channel_width=80MHz

    navigate_to_device_config_interface_wireless  ${ap1.mac}   interface=wifi2
    &{wifi2_interface_detail}=   get_device_configuration_interface_wifi2_details
    Log To Console    ${wifi2_interface_detail}

    ${rc}     verify_page_details   ${wifi2_interface_detail}   ${fields_to_check}
    Should Be Equal    '${rc}'     '1'


TCXM-17449: APC-45525: wifi1: Verify Default d360 Config Interface settings
    [Documentation]     To verify default config values for wifi1 interface settings at d360 page.
    [Tags]              tcxm_17449    development    xiq-mainline   tcxm-17449    t1     apc-45525    d360   wifi1

    &{fields_to_check}=   Create Dictionary   radio_profile=radio_ng_11ax-5g    client_access=ON   channel_width=20MHz

    navigate_to_device_config_interface_wireless  ${ap1.mac}   interface=wifi1
    &{wifi1_interface_detail}=   get_device_configuration_interface_wifi1_details
    Log To Console    ${wifi1_interface_detail}

    ${rc}     verify_page_details   ${wifi1_interface_detail}   ${fields_to_check}
    Should Be Equal    '${rc}'     '1'


TCXM-17450: APC-45525: wifi0: Verify Default d360 Config Interface settings
    [Documentation]     To verify default config values for wifi0 interface settings at d360 page.
    [Tags]              tcxm_17450    development    xiq-mainline   tcxm-17450    t3     apc-45525    d360   wifi0

    &{fields_to_check}=   Create Dictionary   radio_profile=radio_ng_11ax-2g    client_access=ON   channel_width=20MHz

    navigate_to_device_config_interface_wireless  ${ap1.mac}   interface=wifi0
    &{wifi0_interface_detail}=   get_device_configuration_interface_wifi0_details
    Log To Console    ${wifi0_interface_detail}

    ${rc}     verify_page_details   ${wifi0_interface_detail}   ${fields_to_check}
    Should Be Equal    '${rc}'     '1'


TCXM-17451: APC-45525: wifi2: Verify default d360 channel width and channels
    [Documentation]     To verify default config values for wifi2 channel width and channels at d360 page.
    [Tags]              tcxm_17451    development    xiq-mainline   tcxm-17451    t2     apc-45525    d360   wifi2

    navigate_to_device_config_interface_wireless  ${ap1.mac}
    ${rc}    check_interface_channel_width_and_channels   ${wifi2-80-mhz-channels}   mode=disabled    channel_width=80
    Should Be Equal    '${rc}'     '1'
    enabe_override_channel_exclusion_setting_in_radio_profile   interface=wifi2
    ${rc}    check_interface_channel_width_and_channels   ${wifi2-80-mhz-channels}   mode=enabled    channel_width=80
    Should Be Equal    '${rc}'     '1'


TCXM-17705: APC-45525: wifi1: Verify default d360 channel width and channels
    [Documentation]     To verify default config values for wifi1 channel width and channels at d360 page.
    [Tags]              tcxm_17705    development    xiq-mainline   tcxm-17705    t2     apc-45525    d360   wifi1

    navigate_to_device_config_interface_wireless  ${ap1.mac}   interface=wifi1.
    ${rc}    check_interface_channel_width_and_channels   ${wifi1-20-mhz-channels}   mode=disabled    channel_width=20  interface=wifi1
    Should Be Equal    '${rc}'     '1'

    ${rc}    check_interface_channel_width_and_channels   ${wifi1-20-mhz-disabled-DFS-channels}   mode=disabled   channel_width=20  interface=wifi1
    Should Be Equal    '${rc}'     '1'

    enabe_override_channel_exclusion_setting_in_radio_profile   interface=wifi1
    ${rc}    check_interface_channel_width_and_channels   ${wifi1-20-mhz-channels}   mode=enabled    channel_width=20  interface=wifi1
    Should Be Equal    '${rc}'     '1'

    ${rc}    check_interface_channel_width_and_channels   ${wifi1-20-mhz-channels}   mode=included   channel_width=20  interface=wifi1
    Should Be Equal    '${rc}'     '1'


TCXM-17714: APC-45525: wifi0: Verify default d360 channel width and channels
    [Documentation]     To verify default config values for wifi0 channel width and channels at d360 page.
    [Tags]              tcxm_17714    development    xiq-mainline   tcxm-17714    t3     apc-45525    d360   wifi0

    navigate_to_device_config_interface_wireless  ${ap1.mac}   interface=wifi0

    ${rc}    check_interface_channel_width_and_channels   ${wifi0-20-mhz-channels}   mode=enabled    channel_width=20  interface=wifi0
    Should Be Equal    '${rc}'     '1'


TCXM-17715: APC-45525: wifi2: Override excluded channels, include/exclude channels - Step1
    [Documentation]     To verify that user can override excluded channels, exclude/include selected channels on wifi2.
    [Tags]              tcxm_17715    development    xiq-mainline   tcxm-17715    t2     apc-45525    d360   wifi2

    navigate_to_device_config_interface_wireless   ${ap1.mac}
    ${rc}    make_interface_channels_included_excluded    ${wifi2-excluded_channels}  mode=excluded   interface=wifi2
    Should Be Equal    '${rc}'     '1'


TCXM-17715: APC-45525: wifi2: Override excluded channels, include/exclude channels - Step2
    [Documentation]     To verify that user can override excluded channels, exclude/include selected channels on wifi2.
    [Tags]              tcxm_17715    development    xiq-mainline   tcxm-17715    t2     apc-45525    d360   wifi2

    ${DEPLOY_STATUS}=       Deploy Network Policy with Delta Update     ${POLICY_01}          ${ap1.serial}
    Wait Until Device Online    ${ap1.serial}

    ${AP_SPAWN}=        Open Spawn          ${ap1.ip}   ${ap1.port}   ${ap1.username}   ${ap1.password}    ${ap1.cli_type}
    ${OUTPUT}=          Send Commands       ${AP_SPAWN}         console page 0, show running-config | include exclude

    Log To Console      ** Validate 1 - displays corresponding 20 MHz channels displayed in AP CLI **
    Should Contain      ${OUTPUT}     interface wifi2 radio channel exclude ${wifi2-excluded_channels-CLI-1}

    Log To Console      ** Validate 2 - displays corresponding 20 MHz channels displayed in AP CLI **
    Should Contain      ${OUTPUT}     interface wifi2 radio channel exclude ${wifi2-excluded_channels-CLI-2}

    Log To Console      ** Validate 3 - displays corresponding 20 MHz channels displayed in AP CLI **
    Should Contain      ${OUTPUT}     interface wifi2 radio channel exclude ${wifi2-excluded_channels-CLI-3}

    Log To Console      ** Validate 4 - displays corresponding 20 MHz channels displayed in AP CLI **
    Should Contain      ${OUTPUT}     interface wifi2 radio channel exclude ${wifi2-excluded_channels-CLI-4}

    Log To Console      ** Validate 5 - displays corresponding 20 MHz channels displayed in AP CLI **
    Should Contain      ${OUTPUT}     interface wifi2 radio channel exclude ${wifi2-excluded_channels-CLI-5}

    Log To Console      ** Validate 6 - displays corresponding 20 MHz channels displayed in AP CLI **
    Should Contain      ${OUTPUT}     interface wifi2 radio channel exclude ${wifi2-excluded_channels-CLI-6}

    Log To Console      ** Validate 7 - displays corresponding 20 MHz channels displayed in AP CLI **
    Should Contain      ${OUTPUT}     interface wifi2 radio channel exclude ${wifi2-excluded_channels-CLI-7}

    Log To Console      ** Validate 8 - displays corresponding 20 MHz channels displayed in AP CLI **
    Should Contain      ${OUTPUT}     interface wifi2 radio channel exclude ${wifi2-excluded_channels-CLI-8}

    Close Spawn         ${AP_SPAWN}


TCXM-17716: APC-45525: wifi1: Override excluded channels, include/exclude channels - Step1
    [Documentation]     To verify that user can override excluded channels, exclude/include selected channels on wifi1.
    [Tags]              tcxm_17716    development    xiq-mainline   tcxm-17716    t1     apc-45525    d360   wifi1

    navigate_to_device_config_interface_wireless   ${ap1.mac}   interface=wifi1
    ${rc}    make_interface_channels_included_excluded    ${wifi1-excluded_channels}  mode=excluded   interface=wifi1
    Should Be Equal    '${rc}'     '1'


TCXM-17716: APC-45525: wifi1: Override excluded channels, include/exclude channels - Step2
    [Documentation]     To verify that user can override excluded channels, exclude/include selected channels on wifi1.
    [Tags]              tcxm_17716    development    xiq-mainline   tcxm-17716    t1     apc-45525    d360   wifi1

    ${DEPLOY_STATUS}=       Deploy Network Policy with Delta Update     ${POLICY_01}          ${ap1.serial}
    Wait Until Device Online    ${ap1.serial}

    ${AP_SPAWN}=        Open Spawn          ${ap1.ip}   ${ap1.port}   ${ap1.username}   ${ap1.password}    ${ap1.cli_type}
    ${OUTPUT}=          Send Commands       ${AP_SPAWN}         console page 0, show running-config | include exclude

    Log To Console      ** Validate 1  **
    Should Contain      ${OUTPUT}     interface wifi1 radio channel exclude ${wifi1-excluded_channels-CLI-1}

    Log To Console      ** Validate 2  **
    Should Contain      ${OUTPUT}     interface wifi1 radio channel exclude ${wifi1-excluded_channels-CLI-2}

    Close Spawn         ${AP_SPAWN}


TCXM-17717: APC-45525: wifi0: Override excluded channels, include/exclude channels - Step1
    [Documentation]     To verify that user can override excluded channels, exclude/include selected channels on wifi0.
    [Tags]              tcxm_17717    development    xiq-mainline   tcxm-17717    t3     apc-45525    d360   wifi0

    navigate_to_device_config_interface_wireless   ${ap1.mac}    interface=wifi0
    ${rc}    make_interface_channels_included_excluded    ${wifi0-excluded_channels}  mode=excluded   interface=wifi0
    Should Be Equal    '${rc}'     '1'


TCXM-17717: APC-45525: wifi0: Override excluded channels, include/exclude channels - Step2
    [Documentation]     To verify that user can override excluded channels, exclude/include selected channels on wifi0.
    [Tags]              tcxm_17717    development    xiq-mainline   tcxm-17717    t3     apc-45525    d360   wifi0

    ${DEPLOY_STATUS}=       Deploy Network Policy with Delta Update     ${POLICY_01}          ${ap1.serial}
    Wait Until Device Online    ${ap1.serial}

    ${AP_SPAWN}=        Open Spawn          ${ap1.ip}   ${ap1.port}   ${ap1.username}   ${ap1.password}    ${ap1.cli_type}
    ${OUTPUT}=          Send Commands       ${AP_SPAWN}         console page 0, show running-config | include exclude

    Log To Console      ** Validate 1  **
    Should Contain      ${OUTPUT}     interface wifi0 radio channel exclude ${wifi0-excluded_channels-CLI-1}

    Log To Console      ** Validate 2  **
    Should Contain      ${OUTPUT}     interface wifi0 radio channel exclude ${wifi0-excluded_channels-CLI-2}

    Log To Console      ** Validate 3  **
    Should Contain      ${OUTPUT}     interface wifi0 radio channel exclude ${wifi0-excluded_channels-CLI-3}

    Close Spawn         ${AP_SPAWN}


TCXM-17718: APC-44617: wifi2: Create new radio profile and verify settings - Test step1
   [Documentation]    Test Step1: Add a new radio profile from The Common Objects; Verify The Default wifi2 setting and excluded Channels.
   [Tags]       tcxm_17718    development    xiq-mainline   tcxm-17718    t1     apc-44617    radio-profile   wifi2      step1    console1

   ${profile_name}=    Generate Random String  12
   ${profile_name}=    Set Variable  ${profile_name}ax(6GHz)

   Set Suite Variable  ${profile_name}
   navigate_to_radio_profile
   add_radio_profile   ${profile_name}
   choose_radio_profile_radio_mode     ax (6GHz)

   ${rc}    verify_radio_profile_channel_width_and_channels   ${wifi2-80-mhz-channels}   mode=included  channel_width=80
   Should Be Equal    '${rc}'     '1'

   ${rc}    verify_radio_profile_channel_width_and_channels   ${wifi2-80-mhz-channels}   mode=enabled  channel_width=80
   Should Be Equal    '${rc}'     '1'

   ${rc}    select_radio_profile_excluded_channels   ${wifi2-excluded_channels}
   Should Be Equal    '${rc}'     '1'

   ${rc}    verify_radio_profile_channel_width_and_channels   ${wifi2-excluded_channels}   mode=excluded  channel_width=80
   Should Be Equal    '${rc}'     '1'

   save_radio_profile   ${profile_name}


TCXM-17718: APC-44617: wifi2: Create new radio profile and verify settings - Test step2
   [Documentation]      Test Step2: Apply a customized Radio Profile with Excluded Channels in d360 wifi2 Interface
   [Tags]              tcxm_17718    development    xiq-mainline   tcxm-17718    t1     apc-44617    radio-profile   wifi2      step2     console1

   navigate_to_device_config_interface_wireless   ${ap1.mac}   interface=wifi2
   ${rc}   configure_custom_radio_profile         profile_name=${profile_name}   interface=wifi2
   Should Be Equal    '${rc}'     '1'


TCXM-17718: APC-44617: wifi2: Create new radio profile and verify settings - Test step3
# Pre-requisite - AP4000 is onboarded and AP must need to have any wireless policy assigned.
    [Documentation]    Test Step3: Validate The Device Config with the new radio profile assigned to AP
    [Tags]       tcxm_17718    development    xiq-mainline   tcxm-17718    t1     apc-44617    radio-profile   wifi2      step3   console1

    update_override_configuration_to_device  device_serial=${ap1.serial}
    sleep  60s

    ${AP_SPAWN}=        Open Spawn          ${ap1.ip}   ${ap1.port}   ${ap1.username}   ${ap1.password}    ${ap1.cli_type}
    ${OUTPUT}=          Send Commands       ${AP_SPAWN}         console page 0, show running-config | include radio
    sleep  20s

    Log To Console      ** Validate 1 **
#    Should Contain      ${OUTPUT}     interface wifi2 radio profile ${profile_name}
    Should Contain      ${OUTPUT}     radio profile ${profile_name}
    sleep  10s

    Log To Console      ** Validate 2 **
    Should Contain      ${OUTPUT}     radio profile ${profile_name} phymode 11ax-6g
    sleep  5s

    Log To Console      ** Validate 3 **
    Should Contain      ${OUTPUT}     radio profile ${profile_name} channel-width 80
    sleep  5s

    Close Spawn         ${AP_SPAWN}


TCXM-17718: APC-44617: wifi2: Create new radio profile and verify settings - Test step4
    [Documentation]     Test Step4: Verify The New Radio mode and excluded channels In d360 wifi2 Interface
    [Tags]              tcxm_17718    development    xiq-mainline   tcxm-17718    t1     apc-44617    radio-profile   wifi2      step4    console1

    navigate_to_device_config_interface_wireless    ${ap1.mac}    interface=wifi2

    enabe_override_channel_exclusion_setting_in_radio_profile   interface=wifi2
    ${rc}    check_interface_channel_width_and_channels   ${wifi2-excluded_channels}   mode=excluded  channel_width=80
    Should Be Equal    '${rc}'     '1'


TCXM-18403: APC-44617: wifi1: Create new radio profile and verify settings - Test step1
   [Documentation]    Test Step1: Add a new radio profile from The Common Objects; Verify The Default wifi1 setting and excluded Channels.
   [Tags]       tcxm_18403    development    xiq-mainline   tcxm-18403    t2     apc-44617    radio-profile   wifi1      step1    console1

   ${profile_name}=    Generate Random String  12
   ${profile_name}=    Set Variable  ${profile_name}ax(5GHz)

   Set Suite Variable  ${profile_name}
   navigate_to_radio_profile
   add_radio_profile   ${profile_name}
   choose_radio_profile_radio_mode     ax (5GHz)

   ${rc}    verify_radio_profile_channel_width_and_channels   ${wifi1-20-mhz-channels}   mode=included  channel_width=20
   Should Be Equal    '${rc}'     '1'

   ${rc}    verify_radio_profile_channel_width_and_channels   ${wifi1-20-mhz-channels}   mode=enabled  channel_width=20
   Should Be Equal    '${rc}'     '1'

   ${rc}    select_radio_profile_excluded_channels   ${wifi1-excluded_channels}
   Should Be Equal    '${rc}'     '1'

   ${rc}    verify_radio_profile_channel_width_and_channels   ${wifi1-excluded_channels}   mode=excluded  channel_width=20
   Should Be Equal    '${rc}'     '1'

   save_radio_profile   ${profile_name}


TCXM-18403: APC-44617: wifi1: Create new radio profile and verify settings - Test step2
    [Documentation]     Test Step2: Apply a customized Radio Profile with Excluded Channels in d360 wifi1 Interface
    [Tags]              tcxm_18403    development    xiq-mainline   tcxm-18403    t2     apc-44617    radio-profile   wifi1      step2    console1

    navigate_to_device_config_interface_wireless   ${ap1.mac}   interface=wifi1
    ${rc}   configure_custom_radio_profile         profile_name=${profile_name}   interface=wifi1
    Should Be Equal    '${rc}'     '1'


TCXM-18403: APC-44617: wifi1: Create new radio profile and verify settings - Test step3
    [Documentation]     Test Step3: Validate The Device Config with the new radio profile assigned to AP
    [Tags]              tcxm_18403    development    xiq-mainline   tcxm-18403    t2     apc-44617    radio-profile   wifi1      step3    console1

    update_override_configuration_to_device  device_serial=${ap1.serial}
    sleep  60s

    ${AP_SPAWN}=        Open Spawn          ${ap1.ip}   ${ap1.port}   ${ap1.username}   ${ap1.password}    ${ap1.cli_type}
    ${OUTPUT}=          Send Commands       ${AP_SPAWN}         console page 0, show running-config | include radio

    Log To Console      ** Validate 1 **
#    Should Contain      ${OUTPUT}     interface wifi1 radio profile ${profile_name}
    Should Contain      ${OUTPUT}     radio profile ${profile_name}

    Log To Console      ** Validate 2 **
    Should Contain      ${OUTPUT}     radio profile ${profile_name} phymode 11ax-5g

    Close Spawn         ${AP_SPAWN}


TCXM-18403: APC-44617: wifi1: Create new radio profile and verify settings - Test step4
    [Documentation]     Test Step3: Verify The New Radio mode and excluded channels In d360 wifi1 Interface
    [Tags]              tcxm_18403    development    xiq-mainline   tcxm-18403    t2     apc-44617    radio-profile   wifi1      step4    console1

    navigate_to_device_config_interface_wireless    ${ap1.mac}    interface=wifi1

    enabe_override_channel_exclusion_setting_in_radio_profile   interface=wifi1
    ${rc}    check_interface_channel_width_and_channels   ${wifi1-excluded_channels}   mode=excluded  channel_width=20  interface=wifi1
    Should Be Equal    '${rc}'     '1'


TCXM-18404: APC-44617: wifi0: Create new radio profile and verify settings - Test step1
   [Documentation]    Test Step1: Add a new radio profile from The Common Objects; Verify The Default wifi0 setting and excluded Channels.
   [Tags]       tcxm_18404    development    xiq-mainline   tcxm-18404    t3     apc-44617    radio-profile   wifi0      step1

   ${profile_name}=    Generate Random String  12
   ${profile_name}=    Set Variable  ${profile_name}ax(2.4GHz)

   Set Suite Variable  ${profile_name}
   navigate_to_radio_profile
   add_radio_profile   ${profile_name}
   choose_radio_profile_radio_mode     ax (2.4GHz)

   ${rc}    verify_radio_profile_channel_width_and_channels   ${wifi0-20-mhz-channels}   mode=included  channel_width=20
   Should Be Equal    '${rc}'     '1'

   ${rc}    verify_radio_profile_channel_width_and_channels   ${wifi0-20-mhz-channels}   mode=enabled  channel_width=20
   Should Be Equal    '${rc}'     '1'

   ${rc}    select_radio_profile_excluded_channels   ${wifi0-excluded_channels}
   Should Be Equal    '${rc}'     '1'

   ${rc}    verify_radio_profile_channel_width_and_channels   ${wifi0-excluded_channels}   mode=excluded  channel_width=20
   Should Be Equal    '${rc}'     '1'

   save_radio_profile   ${profile_name}


TCXM-18404: APC-44617: wifi0: Create new radio profile and verify settings - Test step2
    [Documentation]     Test Step2: Apply a customized Radio Profile with Excluded Channels in d360 wifi0 Interface
    [Tags]              tcxm_18404    development    xiq-mainline   tcxm-18404    t3     apc-44617    radio-profile   wifi0      step2

    navigate_to_device_config_interface_wireless   ${ap1.mac}   interface=wifi0
    ${rc}   configure_custom_radio_profile         profile_name=${profile_name}   interface=wifi0
    Should Be Equal    '${rc}'     '1'


TCXM-18404: APC-44617: wifi0: Create new radio profile and verify settings - Test step3
    [Documentation]     Test Step3: Verify The New Radio mode and excluded channels In d360 wifi0 Interface
    [Tags]              tcxm_18404    development    xiq-mainline   tcxm-18404    t3     apc-44617    radio-profile   wifi0      step3

    navigate_to_device_config_interface_wireless    ${ap1.mac}    interface=wifi0

    ${rc}    check_interface_channel_width_and_channels   ${wifi0-excluded_channels}   mode=excluded  channel_width=20  interface=wifi0
    Should Be Equal    '${rc}'     '1'


TCXM-18405: APC-44617: Verify The Radio Profile Details with the radio mode ax (5GHz)
    [Documentation]     To verify default config for radio profile with ax (5GHz) mode under common objects.
    [Tags]              tcxm_18405    development    xiq-mainline   tcxm-18405    t3     apc-44617    radio-profile

    &{fields_to_check1}=   Create Dictionary    supported_radio_modes=ax (5GHz)   radio_profile_maximum_transmit_power=20  radio_profile_transmit_power_floor=5
    &{fields_to_check2}=   Create Dictionary    tranmission_power_max_drop=9     maximum_number_of_clients=100            channel_auto_or_manual=Auto
    &{fields_to_check3}=   Create Dictionary    tranmission_power=Auto            transmission_power_control=OFF           background_scan=ON

    navigate_to_radio_profile
    add_radio_profile   sample_radio_profile_abc
    choose_radio_profile_radio_mode     ax (5GHz)
    &{radio_detail_info}       get_radio_profile_details
    Log To Console    ${radio_detail_info}

    Log To Console    Verify 1
    ${rc}     verify_page_details   ${radio_detail_info}   ${fields_to_check1}
    Should Be Equal    '${rc}'     '1'

    Log To Console    Verify 2
    ${rc}     verify_page_details   ${radio_detail_info}   ${fields_to_check2}
    Should Be Equal    '${rc}'     '1'

    Log To Console    Verify 3
    ${rc}     verify_page_details   ${radio_detail_info}   ${fields_to_check3}
    Should Be Equal    '${rc}'     '1'


TCXM-18407: APC-44617: channels for UNII-1 and UNII-3 with channel width 20 MHz for ax (5GHz)
    [Documentation]     Verify default Channels for UNII-1 and UNII-3 with channel width 20 MHz for the radio mode ax (5GHz).
    [Tags]              tcxm_18407    development    xiq-mainline   tcxm-18407    t3     apc-44617    radio-profile      5ghz

    navigate_to_radio_profile
    add_radio_profile   abcde
    choose_radio_profile_radio_mode     ax (5GHz)

    ${rc}    verify_uni_group_channels   ${20mhz-unni-1-channels}   group_channel=uni-1  mode=enabled
    Should Be Equal    '${rc}'     '1'

    ${rc}    verify_uni_group_channels   ${20mhz-unni-3-channels}   group_channel=uni-3  mode=enabled
    Should Be Equal    '${rc}'     '1'


TCXM-18408: APC-44617: channels for UNII-1 and UNII-3 with channel width 40 MHz for ax (5GHz)
    [Documentation]     Verify default Channels for UNII-1 and UNII-3 with channel width 40 MHz for the radio mode ax (5GHz).
    [Tags]              tcxm_18408    development    xiq-mainline   tcxm-18408    t3     apc-44617    radio-profile      5ghz

    navigate_to_radio_profile
    add_radio_profile   abcde
    choose_radio_profile_radio_mode     ax (5GHz)

    ${rc}    verify_uni_group_channels   ${40mhz-unni-1-channels}   group_channel=uni-1  mode=enabled  channel_width=40MHZ
    Should Be Equal    '${rc}'     '1'

    ${rc}    verify_uni_group_channels   ${40mhz-unni-3-channels}   group_channel=uni-1  mode=enabled  channel_width=40MHZ
    Should Be Equal    '${rc}'     '1'


TCXM-18409: APC-44617: channels for UNII-1 and UNII-3 with channel width 80 MHz for ax (5GHz)
    [Documentation]     Verify default Channels for UNII-1 and UNII-3 with channel width 80 MHz for the radio mode ax (5GHz).
    [Tags]              tcxm_18409    development    xiq-mainline   tcxm-18409    t3     apc-44617    radio-profile      5ghz

    navigate_to_radio_profile
    add_radio_profile   abcde
    choose_radio_profile_radio_mode     ax (5GHz)

    ${rc}    verify_uni_group_channels   ${80mhz-unni-1-channels}   group_channel=uni-1  mode=enabled  channel_width=80MHZ
    Should Be Equal    '${rc}'     '1'

    ${rc}    verify_uni_group_channels   ${80mhz-unni-3-channels}   group_channel=uni-1  mode=enabled  channel_width=80MHZ
    Should Be Equal    '${rc}'     '1'


TCXM-18410: APC-44617: channels for UNII-5 to UNII-8 with channel width 20 MHz for ax (6GHz)
    [Documentation]     Verify default Channels for UNII-5 to UNII-8 with channel width 20 MHz for the radio mode ax (6GHz).
    [Tags]              tcxm_18410    development    xiq-mainline   tcxm-18410    t3     apc-44617    radio-profile      6ghz

    navigate_to_radio_profile
    add_radio_profile   abcde
    choose_radio_profile_radio_mode     ax (6GHz)

    ${rc}    verify_uni_group_channels   ${20mhz-unni-5-channels}   group_channel=uni-5  mode=enabled  channel_width=20MHZ
    Should Be Equal    '${rc}'     '1'

    ${rc}    verify_uni_group_channels   ${20mhz-unni-6-channels}   group_channel=uni-6  mode=enabled  channel_width=20MHZ
    Should Be Equal    '${rc}'     '1'

    ${rc}    verify_uni_group_channels   ${20mhz-unni-7-channels}   group_channel=uni-7  mode=enabled  channel_width=20MHZ
    Should Be Equal    '${rc}'     '1'

    ${rc}    verify_uni_group_channels   ${20mhz-unni-8-channels}   group_channel=uni-8  mode=enabled  channel_width=20MHZ
    Should Be Equal    '${rc}'     '1'


TCXM-18411: APC-44617: channels for UNII-5 to UNII-8 with channel width 40 MHz for ax (6GHz)
    [Documentation]     Verify default Channels for UNII-5 to UNII-8 with channel width 40 MHz for the radio mode ax (6GHz).
    [Tags]              tcxm_18411    development    xiq-mainline   tcxm-18411    t3     apc-44617    radio-profile      6ghz

    navigate_to_radio_profile
    add_radio_profile   abcde
    choose_radio_profile_radio_mode     ax (6GHz)

    ${rc}    verify_uni_group_channels   ${40mhz-unni-5-channels}   group_channel=uni-5  mode=enabled  channel_width=40MHZ
    Should Be Equal    '${rc}'     '1'

    ${rc}    verify_uni_group_channels   ${40mhz-unni-6-channels}   group_channel=uni-6  mode=enabled  channel_width=40MHZ
    Should Be Equal    '${rc}'     '1'

    ${rc}    verify_uni_group_channels   ${40mhz-unni-7-channels}   group_channel=uni-7  mode=enabled  channel_width=40MHZ
    Should Be Equal    '${rc}'     '1'

    ${rc}    verify_uni_group_channels   ${40mhz-unni-8-channels}   group_channel=uni-8  mode=enabled  channel_width=40MHZ
    Should Be Equal    '${rc}'     '1'


TCXM-18412: APC-44617: channels for UNII-5 to UNII-8 with channel width 80 MHz for ax (6GHz)
    [Documentation]     Verify default Channels for UNII-5 to UNII-8 with channel width 80 MHz for the radio mode ax (6GHz).
    [Tags]              tcxm_18412    development    xiq-mainline   tcxm-18412    t3     apc-44617    radio-profile      6ghz

    navigate_to_radio_profile
    add_radio_profile   abcde
    choose_radio_profile_radio_mode     ax (6GHz)

    ${rc}    verify_uni_group_channels   ${80mhz-unni-5-channels}   group_channel=uni-5  mode=enabled  channel_width=80MHZ
    Should Be Equal    '${rc}'     '1'

    ${rc}    verify_uni_group_channels   ${80mhz-unni-6-channels}   group_channel=uni-6  mode=enabled  channel_width=80MHZ
    Should Be Equal    '${rc}'     '1'

    ${rc}    verify_uni_group_channels   ${80mhz-unni-7-channels}   group_channel=uni-7  mode=enabled  channel_width=80MHZ
    Should Be Equal    '${rc}'     '1'

    ${rc}    verify_uni_group_channels   ${80mhz-unni-8-channels}   group_channel=uni-8  mode=enabled  channel_width=80MHZ
    Should Be Equal    '${rc}'     '1'


TCXM-18412: cleanup - Setting default radio profiles
   [Documentation]      Setting default radio profiles at the end of test.
   [Tags]              tcxm_18412     tcxm-18412      development    xiq-mainline     t2

    navigate_to_device_config_interface_wireless   ${ap1.mac}
    ${rc2}   configure_custom_radio_profile         profile_name=${profile_name_2}   interface=wifi2
    Should Be Equal    '${rc2}'     '1'

    close_d360_configuration_page

    navigate_to_device_config_interface_wireless   ${ap1.mac}   interface=wifi1
    ${rc1}   configure_custom_radio_profile         profile_name=${profile_name_1}   interface=wifi1
    Should Be Equal    '${rc1}'     '1'

    close_d360_configuration_page

    navigate_to_device_config_interface_wireless   ${ap1.mac}   interface=wifi0
    ${rc0}   configure_custom_radio_profile         profile_name=${profile_name_0}   interface=wifi0
    Should Be Equal    '${rc0}'     '1'

    close_d360_configuration_page

    update_override_configuration_to_device  device_serial=${ap1.serial}
    sleep  60s
