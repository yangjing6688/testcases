*** Variables ***

####Guest WLAN CONFIG####
${fb_web_obj}   *.facebook.com, *.geotrust.com, *.comodoca.com, *.digicert.com, *.usertrust.com, *.verisign.com, *.godaddy.com, g.symcb.com, g.symcd.com, googleads.g.doubleclick.net, *.google.com.br, *.google.com, *.doubleclick.net, *.fbsbx.com, *.atdmt.com, *.fbcdn.net, *.akamaihd.net, *.facebook.net

@{fb_cli_obj}   185.8.148.0/24  46.33.70.0/24   213.254.17.0/24  212.245.45.0/24     31.13.64.0/18   31.13.24.0/21  66.171.231.0/24     2.16.0.0/13     212.119.27.0/25     77.67.96.0/22   80.150.192.0/24     195.27.154.0/24     5.178.32.0/20

${lnkd_web_obj}     *.linkedin.com, *.geotrust.com, *.comodoca.com, *.digicert.com, *.usertrust.com, *.verisign.com, *.godaddy.com, g.symcb.com, g.symcd.com, *.recaptcha.net, *.google.com, *.licdn.com

@{lnkd_cli_obj}     108.174.10.0/24

${gle_web_obj}  *.google.com, accounts.google.com, *.geotrust.com, *.comodoca.com, *.digicert.com, *.usertrust.com, *.verisign.com, *.godaddy.com, g.symcb.com, g.symcd.com, www.googleapis.com, images-lso-opensocial.googleusercontent.com, ssl.gstatic.com, apis.google.com, accounts.google.co.jp, accounts.google.co.in

@{gle_cli_obj}  185.8.148.0/24  46.33.70.0/24   213.254.17.0/24  212.245.45.0/24     31.13.64.0/18   31.13.24.0/21  66.171.231.0/24     2.16.0.0/13     212.119.27.0/25     77.67.96.0/22   80.150.192.0/24     195.27.154.0/24     5.178.32.0/20    108.174.10.0/24    216.58.216.0/24     173.194.0.0/24     207.126.144.0/20     64.18.0.0/20     74.125.0.0/16     66.102.0.0/20     209.85.128.0/17     72.14.192.0/18     66.249.64.0/19     64.233.160.0/19     216.239.32.0/19

&{GUEST_OPEN_NW0}              ssid_name=${SSID_NAME0}                network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}
...                              auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}

&{GUEST_OPEN_NW1}              ssid_name=${SSID_NAME1}                network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}
...                              auth_profile=&{OPEN_AUTHENTICATION_PROFILE1}

&{GUEST_OPEN_NW2}              ssid_name=${SSID_NAME2}                network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}
...                              auth_profile=&{OPEN_AUTHENTICATION_PROFILE2}

&{GUEST_OPEN_NW3}              ssid_name=${SSID_NAME3}                network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}
...                              auth_profile=&{OPEN_AUTHENTICATION_PROFILE3}

&{GUEST_OPEN_NW4}              ssid_name=${SSID_NAME4}                network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}
...                              auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}

&{GUEST_OPEN_NW5}              ssid_name=${SSID_NAME5}                network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}
...                              auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}

&{GUEST_OPEN_NW6}              ssid_name=${SSID_NAME6}                network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}
...                              auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}

&{GUEST_OPEN_NW7}              ssid_name=${SSID_NAME7}                network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}
...                              auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}

&{BORADCAST_SSID_DEFAULT}=       WIFI0=Enable        WIFI1=Enable

&{OPEN_AUTHENTICATION_PROFILE0}     auth_type=Open    cwp_profile=&{OPEN_CWP0}

&{OPEN_AUTHENTICATION_PROFILE1}     auth_type=Open    cwp_profile=&{OPEN_CWP1}

&{OPEN_AUTHENTICATION_PROFILE2}     auth_type=Open    cwp_profile=&{OPEN_CWP2}

&{OPEN_AUTHENTICATION_PROFILE3}     auth_type=Open    cwp_profile=&{OPEN_CWP3}

&{OPEN_CWP0}        enable_ege=Enable

&{OPEN_CWP1}        enable_ege=Enable   wall_garden_profile=&{facebook_profile}

&{OPEN_CWP2}        enable_ege=Enable   wall_garden_profile=&{linkedin_profile}

&{OPEN_CWP3}        enable_ege=Enable   wall_garden_profile=&{google_profile}

&{facebook_profile}     web_objs=${fb_web_obj}  cli_objs=@{fb_cli_obj}

&{linkedin_profile}     web_objs=${lnkd_web_obj}    cli_objs=@{lnkd_cli_obj}

&{google_profile}       web_objs=${gle_web_obj}   cli_objs=@{gle_cli_obj}

