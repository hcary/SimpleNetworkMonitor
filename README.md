
## HeadingConfiguration File

### Variables

#### default section
***url***
fqdn to curl to test http or https connectivity
url = http://www.google.com

***ping_ips***
ping_ips = 10.10.1.1,64.98.121.134,1.1.1.1,www.cnn.com
  
***stdout_log***
stdout_log = stdout.log

***ok_int_report***
Number of successful iterations between no error log entry
ok_int_report = 5 # 

***sleep_time_default***
Default time between curl calls in seconds
sleep_time_default = 60

***sleep_time_error***
Amount of time to sleep between curl calls in seconds when an error is detected
sleep_time_error = 10

***minutes***
minutes = 0

#### debug section
debug = True

#### devel section
gen_error = False