
import codecs

class TextHandler():
    def __init__(self):
        
        self.languageList = ["eng", "swe"]
        self.language = self.languageList[0]


        self.sweGameText = []
        self.sweMenuText = []
        self.sweTutorialText = []

        self.sweList = {
            "game": self.sweGameText, 
            "menu": self.sweMenuText,
            "tutorial": self.sweTutorialText
        }

        self.engGameText = []
        self.engMenuText = []
        self.engTutorialText = []
        
        self.engList = {
            "game": self.engGameText, 
            "menu": self.engMenuText,
            "tutorial": self.engTutorialText
        }

        # -------------------------------------------------------------------------------------------
        # fetch swedish text
        # -------------------------------------------------------------------------------------------
        
        textFile = codecs.open("text/swe/gameText.txt", "r", encoding='utf-8')
        #generaltextFile = open("gameText.txt", "r")
        for line in textFile:
            self.sweGameText.append(line)
        textFile.close()
        textFile = codecs.open("text/swe/TutorialText.txt", "r", encoding='utf-8')
        for line in textFile:
            self.sweTutorialText.append(line)
        textFile.close()
        textFile = codecs.open("text/swe/menuText.txt", "r", encoding='utf-8')
        for line in textFile:
            self.sweMenuText.append(line)
        textFile.close()

        # -------------------------------------------------------------------------------------------
        #fetch english text
        # -------------------------------------------------------------------------------------------

        textFile = codecs.open("text/eng/gameText.txt", "r", encoding='utf-8')
        for line in textFile:
            self.engGameText.append(line)
        textFile.close()
        textFile = codecs.open("text/eng/TutorialText.txt", "r", encoding='utf-8')
        for line in textFile:
            self.engTutorialText.append(line)
        textFile.close()
        textFile = codecs.open("text/eng/menuText.txt", "r", encoding='utf-8')
        for line in textFile:
            self.engMenuText.append(line)
        textFile.close()

    
    def getTextFile(self, file):
        if self.language == "eng":
            return self.engList[file]
        elif self.language == "swe":
            return self.sweList[file]
        else:
            return None
    
    def getLanguageList(self):
        return self.languageList

    def getLanguage(self):
        return self.language

    def setLanguage(self, language):
        self.language = language