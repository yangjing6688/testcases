# Author        : Senthilkumar Karuppasamy
# Description   : Common sourcing library for all the wired modules

*** Settings ***
Library     String
Library     Collections
Library     common/Utils.py
#Library     DebugLibrary
Library     common/Cli.py
Library     common/TestFlow.py

# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     xiq/flows/common/Navigator.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/configure/ExpressNetworkPolicies.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/SwitchTemplate.py
Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/manage/Location.py
Library     xiq/flows/mlinsights/Network360Plan.py
Library     xiq/flows/mlinsights/Network360Monitor.py
Library     xiq/flows/manage/Device360.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Switch.py
Library     xiq/flows/manage/Tools.py
Library     xiq/flows/manage/DeviceConfig.py
Library     xiq/flows/manage/DevicesActions.py

Library     common/Xapi.py
Library     common/XAPISwitch.py  

Variables   TestBeds/${TESTBED}
Variables   Environments/${TOPO}
Variables   Environments/${ENV}

Resource     ExtremeAutomation/Resources/Libraries/DefaultLibraries.robot
#Resource     ExtremeAutomation/Imports/AllWired.robot

#Resource    testsuites/xiq/config/waits.robot
#Resource    testsuites/xiq/topologies/${TESTBED}/${DEVICE}.robot
#Resource    testsuites/xiq/topologies/${TESTBED}/${TOPO}.robot


*** Variables ***

# Please do not change the DUT variables - if you have AP1/SW1-prefixed variables in your device file,
# just edit your device file, copy/paste those AP1/SW1 variables, and change the prefix to DEVICE.
#${DUT_CSV_FILE}             C:\\cw_automation\\testsuites\\xiq\\topologies\\${TESTBED}\\${DEVICE}.csv

#${DUT_SERIAL}               ${SW1_SERIAL}
#${DUT_CONSOLE_IP}           ${SW1_CONSOLE_IP}
#${DUT_CONSOLE_PORT}         ${SW1_CONSOLE_PORT}
#${DUT_USERNAME}             ${SW1_USERNAME}
#${DUT_PASSWORD}             ${SW1_PASSWORD}
#${DUT_MAC}                  ${SW1_MAC}
#${DUT_PLATFORM}             ${SW1_PLATFORM}
#${NOS_DIR_OLD}              ${SW1_NOS_DIR_OLD}
#${NOS_DIR_NEW}              ${SW1_NOS_DIR_NEW}
#${NOS_VERSION_OLD}          ${SW1_NOS_VERSION_OLD}
#${NOS_VERSION_NEW}          ${SW1_NOS_VERSION_NEW}
#${IQAGENT_VERSION_OLD}      ${SW1_IQAGENT_VERSION_OLD}
#${IQAGENT_VERSION_NEW}      ${SW1_IQAGENT_VERSION_NEW}
${STATUS_UP}                green
#${DUT_MGMT_IP}              ${SW1_IP}