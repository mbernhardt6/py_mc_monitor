#!/usr/bin/python2.7

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
server = 'localhost'
port = '25565'
recipient = 'mbernhardt6@gmail.com'
sender = 'mbernhardt6@gmail.com'
log = '/home/minecraft/scripts/mc_monitor.log'
base_path = '/home/minecraft/scripts/mc_monitor'
server_path = '/home/minecraft'
start_server = server_path + '/start-server.sh'
nocheck = base_path + 'nocheck'
pid_file = '/tmp/mc_monitor.pid'
wait_time = 300
mute_reset = 12

if __name__ == '__main__':
  # Is a reboot required?
  reboot = False
  # Will the script follow up after reboot?
  followup = False
  # Is the script muted from sending email?
  mute = False
  # Loop count to determine when to reset mute.
  mute_loop = 0
  if filer.SetPid(pid_file, log):
    logger.logMessage(log, 'Pid file set. Starting monitor.')
    while 1:
      if not (os.path.isfile(nocheck)):
        status = nettools.checkPort(server, port)
        if (status != 'open'):
          if followup and not mute:
            logger.logMessage(log,
                              '%s restart attempted. Muting until restore.' %
                              server)
            mailer.sendMail(recipient, sender,
                            'Minecraft Server Restart Failed',
                            '%s restart failed.\r\n'
                            'Will remind again after %s attempts.' %
                            (server, mute_reset))
            mute = True
            followup = False
          if reboot:
            result = subprocess.Popen(start_server, cwd=server_path)
            logger.logMessage(log, 'Server restart attempted.')
            logger.logMessage(log, '%s' % result)
            if not mute:
              mailer.sendMail(recipient, sender,
                              'Minecraft Server Down - Restart Attempted',
                              '%s was not responding and a restart has been '
                              'attempted.\r\nCheck log for details.' % server)
            reboot = False
            followup = True
          else:
            reboot = True
            logger.logMessage(log, 'Server may be down. No reboot.')
        else:
          logger.logMessage(log, 'Server Check OK')
          reboot = False
          if followup:
            mailer.sendMail(recipient, sender,
                            'Server Restart Successful',
                            '%s restart successful.\r\nServer is back online.' %
                            server)
            followup = False
          mute = False
      if mute:
        if mute_loop > mute_reset:
          logger.logMessage(log, 'Unsetting mute.')
          mute = False
          mute_loop = 0
        else:
          mute_loop += 1
      time.sleep(wait_time)
