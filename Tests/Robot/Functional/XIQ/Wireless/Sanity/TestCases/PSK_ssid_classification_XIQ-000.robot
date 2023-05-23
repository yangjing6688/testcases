#########################################################################################################
# Author        : Binh Nguyen
# Date          : Mar 23rd 2023
# Description   : TCXM-50782 Location based classification
#                 TCXM-50784 CCG based classification
#########################################################################################################

**** Variables ***
################## Policy Detail & Wireless Network ###############################
&{WIRELESS_PESRONAL_00}     ssid_name=w0_1_sc_loc    network_type=Standard    ssid_profile=&{BORADCAST_SSID_00}     auth_profile=&{PERSONAL_AUTH_PROFILE_00}
&{WIRELESS_PESRONAL_01}     ssid_name=w0_1_mil_loc   network_type=Standard    ssid_profile=&{BORADCAST_SSID_00}     auth_profile=&{PERSONAL_AUTH_PROFILE_00}
&{WIRELESS_PESRONAL_02}     ssid_name=w0_1_sc_ccg    network_type=Standard    ssid_profile=&{BORADCAST_SSID_00}     auth_profile=&{PERSONAL_AUTH_PROFILE_00}
&{WIRELESS_PESRONAL_03}     ssid_name=w0_1_mil_cgg   network_type=Standard    ssid_profile=&{BORADCAST_SSID_00}     auth_profile=&{PERSONAL_AUTH_PROFILE_00}

&{BORADCAST_SSID_00}           WIFI0=Enable        WIFI1=Enable      WIFI2=Disable
&{PERSONAL_AUTH_PROFILE_00}    auth_type=PSK   key_encryption=&{PSK_KEY_ENCRYPTION_00}   cwp_config=&{PSK_CWP_00}
&{PSK_KEY_ENCRYPTION_00}       key_management=WPA2-(WPA2 Personal)-PSK    encryption_method=CCMP (AES)    key_type=ASCII Key   key_value=aerohive
&{PSK_CWP_00}                  enable_cwp=Disable

&{CLASS_LOC_00}                classification_rule_name=santaclara_loc     description=ap1_santa_clara_building_02_floor_04
...                            country_node=auto_location_01     loc_node=Santa Clara     building_node=building_02    floor_node=floor_04
&{CLASS_LOC_01}                classification_rule_name=milpitas_loc        description=ap2_milpitas_building_04_floor_05
...                            country_node=auto_location_01     loc_node=Milpitas        building_node=building_04    floor_node=floor_05

&{CCG_00}                      name=ap1_ccg    description=ap1_cloud_config_group    ap=${ap1.serial}
&{CCG_01}                      name=ap2_cgg    description=ap2_cloud_config_group    ap=${ap2.serial}
&{CLASS_CCG_00}                classification_rule_name=santaclara_ccg     description=ap1_classification_ccg     match_type=yes    group_name=${CCG_00}[name]
&{CLASS_CCG_01}                classification_rule_name=Milpitas_ccg       description=ap2_classification_ccg     match_type=yes    group_name=${CCG_01}[name]

################## Device Templates ###############################
&{AP_TEMPLATE_1}         wifi0_configuration=&{AP_TEMPLATE_1_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_1_WIFI1}
&{AP_TEMPLATE_1_WIFI0}   radio_status=On     radio_profile=radio_ng_11ax-2g     client_mode=Disable    client_access=Enable    backhaul_mesh_link=Disable
&{AP_TEMPLATE_1_WIFI1}   radio_status=On     radio_profile=radio_ng_11ax-5g     client_mode=Disable    client_access=Enable    backhaul_mesh_link=Disable

############### Globle Variables ######################
${retry}         3

*** Settings ***
Library     String
Library     Collections
Library     DependencyLibrary

Library     common/Cli.py
Library     common/Utils.py

# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     xiq/flows/manage/Location.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/DevicesActions.py
Library     xiq/flows/manage/DeviceConfig.py
Library     xiq/flows/manage/DeviceCliAccess.py

Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/configure/DeviceTemplate.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/configure/CloudConfigGroup.py
Library     xiq/flows/configure/ClassificationRule.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Force Tags       testbed_none
Suite Setup      Pre_condition
Suite Teardown   Post_condition

*** Test Cases ***
Step1: Create Policies with Classication Rules
    [Documentation]     Create Policies with Classication Rules
    [Tags]              tcxm-50782   tcxm-50784   development   p1   px

    Set Suite Variable             ${POLICY_00}                    per_ssid_class_loc
    Set Suite Variable             ${POLICY_01}                    per_ssid_class_ccg
    Set Suite Variable             ${AP_TEMP_NAME_00}              ${ap1.model}_ssid_classification
    Set Suite Variable             ${AP_TEMP_NAME_01}              ${ap2.model}_ssid_classification

    ${STATUS}                      Add Classification Rule with Location      ${CLASS_LOC_00}[classification_rule_name]   ${CLASS_LOC_00}[description]   ${CLASS_LOC_00}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Add Classification Rule with Location      ${CLASS_LOC_01}[classification_rule_name]   ${CLASS_LOC_01}[description]   ${CLASS_LOC_01}
    should be equal as strings     '${STATUS}'        '1'

    ${STATUS}                      Add Cloud Config Group                     ${CCG_00}[name]                             ${CCG_00}[description]         ${CCG_00}[ap]
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Add Classification Rule with CCG           ${CLASS_CCG_00}[classification_rule_name]   ${CLASS_CCG_00}[description]
    ...                                                                       ${CLASS_CCG_00}[match_type]   ${CLASS_CCG_00}[group_name]
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Add Cloud Config Group                     ${CCG_01}[name]                             ${CCG_01}[description]         ${CCG_01}[ap]
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Add Classification Rule with CCG           ${CLASS_CCG_01}[classification_rule_name]   ${CLASS_CCG_01}[description]
    ...                                                                       ${CLASS_CCG_01}[match_type]   ${CLASS_CCG_01}[group_name]
    should be equal as strings     '${STATUS}'        '1'

    ${STATUS}                      create network policy if does not exist    ${POLICY_00}         ${WIRELESS_PESRONAL_00}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      create ssid to policy                      ${POLICY_00}         &{WIRELESS_PESRONAL_01}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Add Classification Rule to SSID            ${POLICY_00}         ${WIRELESS_PESRONAL_00}[ssid_name]    ${CLASS_LOC_00}[classification_rule_name]
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Add Classification Rule to SSID            ${POLICY_00}         ${WIRELESS_PESRONAL_01}[ssid_name]    ${CLASS_LOC_01}[classification_rule_name]
    should be equal as strings     '${STATUS}'        '1'

    ${STATUS}                      create network policy if does not exist    ${POLICY_01}         ${WIRELESS_PESRONAL_02}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      create ssid to policy                      ${POLICY_01}         &{WIRELESS_PESRONAL_03}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Add Classification Rule to SSID            ${POLICY_01}         ${WIRELESS_PESRONAL_02}[ssid_name]    ${CLASS_CCG_00}[classification_rule_name]
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Add Classification Rule to SSID            ${POLICY_01}         ${WIRELESS_PESRONAL_03}[ssid_name]    ${CLASS_CCG_01}[classification_rule_name]
    should be equal as strings     '${STATUS}'        '1'

    ${STATUS}                      add ap template from common object         ${ap1.model}         ${AP_TEMP_NAME_00}    ${AP_TEMPLATE_1}
    Should Be Equal As Strings     '${STATUS}'        '1'
    ${STATUS}                      add ap template from common object         ${ap2.model}         ${AP_TEMP_NAME_01}    ${AP_TEMPLATE_1}
    Should Be Equal As Strings     '${STATUS}'        '1'
    ${STATUS}                      add ap template to network policy          ${AP_TEMP_NAME_00}   ${POLICY_00}
    Should Be Equal As Strings     '${STATUS}'        '1'
    ${STATUS}                      add ap template to network policy          ${AP_TEMP_NAME_01}   ${POLICY_00}
    Should Be Equal As Strings     '${STATUS}'        '1'
    ${STATUS}                      add ap template to network policy          ${AP_TEMP_NAME_00}   ${POLICY_01}
    Should Be Equal As Strings     '${STATUS}'        '1'
    ${STATUS}                      add ap template to network policy          ${AP_TEMP_NAME_01}   ${POLICY_01}
    Should Be Equal As Strings     '${STATUS}'        '1'

Step2: Assign network policy with Classification on location to AP1 and AP2
    [Documentation]     Assign network policy with Classification on location to AP1 and AP2
    [Tags]              tcxm-50782   development   p2   px

    Depends On Test     Step1: Create Policies with Classication Rules
    ${UPDATE}                      Update Network Policy To All Devices        ${POLICY_00}         Complete
    should be equal as strings     '${UPDATE}'         '1'
    Wait_device_online             ${ap1}
    Wait_device_online             ${ap2}

Step3: Verify AP1 and AP2 with Classification on location
    [Documentation]     Verify AP1 and AP2 with Classification on location
    [Tags]              tcxm-50782   development   p3   px

    Depends On Test     Step2: Assign network policy with Classification on location to AP1 and AP2
    Verify_AP_with_Classification     ${ap1}    ${CLASS_LOC_00}    ${WIRELESS_PESRONAL_00}
    Verify_AP_with_Classification     ${ap2}    ${CLASS_LOC_01}    ${WIRELESS_PESRONAL_01}

Step4: Assign network policy with Classification on ccg to AP1 and AP2
    [Documentation]     Assign network policy with Classification on ccg to AP1 and AP2
    [Tags]              tcxm-50784   development   p4   px

    Depends On Test     Step1: Create Policies with Classication Rules
    ${UPDATE}                      Update Network Policy To All Devices        ${POLICY_01}         Complete
    should be equal as strings     '${UPDATE}'         '1'
    Wait_device_online             ${ap1}
    Wait_device_online             ${ap2}

Step5: Verify AP1 and AP2 with Classification on ccg
    [Documentation]     Verify AP1 and AP2 with Classification on ccg
    [Tags]              tcxm-50784   development   p5   px

    Depends On Test     Step4: Assign network policy with Classification on ccg to AP1 and AP2
    Verify_AP_with_Classification    ${ap1}    ${CLASS_LOC_00}    ${WIRELESS_PESRONAL_02}
    Verify_AP_with_Classification    ${ap2}    ${CLASS_LOC_01}    ${WIRELESS_PESRONAL_03}

*** Keywords ***
Pre_condition
    ${STATUS}                       Login User    ${tenant_username}   ${tenant_password}
    should be equal as strings      '${STATUS}'   '1'
    reset devices to default
    log to console                  Wait for 2 minutes for completing reboot....
    sleep                           2m
    delete all devices
    delete all network policies
    delete all ssids
    delete all ap templates
    Delete Classification rules     ${CLASS_LOC_00}[classification_rule_name]    ${CLASS_LOC_01}[classification_rule_name]
    ...                             ${CLASS_CCG_00}[classification_rule_name]    ${CLASS_CCG_01}[classification_rule_name]
    delete cloud config groups      ${CCG_00}[name]                              ${CCG_01}[name]
    Onboard_AP

Post_condition
    Quit Browser

Onboard_AP
    ${aps}   Create List   ${ap1}   ${ap2}
    FOR   ${ap}   IN   @{aps}
        ${ONBOARD_STATUS}             onboard device quick    ${ap}
        should be equal as integers   ${ONBOARD_STATUS}       1
    END

    FOR   ${ap}   IN   @{aps}
        ${AP_SPAWN}        Open Spawn          ${ap}[ip]   ${ap}[port]   ${ap}[username]   ${ap}[password]   ${ap}[cli_type]
        ${STATUS}          Configure Device To Connect To Cloud          ${ap}[cli_type]   ${capwap_url}     ${AP_SPAWN}
        Should Be Equal As Strings      '${STATUS}'       '1'
        Close Spawn        ${AP_SPAWN}
    END

    FOR   ${ap}   IN   @{aps}
        ${AP_SPAWN}        Open Spawn          ${ap}[ip]   ${ap}[port]     ${ap}[username]   ${ap}[password]   ${ap}[cli_type]
        ${STATUS}          Wait for Configure Device to Connect to Cloud   ${ap}[cli_type]   ${capwap_url}     ${AP_SPAWN}
        Should Be Equal As Strings      '${STATUS}'       '1'
        Close Spawn        ${AP_SPAWN}
    END

    FOR   ${ap}   IN   @{aps}
         Wait_device_online     ${ap}
    END

Wait_device_online
    [Arguments]    ${ap}
    ${STATUS}                       Wait Until Device Online    ${ap}[serial]    retry_count=60
    Should Be Equal As Strings      '${STATUS}'    '1'
    ${STATUS}                       Get Device Status           ${ap}[serial]
    ${STATUS}                       Run Keyword And Return Status    Should contain any    ${STATUS}    green    config audit mismatch
    IF    not ${STATUS}
        Wait Until Device Reboots       ${ap}[serial]
        ${STATUS}                       Wait Until Device Online    ${ap}[serial]    retry_count=60
        Should Be Equal As Strings      '${STATUS}'    '1'
        ${STATUS}                       Get Device Status           ${ap}[serial]
        Should contain any              ${STATUS}      green    config audit mismatch
    END

Verify_AP_with_Classification
    [Arguments]     ${ap}     ${class}     ${ssid}
    ${AP_SPAWN}           Open Spawn      ${ap}[ip]      ${ap}[port]    ${ap}[username]    ${ap}[password]    ${ap}[cli_type]
    ${OUT}                Send            ${AP_SPAWN}                   show run | inc location
    should contain        ${OUT}          ${class}[floor_node]
    ${OUT}                Send            ${AP_SPAWN}                   show ssid
    should contain        ${OUT}          ${ssid}[ssid_name]
    [Teardown]            run keyword     Close Spawn                   ${AP_SPAWN}
