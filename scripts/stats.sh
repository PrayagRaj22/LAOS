(date && echo -e "\n" && cat /proc/meminfo && echo -e "\n------------------------------\n") >>  ./statistics/meminfo.txt

(date && echo -e "\n" && cat /proc/cpuinfo | head -30 && echo -e "\n------------------------------\n") >>  ./statistics/cpuinfo.txt


(date && echo -e "\n" && cat /proc/net/dev && echo -e "\n------------------------------\n") >>  ./statistics/netinfo.txt


(date && echo -e "\n" && grep '^cpu ' /proc/stat && echo -e "\n------------------------------\n") >>  ./statistics/cpu-stats.txt