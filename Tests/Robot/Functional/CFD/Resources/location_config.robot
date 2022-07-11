## Author        : Wenqi Cao
# Date          : May 22th 2022
# For the related configuration of MAP lcation

*** Variables ***

#### This block is for First Maps creation
${1st_LOCATION_ORG}              auto 1st org
${1st_LOCATION_STREET}           auto 1st building
${1st_LOCATION_CITY_STATE}       auto 1st location
${1st_LOCATION_COUNTRY}          People's Republic of China (156)

&{1st_LOC_TEST}          country_node=${1st_LOCATION_ORG}        loc_node=${1st_LOCATION_CITY_STATE}     building_node=${1st_LOCATION_STREET}        floor_node=Floor 1


#### This block is for classification rules with location
&{LOC_TEST_1}          country_node=${1st_LOCATION_ORG}        loc_node=${LOCATION_1}     building_node=${BUILDING_1}        floor_node=${FLOOR_1}
&{LOC_TEST_2}          country_node=${1st_LOCATION_ORG}        loc_node=${LOCATION_2}     building_node=${BUILDING_2}        floor_node=${FLOOR_2}
&{LOC_TEST_3}          country_node=${1st_LOCATION_ORG}        loc_node=${LOCATION_3}     building_node=${BUILDING_3}        floor_node=${FLOOR_3}
&{LOC_TEST_4}          country_node=${1st_LOCATION_ORG}        loc_node=${LOCATION_4}     building_node=${BUILDING_4}        floor_node=${FLOOR_4}
&{LOC_TEST_5}          country_node=${1st_LOCATION_ORG}        loc_node=${LOCATION_5}     building_node=${BUILDING_5}        floor_node=${FLOOR_5}
&{LOC_TEST_6}          country_node=${1st_LOCATION_ORG}        loc_node=${LOCATION_6}     building_node=${BUILDING_6}        floor_node=${FLOOR_6}
&{LOC_TEST_7}          country_node=${1st_LOCATION_ORG}        loc_node=${LOCATION_7}     building_node=${BUILDING_7}        floor_node=${FLOOR_7}
&{LOC_TEST_8}          country_node=${1st_LOCATION_ORG}        loc_node=${LOCATION_8}     building_node=${BUILDING_8}        floor_node=${FLOOR_8}
&{LOC_TEST_9}          country_node=${1st_LOCATION_ORG}        loc_node=${LOCATION_9}     building_node=${BUILDING_9}        floor_node=${FLOOR_9}
&{LOC_TEST_10}          country_node=${1st_LOCATION_ORG}        loc_node=${LOCATION_10}     building_node=${BUILDING_10}        floor_node=${FLOOR_10}
&{LOC_TEST_11}          country_node=${1st_LOCATION_ORG}        loc_node=${LOCATION_11}     building_node=${BUILDING_11}        floor_node=${FLOOR_11}
&{LOC_TEST_12}          country_node=${1st_LOCATION_ORG}        loc_node=${LOCATION_12}     building_node=${BUILDING_12}        floor_node=${FLOOR_12}
&{LOC_TEST_13}          country_node=${1st_LOCATION_ORG}        loc_node=${LOCATION_13}     building_node=${BUILDING_13}        floor_node=${FLOOR_13}
&{LOC_TEST_14}          country_node=${1st_LOCATION_ORG}        loc_node=${LOCATION_14}     building_node=${BUILDING_14}        floor_node=${FLOOR_14}
&{LOC_TEST_15}          country_node=${1st_LOCATION_ORG}        loc_node=${LOCATION_15}     building_node=${BUILDING_15}        floor_node=${FLOOR_15}
&{LOC_TEST_16}          country_node=${1st_LOCATION_ORG}        loc_node=${LOCATION_16}     building_node=${BUILDING_16}        floor_node=${FLOOR_16}
&{LOC_TEST_17}          country_node=${1st_LOCATION_ORG}        loc_node=${LOCATION_17}     building_node=${BUILDING_17}        floor_node=${FLOOR_17}
&{LOC_TEST_18}          country_node=${1st_LOCATION_ORG}        loc_node=${LOCATION_18}     building_node=${BUILDING_18}        floor_node=${FLOOR_18}
&{LOC_TEST_19}          country_node=${1st_LOCATION_ORG}        loc_node=${LOCATION_19}     building_node=${BUILDING_19}        floor_node=${FLOOR_19}
&{LOC_TEST_20}          country_node=${1st_LOCATION_ORG}        loc_node=${LOCATION_20}     building_node=${BUILDING_20}        floor_node=${FLOOR_20}


#### This block is for more maps creation, and also for location tree searching
${MAP_WIDTH}            10
${MAP_HIGHT}            10

${LOCATION_1}         auto test location1
${BUILDING_1}         auto test building1
${FLOOR_1}            auto floor 1

${LOCATION_2}         auto test location2
${BUILDING_2}         auto test building2
${FLOOR_2}            auto floor 2

${LOCATION_3}         auto test location3
${BUILDING_3}         auto test building3
${FLOOR_3}            auto floor 3

${LOCATION_4}         auto test location4
${BUILDING_4}         auto test building4
${FLOOR_4}            auto floor 4

${LOCATION_5}         auto test location5
${BUILDING_5}         auto test building5
${FLOOR_5}            auto floor 5

${LOCATION_6}         auto test location6
${BUILDING_6}         auto test building6
${FLOOR_6}            auto floor 6

${LOCATION_7}         auto test location7
${BUILDING_7}         auto test building7
${FLOOR_7}            auto floor 7

${LOCATION_8}         auto test location8
${BUILDING_8}         auto test building8
${FLOOR_8}            auto floor 8

${LOCATION_9}         auto test location9
${BUILDING_9}         auto test building9
${FLOOR_9}            auto floor 9

${LOCATION_10}         auto test location10
${BUILDING_10}         auto test building10
${FLOOR_10}            auto floor 10

${LOCATION_11}         auto test location11
${BUILDING_11}         auto test building11
${FLOOR_11}            auto floor 11

${LOCATION_12}         auto test location12
${BUILDING_12}         auto test building12
${FLOOR_12}            auto floor 12

${LOCATION_13}         auto test location13
${BUILDING_13}         auto test building13
${FLOOR_13}            auto floor 13

${LOCATION_14}         auto test location14
${BUILDING_14}         auto test building14
${FLOOR_14}            auto floor 14

${LOCATION_15}         auto test location15
${BUILDING_15}         auto test building15
${FLOOR_15}            auto floor 15

${LOCATION_16}         auto test location16
${BUILDING_16}         auto test building16
${FLOOR_16}            auto floor 16

${LOCATION_17}         auto test location17
${BUILDING_17}         auto test building17
${FLOOR_17}            auto floor 17

${LOCATION_18}         auto test location18
${BUILDING_18}         auto test building18
${FLOOR_18}            auto floor 18

${LOCATION_19}         auto test location19
${BUILDING_19}         auto test building19
${FLOOR_19}            auto floor 19

${LOCATION_20}         auto test location20
${BUILDING_20}         auto test building20
${FLOOR_20}            auto floor 20