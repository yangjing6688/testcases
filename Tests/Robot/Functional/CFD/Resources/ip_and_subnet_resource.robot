## Author        : Wenqi Cao
# Date          : May 22th 2022
# For IP Objects configuration



*** Variables ***
###### IP address ######
${IP_OBJECT_TYPE}           IP Address
${IP_OBJECT_NAME}           ip_obj_test
${IP_ADDRESS_GLOBAL}        192.168.1.1
@{IP_ADDRESSES_MORE}        192.168.1.2     192.168.1.3     192.168.1.4     192.168.1.5     192.168.1.6    192.168.1.7     192.168.1.8     192.168.1.9     192.168.1.10     192.168.1.11    192.168.1.12     192.168.1.13       192.168.1.14     192.168.1.15       192.168.1.16     192.168.1.17
@{IP_ADDRESSES_MORE_1}      192.168.2.1

###### Network ######
${NETWORK_OBJECT_TYPE}          Network
${IP_NETWORKS_OBJECT_NAME}      ip_networks_obj_test
${IP_NETWORK_GLOBAL}            192.168.1.0
${NETMASK}                      255.255.255.0
@{IP_NETWORKS_MORE}            192.168.2.0     192.168.3.0     192.168.4.0    192.168.5.0     192.168.6.0    192.168.7.0     192.168.8.0     192.168.9.0     192.168.10.0     192.168.11.0    192.168.12.0     192.168.13.0       192.168.14.0     192.168.15.0       192.168.16.0     192.168.17.0
@{IP_NETWORKS_MORE_1}          192.168.100.0

###### Host Name ######
${HOSTNAME_OBJECT_TYPE}     Host Name
${HOSTNAME_OBJECT_NAME}     hostname_obj_test
${HOSTNAME_GLOBAL}          www.hostname-global.com
@{HOSTNAME_MORE}            www.hostname-classified-1.com     www.hostname-classified-2.com     www.hostname-classified-3.com    www.hostname-classified-4.com      www.hostname-classified-5.com     www.hostname-classified-6.com     www.hostname-classified-7.com    www.hostname-classified-8.com      www.hostname-classified-9.com     www.hostname-classified-10.com     www.hostname-classified-11.com    www.hostname-classified-12.com      www.hostname-classified-13.com     www.hostname-classified-14.com     www.hostname-classified-15.com    www.hostname-classified-16.com       www.hostname-classified-17.com
@{HOSTNAME_MORE_1}          www.hostname-classified-100.com


###### Wildcard Host Name ######
${WILDHOSTNAME_OBJECT_TYPE}          Wildcard Host Name
${WILDCARD_HOSTNAME_OBJECT_NAME}     wildcard_hostname_obj_test
${WILDCARD_HOSTNAME_GLOBAL}          *.hostname_global.com
@{WILDCARD_HOSTNAME_MORE}            *.hostname-classified-1.com     *.hostname-classified-2.com     *.hostname-classified-3.com    *.hostname-classified-4.com      *.hostname-classified-5.com     *.hostname-classified-6.com     *.hostname-classified-7.com    *.hostname-classified-8.com      *.hostname-classified-9.com     *.hostname-classified-10.com     *.hostname-classified-11.com    *.hostname-classified-12.com      *.hostname-classified-13.com     *.hostname-classified-14.com     *.hostname-classified-15.com    *.hostname-classified-16.com       *.hostname-classified-17.com
@{WILDCARD_HOSTNAME_MORE_1}          *.hostname-classified-100.com

###### Wildcard Network?????? ######
${WILD_NETWORK_OBJECT_TYPE}           Wildcard
${WILDCARD_NETWORK_OBJECT_NAME}       wildcard_network_obj_test
${WILDCARD_NETWORK_GLOBAL}            192.168.1.0
${WILDCARD_NETMASK}                   0.0.0.255
@{WILDCARD_NETWORKS_MORE}             192.168.2.0     192.168.3.0     192.168.4.0    192.168.5.0     192.168.6.0    192.168.7.0     192.168.8.0     192.168.9.0     192.168.10.0     192.168.11.0    192.168.12.0     192.168.13.0       192.168.14.0     192.168.15.0       192.168.16.0     192.168.17.0
@{WILDCARD_NETWORKS_MORE_1}           192.168.100.0

###### IP Range ######
${IP_RANGE_OBJECT_TYPE}             IP Range
${IP_RANGE_OBJECT_NAME}             ip_range_obj_test
${IP_RANGE_START_GLOBAL}            192.168.1.1
${IP_RANGE_GAP}                     00
@{IP_RANGE_START_CLASSIFIED}        192.168.2.1     192.168.3.1     192.168.4.1     192.168.5.1     192.168.6.1     192.168.7.1     192.168.8.1     192.168.9.1     192.168.10.1        192.168.11.1        192.168.12.1        192.168.13.1        192.168.14.1        192.168.15.1        192.168.16.1        192.168.17.1
@{IP_RANGE_START_CLASSIFIED_1}      192.168.100.1



