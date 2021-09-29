# Test Bed Standard Configurations
We have standard test bed configurations that include setups for 1-5 node DUTs, traffic generators and a primary and secondary net-tools system. The user will need to choose from the topology diagrams below in order to ensure that all tests will run on a standard test setup. 

## 1-Node Topology

![1-Node Topology](/doc/img/OneNodeTopo.png)

## 2-Node Topology

![2-Node Topology](/doc/img/TwoNodeTopo.png)

## 3-Node Topology

![3-Node Topology](/doc/img/ThreeNodeTopo.png)

## 4-Node Topology

![4-Node Topology](/doc/img/FourNodeTopo.png)

## 5-Node Topology (Legacy TCL only)

![5-Node Topology](/doc/img/FiveNodeTopo.png)


There are two types of TRM yaml files. One type is a test bed yaml and the other type is the test suite yaml.

### Test Suite Yaml File
This file will contain variables and elements that are bound to the test suite and not to a test bed. This will include variables that are not part of the larger test bed and test level variables. 


### Test Bed Yaml Machine Types
All machine types are defined by the name and a number. For example the 1st and 2nd netelem should be defined as the following:
	
	netelem1
	netelem2
	
The testengine is the only machine type that does not require a number after the name. For all test bed yaml file the testengine is required and there can only be one defined. Here is a list of the supported machine types for TRM.

	netelem[x]      - The Network Element (switch)
	tgen[x]	        - The Traffic Generator Element
	endsys[x]       - The End System machine

Other types of machine can be used in this file but TRM will not check them out or use them in any way. It is best to stick to the types listed above unless the feature in TRM are not needed.

### Test Bed Yaml Machine Required Attributes
All test bed machine types require a set of attributes to be defined in order to work properly with the automation framework. The following field are required for any machine type:

	name								= The name of the device
	ip                                  = IP address
	username							= login user name
	password							= login password

For netelems we require the following in addition to the ones listed above.

	os 			    = This will determine which API to load for the device
	platform 	    = This will determine which API to load for the device
	
### Test Bed Yaml Other Types
All machine types are defined by the name and a number. For example the 1st and 2nd netelem should be defined as the following:
	
	environment 			= The yaml file general attributes
	environment_host 	    = The Virtual Machine Host information, if the test needs to interaface with it
	tgen_ports 			    = Defined the mapping between the other machine types and the tgen resource
	

# Type: Lab
This is the main environment section.

 |  Attribute  				 | Required | TRM Used   | Notes |
 | ------------------------- | -------- | ---------- | ----- |  
 |  lab 				     | REQUIRED | YES        | The version of the yaml file (1.0) |

# Type: netelem<x>
This type is the Network Element. This type of element requires a number to be placed at the end of the name. For example netelem1, netelem2. 

|  Attribute  | Required | TRM Used   | Notes |
| ----------- | -------- | ---------- | ----- |  
| name:       | REQUIRED     | YES    | unique netelem name |
| os:         | REQUIRED     | YES    | exos/eos/linux |
| platform:   | REQUIRED      | YES   | x460G2 |
| ip:         | REQUIRED     | YES | 1.1.1.3 |
| host_mac:      | OPTIONAL     | NO  | 00-aa-bb-cc-dd-ee |
| username:      | REQUIRED     | YES | netelem1 username |
| password:      | REQUIRED     | YES | netelem1 password |
| connection_agent:   | REQUIRED     | NO | telnet (default) /ssh/snmp/rest |
| port:            | OPTIONAL     | NO | rewrite L4 port for static port forwarding | 
| snmp_version:    | SNMP REQUIREMENT | NO| "v2c" # The snmp version to use (v1, v2c, or v3). |
| snmp_community_name: | SNMP REQUIREMENT | NO | "extreme123" # The community name for v1 or v2c. |
| snmp_user_name:      | SNMP REQUIREMENT | NO | "user_md5_des" # The user security name for v3 USM. |
| snmp_auth_protocol:  | SNMP REQUIREMENT | NO | "md5" # The authentication protocol used by the user_name ('noauth', 'md5', or 'sha'). |
| snmp_auth_password:  | SNMP REQUIREMENT | NO | "extreme123" # The clear text password for the auth_protocol. |
| snmp_privacy_protocol:  | SNMP REQUIREMENT | NO | "des" # The privacy protocol used by the user_name ('nopriv', 'des', '3des', 'aes128', 'aes192', or 'aes256'). |
|   snmp_privacy_password:  | SNMP REQUIREMENT | NO | "extreme123" # The clear text password for the privacy_protocol. |
|   primary_test_target:  | OPTIONAL    | NO | "True"/"False" |
|   vm_location:          | OPTIONAL    | YES | //server/netelem.ova |
|   base_cfg_location:    | OPTIONAL    | NO |{path}/netelem1.cfg |
|   mgmt_vlan:            | OPTIONAL    | NO |The netelem VLAN that provides connectivity outside of the test environment (i.e. lab network) - "VLAN_123" |
|   management_gateway_ip:  | OPTIONAL | NO |The IP of the router that provides connectivity outside of the test environment (i.e. lab network) - "10.52.16.17" |
|   management_gateway_mac:  | OPTIONAL | NO |The MAC of the router that provides connectivity outside of the test environment (i.e. lab network) - "20:b3:99:ad:78:fb" |
|   ***tgen:***       | | | The Tgen ports |        
|   --port_a:    | | | The Port name [port_(a-z)]|
|   ----ifname:  | REQUIRED | YES | The netelem's interface name, as it would be entered on the device (i.e "5", "2:3" "ge.1.2" or "eth1') |
|   ----intnet:  | REQUIRED | "intnet4" | YES | |
|   ***management:*** | | | The Management port |
|   --port_a: | | | The Port name [port_(a-z)]|
|  	----ifname: | REQUIRED | YES | The netelem's interface name, as it would be entered on the device (i.e "5", "2:3" "ge.1.2" or "eth1') |
|  	----intnet: | REQUIRED | YES | "intnetmgmt1"   | 
|   ***isl:*** | | | The inter switch link | 
|   --port_a: | | | The Port name [port_(a-z)]|
|   ----ifname: | REQUIRED | YES | The netelem's interface name, as it would be entered on the device (i.e "5", "2:3" "ge.1.2" or "eth1') |
|   ----intnet: | REQUIRED | YES | "intnetisl1" |
|   ***endsys:*** | | | The End system ports |
|   --port_a: | | | The Port name [port_(a-z)]|
|   ----ifname: | REQUIRED | YES | The netelem's interface name, as it would be entered on the device (i.e "5", "2:3" "ge.1.2" or "eth1') |
|   ----intnet: | REQUIRED | YES | "intnetisl1" |

# Type: tgen<x>
This type is the Traffic Generator  Element. This type of element requires a number to be placed at the end of the name. For example tgen1, tgen1. The port will be mapped for these devices in the tgen_ports section.

|  Attribute         | Required          | TRM Used   | Notes |
| ------------------ | ----------------- | ---------- | ----- |  
| name @tgen1_name   | REQUIRED 		 | YES        | unique tgen name |
| vendor             | REQUIRED          | YES        | ixia/ostinato/spirent |
| chassis_type       | REQUIRED          | YES        | ixia/ostinato/spirent |
| software           | REQUIRED          | NO         | 5.2.3 | 
| ipv4_address       | REQUIRED          | YES        | 1.1.1.5 |
| ipv6_address       | OPTIONAL          | YES        | 2005::5 |
| vm_ipv4_address    | IXIA REQUIREMENT) | NO         | IPv4 address of Ixia Socket Listener - 1.2.3.4 |
| vm_port            | IXIA REQUIREMENT) | YES        | "5678" | 
| username           | REQUIRED          | YES        | tgen1 username | 
| password           | REQUIRED          | YES        | tgen1 password | 
| dynamic_deployment | REQUIRED          | YES        |"True"/"False" |
| vm_location        | OPTIONAL          | YES        |Tgen.ova |


# Type: tgen_ports
This is where the mappings between the devices and the tgen are stated. It starts with the device name, in the example below the name netelem1. The port of the netelem1 is defined next as port_a. Then the tgen that will be used is defined and last the port of the tgen device is defined.

|  Attribute     | Required | TRM Used   | Notes |
| -------------- | -------- | ---------- | ----- |  
| netelem1:      | REQUIRED | YES        | The element name |
| --port_a:      | REQUIRED | YES        | The port name [port_(a-z)] |
| ----tgen_name: | REQUIRED | YES        | The tgen name *tgen1_name    
| ------ifname:  | REQUIRED | YES        | The tgen interface name (i.e "1/12/1" or "eth1') |
| ------intnet:  | REQUIRED | YES        | The interface name "intnet4" |
  

# Type: endsys<x>
This type is the End System. This type of element requires a number to be placed at the end of the name. For example endsys1, endsys2. 

|  Attribute          | Required | TRM Used   | Notes |
| ------------------- | -------- | ---------- | ----- |  
| name                | REQUIRED | YES        | endsys name |
| ipv4_address        | REQUIRED | YES        | 1.1.1.2 Either the IPv4 or IPv6 Address must be used. |
| ipv6_address        | OPTIONAL | YES        | 2005::2 Either the IPv4 or IPv6 Address must be used. |
| username            | REQUIRED | YES        | test engine user's name |
| connection_method   | REQUIRED | YES        | telnet/ssh/snmp/rest |
| ssh_port            | OPTIONAL | YES        | rewrite L4 port for static port forwarding |
| password            | REQUIRED | YES        | test engine user's password |
| dynamic_deployment  | REQUIRED | YES        | "True"/"False" |
| vm_location         | OPTIONAL | YES        | endsys.ova |
| salt_ssh_location   | OPTIONAL | YES        | endsys.sls |
  
