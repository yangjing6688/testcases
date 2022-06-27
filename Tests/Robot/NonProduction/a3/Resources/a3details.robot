*** Settings ***
Resource        testsuites/a3/env/envirnoment.robot

*** Variables ***
### Server Details
${TEST_URL}     https://10.133.231.174:1443
${PAGE_TITLE}   ExtremeCloud IQ

${TEST_URL}
${PAGE_TITLE}

### Tenant Details
${TENANT_USERNAME}
${TENANT_PASSWORD}

${ELEMENT_TO_IDENTIFY}
${ELEMENT_IDENTIFY_TYPE}

${WINDOWS7}                 10.234.137.116
${WINDOWS10}                10.234.63.21
${MAC}                      10.234.178.117
${WEBDRIVER_PORT}           4444
${REMOTE_SERVER_PORT}       8270

${MU1_IP}                   10.234.63.16
${MU1_REMOTE_PORT}          8270
${MU1_USERNAME}             extreme/Extreme
${MU1_PASSWORD}             Extreme@123
${MU1_PLATFORM}             windows
${MU1_INTERFACE}            wlan0
${MU1_WIFI_MAC}             548D5A693C55
${MU1_ETH_MAC}              D03745E21F8C
${MU1_WI_FI_NETWORK}        20.1.1

${SSID_EMP}                 A3-AP13-Employee
${SSID_GUEST}               A3-AP13-Guest