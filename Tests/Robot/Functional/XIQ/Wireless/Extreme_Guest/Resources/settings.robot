*** Settings ***
Library     common/Screen.py
Library     common/GmailHandler.py
Library     common/CloudDriver.py
Library     common/TestFlow.py
# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     xiq/flows/globalsettings/AccountManagement.py
Library     xiq/flows/common/Navigator.py
Library     xiq/flows/extreme_guest/SplashTemplate.py
Library     xiq/flows/extreme_guest/ExtremeGuest.py
Library     xiq/flows/extreme_guest/Landing.py
Library     xiq/flows/extreme_guest/Onboarding.py
Library     xiq/flows/extreme_guest/Notification.py
Library     xiq/flows/extreme_guest/Summary.py
Library     xiq/flows/extreme_guest/ExtremeGuestUsers.py
Library     xiq/flows/extreme_guest/AnalyzeClients.py
Library     xiq/flows/extreme_guest/Reports.py
Library     xiq/flows/extreme_guest/AnalyzeUsers.py
Library     xiq/flows/extreme_guest/Dashboard.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/manage/Location.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/mlinsights/Network360Plan.py
Library     xiq/flows/configure/WirelessNetworks.py
Library     common/Cli.py
Library     Collections
Library     common/Utils.py
Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/manage/Client.py
Library     xiq/flows/configure/ExpressNetworkPolicies.py
Library     xiq/flows/extreme_guest/MuGuestPortal.py
Library     ExtremeAutomation/Imports/CommonObjectUtils.py