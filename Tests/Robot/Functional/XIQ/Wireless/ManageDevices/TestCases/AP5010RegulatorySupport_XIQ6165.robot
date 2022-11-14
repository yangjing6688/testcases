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
# Test30 - TCXM-20842 - Verify: AP Can Be Configured To Estonia
#             Verifies that AP can be configured to Country Estonia
# Test31 - TCXM-20843 - Verify: AP Can Be Configured To Liechtenstein
#             Verifies that AP can be configured to Country Liechtenstein
# Test32 - TCXM-20858 - Verify: AP Can Be Configured To Lithuania
#             Verifies that AP can be configured to Country Lithuenia
# Test33 - TCXM-20844 - Verify: AP Can Be Configured To Luxembourg
#             Verifies that AP can be configured to Country Luxembourg
# Test34 - TCXM-20845 - Verify: AP Can Be Configured To Macedonia
#             Verifies that AP can be configured to Country Macedonia
# Test35 - TCXM-20846 - Verify: AP Can Be Configured To Malta
#             Verifies that AP can be configured to Country Malta
# Test36 - TCXM-20847 - Verify: AP Can Be Configured To Montenegro
#             Verifies that AP can be configured to Country Montenegro
# Test37 - TCXM-20859 - Verify: AP Can Be Configured To Norway
#             Verifies that AP can be configured to Country Norway
# Test38 - TCXM-20850 - Verify: AP Can Be Configured To Serbia
#             Verifies that AP can be configured to Country Serbia
# Test39 - TCXM-20851 - Verify: AP Can Be Configured To Slovakia
#             Verifies that AP can be configured to Country Slovakia
# Test40 - TCXM-20852 - Verify: AP Can Be Configured To Slovenia
#             Verifies that AP can be configured to Country Slovenia
# Test41 - TCXM-20855 - Verify: AP Can Be Configured To Turkey
#             Verifies that AP can be configured to Country Turkey
# Test42 - TCXM-20779 - Verify: AP Can Be Configured To UK
#             Verifies that AP can be configured to UK
#  Test43 - TCXM-20769 - Verify: A Country Cannot Be Reconfigured To "United States (840)"
#             Verifies that AP set to World region cannot be configured to United States.
#  Test44 - TCXM-20771 - Verify: A Country Cannot Be Reconfigured To "Canada (124)"
#             Verifies that AP set to World region cannot be configured to Canada.
#  Test45 - TCXM-20768 - Verify: "United States (840)" Country Cannot Be Reconfigured
#             Verifies that AP congigured to US cannot be reconfigured to a different country
#  Test46 - TCXM-20770 - Verify: "Canada (124)" Country Cannot Be Reconfigured
#             Verifies that AP congigured to Canada cannot be reconfigured to a different country
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
Library     xiq/flows/common/Login.py
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
Library     extauto/xiq/flows/common/Login.py
Library     extauto/xiq/flows/common/Navigator.py



Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    TestBeds/${TESTBED}
Variables    Environments/Config/device_commands.yaml
Variables    Environments/Config/waits.yaml
# Variables    Tests/Robot/Functional/XIQ/Wireless/Network360Monitor/Resources/n360waits.yaml


Force Tags   testbed_1_node
Suite Setup    InitialSetup

*** Test Cases ***
Test1 - TCXM-20804 - Verify: AP Can Be Configured To Albania
    [Documentation]         AP's country code is changed to Albania and result it verified on UI level
    [Tags]                  tcxm-20804    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Albania
    ${COUNTRY_CODE}     Set Variable    8

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test2 - TCXM-20816 - Verify: AP Can Be Configured To Austria
    [Documentation]         AP's country code is changed to Austria and result it verified on UI level
    [Tags]                  tcxm-20816    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Austria
    ${COUNTRY_CODE}     Set Variable    40

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test3 - TCXM-20828 - Verify: AP Can Be Configured To Belgium
    [Documentation]         AP's country code is changed to Belgium and result it verified on UI level
    [Tags]                  tcxm-20828    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Belgium
    ${COUNTRY_CODE}     Set Variable    56

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test4 - TCXM-20829 - Verify: AP Can Be Configured To Bulgaria
    [Documentation]         AP's country code is changed to Bulgaria and result it verified on UI level
    [Tags]                  tcxm-20829    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Bulgaria
    ${COUNTRY_CODE}     Set Variable    100

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test5 - TCXM-20830 - Verify: AP Can Be Configured To Bosnia-Herzegovina
    [Documentation]         AP's country code is changed to Bosnia-Herzegovina and result it verified on UI level
    [Tags]                  tcxm-20830    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Bosnia-Herzegovina
    ${COUNTRY_CODE}     Set Variable    70

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test6 - TCXM-20772 - Verify: AP Can Be Configured To Puerto Rico
    [Documentation]         AP's country code is changed to Puerto Rico and result it verified on UI level
    [Tags]                  tcxm-20772    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}            Set Variable    Puerto Rico
    ${COUNTRY_CODE}       Set Variable    630
    ${SHORT_COUNTRY}      Set Variable    Puerto

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE} ${SHORT_COUNTRY}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}   ${SHORT_COUNTRY}
    VerifyInterfacesAreUP

Test7 - TCXM-20773 - Verify: AP Can Be Configured To Colombia
    [Documentation]         AP's country code is changed to Colombia and result it verified on UI level
    [Tags]                  tcxm-20773    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   170
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Colombia
    ${COUNTRY_CODE}     Set Variable    170

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test8 - TCXM-20786 - Verify: AP Can Be Configured To Australia
    [Documentation]         AP's country code is changed to Australia and result it verified on UI level
    [Tags]                  tcxm-20786    development
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Australia
    ${COUNTRY_CODE}     Set Variable    36

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test9 - TCXM-20798 - Verify: AP Can Be Configured To Italy
    [Documentation]         AP's country code is changed to Italy and result it verified on UI level
    [Tags]                  tcxm-20798    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Italy
    ${COUNTRY_CODE}     Set Variable    380

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test10 - TCXM-20822 - Verify: AP Can Be Configured To Poland
    [Documentation]         AP's country code is changed to Poland and result it verified on UI level
    [Tags]                  tcxm-20822    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Poland
    ${COUNTRY_CODE}     Set Variable    616

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test11 - TCXM-20848 - Verify: AP Can Be Configured To Netherlands
    [Documentation]         AP's country code is changed to Netherlands and result it verified on UI level
    [Tags]                  tcxm-20848    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Netherlands
    ${COUNTRY_CODE}     Set Variable    528

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test12 - TCXM-20860 - Verify: AP Can Be Configured To Portugal
    [Documentation]         AP's country code is changed to Portugal and result it verified on UI level
    [Tags]                  tcxm-20860    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Portugal
    ${COUNTRY_CODE}     Set Variable    620

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test13 - TCXM-20785 - Verify: AP Can Be Configured To Germany
    [Documentation]         AP's country code is changed to Germany and result it verified on UI level
    [Tags]                  tcxm-20785    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Germany
    ${COUNTRY_CODE}     Set Variable    276

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test14 - TCXM-20797 - Verify: AP Can Be Configured To France
    [Documentation]         AP's country code is changed to France and result it verified on UI level
    [Tags]                  tcxm-20797    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    France
    ${COUNTRY_CODE}     Set Variable    250

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test15 - TCXM-20810 - Verify: AP Can Be Configured To Spain
    [Documentation]         AP's country code is changed to Spain and result it verified on UI level
    [Tags]                  tcxm-20810    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Spain
    ${COUNTRY_CODE}     Set Variable    724

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test16 - TCXM-20836 - Verify: AP Can Be Configured To Finland
    [Documentation]         AP's country code is changed to Finland and result it verified on UI level
    [Tags]                  tcxm-20836    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Finland
    ${COUNTRY_CODE}     Set Variable    246

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test17 - TCXM-20853 - Verify: AP Can Be Configured To Sweden
    [Documentation]         AP's country code is changed to Sweden and result it verified on UI level
    [Tags]                  tcxm-20853    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Sweden
    ${COUNTRY_CODE}     Set Variable    752

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test18 - TCXM-20849 - Verify: AP Can Be Configured To Romania
    [Documentation]         AP's country code is changed to Romania and result it verified on UI level
    [Tags]                  tcxm-20849    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Romania
    ${COUNTRY_CODE}     Set Variable    642

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test19 - TCXM-20838 - Verify: AP Can Be Configured To Hungary
    [Documentation]         AP's country code is changed to Hungary and result it verified on UI level
    [Tags]                  tcxm-20838    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Hungary
    ${COUNTRY_CODE}     Set Variable    348

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test20 - TCXM-20854 - Verify: AP Can Be Configured To Switzerland
    [Documentation]         AP's country code is changed to Switzerland and result it verified on UI level
    [Tags]                  tcxm-20854    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Switzerland
    ${COUNTRY_CODE}     Set Variable    756

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test21 - TCXM-20831 - Verify: AP Can Be Configured To Croatia
    [Documentation]         AP's country code is changed to Croatia and result it verified on UI level
    [Tags]                  tcxm-20831    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Croatia
    ${COUNTRY_CODE}     Set Variable    191

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test22 - TCXM-20832 - Verify: AP Can Be Configured To Cyprus
    [Documentation]         AP's country code is changed to Cyprus and result it verified on UI level
    [Tags]                  tcxm-20832    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Cyprus
    ${COUNTRY_CODE}     Set Variable    196

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test23 - TCXM-20833 - Verify: AP Can Be Configured To Czech Republic
    [Documentation]         AP's country code is changed to Czech Republic and result it verified on UI level
    [Tags]                  tcxm-20833    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}            Set Variable    Czech Republic
    ${COUNTRY_CODE}       Set Variable    203
    ${SHORT_COUNTRY}      Set Variable    Czech

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE} ${SHORT_COUNTRY}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}   ${SHORT_COUNTRY}
    VerifyInterfacesAreUP

Test24 - TCXM-20834 - Verify: AP Can Be Configured To Denmark
    [Documentation]         AP's country code is changed to Denmark and result it verified on UI level
    [Tags]                  tcxm-20834    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Denmark
    ${COUNTRY_CODE}     Set Variable    208

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test25 - TCXM-20835 - Verify: AP Can Be Configured To Estonia
    [Documentation]         AP's country code is changed to Estonia and result it verified on UI level
    [Tags]                  tcxm-20835    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Estonia
    ${COUNTRY_CODE}     Set Variable    233

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test26 - TCXM-20837 - Verify: AP Can Be Configured To Greece
    [Documentation]         AP's country code is changed to Greece and result it verified on UI level
    [Tags]                  tcxm-20837    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Greece
    ${COUNTRY_CODE}     Set Variable    300

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test27 - TCXM-20839 - Verify: AP Can Be Configured To Iceland
    [Documentation]         AP's country code is changed to Iceland and result it verified on UI level
    [Tags]                  tcxm-20839    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   170
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Iceland
    ${COUNTRY_CODE}     Set Variable    352

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test28 - TCXM-20840 - Verify: AP Can Be Configured To Ireland
    [Documentation]         AP's country code is changed to Ireland and result it verified on UI level
    [Tags]                  tcxm-20840    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Ireland
    ${COUNTRY_CODE}     Set Variable    372

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test29 - TCXM-20841 - Verify: AP Can Be Configured To Latvia
    [Documentation]         AP's country code is changed to Latvia and result it verified on UI level
    [Tags]                  tcxm-20841    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Latvia
    ${COUNTRY_CODE}     Set Variable    428

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test30 - TCXM-20842 - Verify: AP Can Be Configured To Estonia
    [Documentation]         AP's country code is changed to Estonia and result it verified on UI level
    [Tags]                  tcxm-20842    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Estonia
    ${COUNTRY_CODE}     Set Variable    233

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test31 - TCXM-20843 - Verify: AP Can Be Configured To Liechtenstein
    [Documentation]         AP's country code is changed to Liechtenstein and result it verified on UI level
    [Tags]                  tcxm-20843    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Liechtenstein
    ${COUNTRY_CODE}     Set Variable    438

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test32 - TCXM-20858 - Verify: AP Can Be Configured To Lithuania
    [Documentation]         AP's country code is changed to Lithuania and result it verified on UI level
    [Tags]                  tcxm-20858    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Lithuania
    ${COUNTRY_CODE}     Set Variable    440

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test33 - TCXM-20844 - Verify: AP Can Be Configured To Luxembourg
    [Documentation]         AP's country code is changed to Luxembourg and result it verified on UI level
    [Tags]                  tcxm-20844    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Luxembourg
    ${COUNTRY_CODE}     Set Variable    442

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test34 - TCXM-20845 - Verify: AP Can Be Configured To Macedonia
    [Documentation]         AP's country code is changed to Macedonia and result it verified on UI level
    [Tags]                  tcxm-20845    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}            Set Variable    North Macedonia
    ${COUNTRY_CODE}       Set Variable    807
    ${SHORT_COUNTRY}      Set Variable    Macedonia

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE} ${SHORT_COUNTRY}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}   ${SHORT_COUNTRY}
    VerifyInterfacesAreUP

Test35 - TCXM-20846 - Verify: AP Can Be Configured To Malta
    [Documentation]         AP's country code is changed to Malta and result it verified on UI level
    [Tags]                  tcxm-20846    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Malta
    ${COUNTRY_CODE}     Set Variable    470

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test36 - TCXM-20847 - Verify: AP Can Be Configured To Montenegro
    [Documentation]         AP's country code is changed to Montenegro and result it verified on UI level
    [Tags]                  tcxm-20847    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Montenegro
    ${COUNTRY_CODE}     Set Variable    499

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test37 - TCXM-20859 - Verify: AP Can Be Configured To Norway
    [Documentation]         AP's country code is changed to Norway and result it verified on UI level
    [Tags]                  tcxm-20859    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Norway
    ${COUNTRY_CODE}     Set Variable    578

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test38 - TCXM-20850 - Verify: AP Can Be Configured To Serbia
    [Documentation]         AP's country code is changed to Serbia and result it verified on UI level
    [Tags]                  tcxm-20850    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Serbia
    ${COUNTRY_CODE}     Set Variable    688

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test39 - TCXM-20851 - Verify: AP Can Be Configured To Slovakia
    [Documentation]         AP's country code is changed to Slovakia and result it verified on UI level
    [Tags]                  tcxm-20851    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}            Set Variable    Slovak Republic
    ${COUNTRY_CODE}       Set Variable    703
    ${SHORT_COUNTRY}      Set Variable    Slovak

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE} ${SHORT_COUNTRY}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}   ${SHORT_COUNTRY}
    VerifyInterfacesAreUP

Test40 - TCXM-20852 - Verify: AP Can Be Configured To Slovenia
    [Documentation]         AP's country code is changed to Slovenia and result it verified on UI level
    [Tags]                  tcxm-20852    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Slovenia
    ${COUNTRY_CODE}     Set Variable    705

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test41 - TCXM-20855 - Verify: AP Can Be Configured To Turkey
    [Documentation]         AP's country code is changed to Turkey and result it verified on UI level
    [Tags]                  tcxm-20855    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}          Set Variable    Turkey
    ${COUNTRY_CODE}     Set Variable    792
    ${CHANNEL}          Set Variable    7

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}
    VerifyInterfacesAreUP

Test42 - TCXM-20779 - Verify: AP Can Be Configured To UK
    [Documentation]         AP's country code is changed to UK and result it verified on UI level
    [Tags]                  tcxm-20779    development     eu
    [Teardown]   run keywords     Logout User
    ...          AND              Sleep   10
    ...          AND              Quit Browser

    ${COUNTRY}            Set Variable    United Kingdom
    ${COUNTRY_CODE}       Set Variable    826
    ${SHORT_COUNTRY}      Set Variable    Kingdom

    Log to Console              SetCountryCodeAndVerify-Parameters: ${COUNTRY} ${COUNTRY_CODE} ${SHORT_COUNTRY}
    SetCountryCodeAndVerify     ${COUNTRY}    ${COUNTRY_CODE}   ${SHORT_COUNTRY}
    VerifyInterfacesAreUP

Test43 - TCXM-20769 - Verify: A Country Cannot Be Reconfigured To "United States (840)"
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

Test44 - TCXM-20771 - Verify: A Country Cannot Be Reconfigured To "Canada (124)"
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

Test45 - TCXM-20768 - Verify: "United States (840)" Country Cannot Be Reconfigured
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

Test46 - TCXM-20770 - Verify: "Canada (124)" Country Cannot Be Reconfigured
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

    ${onboard_result}=      onboard device quick     ${ap1}
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

    ${NUM}=                        Generate Random String    5     012345678
    Log to Console                 Creating Network Policy 1
    Set Suite Variable             ${POLICY}                       personal_wl0_wl1_wl2_${NUM}
    Set Suite Variable             ${SSID_00}                      wl0_wl1_${NUM}
    Set Suite Variable             ${SSID_01}                      wl2_${NUM}
    Set To Dictionary              ${WIRELESS_PESRONAL_00}         ssid_name=${SSID_00}
    Set To Dictionary              ${WIRELESS_PESRONAL_04}         ssid_name=${SSID_01}

    Log to Console                 Creating Network Policy
    ${STATUS}                      Create Network Policy    policy=${POLICY}      &{WIRELESS_PESRONAL_00}
    should be equal as strings     '${STATUS}'       '1'
    ${STATUS}                      create ssid to policy    ${POLICY}      &{WIRELESS_PESRONAL_04}
    should be equal as strings     '${STATUS}'        '1'

    ${UPDATE}                      Update Network Policy To Ap             ${POLICY}          ${ap1.serial}      Complete
    should be equal as strings     '${UPDATE}'       '1'
    Wait Until Device Online       ${ap1.serial}
    ${AP_STATUS}                   Get AP Status     ap_mac=${ap1.mac}
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
    Should Contain                      ${OUTPUT0}    ${WIFI2}
