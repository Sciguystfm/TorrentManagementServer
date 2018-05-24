import os
import subprocess
import requests, json

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



def addTorrentToTransmission(torrentPath,headers):
    jsonBlob= json.dumps({
        "arguments": {
            "filename": torrentPath
        },
        "method": "torrent-add"
    })
    r = requests.post('CENSORED:9091/transmission/rpc', auth=('CENSORED', 'CENSORED'), data=jsonBlob,headers=headers)


    print (json.dumps(r.json()["result"]))
    
    try:
        print (json.dumps(r.json()["arguments"]["torrent-added"]["name"]))
    except:
        pass

    return


def establishHeaders():
    jsonBlob= json.dumps({
        "arguments": {
            "fields": ["name"]
        },
        "method": "torrent-get"
    })
    r = requests.post('CENSORED:9091/transmission/rpc', auth=('CENSORED', 'CENSORED'), data=jsonBlob)

    if (r.status_code==409):
        headers = headers = {'X-Transmission-Session-Id': r.text[r.text.find("X-Transmission-Session-Id: ")+27:-11]}
        return(headers)
    else:
        return False


def main():
    magnet = input("Magnet Link?:")
    torrentPath = generateTorrentFileFromMagnet(magnet)
    if establishHeaders() != False:
        headers= establishHeaders()
        addTorrentToTransmission(torrentPath,headers)

if __name__ == "__main__":
    main()