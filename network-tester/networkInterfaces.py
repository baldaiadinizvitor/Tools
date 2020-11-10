import subprocess

class networkInterfaces:
    def isInterfaceUp(self, interfaceName):
        isUp = False

        try:
            PARAMS = "/sys/class/net/%s/operstate" % interfaceName
            process = subprocess.Popen(['cat', PARAMS],
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if stderr:
                isUp = False
            else:
                if stdout == b'up\n':
                    isUp = True
                else:
                    isUp = False
        except Exception as ex:
            print(ex)

        return isUp

NetworkInterfaces = networkInterfaces()