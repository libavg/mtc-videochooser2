# -*- coding: utf-8 -*-

class DirInfo:
    def __init__(self, videoInfos, dirName, title):
        self.videoInfos = videoInfos
        self.dirName = dirName
        self.title = title

class VideoInfo:
    def __init__(self, videoFile, title, description, imageFile1, imageFile2):
        self.videoFile = videoFile
        self.title = title
        self.description = description
        self.imageFile1 = imageFile1
        self.imageFile2 = imageFile2

cwarsVideoInfos = [
    VideoInfo("cwars-scene0.avi", "Pre-Title",  "", 
            "", ""),
    VideoInfo("cwars-scene1.avi", "Vorgeschichte", "Die Vorgeschichte wird erzählt",
            "Scene1.png", "Scene2.png"),
    VideoInfo("cwars-scene3.avi", "Titel", "Die Titelsequenz",
            "", ""),
    VideoInfo("cwars-scene5.avi", "Protocollarisches", "Kommunikation zwischen den Threa'in und c-beam",
            "Scene4.png", "Scene6.png"),
    VideoInfo("cwars-scene7.avi", "Viraner", "Die Flotte der Viraner wird gezeigt",
            "", ""),
    VideoInfo("cwars-scene8.avi", "Angriff der Viraner", 
            "Die Viraner greifen die Thera'in an. Die unbewaffnete c-base sendet Siri-Sonden aus, die ihre Datenbanken retten sollen. Erster Auftritt der dunklen Macht.",
            "Scene8.png", "Scene8a.png"),
    VideoInfo("cwars-scene8a.avi", "Die Dunkle Macht",
            "Begegnung der Viraner mit der dunklen Macht bei der Jagd nach der letzten Siri-Sonde",
            "", ""),
    VideoInfo("cwars-scene10.avi", "Nindith",
            "Die hier erstmals gezeigten Nindith finden die letzte überlebende Siri-Sonde und fangen sie ein.",
            "Scene10.png", "Scene10a.png"),
    VideoInfo("cwars-scene10a.avi", "Vorbereitungen",
            "", "", ""),
    VideoInfo("cwars-scene11.avi", "Ercenntnis",
            "Einer der Nindith identifiziert die Siri-Sonde",
            "Scene11.png", "Scene11a.png"),
    VideoInfo("cwars-scene12.avi", "Handelspläne",
            "Die Nindith machen sich auf die Reise zur c-base, um die Siri-Sonde einzulösen.",
            "Scene12.png", ""),
    VideoInfo("cwars-scene13.avi", "Das Dimensionsparadoxon",
            "Mithilfe des umgebauten Prospectors wird ein dimensionales Paradoxon erzeugt, das die c-base aus dem hiesigen Raum ausschneidet und durch ihr böses Gegenstück, die Base 4-5, austauscht.",
            "Scene13.png", "Scene13a.png"),
    VideoInfo("cwars-scene13a.avi", "Mean Beam",
            "Auf der Base 4-5 beginnt der Bordcomputer Mean Beam mit der Vorbereitung der geplanten Aktionen",
            "Scene14.png", "Scene17.png"),
    VideoInfo("cwars-scene15.avi", "Ankunft der Nindith",
            "Die Nindith erreicht die jetzige Base 4-5 und bereitet sich auf einen Anfgiff vor.",
            "", ""),
    VideoInfo("cwars-scene18.avi", "Paradoxe Signale",
            "Die Übertragungen der Siri-Sonde sind mit der Base 4-5 nicht kompatibel.",
            "", ""),
    VideoInfo("cwars-scene19.avi", "Paradoxe Ercenntnis",
            "Mean Beam analysiert die Signale der Siri-Sonde und erkennt, dass die Base 4-5 nur aufgrund eines Paradoxons im C-Space existieren kann.",
            "Scene19.png", "Scene19b.png"),
    VideoInfo("cwars-scene20.avi", "Umkehr",
            "Die Umkehr des dimensionalen Paradoxons beginnt.",
            "Scene20.png", ""),
    VideoInfo("cwars-scene22.avi", "Animositäten",
            "Der Nindith wird klar, dass sie es mit Viranern zu tun hat. Kommunikation wird eingeleitet.",
            "", ""),
    VideoInfo("cwars-scene24.avi", "Rüccehr der c-base",
            "Die Umkehr des Paradoxons wird abgeschlossen, und die c-base tritt wieder an die Stelle der Base 4-5.",
            "Scene24.png", "Scene24a.png"),
    VideoInfo("cwars-scene25.avi", "Nindith auf der Flucht",
            "Bevor die Nindith-Flotte von den Viranern restlos vernichtet wird, ergreift sie die Flucht.",
            "Scene25.png", "Scene25a.png"),
    VideoInfo("cwars-scene26.avi", "Mehr Thera'in",
            "Die Thera'in erhalten Verstärkung, Raumschlacht",
            "Scene25b.png", ""),
    VideoInfo("cwars-scene29.avi", "Die Schlacht Endet", 
            "Mit der Zerstörung des Viraner-Kommandoschiffes ist die Schlacht gewonnen.",
            "", ""),
    VideoInfo("cwars-scene30.avi", "Siri-Sortierung",
            "Die Siri-Sone beginnt wieder mit der Übertragung, nun an die echte c-base.",
            "Scene31.png", "Scene32.png"),
    VideoInfo("cwars-scene31.avi", "Abspann", "", "", "")
    ]

chillVideoInfos = [
    VideoInfo("sequenz_01_wos4_thg.avi", "", "", "", ""),
    VideoInfo("sequenz_02_wos4_thg.avi", "", "", "", ""),
    VideoInfo("sequenz_03_wos4_thg.avi", "", "", "", ""),
    VideoInfo("sequenz_04_wos4_thg.avi", "", "", "", ""),
    VideoInfo("sequenz_05_wos4_thg.avi", "", "", "", ""),
    VideoInfo("sequenz_06_wos4_thg.avi", "", "", "", ""),
    VideoInfo("sequenz_07_wos4_thg.avi", "", "", "", ""),
    VideoInfo("sequenz_08_wos4_thg.avi", "", "", "", ""),
    VideoInfo("sequenz_09_wos4_thg.avi", "", "", "", ""),
    VideoInfo("sequenz_10_wos4_thg.avi", "", "", "", ""),
    VideoInfo("sequenz_11_wos4_thg.avi", "", "", "", ""),
    VideoInfo("sequenz_12_wos4_thg.avi", "", "", "", ""),
    VideoInfo("sequenz_13_wos4_thg.avi", "", "", "", ""),
    VideoInfo("sequenz_14_wos4_thg.avi", "", "", "", ""),
    VideoInfo("sequenz_15_wos4_thg.avi", "", "", "", ""),
    VideoInfo("sequenz_16_wos4_thg.avi", "", "", "", ""),
    VideoInfo("sequenz_17_wos4_thg.avi", "", "", "", ""),
    VideoInfo("sequenz_18_wos4_thg.avi", "", "", "", ""),
    VideoInfo("sequenz_19_wos4_thg.avi", "", "", "", ""),
    VideoInfo("sequenz_20_wos4_thg.avi", "", "", "", ""),
    VideoInfo("sequenz_21_wos4_thg.avi", "", "", "", "")
    ]

ourDirInfos = [
    DirInfo(cwarsVideoInfos, "c-wars", "c-wars"),
    DirInfo(chillVideoInfos, "golle", "chill")
    ]
