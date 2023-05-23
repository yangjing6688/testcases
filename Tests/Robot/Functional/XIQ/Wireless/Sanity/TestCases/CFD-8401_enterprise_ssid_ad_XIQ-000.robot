#########################################################################################################
# Author        : Binh Nguyen
# Date          : Jan 18th 2023
# Description   : CFD-8401: Unable to access data occur in RADIUS Settings
#                 TCCS-13557
#########################################################################################################

**** Variables ***
##################  Policy Detail & Wireless Network ##################
&{WIRELESS_ENTERPRISE_00}       ssid_name=""   network_type=Standard   ssid_profile=&{BORADCAST_SSID_00}   auth_profile=&{ENTERPRISE_AUTH_PROFILE_00}

&{BORADCAST_SSID_00}            WIFI0=Enable      WIFI1=Enable      WIFI2=Disable
&{ENTERPRISE_AUTH_PROFILE_00}   auth_type=enterprise    key_encryption=&{KEY_ENCRYPTION_00}   cwp_profile=&{ENTERPRISE_CWP_00}  auth_settings_profile=&{AUTHENTICATION_SETTINGS_00}
...                             user_access_settings=None   additional_settings=None

&{KEY_ENCRYPTION_00}            key_management=WPA2-802.1X    encryption_method=CCMP (AES)
&{ENTERPRISE_CWP_00}            enable_cwp=Disable
&{AUTHENTICATION_SETTINGS_00}   auth_with_extcldiq_service=Disable   radius_server_group_config=&{RADIUS_SERVER_GROUP_00}

##################  Authentication Service(Active Directory) ##################
&{RADIUS_SERVER_GROUP_00}            radius_server_group_name=Auth_Radius_server00   radius_server_config=&{RADIUS_SERVER_00}

&{RADIUS_SERVER_00}                  radius_server_group_desc=Test Raidus Server with Active Directory   server_type=EXTREME NETWORKS RADIUS SERVER   extreme_radius_server_config=&{EXTREME_RADIUS_SERVER_CONFIG_00}
&{EXTREME_RADIUS_SERVER_CONFIG_00}   radius_server_name=bui-flo-2763   aaa_profile_name=AAA_Server_Setting00   user_db_type=Active Directory
...                                  ad_server_name=AD_Server00        ad_server_domain=binh.com               ad_server_config=&{ACTIVE_DIRECTORY_PROFILE_00}
...                                  baseDN=DC=binh,DC=com             short_domain_name=binh                  realm=binh.com
...                                  domain_admin=Administrator        domain_admin_password=Aerohive123
...                                  domain_user=user1                 domain_user_password=Aerohive123
&{ACTIVE_DIRECTORY_PROFILE_00}       host_ip_type=IP Address   name=10.254.152.60   ip_address=10.254.152.60   host_name=None

################## Device Templates ################## bui-flo-0048    AH-6ef0c0
&{AP_TEMPLATE_1}         wifi0_configuration=&{AP_TEMPLATE_1_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_1_WIFI1}   wifi2_configuration=&{AP_TEMPLATE_1_WIFI2}
&{AP_TEMPLATE_1_WIFI0}   radio_status=On     radio_profile=radio_ng_11ax-2g     client_mode=Disable    client_access=Enable    backhaul_mesh_link=Disable   sensor=Disable
&{AP_TEMPLATE_1_WIFI1}   radio_status=On     radio_profile=radio_ng_11ax-5g     client_mode=Disable    client_access=Enable    backhaul_mesh_link=Disable   sensor=Disable
&{AP_TEMPLATE_1_WIFI2}   radio_status=On     radio_profile=radio_ng_11ax-6g                            client_access=Enable    backhaul_mesh_link=Disable   sensor=Disable

##################  Globle Variables ##################
${retry}     3

*** Settings ***
Library     String
Library     Collections
Library     DependencyLibrary

Library     common/Cli.py
Library     common/Utils.py
Library     common/tools/remote/WinMuConnect.py

# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     xiq/flows/mlinsights/MLInsightClient360.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/DevicesActions.py
Library     xiq/flows/manage/DeviceConfig.py
Library     xiq/flows/manage/DeviceCliAccess.py

Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/configure/DeviceTemplate.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/CommonObjects.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Library	    Remote 	http://${mu1.ip}:${mu1.port}   WITH NAME   rem_mu

Force Tags       testbed_none
Suite Setup      Pre_condition
Suite Teardown   Post_condition

*** Test Cases ***
Step1: Create Policy - Enterprise with Cloud and Radius auth
    [Documentation]     Create policy, select wifi0,1,2, and update policy to AP
    [Tags]              tccs-13557   development   step1   steps

    Set Suite Variable             ${POLICY}                       enterprise_AD
    Set Suite Variable             ${SSID_00}                      w0_1_AD
    Set Suite Variable             ${AP_TEMP_NAME}                 ${ap1.model}_AD
    Set To Dictionary              ${WIRELESS_ENTERPRISE_00}       ssid_name=${SSID_00}

    ${STATUS}                      create network policy if does not exist    ${POLICY}          ${WIRELESS_ENTERPRISE_00}
    Should Be Equal As Strings     '${STATUS}'       '1'
    ${STATUS}                      add ap template from common object         ${ap1.model}       ${AP_TEMP_NAME}    ${AP_TEMPLATE_1}
    Should Be Equal As Strings     '${STATUS}'       '1'
    ${STATUS}                      add ap template to network policy          ${AP_TEMP_NAME}    ${POLICY}

Step2: Assign network policy to AP
    [Documentation]     Assign network policy to AP
    [Tags]              tccs-13557   development   step2   steps

    Depends On Test     Step1: Create Policy - Enterprise with Cloud and Radius auth
    ${UPDATE}                      Update Network Policy To Ap    ${POLICY}     ${ap1.serial}    Complete
    should be equal as strings     '${UPDATE}'    '1'
    Wait_device_online             ${ap1}
    Enable disable client Wifi device             ${mu1}

Step3: MU connect to wifi0-1 - Auth service from AD Server
    [Documentation]     MU connect to wifi0-1 - Enterprise SSID using Auth service from AD Server
    [Tags]              tccs-13557   development   step3   steps

    Depends On Test     Step2: Assign network policy to AP
    FOR    ${i}    IN RANGE    ${retry}
        ${STATUS}               rem_mu.connect wifi network        ${SSID_00}
        exit for loop if        '${STATUS}'=='1'
    END
    should be equal as strings      '${STATUS}'     '1'

Step4: Verify Client360 to wifi0-1 - Auth service from AD Server
    [Documentation]     Verify Client360 to wifi0-1 - Enterprise SSID using Auth service from AD Server
    [Tags]              tccs-13557    development     step4      steps

    Depends On Test    Step3: MU connect to wifi0-1 - Auth service from AD Server
    ${OUT}             get client360 current connection status      ${mu1.wifi_mac}
    should contain     ${OUT['USER']}                               ${EXTREME_RADIUS_SERVER_CONFIG_00}[domain_user]

*** Keywords ***
Pre_condition
    ${STATUS}                           Login User    ${tenant_username}   ${tenant_password}
    should be equal as strings          '${STATUS}'   '1'
    reset devices to default
    log to console                      Wait for 2 minutes for completing reboot....
    sleep                               2m
    delete all devices
    delete all network policies
    delete all ssids
    delete radius server group          ${RADIUS_SERVER_GROUP_00}[radius_server_group_name]
    delete aaa server profile           ${EXTREME_RADIUS_SERVER_CONFIG_00}[aaa_profile_name]
    delete all ap templates
    delete ad server                    ${EXTREME_RADIUS_SERVER_CONFIG_00}[ad_server_name]
    Onboard_AP

Post_condition
    Logout User
    Quit Browser

Onboard_AP
    ${STATUS}       onboard device quick                            ${ap1}
    Should Be Equal As Strings                                      '${STATUS}'       '1'
    ${AP_SPAWN}     Open Spawn                                      ${ap1.ip}         ${ap1.port}      ${ap1.username}   ${ap1.password}   ${ap1.cli_type}
    ${STATUS}       Configure Device To Connect To Cloud            ${ap1.cli_type}   ${capwap_url}    ${AP_SPAWN}
    Should Be Equal As Strings                                      '${STATUS}'       '1'

    ${STATUS}       Wait for Configure Device to Connect to Cloud   ${ap1.cli_type}   ${capwap_url}    ${AP_SPAWN}
    Should Be Equal As Strings                                      '${STATUS}'       '1'
    Wait_device_online                                              ${ap1}
    [Teardown]      Close Spawn                                     ${AP_SPAWN}

Enable_disable_client_Wifi_device
    [Arguments]     ${mu}
    ${SPAWN}        Open Spawn    ${mu}[ip]     22    ${mu}[username]    ${mu}[password]    cli_type=MU-WINDOWS
    Send Commands   ${SPAWN}      pnputil /disable-device /deviceid \"PCI\\CC_0280\", pnputil /enable-device /deviceid \"PCI\\CC_0280\"
    [Teardown]      run keyword   Close Spawn   ${SPAWN}

Wait_device_online
    [Arguments]    ${ap}
    ${STATUS}                       Wait Until Device Online    ${ap}[serial]
    Should Be Equal As Strings      '${STATUS}'    '1'
    ${STATUS}                       Get Device Status           ${ap}[serial]
    ${STATUS}                       Run Keyword And Return Status    Should contain any    ${STATUS}    green    config audit mismatch
    IF    not ${STATUS}
        Wait Until Device Reboots       ${ap}[serial]
        ${STATUS}                       Wait Until Device Online    ${ap}[serial]    retry_count=60
        Should Be Equal As Strings      '${STATUS}'    '1'
        ${STATUS}                       Get Device Status           ${ap}[serial]
        Should contain any              ${STATUS}      green        config audit mismatch
    END