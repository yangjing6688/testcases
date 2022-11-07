#########################################################################################################
# Author        : Binh Nguyen
# Date          : Oct 6th 2022
# Description   : TCCS-6847 Default userprofile with vlan classification
#                 TCCS-8582 Multiple Userprofile with different vlan and classification
#########################################################################################################

**** Variables ***
################## Policy Detail & Wireless Network ###############################
&{WIRELESS_PESRONAL_00}     ssid_name=""    network_type=Standard    ssid_profile=&{BORADCAST_SSID_00}     auth_profile=&{PERSONAL_AUTH_PROFILE_00}
&{WIRELESS_PESRONAL_01}     ssid_name=""    network_type=Standard    ssid_profile=&{BORADCAST_SSID_00}     auth_profile=&{PERSONAL_AUTH_PROFILE_01}

&{BORADCAST_SSID_00}            WIFI0=Enable        WIFI1=Enable      WIFI2=Disable
&{PERSONAL_AUTH_PROFILE_00}     auth_type=PSK   key_encryption=&{PSK_KEY_ENCRYPTION_00}   cwp_config=&{PSK_CWP_00}   user_profile_config=&{USER_PROFILE_00}
&{PERSONAL_AUTH_PROFILE_01}     auth_type=PSK   key_encryption=&{PSK_KEY_ENCRYPTION_00}   cwp_config=&{PSK_CWP_00}
&{PSK_CWP_00}                   enable_cwp=Disable

&{PSK_KEY_ENCRYPTION_00}        key_management=WPA2-(WPA2 Personal)-PSK    encryption_method=CCMP (AES)    key_type=ASCII Key   key_value=aerohive
&{USER_PROFILE_00}              profile_name=up_105       vlan_name=vlan_105      vlan_id=105     classification_rule_name=up105_location0     description=building_02_floor_04
&{USER_PROFILE_01}              profile_name=up_104       vlan_name=vlan_104      vlan_id=104     classification_rule_name=up104_location1     description=building_02_floor_02
&{USER_PROFILE_02}              profile_name=up_103       vlan_name=vlan_103      vlan_id=103     assignment_rule=building3_floor3
&{USER_PROFILE_03}              profile_name=up_101       vlan_name=vlan_101      vlan_id=101     assignment_rule=building1_floor1

&{LOC_TEST_00}          country_node=auto_location_01     loc_node=Santa Clara     building_node=building_02    floor_node=floor_04
&{LOC_TEST_01}          country_node=auto_location_01     loc_node=Santa Clara     building_node=building_02    floor_node=floor_02
&{LOC_TEST_02}          country_node=auto_location_01     loc_node=Santa Clara     building_node=building_03    floor_node=floor_03
&{LOC_TEST_03}          country_node=auto_location_01     loc_node=Santa Clara     building_node=building_01    floor_node=floor_01

################## Device Templates ###############################
&{AP_TEMPLATE_1}         wifi0_configuration=&{AP_TEMPLATE_1_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_1_WIFI1}
&{AP_TEMPLATE_1_WIFI0}   radio_status=On     radio_profile=radio_ng_11ax-2g     client_mode=Disable    client_access=Enable    backhaul_mesh_link=Disable   sensor=Disable
&{AP_TEMPLATE_1_WIFI1}   radio_status=On     radio_profile=radio_ng_11ax-5g     client_mode=Disable    client_access=Enable    backhaul_mesh_link=Disable   sensor=Disable

############### Globle Variables ######################
${retry}         3

*** Settings ***
Library     String
Library     Collections

Library     common/Cli.py
Library     common/Utils.py
Library     common/TestFlow.py
Library     common/tools/remote/WinMuConnect.py

Library     xiq/flows/common/Login.py
Library     xiq/flows/manage/Location.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/DevicesActions.py
Library     xiq/flows/manage/DeviceConfig.py
Library     xiq/flows/manage/DeviceCliAccess.py

Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/configure/DeviceTemplate.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/configure/ClassificationRule.py
Library     xiq/flows/configure/UserProfile.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Library	    Remote 	http://${mu1.ip}:${mu1.port}   WITH NAME   rem_mu

Force Tags       testbed_1_node     testbed_2_node     testbed_3_node
Suite Setup      Pre_condition
Suite Teardown   Post_condition

*** Test Cases ***
Step0: Onboard AP
    [Documentation]    Onboard AP
    [Tags]             tcxm-6847    tcxm-8582    development     step0    steps
    ${STATUS}                      onboard device quick      ${ap1}
    should be equal as integers    ${STATUS}         1

    ${AP_SPAWN}   Open Spawn          ${ap1.ip}          ${ap1.port}      ${ap1.username}      ${ap1.password}     ${ap1.cli_type}
    ${OUTPUT0}    Send Commands       ${AP_SPAWN}        capwap client server name ${capwap_url}, capwap client default-server-name ${capwap_url}, capwap client server backup name ${capwap_url}, no capwap client enable, capwap client enable, save config
    ${OUTPUT0}    Send                ${AP_SPAWN}        console page 0
    ${OUTPUT0}    Send                ${AP_SPAWN}        show version detail
    ${OUTPUT0}    Send                ${AP_SPAWN}        show capwap client
    ${OUTPUT2}    Send                ${AP_SPAWN}        ${cmd_capwap_hm_primary_name}
    ${OUTPUT3}    Send                ${AP_SPAWN}        ${cmd_capwap_server_ip}
    ${OUTPUT1}    Wait For CLI Output                    ${AP_SPAWN}         ${cmd_capwap_client_state}          ${output_capwap_status}
    Should Be Equal as Integers             ${OUTPUT1}          1
    Close Spawn         ${AP_SPAWN}

    Wait Until Device Online                ${ap1.serial}
    ${AP_STATUS}=                           Get AP Status      ap_mac=${ap1.mac}
    Should Be Equal As Strings             '${AP_STATUS}'      'green'

Step1: Create Policy
    [Documentation]     Creat Policy, User Profile, VLAN Profile, and Classification Rule.
    [Tags]              tcxm-6847    tcxm-8582    development     step1      steps
    Depends On          Step0
    ${NUM}=                        Generate Random String    5     012345678
    Set Suite Variable             ${POLICY}                       per_vlan_${NUM}
    Set Suite Variable             ${SSID_00}                      w0_1_105_${NUM}
    Set Suite Variable             ${SSID_01}                      w0_1_101_3_${NUM}
    Set Suite Variable             ${AP_TEMP_NAME}                 ${ap1.model}_${NUM}
    Set To Dictionary              ${WIRELESS_PESRONAL_00}         ssid_name=${SSID_00}
    Set To Dictionary              ${WIRELESS_PESRONAL_01}         ssid_name=${SSID_01}

    ${STATUS}                      Add Classification Rule with Location      ${USER_PROFILE_00}[classification_rule_name]   ${USER_PROFILE_00}[description]   &{LOC_TEST_00}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Add Classification Rule with Location      ${USER_PROFILE_01}[classification_rule_name]   ${USER_PROFILE_01}[description]   &{LOC_TEST_01}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Add User Profile                           ${USER_PROFILE_00}[profile_name]   ${USER_PROFILE_00}[vlan_name]   1
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Add Classification Rule to User Profile    ${USER_PROFILE_00}[profile_name]   ${USER_PROFILE_00}[vlan_id]     ${USER_PROFILE_00}[classification_rule_name]
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Add Classification Rule to User Profile    ${USER_PROFILE_00}[profile_name]   ${USER_PROFILE_01}[vlan_id]     ${USER_PROFILE_01}[classification_rule_name]
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Create Network Policy                              ${POLICY}         &{WIRELESS_PESRONAL_00}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      create ssid to policy                              ${POLICY}         &{WIRELESS_PESRONAL_01}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Apply Different User Profile to Various Clients    ${SSID_01}        &{USER_PROFILE_02}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Apply Different User Profile to Various Clients    ${SSID_01}        &{USER_PROFILE_03}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      add ap template from common object                 ${ap1.model}      ${AP_TEMP_NAME}      &{AP_TEMPLATE_1}
    Should Be Equal As Strings     '${STATUS}'        '1'
    ${STATUS}                      add ap template to network policy                  ${AP_TEMP_NAME}   ${POLICY}
    Should Be Equal As Strings     '${STATUS}'        '1'

Step2: Assign network policy with VLANs to AP1
    [Documentation]     Assign network policy with VLAN 105 to AP1
    [Tags]              tcxm-6847   development     step2      steps
    Depends On          Step1
    ${UPDATE}                      Update Network Policy To Ap     ${POLICY}     ${ap1.serial}    Complete
    should be equal as strings     '${UPDATE}'       '1'
    Wait Until Device Online       ${ap1.serial}
    ${AP_STATUS}                   Get AP Status     ap_mac=${ap1.mac}
    Should Be Equal As Strings    '${AP_STATUS}'    'green'

Step3: Verify (105) cli user-profile attr and ssid security object attr - Default User Profile
    [Documentation]     Verify (105) cli user-profile attr and ssid security object attr - Default User Profile
    [Tags]              tcxm-6847    development     step3     steps
    Depends On          Step2
    ${AP_SPAWN}         Open Spawn       ${ap1.ip}      ${ap1.port}    ${ap1.username}    ${ap1.password}    ${ap1.cli_type}
    ${OUT}              Send             ${AP_SPAWN}    show run | inc attr
    should contain      ${OUT}           security-object ${SSID_00} default-user-profile-attr 1
    should contain      ${OUT}           user-profile ${USER_PROFILE_00}[profile_name] qos-policy def-user-qos vlan-id ${USER_PROFILE_00}[vlan_id] attribute 1
    [Teardown]          run keyword      Close Spawn   ${AP_SPAWN}

Step4: Verify (105) cli vlanid assigned to the client - Default User Profile
    [Documentation]     Verify (105) cli vlanid assigned to the client - Default User Profile
    [Tags]              tcxm-6847    development     step4     steps
    Depends On          Step2
    Connect_to_client    ${SSID_00}      ${WIRELESS_PESRONAL_00}[auth_profile][key_encryption][key_value]
    Show_station         ${ap1}          ${USER_PROFILE_00}[vlan_id]

Step5: Verify (104) cli user-profile attr and ssid security object attr - Default User Profile
    [Documentation]     Verify (104) cli user-profile attr and ssid security object attr - Default User Profile
    [Tags]              tcxm-6847    development     step5     steps
    Depends On          Step2
    ${STATUS}                            rem_mu.disconnect_wifi
    Should Be Equal As Strings           '${STATUS}'    '1'
    Change_ap_location_and_update        ${ap1}         auto_location_01, Santa Clara, building_02, floor_02

    ${AP_SPAWN}         Open Spawn       ${ap1.ip}      ${ap1.port}    ${ap1.username}    ${ap1.password}    ${ap1.cli_type}
    ${OUT}              Send             ${AP_SPAWN}    show run | inc attr
    should contain      ${OUT}           security-object ${SSID_00} default-user-profile-attr 1
    should contain      ${OUT}           user-profile ${USER_PROFILE_00}[profile_name] qos-policy def-user-qos vlan-id ${USER_PROFILE_01}[vlan_id] attribute 1
    [Teardown]          run keyword      Close Spawn   ${AP_SPAWN}

Step6: Verify (104) cli vlanid assigned to the client - Default User Profile
    [Documentation]     Verify (104) cli vlanid assigned to the client - Default User Profile
    [Tags]              tcxm-6847    development     step6     steps
    Depends On          Step5
    Connect_to_client    ${SSID_00}      ${WIRELESS_PESRONAL_00}[auth_profile][key_encryption][key_value]
    Show_station         ${ap1}          ${USER_PROFILE_01}[vlan_id]

Step7: Verify (103) cli location1 and attribute - Multiple User Profile
    [Documentation]     Verify (103) cli location1 and attrible - Multiple User Profile
    [Tags]              tcxm-8582    development     step7     steps
    Depends On          Step2
    ${STATUS}                            rem_mu.disconnect_wifi
    Should Be Equal As Strings           '${STATUS}'    '1'
    Change_ap_location_and_update        ${ap1}         auto_location_01, Santa Clara, building_03, floor_03

    ${AP_SPAWN}         Open Spawn       ${ap1.ip}      ${ap1.port}    ${ap1.username}    ${ap1.password}    ${ap1.cli_type}
    ${OUT}              Send             ${AP_SPAWN}    show run | inc location
    should contain      ${OUT}           device-location ${LOC_TEST_02}[building_node]|${LOC_TEST_02}[floor_node]
    should contain      ${OUT}           user-profile-policy ${SSID_01} rule 1 device-location ${LOC_TEST_02}[building_node]|${LOC_TEST_02}[floor_node]
    ${OUT}              Send             ${AP_SPAWN}    show run | inc attr
    should contain      ${OUT}           user-profile-policy ${SSID_01} rule 1 user-profile-attr-id 2
    should contain      ${OUT}           user-profile ${USER_PROFILE_02}[profile_name] qos-policy def-user-qos vlan-id ${USER_PROFILE_02}[vlan_id] attribute 2
    [Teardown]          run keyword      Close Spawn   ${AP_SPAWN}

Step8: Verify (103) cli location1 vlanid assigned to the client - Multiple User Profile
    [Documentation]     Verify (103) cli location1 vlanid assigned to the client - Multiple User Profile
    [Tags]              tcxm-8582    development     step8     steps
    Depends On          Step7
    Connect_to_client    ${SSID_01}    ${WIRELESS_PESRONAL_01}[auth_profile][key_encryption][key_value]
    Show_station         ${ap1}        ${USER_PROFILE_02}[vlan_id]

Step9: Verify (101) cli location2 and attribute - Multiple User Profile
    [Documentation]     Verify cli location2 and attrible - Multiple User Profile
    [Tags]              tcxm-8582    development     step9     steps
    Depends On          Step2
    ${STATUS}                            rem_mu.disconnect_wifi
    Should Be Equal As Strings           '${STATUS}'    '1'
    Change_ap_location_and_update        ${ap1}         auto_location_01, Santa Clara, building_01, floor_01

    ${AP_SPAWN}         Open Spawn       ${ap1.ip}      ${ap1.port}    ${ap1.username}    ${ap1.password}    ${ap1.cli_type}
    ${OUT}              Send             ${AP_SPAWN}    show run | inc location
    should contain      ${OUT}           device-location ${LOC_TEST_03}[building_node]|${LOC_TEST_03}[floor_node]
    should contain      ${OUT}           user-profile-policy ${SSID_01} rule 2 device-location ${LOC_TEST_03}[building_node]|${LOC_TEST_03}[floor_node]
    ${OUT}              Send             ${AP_SPAWN}    show run | inc attr
    should contain      ${OUT}           user-profile-policy ${SSID_01} rule 2 user-profile-attr-id 3
    should contain      ${OUT}           user-profile ${USER_PROFILE_03}[profile_name] qos-policy def-user-qos vlan-id ${USER_PROFILE_03}[vlan_id] attribute 3
    [Teardown]          run keyword      Close Spawn   ${AP_SPAWN}

Step10: Verify (101) cli location2 vlanid assigned to the client - Multiple User Profile
    [Documentation]     Verify (101) cli location2 vlanid assigned to the client - Multiple User Profile
    [Tags]              tcxm-8582    development     step10     steps
    Depends On          Step9
    Connect_to_client    ${SSID_01}    ${WIRELESS_PESRONAL_01}[auth_profile][key_encryption][key_value]
    Show_station         ${ap1}        ${USER_PROFILE_03}[vlan_id]

*** Keywords ***
Pre_condition
    ${STATUS}                       Login User    ${tenant_username}   ${tenant_password}
    should be equal as strings      '${STATUS}'   '1'
    ${failed}     ${success}        reset device to default    ${ap1.serial}
    log to console                  Wait for 2 minutes for completing reboot....
    sleep                           2m
    delete all aps
    delete all network policies
    delete all ssids
    delete all ap templates
    Delete All User Profiles
    Delete All Vlan Profiles
    Delete Classification rules     ${USER_PROFILE_00}[classification_rule_name]    ${USER_PROFILE_01}[classification_rule_name]

Post_condition
    Logout User
    Quit Browser

Change_ap_location_and_update
    [Arguments]    ${ap}   ${location}
    ${STATUS}                      Assign Location With Device Actions    ${ap1}[serial]   ${location}
    Should Be Equal As Strings     '${STATUS}'     '1'
    Update_policy_to_ap            ${ap}
    clear_ap_auth_user_profile     ${ap}

Update_policy_to_ap
    [Arguments]    ${ap}
    update device delta configuration    ${ap}[serial]
    Wait Until Device Online             ${ap}[serial]
    ${AP_STATUS}                         Get AP Status     ap_mac=${ap}[mac]
    Should Be Equal As Strings           '${AP_STATUS}'    'green'

Clear_ap_auth_user_profile
    [Arguments]    ${ap}
    ${AP_SPAWN}   Open Spawn     ${ap}[ip]      ${ap}[port]    ${ap}[username]    ${ap}[password]    ${ap}[cli_type]
    ${OUT}        Send           ${AP_SPAWN}    clear auth station
    ${OUT}        Send           ${AP_SPAWN}    clear auth roaming-cache
    ${OUT}        Send           ${AP_SPAWN}    clear auth local-cache
    [Teardown]    run keyword    Close Spawn    ${AP_SPAWN}

Connect_to_client
    [Arguments]    ${ssid}    ${password}
    FOR    ${i}    IN RANGE    ${retry}
        ${STATUS}            rem_mu.connect wpa2 psk network     ${ssid}    ${password}
        exit for loop if    '${STATUS}'=='1'
    END

Show_station
    [Arguments]     ${ap}      ${vlan_id}
    ${AP_SPAWN}           Open Spawn       ${ap}[ip]      ${ap}[port]    ${ap}[username]    ${ap}[password]    ${ap}[cli_type]
    ${OUT}                Send             ${AP_SPAWN}    console page 0
    ${OUT}                Send             ${AP_SPAWN}    show station
    should match regexp   ${OUT}           ccmp\\s+\\d+:\\d+:\\d+\\s+${vlan_id}
    [Teardown]            run keyword      Close Spawn   ${AP_SPAWN}
