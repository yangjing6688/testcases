*** Variables ***
&{BORADCAST_SSID_DEFAULT}=          WIFI0=Enable               WIFI1=Enable
&{XAPI_NETWORK}                     ssid_name=${XAPI_SSID}      network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}   auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}
&{DEFAULT_NETWORK}                  ssid_name=AutoOPenNw        network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}   auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}
&{OPEN_AUTHENTICATION_PROFILE0}     auth_type=Open              cwp_profile=&{OPEN_CWP}
&{OPEN_CWP}                         enable_cwp=Disable