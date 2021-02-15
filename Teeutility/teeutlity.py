import sys

#Generic class to emulate tee -a command in unix
class Tee():
    def __init__(self, logfile):
        self.console = sys.stdout
        self.log = open(logfile, "w")

    def write(self, statement):
        self.console.write(statement)
        self.log.write(statement)
