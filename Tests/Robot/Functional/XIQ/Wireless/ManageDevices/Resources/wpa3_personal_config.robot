*** Variables ***

###Personal Network##
&{BORADCAST_SSID_DEFAULT}=          WIFI0=Enable        WIFI1=Enable        WIFI2=Enable
&{WIRELESS_PESRONAL_NW1}            ssid_name=automation_wpa3_personal     network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}    auth_profile=&{PERSONAL_AUTH_PROFILE1}
&{PERSONAL_AUTH_PROFILE1}           auth_type=PSK   key_encryption=&{PSK_KEY_ENCRYPTION1}   cwp_config=&{PSK_CWP_DEFAULT}
&{PSK_KEY_ENCRYPTION1}              key_management=WPA3 (SAE)   sae_group=All  transition_mode=enable   key_type=ASCII  key_value=Extreme@123  anti_logging_Threshold=10
&{PSK_CWP_DEFAULT}                  enable_cwp=Disable

