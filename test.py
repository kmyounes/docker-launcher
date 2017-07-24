#/bin/env python

import getopt
import sys
import os
import docker




#init docker
dock=docker.from_env()

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "haf:", ["help", "file"])
        if (len(opts)==0 ) :
            printUsage(True)
            sys.exit(2)
        for opt, arg in opts:
            if opt in ("-h, --help"):
                printUsage()
                sys.exit(2)
            if opt in ("-f, --file"):
                print ("Reading File '" + arg +"'")
                file=open(arg, 'r')
                start_containers(file)
            if opt in ("-a , --all"):
                start_all()
    except getopt.GetoptError:
        printUsage(True)
        sys.exit(2)
    except IndexError:
        printUsage(True)
        sys.exit(2)

def printUsage(error = False):
    if error:
        print ("Unknown option or missing argument.")
    print("""
    Usage: ./docker-launcher [options] <containers list file>

    -h, --help              show this help
    -f, --file             use specific file
    -a, --all               launch all containers
    """)

def start_containers(f):
    f.seek(0)
    for entry in f.readlines():
        entry=str(entry)
        entry=entry.strip()
        print(entry)
        try:
            container=dock.containers.get(entry)
            container.start()
        except docker.errors.NotFound as err:
            print(err.args)
        except docker.errors.APIError as err:
            print(err.args)


def start_all():
    for cont in dock.containers.list(all):
        try:
            cont.start()
        except docker.errors.APIError as err:
                print(err.args)
        print("Container  " + cont.name + "  Started" )
if __name__ == "__main__":
    main(sys.argv[1:])
