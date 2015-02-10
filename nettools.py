import subprocess

def findSubnet():
  rawsubnet = subprocess.check_output("ip -f inet addr | grep global", shell=True)
  subnet = rawsubnet.split()[1].decode("utf-8")
  return subnet

def checkPort(addr, port):
  output = subprocess.check_output(
    "nmap -A %s -p %s | grep %s | awk '{print $2}'" % (addr, port, port), 
	shell=True)
  try:
    portstatus = output.split()[0].decode("utf-8")
  except:
    portstatus = "error"
  return portstatus
