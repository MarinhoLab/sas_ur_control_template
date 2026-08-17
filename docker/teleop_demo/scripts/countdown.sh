#!/bin/bash

RED='\033[0;31m'
NC='\033[0m' # No Color

seconds=$1

echo -e "${RED}CAUTION${NC}: The robot will ${RED}MOVE${NC}."
echo "You must have the emergency button at hand or you must STOP this program NOW."
while [ $seconds -gt 0 ]; do
   echo -e "${RED}CAUTION${NC}: The robot will move in ${RED}$seconds${NC} seconds."
   sleep 1
   : $((seconds--))
done
echo -e "------------------------------------------------"
echo -e "${RED}CAUTION${NC}: Robot is ${RED}MOVING${NC}"
