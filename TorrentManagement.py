# import requests
import os
import subprocess

rpc_url="rpcurlgoeshere"


def generateTorrentFileFromMagnet(magnet):
    """
    Takes a magnetic link, and generates a torrent file in the /torrentFiles directory
    using aria2. The newly created file's path is then returned
    """
    fileDir= os.getcwd()+"/torrentFiles"
    if (not os.path.exists(fileDir)):
        print("Making directory /torrentFiles")
        os.makedirs(fileDir)
    else:
        print("directory/torrentFiles Exists!")

    oldFiles=set(os.listdir(fileDir))
    print("Generating torrent file")

    command = "aria2c -d %s --bt-metadata-only=true --bt-save-metadata=true %s" % (fileDir,magnet)
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output, error = process.communicate()


    if process.returncode != 0: 
        if "errorCode=1" in error:
            print("Error: Incorrect Magnetic Link")
            exit()
        else:
            print(error)
            exit()

    newFiles=set(os.listdir(fileDir))
    try:
        generatedFile= list(newFiles - oldFiles)[0]
    except IndexError:
        print("Error: Torrent file not Generated!")
        exit()
        
    print(generatedFile,"Created!")
    print("Path to generated file: " +fileDir+"/"+generatedFile)
    return(fileDir+"/"+generatedFile)



def addTorrentToTransmission(path):
    return

def main():
    magnet = r"magnetlinkgoeshere"
    torrentPath = generateTorrentFileFromMagnet(magnet)
    addTorrentToTransmission(torrentPath)

if __name__ == "__main__":
    main()