#!/usr/local/bin/python2.7

# Homegrown Modules
import filer
import logger
import mailer
import nettools

# Python Modules
import os
import subprocess
import time

# Variables
server = "mortimer"
port = "25565"
recipient = "mark@transcendedlife.local"
sender = "feros@transcendedlife.local"
log = "/var/log/mc_monitor.log"
base_path = "/home/mark/mc_monitor"
nocheck = base_path + "nocheck"
pid_file = "/tmp/mc_monitor.pid"
wait_time = 300

if __name__ == "__main__":
  # Is a reboot required?
  reboot = False
  # Will the script follow up after reboot?
  followup = False
  # Is the script muted from sending email?
  mute = False
  if filer.SetPid(pid_file, log):
    logger.logMessage(log, "Pid file set. Starting monitor.")
    while 1:
      if not (os.path.isfile(nocheck)):
        status = nettools.checkPort(server, port)
        if (status != "open"):
          if followup and not mute:
            logger.logMessage(log, "%s restart attempted. Muting until restore." %
                server)
            mailer.sendMail(recipient, sender,
                "Minecraft Server Restart Failed - Muting until restore",
                "%s restart failed.\r\nMuting until restore." % server)
            mute = True
            followup = False
          if reboot:
            result = subprocess.Popen("ssh mc@%s \"./forcestop_start.sh\"" %
                server, shell=True)
            logger.logMessage(log, "Server restart attempted.")
            logger.logMessage(log, "%s" % result)
            if not mute:
              mailer.sendMail(recipient, sender,
                  "Minecraft Server Down - Restart Attempted",
                  "%s was not responding and a restart has been attempted.\r\nCheck log for details."
                  % server)
            reboot = False
            followup = True
          else:
            reboot = True
            logger.logMessage(log, "Server may be down. No reboot.")
        else:
          logger.logMessage(log, "Server Check OK")
          reboot = False
          if followup:
            mailer.sendMail(recipient, sender,
                "Server Restart Successful",
                "%s restart successful.\r\nServer is back online." % server)
            followup = False
          mute = False
      time.sleep(wait_time)