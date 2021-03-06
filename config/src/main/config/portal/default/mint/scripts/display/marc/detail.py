from com.googlecode.fascinator.common import JsonConfigHelper
from java.io import ByteArrayOutputStream
from java.util import ArrayList
from org.apache.commons.io import IOUtils
from org.apache.commons.lang import StringEscapeUtils

class DetailData:
    def __init__(self):
        pass
    
    def __activate__(self, context):
        self.__ffmpegRaw = None
        self.__ffmpegData = None
        self.__urlBase = context["urlBase"]
        
        formData = context["formData"]
        self.__sourceUrl = formData.get("from")
    
    def getSourceUrl(self):
        if self.__sourceUrl:
            return "%sauthor/detail/%s" % (self.__urlBase, self.__sourceUrl)
        return None
    
    def escape(self, text):
        return StringEscapeUtils.escapeHtml(text)

    def getFFmpegData(self, pid, index):
        if self.__ffmpegData is not None:
            output = self.__ffmpegData.get(pid).get("/" + index)
            if output is not None:
                return output
        return ""

    def getFFmpegDebugging(self, pid):
        if self.__ffmpegData is not None:
            output = self.__ffmpegData.get(pid).get("/debugOutput")
            return self.makeHtml(output)
        else:
            return "Not found!"

    # Get The MIME Type of a payload
    def getMimeType(self, pid, parent):
        if parent is not None:
            object = parent.getObject()
            if object is not None:
                try:
                    payload = object.getPayload(pid)
                    return payload.getContentType()
                except:
                    pass
        return "unknown"

    def getRawFFmpeg(self):
        return self.makeHtml(self.__ffmpegRaw)

    def getTranscodings(self):
        if self.__ffmpegData is not None:
            return self.__ffmpegData.keySet()
        else:
            return ArrayList()

    def isAudio(self, mime):
        return mime.startswith("audio/")

    def isVideo(self, mime):
        return mime.startswith("video/")

    # Turn a Python boolean into a javascript boolean
    def jsBool(self, pBool):
        if pBool:
            return "true"
        else:
            return "false"

    def makeHtml(self, input):
        input = input.replace(" ", "&nbsp;")
        input = input.replace("\r\n", "<br/>")
        input = input.replace("\r", "<br/>")
        input = input.replace("\n", "<br/>")
        input = input.replace("\\r\\n", "<br/>")
        input = input.replace("\\r", "<br/>")
        input = input.replace("\\n", "<br/>")
        return input

    def niceSize(self, size):
        # Cast to a number
        size = eval(size)
        # Bytes
        if (size > 1000):
            # KBytes
            size = size / 1000;
            if (size > 1000):
                # MBytes
                size = size / 1000;
                if (size > 1000):
                    # GBytes
                    size = size / 1000;
                    return str(round(size, 1)) + "Gb"
                else:
                    return str(round(size, 1)) + "Mb"
            else:
                return str(round(size, 1)) + "Kb"
        else:
            return str(size) + "b"

    def parseFFmpeg(self, parent):
        if parent is not None:
            object = parent.getObject()
            if object is not None:
                payload = None
                try:
                    payload = object.getPayload("ffmpeg.info")
                    # Stream the content out to string
                    out = ByteArrayOutputStream()
                    IOUtils.copy(payload.open(), out)
                    payload.close()
                    self.__ffmpegRaw = out.toString("UTF-8")
                    out.close()
                    payload.close()
                    # And parse it
                    jsonData = JsonConfigHelper(self.__ffmpegRaw)
                    if jsonData is None:
                        return False
                    else:
                        self.__ffmpegData = jsonData.getJsonMap("/outputs")
                        return True
                except:
                    if payload is not None:
                        payload.close()
        return False
    
    def getUrlBase(self):
        return self.__urlBase

