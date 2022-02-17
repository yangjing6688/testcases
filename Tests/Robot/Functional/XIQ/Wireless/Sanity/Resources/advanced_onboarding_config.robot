*** Variables ***
&{BORADCAST_SSID_DEFAULT}       WIFI0=Enable        WIFI1=Enable

# Open Network
&{CONFIG_PUSH_OPEN_NW_01}           ssid_name=AutoOPenNw     network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}   auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}
&{OPEN_AUTHENTICATION_PROFILE0}     auth_type=Open           cwp_profile=&{OPEN_CWP}
&{OPEN_CWP}                         enable_cwp=Disable

&{DEVICE_DETAIL1}            device_type=real                              device_model=Extreme-Aerohive    device_sn=${ap1.serial}
&{LOCATION01}                loc_node=auto_location_01                     country_node=San Jose            building_node=building_01            floor_node=floor_01
&{NW_POLICY01}               policy_name=${ADVANCE_NW_POLICY1}             internal_nw_type=Enable          guest_acc_nw_type=Enable
&{INTERNAL_SSID1_CONFIG}     internal_ssid_name=${INTERNAL_SSID_NAME1}     network_type=Secure              create_global_password=Enable        global_passwd=Extreme@123
&{GUEST_SSID1_CONFIG}        guest_ssid_name=${GUEST_SSID_NAME1}           network_type=Unsecure            guest_access_without_login=Enable


&{DEVICE_DETAIL2}            device_type=simulated            device_model=AP550
&{LOCATION02}                loc_node=auto_location_01        country_node=Santa Clara         building_node=building_02            floor_node=floor_04
&{NW_POLICY02}               policy_name=AUTO_ADVANCE_TEST    internal_nw_type=Enable          guest_acc_nw_type=Disable
&{INTERNAL_SSID2_CONFIG}     internal_ssid_name=AUTO_TEST     network_type=Secure              create_global_password=Enable        global_passwd=Extreme@123
&{GUEST_SSID2_CONFIG}        guest_ssid_name=AUTO_GUEST       network_type=Unsecure            guest_access_without_login=Enable


&{DEVICE_DETAIL3}            device_type=simulated            device_model=AP550
&{LOCATION03}                loc_node=auto_location_01        country_node=Santa Clara         building_node=building_02            floor_node=floor_04
&{NW_POLICY03}               policy_name=OPEN_AUTO            existing_nw_policy=enable