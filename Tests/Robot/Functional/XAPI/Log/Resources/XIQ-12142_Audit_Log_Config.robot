## Author       : Kun Li
# Date          : Jan 13th 2023
# Prepare the audit log

*** Variables ***

#### This block is for First Maps creation
${1st_LOCATION_ORG}              auto test org 1st
${1st_LOCATION_STREET}           auto test building 1st
${1st_LOCATION_CITY_STATE}       auto test location 1st
${1st_LOCATION_COUNTRY}          People's Republic of China (156)

#### This block is for more maps creation, and also for location tree searching
${MAP_WIDTH}            10
${MAP_HIGHT}            10

${LOCATION_1}             auto test location1
${BUILDING_1_1}           auto test building1_1
${FLOOR_1_1_1}            auto floor 1_1_1
${BUILDING_1_2}           auto test building1_2
${FLOOR_1_2_1}            auto floor 1_2_1
${FLOOR_1_2_2}            auto floor 1_2_2

${LOCATION_2}             auto test location2
${BUILDING_2_1}           auto test building2_1
${FLOOR_2_1_1}            auto floor 2_1_1
${BUILDING_2_2}           auto test building2_2
${FLOOR_2_2_1}            auto floor 2_2_1
${FLOOR_2_2_2}            auto floor 2_2_2

################# Network Policy #################
${NW_POLICY_NAME1}            Auto_NW_POLICY_1
${PSK_WPA2CCMP_SSID_NAME}     auto_psk_wpa2_ccmp
${USER_PROFILE_NAME_VLAN2}    Auto_User_Profile_Vlan2

################# Personal WPA/WPA2/WPA3 #################
&{WIRELESS_PESRONAL_WPA2CCMP}            network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}    auth_profile=&{PERSONAL_AUTH_PROFILE_WPA2CCMP}

# Broadcast SSID setting
&{BORADCAST_SSID_DEFAULT}=          WIFI0=Enable        WIFI1=Enable

# Auth profile
&{PERSONAL_AUTH_PROFILE_WPA2CCMP}           auth_type=PSK   key_encryption=&{PSK_KEY_ENCRYPTION_WPA2CCMP}   cwp_config=&{PSK_CWP_DEFAULT}

# Key profile
&{PSK_KEY_ENCRYPTION_WPA2CCMP}              key_management=WPA2-(WPA2 Personal)-PSK    encryption_method=CCMP (AES)   key_type=ASCII Key  key_value=Extreme@123

# CWP option
&{PSK_CWP_DEFAULT}                  enable_cwp=Disable



