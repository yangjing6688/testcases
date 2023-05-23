# Author        : Barbara Sochor
# Date          : August 10th 2022
# Description   : XIQ-6165 AP5010 Regulatory Support
#
# Topology:
# Host ----- XIQ
#
#  To run using topo and environment:
#  ----------------------------------
#  robot -v TOPO:topology.yaml -v ENV:environment.yaml -v TESTBED:SJ/Dev/xiq_sj_tb0_all.yaml -i tcxm-20828 -d /home/bsochor/logs AP5010xxx.robot
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
# Test21 - TCXM-20831 - Verify: AP Can Be Configured To Croatia
#             Verifies that AP can be configured to Country Craatia
# Test22 - TCXM-20832 - Verify: AP Can Be Configured To Cyprus
#             Verifies that AP can be configured to Country Cyprus
# Test23 - TCXM-20833 - Verify: AP Can Be Configured To Czech Republic
#             Verifies that AP can be configured to Country Czech Republic
# Test24 - TCXM-20834 - Verify: AP Can Be Configured To Denmark
#             Verifies that AP can be configured to Country Denmark
# Test25 - TCXM-20835 - Verify: AP Can Be Configured To Estonia
#             Verifies that AP can be configured to Country Estonia
# Test26 - TCXM-20837 - Verify: AP Can Be Configured To Greece
#             Verifies that AP can be configured to Country Greece
# Test27 - TCXM-20839 - Verify: AP Can Be Configured To Iceland
#             Verifies that AP can be configured to Country Iceland
# Test28 - TCXM-20840 - Verify: AP Can Be Configured To Ireland
#             Verifies that AP can be configured to Country Ireland
# Test29 - TCXM-20841 - Verify: AP Can Be Configured To Latvia
#             Verifies that AP can be configured to Country Latvia
# Test30 - TCXM-20843 - Verify: AP Can Be Configured To Liechtenstein
#             Verifies that AP can be configured to Country Liechtenstein
# Test31 - TCXM-20858 - Verify: AP Can Be Configured To Lithuania
#             Verifies that AP can be configured to Country Lithuenia
# Test32 - TCXM-20844 - Verify: AP Can Be Configured To Luxembourg
#             Verifies that AP can be configured to Country Luxembourg
# Test33 - TCXM-20845 - Verify: AP Can Be Configured To Macedonia
#             Verifies that AP can be configured to Country Macedonia
# Test34 - TCXM-20846 - Verify: AP Can Be Configured To Malta
#             Verifies that AP can be configured to Country Malta
# Test35 - TCXM-20847 - Verify: AP Can Be Configured To Montenegro
#             Verifies that AP can be configured to Country Montenegro
# Test36 - TCXM-20859 - Verify: AP Can Be Configured To Norway
#             Verifies that AP can be configured to Country Norway
# Test37 - TCXM-20850 - Verify: AP Can Be Configured To Serbia
#             Verifies that AP can be configured to Country Serbia
# Test38 - TCXM-20851 - Verify: AP Can Be Configured To Slovakia
#             Verifies that AP can be configured to Country Slovakia
# Test39 - TCXM-20852 - Verify: AP Can Be Configured To Slovenia
#             Verifies that AP can be configured to Country Slovenia
# Test40 - TCXM-20855 - Verify: AP Can Be Configured To Turkey
#             Verifies that AP can be configured to Country Turkey
# Test41 - TCXM-20779 - Verify: AP Can Be Configured To UK
#             Verifies that AP can be configured to UK
# Test42 - TCXM-24874 - Verify: AP Can Be Configured To Georgia
#             Verifies that AP can be configured to Georgia
# Test43 - TCXM-24227 - Verify: AP Can Be Configured To New Zealand
#             Verifies that AP can be configured to New Zealand
# Test44 - TCXM-24879 - Verify: AP Can Be Configured To US Virgin Island
#             Verifies that AP can be configured to Virgin Island
# Test45 - TCXM-41044 - Verify: AP Can Be Configured To Mexico
#             Verifies that AP can be configured to Mexico
# Test46 - TCXM-41413 - Verify: AP Can Be Configured To Kazakhstan
#             Verifies AP's functionality after being set to Kazakhstan
# Test47 - TCXM-41855 - Verify: AP Can Be Configured To People's Republic of China
#             Verifies AP's functionality after being set to People's Republic of China
# Test48 - TCXM-42053 - Verify: AP Can Be Configured To Taiwan
#             Verifies AP's functionality after being set to Taiwan
# Test49 - TCXM-41319 - Verify: AP Can Be Configured To Singapore
#             Verifies AP's functionality after being set to Singapore
# Test50 - TCXM-40000 - Verify: AP Can Be Configured To Indonesia
#             Verifies AP's functionality after being set to Indonesia
# Test51 - TCXM-39969 - Verify: AP Can Be Configured To Thailand
#             Verifies AP's functionality after being set to Thailand
# Test52 - TCXM-39498 - Verify: AP Can Be Configured To Republic of the Philippines
#             Verifies AP's functionality after being set to Republic of the Philippines
# Test53 - TCXM-39817 - Verify: AP Can Be Configured To Vietnam
#             Verifies AP's functionality after being set to Vietnam
# Test54 - TCXM-39629 - Verify: AP Can Be Configured To South Africa
#             Verifies AP's functionality after being set to South Africa
# Test55 - TCXM-39745 - Verify: AP Can Be Configured To Dominican Republic
#             Verifies AP's functionality after being set to Dominican Republic
# Test56 - TCXM-40014 - Verify: AP Can Be Configured To Macao
#             Verifies AP's functionality after being set to Macao
# Test57 - TCXM-41790 - Verify: AP Can Be Configured To Russia
#             Verifies AP's functionality after being set to Russia
# Test58 - TCXM-41373 - Verify: AP Can Be Configured To Ecuador
#             Verifies AP's functionality after being set to Ecuador
# Test59 - TCXM-41214 - Verify: AP Can Be Configured To Kuwait
#             Verifies AP's functionality after being set to Kuwait
# Test60 - TCXM-39674 - Verify: AP Can Be Configured To Qatar
#             Verifies AP's functionality after being set to Qatar
# Test61 - TCXM-39306 - Verify: AP Can Be Configured To U.A.E.
#             Verifies AP's functionality after being set to U.A.E
# Test62 - TCXM-39413 - Verify: AP Can Be Configured To Saudi Arabia
#             Verifies AP's functionality after being set to Saudi Arabia
# Test63 - TCXM-39371 - Verify: AP Can Be Configured To Brazil
#             Verifies AP's functionality after being set to Brazil
# Test64 - TCXM-39262 - Verify: AP Can Be Configured To Japan
#             Verifies AP's functionality after being set to Japan
# Test65 - TCXM-39997 - Verify: AP Can Be Configured To Guyana
#             Verifies AP's functionality after being set to Guyana
# Test66 - TCXM-39481 - Verify: AP Can Be Configured To India
#             Verifies AP's functionality after being set to India
# Test67 - TCXM-41231 - Verify: AP Can Be Configured To Malaysia
#             Verifies AP's functionality after being set to Malaysia
# Test68 - TCXM-41666 - Verify: AP Can Be Configured To Korea
#             Verifies AP's functionality after being set to Korea
# Test60 - TCXM-42002 - Verify: AP Can Be Configured To Hong Kong
#             Verifies AP's functionality after being set to Hong Kong
# Test70 - TCXM-20769 - Verify: A Country Cannot Be Reconfigured To "United States (840)"
#             Verifies that AP set to World region cannot be configured to United States.
# Test71 - TCXM-20771 - Verify: A Country Cannot Be Reconfigured To "Canada (124)"
#             Verifies that AP set to World region cannot be configured to Canada.
# Test72 - TCXM-20768 - Verify: "United States (840)" Country Cannot Be Reconfigured
#             Verifies that AP congigured to US cannot be reconfigured to a different country
# Test73 - TCXM-20770 - Verify: "Canada (124)" Country Cannot Be Reconfigured
#             Verifies that AP congigured to Canada cannot be reconfigured to a different country
# Test74 - TCXM-34876 - Verify: D360 Channels Can Be Configured
#             Verifies AP's functionality assuming it was already been set to a region
########################################################################################################################

*** Variables ***
################## Policy Detail & Wireless Network ###############################
&{WIRELESS_PESRONAL_00}     ssid_name=""    network_type=Standard    ssid_profile=&{BORADCAST_SSID_00}     auth_profile=&{PERSONAL_AUTH_PROFILE_00}
&{WIRELESS_PESRONAL_01}     ssid_name=""    network_type=Standard    ssid_profile=&{BORADCAST_SSID_00}     auth_profile=&{PERSONAL_AUTH_PROFILE_01}
&{WIRELESS_PESRONAL_02}     ssid_name=""    network_type=Standard    ssid_profile=&{BORADCAST_SSID_01}     auth_profile=&{PERSONAL_AUTH_PROFILE_02}
&{WIRELESS_PESRONAL_03}     ssid_name=""    network_type=Standard    ssid_profile=&{BORADCAST_SSID_01}     auth_profile=&{PERSONAL_AUTH_PROFILE_03}
&{WIRELESS_PESRONAL_04}     ssid_name=""    network_type=Standard    ssid_profile=&{BORADCAST_SSID_01}     auth_profile=&{PERSONAL_AUTH_PROFILE_04}

&{BORADCAST_SSID_00}        WIFI0=Enable        WIFI1=Enable      WIFI2=Disable
&{BORADCAST_SSID_01}        WIFI0=Disable       WIFI1=Disable     WIFI2=Enable
&{BORADCAST_SSID_02}        WIFI0=Enable        WIFI1=Enable      WIFI2=Enable

&{PERSONAL_AUTH_PROFILE_00}     auth_type=PSK   key_encryption=&{PSK_KEY_ENCRYPTION_01}   cwp_config=&{PSK_CWP_00}
&{PERSONAL_AUTH_PROFILE_01}     auth_type=PSK   key_encryption=&{PSK_KEY_ENCRYPTION_00}   cwp_config=&{PSK_CWP_01}
&{PERSONAL_AUTH_PROFILE_02}     auth_type=PSK   key_encryption=&{PSK_KEY_ENCRYPTION_01}   cwp_config=&{PSK_CWP_00}
&{PERSONAL_AUTH_PROFILE_03}     auth_type=PSK   key_encryption=&{PSK_KEY_ENCRYPTION_01}   cwp_config=&{PSK_CWP_01}
&{PERSONAL_AUTH_PROFILE_04}     auth_type=PSK   key_encryption=&{PSK_KEY_ENCRYPTION_01}   cwp_config=&{PSK_CWP_00}

&{PSK_KEY_ENCRYPTION_00}        key_management=WPA2-(WPA2 Personal)-PSK    encryption_method=CCMP (AES)    key_type=ASCII Key   key_value=aerohive
&{PSK_KEY_ENCRYPTION_01}        key_management=WPA3 (SAE)    encryption_method=CCMP (AES)   sae_group=All    transition_mode=disable    key_value=aerohive
...                             anti_logging_Threshold=5     key_type=ASCII Key

&{PSK_CWP_00}                   enable_cwp=Disable
&{PSK_CWP_01}                   enable_cwp=Enable    enable_upa=Enable    cwp_name=""

################## Device Templates ###############################
&{AP_TEMPLATE_1}         wifi0_configuration=&{AP_TEMPLATE_1_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_1_WIFI1}   wifi2_configuration=&{AP_TEMPLATE_1_WIFI2}
&{AP_TEMPLATE_1_WIFI0}   radio_status=On     radio_profile=radio_ng_11ax-2g     client_mode=Disable    client_access=Enable    backhaul_mesh_link=Disable   sensor=Disable
&{AP_TEMPLATE_1_WIFI1}   radio_status=On     radio_profile=radio_ng_11ax-5g     client_mode=Disable    client_access=Enable    backhaul_mesh_link=Disable   sensor=Disable
&{AP_TEMPLATE_1_WIFI2}   radio_status=On     radio_profile=radio_ng_11ax-6g                            client_access=Enable    backhaul_mesh_link=Disable   sensor=Disable

############### Globle Variables ######################
${retry}     3


*** Settings ***
# import libraries
Library     String
Library     Collections
# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     common/Utils.py
Library     common/Screen.py
Library     common/ImageHandler.py
Library     common/ScreenDiff.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/DeviceCliAccess.py
Library     xiq/flows/manage/DevicesActions.py
Library     xiq/flows/manage/DeviceConfig.py
Library     common/ImageAnalysis.py
Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/ExpressNetworkPolicies.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/configure/DeviceTemplate.py
Library     extauto/common/Cli.py
Library     extauto/common/TestFlow.py
# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     extauto/xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     extauto/xiq/flows/common/Navigator.py



Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    TestBeds/${TESTBED}
Variables    Environments/Config/device_commands.yaml
Variables    Environments/Config/waits.yaml
# Variables    Tests/Robot/Functional/XIQ/Wireless/Network360Monitor/Resources/n360waits.yaml


Force Tags   testbed_1_node
# Suite Setup    InitialSetup

*** Test Cases ***
 Test1 - TCXM-20804 - Verify: AP Can Be Configured To Albania
    [Documentation]         AP's country code is changed to Albania and result it verified on UI level
    [Tags]                  tcxm-20804    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Albania
    ${COUNTRY_CODE}           Set Variable    8
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test2 - TCXM-20816 - Verify: AP Can Be Configured To Austria
    [Documentation]         AP's country code is changed to Austria and result it verified on UI level
    [Tags]                  tcxm-20816    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Austria
    ${COUNTRY_CODE}           Set Variable    40
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test3 - TCXM-20828 - Verify: AP Can Be Configured To Belgium
    [Documentation]         AP's country code is changed to Belgium and result it verified on UI level
    [Tags]                  tcxm-20828    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Belgium
    ${COUNTRY_CODE}           Set Variable    56
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test4 - TCXM-20829 - Verify: AP Can Be Configured To Bulgaria
    [Documentation]         AP's country code is changed to Bulgaria and result it verified on UI level
    [Tags]                  tcxm-20829    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Bulgaria
    ${COUNTRY_CODE}           Set Variable    100
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test5 - TCXM-20830 - Verify: AP Can Be Configured To Bosnia-Herzegovina
    [Documentation]         AP's country code is changed to Bosnia-Herzegovina and result it verified on UI level
    [Tags]                  tcxm-20830    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Bosnia-Herzegovina
    ${COUNTRY_CODE}           Set Variable    70
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test6 - TCXM-20772 - Verify: AP Can Be Configured To Puerto Rico
    [Documentation]         AP's country code is changed to Puerto Rico and result it verified on UI level
    [Tags]                  tcxm-20772    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Puerto Rico
    ${COUNTRY_CODE}           Set Variable    630
    ${SHORT_COUNTRY}          Set Variable    Puerto
    ${NEW_WiFi0_CHANNEL}      Set Variable    11
    ${NEW_WiFi1_CHANNEL}      Set Variable    165
    ${NEW_WiFi2_CHANNEL}      Set Variable    229

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE} ${SHORT_COUNTRY}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}   ${SHORT_COUNTRY}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test7 - TCXM-20773 - Verify: AP Can Be Configured To Colombia
    [Documentation]         AP's country code is changed to Colombia and result it verified on UI level
    [Tags]                  tcxm-20773    development   ap-5050
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   170
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Colombia
    ${COUNTRY_CODE}           Set Variable    170
    ${NEW_WiFi0_CHANNEL}      Set Variable    11
    ${NEW_WiFi1_CHANNEL}      Set Variable    165
    ${NEW_WiFi2_CHANNEL}      Set Variable    229

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test8 - TCXM-20786 - Verify: AP Can Be Configured To Australia
    [Documentation]         AP's country code is changed to Australia and result it verified on UI level
    [Tags]                  tcxm-20786    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Australia
    ${COUNTRY_CODE}           Set Variable    36
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    165
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test9 - TCXM-20798 - Verify: AP Can Be Configured To Italy
    [Documentation]         AP's country code is changed to Italy and result it verified on UI level
    [Tags]                  tcxm-20798    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Italy
    ${COUNTRY_CODE}           Set Variable    380
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test10 - TCXM-20822 - Verify: AP Can Be Configured To Poland
    [Documentation]         AP's country code is changed to Poland and result it verified on UI level
    [Tags]                  tcxm-20822    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Poland
    ${COUNTRY_CODE}           Set Variable    616
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test11 - TCXM-20848 - Verify: AP Can Be Configured To Netherlands
    [Documentation]         AP's country code is changed to Netherlands and result it verified on UI level
    [Tags]                  tcxm-20848    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Netherlands
    ${COUNTRY_CODE}           Set Variable    528
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test12 - TCXM-20860 - Verify: AP Can Be Configured To Portugal
    [Documentation]         AP's country code is changed to Portugal and result it verified on UI level
    [Tags]                  tcxm-20860    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Portugal
    ${COUNTRY_CODE}           Set Variable    620
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test13 - TCXM-20785 - Verify: AP Can Be Configured To Germany
    [Documentation]         AP's country code is changed to Germany and result it verified on UI level
    [Tags]                  tcxm-20785    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Germany
    ${COUNTRY_CODE}           Set Variable    276
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test14 - TCXM-20797 - Verify: AP Can Be Configured To France
    [Documentation]         AP's country code is changed to France and result it verified on UI level
    [Tags]                  tcxm-20797    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    France
    ${COUNTRY_CODE}           Set Variable    250
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test15 - TCXM-20810 - Verify: AP Can Be Configured To Spain
    [Documentation]         AP's country code is changed to Spain and result it verified on UI level
    [Tags]                  tcxm-20810    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Spain
    ${COUNTRY_CODE}           Set Variable    724
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test16 - TCXM-20836 - Verify: AP Can Be Configured To Finland
    [Documentation]         AP's country code is changed to Finland and result it verified on UI level
    [Tags]                  tcxm-20836    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Finland
    ${COUNTRY_CODE}           Set Variable    246
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test17 - TCXM-20853 - Verify: AP Can Be Configured To Sweden
    [Documentation]         AP's country code is changed to Sweden and result it verified on UI level
    [Tags]                  tcxm-20853    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Sweden
    ${COUNTRY_CODE}           Set Variable    752
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test18 - TCXM-20849 - Verify: AP Can Be Configured To Romania
    [Documentation]         AP's country code is changed to Romania and result it verified on UI level
    [Tags]                  tcxm-20849    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Romania
    ${COUNTRY_CODE}           Set Variable    642
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test19 - TCXM-20838 - Verify: AP Can Be Configured To Hungary
    [Documentation]         AP's country code is changed to Hungary and result it verified on UI level
    [Tags]                  tcxm-20838    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Hungary
    ${COUNTRY_CODE}           Set Variable    348
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test20 - TCXM-20854 - Verify: AP Can Be Configured To Switzerland
    [Documentation]         AP's country code is changed to Switzerland and result it verified on UI level
    [Tags]                  tcxm-20854    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Switzerland
    ${COUNTRY_CODE}           Set Variable    756
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test21 - TCXM-20831 - Verify: AP Can Be Configured To Croatia
    [Documentation]         AP's country code is changed to Croatia and result it verified on UI level
    [Tags]                  tcxm-20831    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Croatia
    ${COUNTRY_CODE}           Set Variable    191
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test22 - TCXM-20832 - Verify: AP Can Be Configured To Cyprus
    [Documentation]         AP's country code is changed to Cyprus and result it verified on UI level
    [Tags]                  tcxm-20832    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Cyprus
    ${COUNTRY_CODE}           Set Variable    196
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test23 - TCXM-20833 - Verify: AP Can Be Configured To Czech Republic
    [Documentation]         AP's country code is changed to Czech Republic and result it verified on UI level
    [Tags]                  tcxm-20833    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Czech Republic
    ${COUNTRY_CODE}           Set Variable    203
    ${SHORT_COUNTRY}          Set Variable    Czech
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE} ${SHORT_COUNTRY}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}   ${SHORT_COUNTRY}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test24 - TCXM-20834 - Verify: AP Can Be Configured To Denmark
    [Documentation]         AP's country code is changed to Denmark and result it verified on UI level
    [Tags]                  tcxm-20834    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Denmark
    ${COUNTRY_CODE}           Set Variable    208
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test25 - TCXM-20835 - Verify: AP Can Be Configured To Estonia
    [Documentation]         AP's country code is changed to Estonia and result it verified on UI level
    [Tags]                  tcxm-20835    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Estonia
    ${COUNTRY_CODE}           Set Variable    233
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test26 - TCXM-20837 - Verify: AP Can Be Configured To Greece
    [Documentation]         AP's country code is changed to Greece and result it verified on UI level
    [Tags]                  tcxm-20837    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Greece
    ${COUNTRY_CODE}           Set Variable    300
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test27 - TCXM-20839 - Verify: AP Can Be Configured To Iceland
    [Documentation]         AP's country code is changed to Iceland and result it verified on UI level
    [Tags]                  tcxm-20839    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   170
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Iceland
    ${COUNTRY_CODE}           Set Variable    352
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test28 - TCXM-20840 - Verify: AP Can Be Configured To Ireland
    [Documentation]         AP's country code is changed to Ireland and result it verified on UI level
    [Tags]                  tcxm-20840    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Ireland
    ${COUNTRY_CODE}           Set Variable    372
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test29 - TCXM-20841 - Verify: AP Can Be Configured To Latvia
    [Documentation]         AP's country code is changed to Latvia and result it verified on UI level
    [Tags]                  tcxm-20841    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Latvia
    ${COUNTRY_CODE}           Set Variable    428
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test30 - TCXM-20843 - Verify: AP Can Be Configured To Liechtenstein
    [Documentation]         AP's country code is changed to Liechtenstein and result it verified on UI level
    [Tags]                  tcxm-20843    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Liechtenstein
    ${COUNTRY_CODE}           Set Variable    438
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test31 - TCXM-20858 - Verify: AP Can Be Configured To Lithuania
    [Documentation]         AP's country code is changed to Lithuania and result it verified on UI level
    [Tags]                  tcxm-20858    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Lithuania
    ${COUNTRY_CODE}           Set Variable    440
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test32 - TCXM-20844 - Verify: AP Can Be Configured To Luxembourg
    [Documentation]         AP's country code is changed to Luxembourg and result it verified on UI level
    [Tags]                  tcxm-20844    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Luxembourg
    ${COUNTRY_CODE}           Set Variable    442
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test33 - TCXM-20845 - Verify: AP Can Be Configured To Macedonia
    [Documentation]         AP's country code is changed to Macedonia and result it verified on UI level
    [Tags]                  tcxm-20845    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    North Macedonia
    ${COUNTRY_CODE}           Set Variable    807
    ${SHORT_COUNTRY}          Set Variable    Macedonia
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE} ${SHORT_COUNTRY}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}   ${SHORT_COUNTRY}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test34 - TCXM-20846 - Verify: AP Can Be Configured To Malta
    [Documentation]         AP's country code is changed to Malta and result it verified on UI level
    [Tags]                  tcxm-20846    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Malta
    ${COUNTRY_CODE}           Set Variable    470
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test35 - TCXM-20847 - Verify: AP Can Be Configured To Montenegro
    [Documentation]         AP's country code is changed to Montenegro and result it verified on UI level
    [Tags]                  tcxm-20847    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Montenegro
    ${COUNTRY_CODE}           Set Variable    499
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test36 - TCXM-20859 - Verify: AP Can Be Configured To Norway
    [Documentation]         AP's country code is changed to Norway and result it verified on UI level
    [Tags]                  tcxm-20859    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Norway
    ${COUNTRY_CODE}           Set Variable    578
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test37 - TCXM-20850 - Verify: AP Can Be Configured To Serbia
    [Documentation]         AP's country code is changed to Serbia and result it verified on UI level
    [Tags]                  tcxm-20850    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Serbia
    ${COUNTRY_CODE}           Set Variable    688
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test38 - TCXM-20851 - Verify: AP Can Be Configured To Slovakia
    [Documentation]         AP's country code is changed to Slovakia and result it verified on UI level
    [Tags]                  tcxm-20851    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Slovak Republic
    ${COUNTRY_CODE}           Set Variable    703
    ${SHORT_COUNTRY}          Set Variable    Slovak
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE} ${SHORT_COUNTRY}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}   ${SHORT_COUNTRY}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test39 - TCXM-20852 - Verify: AP Can Be Configured To Slovenia
    [Documentation]         AP's country code is changed to Slovenia and result it verified on UI level
    [Tags]                  tcxm-20852    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Slovenia
    ${COUNTRY_CODE}           Set Variable    705
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test40 - TCXM-20855 - Verify: AP Can Be Configured To Turkey
    [Documentation]         AP's country code is changed to Turkey and result it verified on UI level
    [Tags]                  tcxm-20855    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Turkey
    ${COUNTRY_CODE}           Set Variable    792
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test41 - TCXM-20779 - Verify: AP Can Be Configured To UK
    [Documentation]         AP's country code is changed to UK and result it verified on UI level
    [Tags]                  tcxm-20779    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    United Kingdom
    ${COUNTRY_CODE}           Set Variable    826
    ${SHORT_COUNTRY}          Set Variable    Kingdom
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    144
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE} ${SHORT_COUNTRY}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}   ${SHORT_COUNTRY}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test42 - TCXM-24874 - Verify: AP Can Be Configured To Georgia
    [Documentation]         AP's country code is changed to Georgia and result it verified on UI level
    [Tags]                  tcxm-24874    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Georgia
    ${COUNTRY_CODE}           Set Variable    268
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    140
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test43 - TCXM-24227 - Verify: AP Can Be Configured To New Zealand
    [Documentation]         AP's country code is changed to New Zealand and result it verified on UI level
    [Tags]                  tcxm-24227    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    New Zealand
    ${COUNTRY_CODE}           Set Variable    554
    ${SHORT_COUNTRY}          Set Variable    Zealand
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    165
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE} ${SHORT_COUNTRY}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}   ${SHORT_COUNTRY}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test44 - TCXM-24879 - Verify: AP Can Be Configured To US Virgin Island
    [Documentation]         AP's country code is changed to US Virgin Islan and result it verified on UI level
    [Tags]                  tcxm-24879    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    US Virgin Islands
    ${COUNTRY_CODE}           Set Variable    850
    ${SHORT_COUNTRY}          Set Variable    Virgin
    ${NEW_WiFi0_CHANNEL}      Set Variable    11
    ${NEW_WiFi1_CHANNEL}      Set Variable    165
    ${NEW_WiFi2_CHANNEL}      Set Variable    229

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE} ${SHORT_COUNTRY}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}   ${SHORT_COUNTRY}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test45 - TCXM-41044 - Verify: AP Can Be Configured To Mexico
    [Documentation]         AP's country code is changed to Mexico and result it verified on UI level
    [Tags]                  tcxm-41044    development   ap-4000    ap-5010    ap-5050    mexico
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Mexico
    ${COUNTRY_CODE}           Set Variable    484
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    165
    ${NEW_WiFi2_CHANNEL}      Set Variable    229

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test46 - TCXM-41413 - Verify: AP Can Be Configured To Kazakhstan
    [Documentation]         AP's country code is changed to Kazakhstan and result it verified on UI level
    [Tags]                  tcxm-41413    development   ap-4000    ap-5010    ap-5050dfs
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Kazakhstan
    ${COUNTRY_CODE}           Set Variable    398
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    48
    ${NEW_WiFi2_CHANNEL}      Set Variable    229

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test47 - TCXM-41855 - Verify: AP Can Be Configured To People's Republic of China
    [Documentation]         AP's country code is changed to People's Republic of China and result it verified on UI level
    [Tags]                  tcxm-41855    development   ap-4000    ap-5010    ap-5050
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    People's Republic of China
    ${COUNTRY_CODE}           Set Variable    156
    ${SHORT_COUNTRY}          Set Variable    China
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    165
    ${NEW_WiFi2_CHANNEL}      Set Variable    229

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE} ${SHORT_COUNTRY}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}   ${SHORT_COUNTRY}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test48 - TCXM-42053 - Verify: AP Can Be Configured To Taiwan
    [Documentation]         AP's country code is changed to Taiwan and result it verified on UI level
    [Tags]                  tcxm-42053    development   ap-4000    ap-5010    ap-5050
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Taiwan
    ${COUNTRY_CODE}           Set Variable    158
    ${NEW_WiFi0_CHANNEL}      Set Variable    11
    ${NEW_WiFi1_CHANNEL}      Set Variable    165
    ${NEW_WiFi2_CHANNEL}      Set Variable    229

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test49 - TCXM-41319 - Verify: AP Can Be Configured To Singapore
    [Documentation]         AP's country code is changed to Singapore and result it verified on UI level
    [Tags]                  tcxm-41319    development   ap-4000    ap-5010    ap-5050
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Singapore
    ${COUNTRY_CODE}           Set Variable    702
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    165
    ${NEW_WiFi2_CHANNEL}      Set Variable    229

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test50 - TCXM-40000 - Verify: AP Can Be Configured To Indonesia
    [Documentation]         AP's country code is changed to Indonesia and result it verified on UI level
    [Tags]                  tcxm-40000    development   ap-4000    ap-5010
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Indonesia
    ${COUNTRY_CODE}           Set Variable    360
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    48
    ${NEW_WiFi2_CHANNEL}      Set Variable    229

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test51 - TCXM-39969 - Verify: AP Can Be Configured To Thailand
    [Documentation]         AP's country code is changed to Thailand and result it verified on UI level
    [Tags]                  tcxm-39969    development   ap-4000    ap-5010
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Thailand
    ${COUNTRY_CODE}           Set Variable    764
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    165
    ${NEW_WiFi2_CHANNEL}      Set Variable    229

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test52 - TCXM-39498 - Verify: AP Can Be Configured To Republic of the Philippines
    [Documentation]         AP's country code is changed to Republic of the Philippines and result it verified on UI level
    [Tags]                  tcxm-39498    development   ap-4000    ap-5010
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Republic of the Philippines
    ${COUNTRY_CODE}           Set Variable    608
    ${SHORT_COUNTRY}          Set Variable    Philippines
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    165
    ${NEW_WiFi2_CHANNEL}      Set Variable    229

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE} ${SHORT_COUNTRY}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}   ${SHORT_COUNTRY}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test53 - TCXM-39817 - Verify: AP Can Be Configured To Vietnam
    [Documentation]         AP's country code is changed to Vietnam and result it verified on UI level
    [Tags]                  tcxm-39817    development   ap-4000    ap-5010
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Vietnam
    ${COUNTRY_CODE}           Set Variable    704
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    165
    ${NEW_WiFi2_CHANNEL}      Set Variable    229

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test54 - TCXM-39629 - Verify: AP Can Be Configured To South Africa
    [Documentation]         AP's country code is changed to South Africa and result it verified on UI level
    [Tags]                  tcxm-39629    development   ap-4000    ap-5010    ap-5050
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    South Africa
    ${COUNTRY_CODE}           Set Variable    710
    ${SHORT_COUNTRY}          Set Variable    Africa
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    165
    ${NEW_WiFi2_CHANNEL}      Set Variable    229

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE} ${SHORT_COUNTRY}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}   ${SHORT_COUNTRY}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test55 - TCXM-39745 - Verify: AP Can Be Configured To Dominican Republic
    [Documentation]         AP's country code is changed to Dominican Republic and result it verified on UI level
    [Tags]                  tcxm-39745    development   ap-4000    ap-5010    ap-5050
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Dominican Republic
    ${COUNTRY_CODE}           Set Variable    214
    ${SHORT_COUNTRY}          Set Variable    Dominican
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    165
    ${NEW_WiFi2_CHANNEL}      Set Variable    229

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE} ${SHORT_COUNTRY}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}   ${SHORT_COUNTRY}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test56 - TCXM-40014 - Verify: AP Can Be Configured To Macao
    [Documentation]         AP's country code is changed to Macao and result it verified on UI level
    [Tags]                  tcxm-40014    development   ap-4000    ap-5010    ap-5050
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Macao
    ${COUNTRY_CODE}           Set Variable    446
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    165
    ${NEW_WiFi2_CHANNEL}      Set Variable    229

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test57 - TCXM-41790 - Verify: AP Can Be Configured To Russia
    [Documentation]         AP's country code is changed to Russia and result it verified on UI level
    [Tags]                  tcxm-41790    development   ap-4000    ap-5010    ap-5050dfs
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Russia
    ${COUNTRY_CODE}           Set Variable    643
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    48
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test58 - TCXM-41373 - Verify: AP Can Be Configured To Ecuador
    [Documentation]         AP's country code is changed to Ecuador and result it verified on UI level
    [Tags]                  tcxm-41373    development   ap-4000    ap-5010    ap-5050
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Ecuador
    ${COUNTRY_CODE}           Set Variable    218
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    165
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test59 - TCXM-41214 - Verify: AP Can Be Configured To Kuwait
    [Documentation]         AP's country code is changed to Kuwait and result it verified on UI level
    [Tags]                  tcxm-41214    development   ap-4000    ap-5010    ap-5050dfs
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Kuwait
    ${COUNTRY_CODE}           Set Variable    414
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    48
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test60 - TCXM-39674 - Verify: AP Can Be Configured To Qatar
    [Documentation]         AP's country code is changed to Qatar and result it verified on UI level
    [Tags]                  tcxm-39674    development   ap-4000    ap-5010
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Qatar
    ${COUNTRY_CODE}           Set Variable    634
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    48
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test61 - TCXM-39306 - Verify: AP Can Be Configured To U.A.E.
    [Documentation]         AP's country code is changed to U.A.E. and result it verified on UI level
    [Tags]                  tcxm-39306    development    ap-5010
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    U.A.E.
    ${COUNTRY_CODE}           Set Variable    784
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    165
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test62 - TCXM-39413 - Verify: AP Can Be Configured To Saudi Arabia
    [Documentation]         AP's country code is changed to Saudi Arabia and result it verified on UI level
    [Tags]                  tcxm-39413    development   ap-5010
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Saudi Arabia
    ${COUNTRY_CODE}           Set Variable    682
    ${SHORT_COUNTRY}          Set Variable    Saudi
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    161
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}  ${SHORT_COUNTRY}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}   ${SHORT_COUNTRY}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test63 - TCXM-39371 - Verify: AP Can Be Configured To Brazil
    [Documentation]         AP's country code is changed to Brazil and result it verified on UI level
    [Tags]                  tcxm-39371    development   ap-5010
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Brazil
    ${COUNTRY_CODE}           Set Variable    76
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    165
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test64 - TCXM-39262 - Verify: AP Can Be Configured To Japan
    [Documentation]         AP's country code is changed to Japan and result it verified on UI level
    [Tags]                  tcxm-39262    development   ap-4000    ap-5010
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Japan
    ${COUNTRY_CODE}           Set Variable    4014
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    48
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test65 - TCXM-39997 - Verify: AP Can Be Configured To Guyana
    [Documentation]         AP's country code is changed to Guyana and result it verified on UI level
    [Tags]                  tcxm-39997    development   ap-4000
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Guyana
    ${COUNTRY_CODE}           Set Variable    328
    ${NEW_WiFi0_CHANNEL}      Set Variable    11
    ${NEW_WiFi1_CHANNEL}      Set Variable    165
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test66 - TCXM-39481 - Verify: AP Can Be Configured To India
    [Documentation]         AP's country code is changed to India and result it verified on UI level
    [Tags]                  tcxm-39481    development   ap-4000    ap-5010    ap-5050
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    India
    ${COUNTRY_CODE}           Set Variable    356
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    165
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test67 - TCXM-41231 - Verify: AP Can Be Configured To Malaysia
    [Documentation]         AP's country code is changed to Malaysia and result it verified on UI level
    [Tags]                  tcxm-41231    development   ap-5050
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Malaysia
    ${COUNTRY_CODE}           Set Variable    458
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    165
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test68 - TCXM-41666 - Verify: AP Can Be Configured To Korea
    [Documentation]         AP's country code is changed to Korea and result it verified on UI level
    [Tags]                  tcxm-41666    development   ap-5050
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Korea
    ${COUNTRY_CODE}           Set Variable    410
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    165
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test69 - TCXM-42002 - Verify: AP Can Be Configured To Hong Kong
    [Documentation]         AP's country code is changed to Hong Kong and result it verified on UI level
    [Tags]                  tcxm-42002    development   ap-5050
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}                Set Variable    Hong Kong
    ${COUNTRY_CODE}           Set Variable    344
    ${SHORT_COUNTRY}          Set Variable    Hong
    ${NEW_WiFi0_CHANNEL}      Set Variable    13
    ${NEW_WiFi1_CHANNEL}      Set Variable    165
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}    ${SHORT_COUNTRY}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}   ${SHORT_COUNTRY}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

Test70 - TCXM-20769 - Verify: A Country Cannot Be Reconfigured To "United States (840)"
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

Test71 - TCXM-20771 - Verify: A Country Cannot Be Reconfigured To "Canada (124)"
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

Test72 - TCXM-20768 - Verify: "United States (840)" Country Cannot Be Reconfigured
    [Documentation]    AP is configured to US and cannot be reconfigured to a different country.
    [Tags]             tcxm-20768    development    fcc
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
    ${OUTPUT}=             Send Commands       ${SPAWN}      show boot-param
    Log to console                            ${OUTPUT}
    Close Spawn                               ${SPAWN}
    Should Contain Any                        ${OUTPUT}    FCC     840
    should be equal as integers               ${REBOOT_STATUS}        1

Test73 - TCXM-20770 - Verify: "Canada (124)" Country Cannot Be Reconfigured
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
    ${OUTPUT}=             Send Commands       ${SPAWN}      show boot-param
    Log to console                            ${OUTPUT}
    Close Spawn                               ${SPAWN}
    Should Contain Any                        ${OUTPUT}    Canada     124
    should be equal as integers               ${REBOOT_STATUS}        1

Test74 - TCXM-34876 - Verify: D360 Channels Can Be Configured
    [Documentation]         2.4 and 5 GHz channel is configured and verified on CLI on UI level
    [Tags]                  tcxm-34876    development   fcc
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${NEW_WiFi0_CHANNEL}      Set Variable    11
    ${NEW_WiFi1_CHANNEL}      Set Variable    165
    ${NEW_WiFi2_CHANNEL}      Set Variable    93

    ${result}=                  Login User          ${tenant_username}    ${tenant_password}
    SetWiFi_0_1_2_Channel       ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}
    VerifyInterfacesAreUP
    Log to Console              RevertDeviceToTemplate
    Revert Device to Template   ${ap1.serial}

*** Keywords ***
InitialSetup
    Login User      ${tenant_username}      ${tenant_password}
    delete all devices
    delete all network policies
    delete_all_ssids

    ${onboard_result}=      onboard device quick     ${ap1}
    ${search_result}=       search device    device_serial=${ap1.serial}
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

    ${NUM}=                        Generate Random String    5     012345678
    Log to Console                 Creating Network Policy 1
    Set Suite Variable             ${POLICY}                       personal_wl0_wl1_wl2_${NUM}
    Set Suite Variable             ${SSID_00}                      wl0_wl1_${NUM}
    Set Suite Variable             ${SSID_01}                      wl2_${NUM}
    Set To Dictionary              ${WIRELESS_PESRONAL_00}         ssid_name=${SSID_00}
    Set To Dictionary              ${WIRELESS_PESRONAL_04}         ssid_name=${SSID_01}

    Log to Console                 Creating Network Policy
    ${STATUS}                      Create Network Policy    ${POLICY}      ${WIRELESS_PESRONAL_00}
    should be equal as strings     '${STATUS}'       '1'

# Add 6e SSID
# Don't configure 6e SSID if this is not AP5010
    run keyword if    "${ap1.model}" == "AP5010"    Log to Console    Create6e_SSID
    ...         AND    ${STATUS}   create ssid to policy   ${POLICY}   &{WIRELESS_PESRONAL_04}
    ...         AND    should be equal as strings     '${STATUS}'    '1'

    ${UPDATE}   Update Network Policy To Ap   ${POLICY}   ${ap1.serial}   Complete
    should be equal as strings    '${UPDATE}'   '1'

    Wait Until Device Online       ${ap1.serial}
    ${AP_STATUS}                   get device status     device_mac=${ap1.mac}
    Should Be Equal As Strings    '${AP_STATUS}'    'green'

    Logout User
    Sleep   10
    Quit Browser


SetCountryCodeAndVerify
    [Documentation]    AP is configured to a country provided in ${country} and it is verified that operation was successful.
    ...                ${country} - name of the country
    ...                ${country_code} - numeric code of the country
    ...                ${short_name} - short name for countries with multiple words names
    [Arguments]        ${country}     ${country_code}     ${short_name}=noName

    Log                         ${country}
    Log to Console              ${country}
    ${result}=                  Login User          ${tenant_username}    ${tenant_password}
    ${COUNTRY_STATUS}=          Change Country      ${ap1.serial}         ${country}
    Wait Until Device Reboots   ${ap1.serial}
    sleep    10
    refresh devices page
    ${AP_STATUS2}=              get device status       device_serial=${ap1.serial}
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
    Should Contain                      ${OUTPUT0}              ${country_code}
    Log to Console                      AP_COUNTRY: ${AP_COUNTRY}
    Log to Console                      short_name: ${short_name}

    Run Keyword If      "${short_name}" == "noName"    Should Contain    ${AP_COUNTRY}   ${country}
    ...         ELSE    Should Contain    ${AP_COUNTRY}   ${short_name}

    Log to Console                      GET_FLAG_STATUS: ${GET_FLAG_STATUS}
    Should Not Be Equal as Integers     ${GET_FLAG_STATUS}      -1
    Log to Console                      COUNTRY_STATUS: ${COUNTRY_STATUS}
    Should Be Equal as Integers         ${COUNTRY_STATUS}       1
    Log to Console                      AP_STATUS2: ${AP_STATUS2}
    Should Be Equal as Strings          '${AP_STATUS2}'         'green'
    Log to Console                      END_RESTULTS====

VerifyInterfacesAreUP
    [Documentation]    It is verified that 3 interfaces, WiFi0, WiFi1, WiFi2, are present in running-config.

    ${WIFI0}  Set Variable    wifi0
    ${WIFI1}  Set Variable    wifi1
    ${WIFI2}  Set Variable    wifi2

    Log                         AP_SPAWN in VerifyInterfacesAreUP
    Log to Console              AP_SPAWN in VerifyInterfacesAreUP

    ${AP_SPAWN}=                Open Spawn          ${ap1.ip}     ${ap1.port}     ${ap1.username}     ${ap1.password}     ${ap1.platform}
    ${OUTPUT0}=                 Send                ${AP_SPAWN}   ${CMD_SHOW_RUN_CONF_INTRFC}
    Close Spawn                 ${AP_SPAWN}

    Log to Console                      RESTULTS====
    Log to Console                      RUNNING_CONFIG_INTRFC: ${OUTPUT0}
    Should Contain                      ${OUTPUT0}    ${WIFI0}
    Should Contain                      ${OUTPUT0}    ${WIFI1}
#    run keyword if    "${ap1.model}" == "AP5010"   Should Contain    ${OUTPUT0}    ${WIFI2}


SetWiFi_0_1_2_Channel
    [Documentation]    Configure wifi Channel through the DEVICE 360 page. Verify the new column values of WiFi Radio Channel and channel in acsp.
    [Arguments]         ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}

    ${WiFi0_INTERFACE}            Set Variable    WiFi0
    ${WiFi1_INTERFACE}            Set Variable    WiFi1

    ${CHANNEL0_STATUS}=           Override Ap Config Wireless Channel   ${ap1.mac}  ${WiFi0_INTERFACE}  ${NEW_WiFi0_CHANNEL}
#    should be equal as integers   ${CHANNEL0_STATUS}      1
    Sleep    10
    ${CHANNEL1_STATUS}=           Override Ap Config Wireless Channel   ${ap1.mac}  ${WiFi1_INTERFACE}  ${NEW_WiFi1_CHANNEL}
#    should be equal as integers   ${CHANNEL1_STATUS}      1
    Sleep    10
#    Run Keyword If                "${ap1.ap_type}" == "wifi6"    Log to Console    ConfigureWiFi6Channel
#    ...         AND               ${NAVIGATE}=    navigate_to_device_config_interface_wireless   ${ap1.mac}
#    ...         AND               should be equal as integers   ${NAVIGATE}   1
#    ...         AND               ${CHANNEL2_STATUS}=           override_wifi2_channel		${NEW_WiFi2_CHANNEL}
#    ...         AND               should be equal as integers   ${CHANNEL2_STATUS}      1

    Refresh Devices Page
# Update Device: Delta is Default
    ${DEVICE_UPDATE}=         Update Override Configuration To Device   ${ap1.serial}
    should be equal as integers     ${DEVICE_UPDATE}    1
    Sleep    60
    ${AP_SPAWN1}=             Open Spawn    ${ap1.ip}   ${ap1.port}   ${ap1.username}   ${ap1.password}   ${ap1.cli_type}
    ${ACSP_WIFI0}=            Send Commands             ${AP_SPAWN1}         show acsp | in wifi0
    ${ACSP_WIFI1}=            Send Commands             ${AP_SPAWN1}         show acsp | in wifi1
#    ${ACSP_WIFI2}=            Send Commands             ${AP_SPAWN1}         show acsp | in wifi2
    Sleep    60
    Close Spawn               ${AP_SPAWN1}
    Refresh Devices Page
    ${DEV_CHANNEL0}=          Get Ap WiFi0 Channel      ${ap1.serial}
    ${DEV_CHANNEL1}=          Get Ap WiFi1 Channel      ${ap1.serial}
#    ${DEV_CHANNEL2}           Get Ap Wifi2 Channel      ${ap1.serial}

    Log to Console            ACSP_WIFI0: ${ACSP_WIFI0}
    Log to Console            DEV_CHNNEL0: ${DEV_CHANNEL0}
    should be equal as strings    '${NEW_WIFI0_CHANNEL}'    '${DEV_CHANNEL0}'
    should contain            ${ACSP_WIFI0}             ${DEV_CHANNEL0}

    Log to Console            ACSP_WIFI1: ${ACSP_WIFI1}
    Log to Console            DEV_CHNNEL1: ${DEV_CHANNEL1}
    should be equal as strings    '${NEW_WIFI1_CHANNEL}'    '${DEV_CHANNEL1}'
    should contain            ${ACSP_WIFI1}             ${DEV_CHANNEL1}

#    Run Keyword If            "${ap1.ap_type}" == "wifi6"    Log to Console    ACSP_WIFI2: ${ACSP_WIFI2}
#    ...         AND           Log to Console            DEV_CHNNEL2: ${DEV_CHANNEL2}
#    ...         AND           should contain            ${NEW_WIFI2_CHANNEL}      ${DEV_CHANNEL2}
#    ...         AND           should contain            ${ACSP_WIFI2}             ${DEV_CHANNEL2}



SetWiFi_0_1_2_Channel_tested_working
    [Documentation]     The following is working code. Configure wifi Channel through the DEVICE 360 page. Verify the new column values of WiFi Radio Channel and channel in acsp.
    [Arguments]         ${NEW_WiFi0_CHANNEL}    ${NEW_WiFi1_CHANNEL}    ${NEW_WiFi2_CHANNEL}

    ${WiFi0_INTERFACE}            Set Variable    WiFi0
    ${WiFi1_INTERFACE}            Set Variable    WiFi1

    ${CHANNEL0_STATUS}=           Override Ap Config Wireless Channel   ${ap1.mac}  ${WiFi0_INTERFACE}  ${NEW_WiFi0_CHANNEL}
    should be equal as integers   ${CHANNEL0_STATUS}      1
    ${CHANNEL1_STATUS}=           Override Ap Config Wireless Channel   ${ap1.mac}  ${WiFi1_INTERFACE}  ${NEW_WiFi1_CHANNEL}
    should be equal as integers   ${CHANNEL1_STATUS}      1
    Run Keyword If                "${ap1.ap_type}" == "wifi6"    Log to Console    ConfigureWiFi6Channel
    ...         AND               ${NAVIGATE}=    navigate_to_device_config_interface_wireless   ${ap1.mac}
    ...         AND               should be equal as integers   ${NAVIGATE}   1
    ...         AND               ${CHANNEL2_STATUS}=           override_wifi2_channel		${NEW_WiFi2_CHANNEL}
    ...         AND               should be equal as integers   ${CHANNEL2_STATUS}      1

    Refresh Devices Page
# Update Device: Delta is Default
    ${DEVICE_UPDATE}=         Update Override Configuration To Device   ${ap1.serial}
    should be equal as integers     ${DEVICE_UPDATE}    1
    Sleep    60
    ${AP_SPAWN1}=             Open Spawn    ${ap1.ip}   ${ap1.port}   ${ap1.username}   ${ap1.password}   ${ap1.cli_type}
    ${ACSP_WIFI0}=            Send Commands             ${AP_SPAWN1}         show acsp | in wifi0
    ${ACSP_WIFI1}=            Send Commands             ${AP_SPAWN1}         show acsp | in wifi1
    ${ACSP_WIFI2}=            Send Commands             ${AP_SPAWN1}         show acsp | in wifi2
    Sleep    60
    Close Spawn               ${AP_SPAWN1}
    Refresh Devices Page
    ${DEV_CHANNEL0}=          Get Ap WiFi0 Channel      ${ap1.serial}
    ${DEV_CHANNEL1}=          Get Ap WiFi1 Channel      ${ap1.serial}
    ${DEV_CHANNEL2}           Get Ap Wifi2 Channel      ${ap1.serial}

    Log to Console            ACSP_WIFI0: ${ACSP_WIFI0}
    Log to Console            DEV_CHNNEL0: ${DEV_CHANNEL0}
    should be equal as integers  ${NEW_WIFI0_CHANNEL}      ${DEV_CHANNEL0}
    should contain            ${ACSP_WIFI0}             ${DEV_CHANNEL0}

    Log to Console            ACSP_WIFI1: ${ACSP_WIFI1}
    Log to Console            DEV_CHNNEL1: ${DEV_CHANNEL1}
    should contain            ${NEW_WIFI1_CHANNEL}      ${DEV_CHANNEL1}
    should contain            ${ACSP_WIFI1}             ${DEV_CHANNEL1}

    Run Keyword If            "${ap1.ap_type}" == "wifi6"    Log to Console    ACSP_WIFI2: ${ACSP_WIFI2}
    ...         AND           Log to Console            DEV_CHNNEL2: ${DEV_CHANNEL2}
    ...         AND           should contain            ${NEW_WIFI2_CHANNEL}      ${DEV_CHANNEL2}
    ...         AND           should contain            ${ACSP_WIFI2}             ${DEV_CHANNEL2}


