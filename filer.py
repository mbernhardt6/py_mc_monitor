# Homegrown Modules
import logger

# Python Modules
import glob
import os
import sys


def countLines(filename):
  """Count the number of lines in a file.

  Args:
    filename: File to count lines of.

  Returns:
    Int value of the number of lines in a file.
  """
  try:
    with open(filename, 'r') as file:
      for i, l in enumerate(file):
        pass
    file.close()
    return i + 1
  except:
    return 0


def ReadFileData(target_file_name, log):
  """Read data from a file ignoring commented out lines.

  Args:
    target_file_name: Filename of file to read.

  Returns:
    Contents of file as a set.
  """
  file_contents = set()
  try:
    target_file = open(target_file_name, 'r')
    for line in target_file:
      if line.encode('utf-8')[:1] != '#':
        file_contents.add(line.encode('utf-8').replace('\n', ''))
    target_file.close()
  except:
    logger.logMessage(log, "WARNING: Unspecified error processing %s" %
        target_file_name)
  return file_contents


def tailFile(filename, tailCount):
  """Trim a file to a set line count via tail.

  Args:
    filename: Name of file to trim.
    tailCount: Number of lines to trim to.
  """
  length = countLines(filename)
  oldFile = open(filename, 'r')
  start = length - (int(tailCount) + 1)
  if (start > 0):
    arrOutFile = []
    for i, line in enumerate(oldFile):
      if (i > start):
        arrOutFile.append(line)
    oldFile.close()
    newFile = open(filename, 'wb')
    for line in arrOutFile:
      if len(line) > 0:
        newFile.write(line)
    newFile.close()
  else:
    oldFile.close()
    return 0


def SetPid(pid_file, log):
  """Function to handle check and setting pid files.

  If pid_file doesn't exist, this function will setit and return True. If the
  pid_file already exists it will return False.

  Args:
    pid_file: File to check for and possibly set.
    log: script log file.

  Returns:
    Boolean if pid_file has been set or not.
  """
  if os.path.isfile(pid_file):
    check_pid = ReadFileData(pid_file, log)
    try:
      os.getpgid(int(list(check_pid)[0]))
      logger.logMessage(log, "%s exists, exiting." % pid_file)
      return False
    except:
      try:
        logger.logMessage(log, "Stale pid: %s" % pid_file)
        os.unlink(pid_file)
      except:
        logger.logMessage(log, "Unable to clear stale pid: %s" % pid_file)
  pid = str(os.getpid())
  file(pid_file, 'w').write(pid)
  return True