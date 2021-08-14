#!/bin/bash

function log_error () {

	local log=$1
	dt=$(get_date)

	echo $dt " $log" >> $error_log

}

function log_std () {

	local log=$1
	dt=$(get_date)

	echo $dt " $log" >> $std_log

}

function log_all () {

	local log=$1

	log_error "$log"
	log_std "$log"

}

function get_date () {

	dt=`date '+%b %d %Y %H:%M:%S'`
	echo $dt

}

################################################################################
base_dir="${BASH_SOURCE%/*}"

error_log=$base_dir/error.log
std_log=$base_dir/std.log
url="http://www.google.com"
down_flag=false

if [ "$1" == "debug" ];
then
	down_count=0
	pass_count=0
	sleep_time=5
	sleep_time_down=5
	pass_notify=2
else
	down_count=0
	pass_count=0
	sleep_time=15
	sleep_time_down=5
	pass_notify=30
fi


log_all "--------------------------------------------------------"
log_all " $0 Starting"
log_all "--------------------------------------------------------"

log_std "            URL: $url"
log_std "     sleep_time: $sleep_time"
log_std "sleep_time_down: $sleep_time_down"
log_std "    pass_notify: $pass_notify"

while true; do

	wget -q --tries=5 --timeout=5 -O - $url > /dev/null

	if [[ ! $? -eq 0 ]];
	then

		log_error "ERROR: Unable to connect to $url"
		((down_count+=1))
		down_flag=true

		if [ $down_count -eq 3 ];
		then
			log_std "ERROR: Down for 3 iterations, setting sleep_time to $sleep_time_down seconds"
			sleep_time=$sleep_time_down
			$pass_count=0
		fi

		# if [ $down_count -eq 5 ];
		# then
		# 	url="http://www.google.com"
		# fi

	else

		if [ $down_flag == true ];
		then
			log_all "RECOVERY: Connection recovered, successful connection to $url"
			sleep_time=$sleep_time
		fi

		down_flag=false
		((pass_count+=1))


	fi

	echo pass_count: $pass_count
	echo pass_notify: $pass_notify

	if [ $pass_count -ge $pass_notify ];
	then
		log_std "No outages for last $pass_notify cycles"
		pass_count=0
	fi

	echo $0 running, press ctrl-C to cancel
	sleep $sleep_time

done

