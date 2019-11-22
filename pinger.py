# This software is designed with firm-code in mind. This is also my first
# at a personal program that I decided to upload to GitHub. My college's
# wifi was causing me problems and I needed proof. This ran on my Raspberry
# Pi and gave me the proof I needed to show to the University the network was
# flawed. Forks and optimization ideas are more than welcome.

import time
import subprocess  # For executing a shell command
import datetime
import os

# The program involves the use of making .txt files to store data.
# File 1: Raw Output. Never Clears
# File 2: Daily Averages. Prints the Average and Highest Ping for that Dail
# File 3: Latency Spikes. Records date and time each time google.com pings
#        over 250ms
# File 4: Daily Records. Placeholder to record Raw Output for that day.
#        Refreshes every day (only if it runs through midnight)


# Adds the info that is already in Daily Records.txt
now = datetime.datetime.now()
current_day = now.day
current_minute = now.minute
file4 = open("Daily Records.txt", "a+")
totals_for_the_day = []
for p in file4.readlines():
    totals_for_the_day.append(float(p[:-2]))
count = 1
file4.close()

while True:
    try:
        # If you are using Windows, change the "-c" to "-n"
        text = subprocess.check_output(["ping", "-c",
                                        "50", "google.com"]).decode("utf-8")
        text = text.splitlines()
    except subprocess.CalledProcessError:
        text = ["NaN"]
        time.sleep(10)
    file = open("Output.txt", "a+")
    file3 = open("Latency Spikes.txt", "a+")
    file4 = open("Daily Records.txt", "a+")
    for index, x in enumerate(text):
        try:
            x.split()
            z = float(x[x.index("time=")+5:-3])
            totals_for_the_day.append(z)

            if(z >= 250):
                now = datetime.datetime.now()
                # Prints to console every time google.com pings >= 250ms
                print("Spike Number {0} occured during the minute frame {1}"
                      "with a ping of {2} ms".format(count, now.strftime("%X"),
                                                     z))
                file3.write("Date of spike: {0}\n"
                            .format(now.strftime("%c %Z")))
                file3.write("Ping: {0}\n".format(z))
                count += 1
            file.write(str(z))
            file.write('\n')
            file4.write(str(z))
            file4.write('\n')
        except ValueError:
            pass

    now = datetime.datetime.now()
    # Prints to console every minute to give you updates.
    if(current_minute != now.minute):
        print("Current time: {0}".format(now.strftime("%X")))
        print("Highest Ping: {0} ms".format(max(totals_for_the_day)))
        current_minute = now.minute
        count = 1
    if(current_day != now.day):
        file2 = open("Daily Averages.txt", "a+")
        file2.write("{0} Averages:\n".format(now.strftime("%Y-%m-%d")))
        file2.write("Average Ping: {0} ms".format(sum(totals_for_the_day) /
                                                  len(totals_for_the_day)))
        file2.write("\tHighest Ping: {0} ms\n".format(max(totals_for_the_day)))
        totals_for_the_day = []
        current_day = now.day
        file4.close()
        os.remove("Daily Records.txt")
        file4 = open("Daily Records.txt", "a+")
        file2.close()
    file4.close()
    file3.close()
    file.close()
