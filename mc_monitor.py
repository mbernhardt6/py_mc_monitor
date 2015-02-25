#!/usr/local/bin/python2.7

#Homegrown Modules
import logger
import mailer
import nettools
#Python Modules
import os
import subprocess

#Variables
server = "mortimer"
port = "25565"
recipient = "mark@transcendedlife.local"
sender = "feros@transcendedlife.local"
log = "/var/log/mc_monitor.log"
basepath = "/home/mark/mc_monitor/"
reboot = basepath + ".reboot"
followup = basepath + ".followup"
nocheck = basepath + "nocheck"
mute = basepath + "mute"

if __name__ == "__main__":
  if not(os.path.isfile(nocheck)):
    status = nettools.checkPort(server, port)
    logger.logMessage(log, "Status returned %s" % status)
    
    if (status != "open"):
      if (os.path.isfile(followup) and not(os.path.isfile(mute))):
        logger.logMessage(log, "%s restart attempted. Muting until restore." % server)
        mailer.sendMail(recipient, sender, 
                        "Minecraft Server Restart Failed - Muting until restore", 
                        "%s restart failed.\r\nMuting until restore." % server)
        open(mute, 'a').close()
        os.remove(followup)
      if (os.path.isfile(reboot)):
        result = subprocess.Popen("ssh mc@%s \"./forcestop_start.sh\"" % server, shell=True)
        logger.logMessage(log, "Server restart attempted.")
        logger.logMessage(log, "%s" % result)
        if not(os.path.isfile(mute)):
          mailer.sendMail(recipient, sender,
                          "Minecraft Server Down - Restart Attempted",
                          "%s was not responding and a restart has been attempted.\r\nCheck logs for details." % server)
        os.remove(reboot)
        open(followup, 'a').close()
      else:
        open(reboot, 'a').close()
        logger.logMessage(log, "Server may be down. No reboot.")
    else:
      logger.logMessage(log, "Server Check OK")
      if (os.path.isfile(reboot)):
        os.remove(reboot)
      if (os.path.isfile(followup)):
        mailer.sendMail(recipient, sender,
                        "Server Restart Successful",
                        "%s restart successful.\r\nServer is back online." % server)
        os.remove(followup)
      if (os.path.isfile(mute)):
        os.remove(mute)