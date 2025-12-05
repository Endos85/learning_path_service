Learning Path Service


Beschreibung: REST-API zur Generierung personalisierter Learning Paths basierend auf Skills, Topics und Ressourcen. Die Pfade können erstellt, abgefragt und aufgelistet werden.

Features

Generierung von Lernpfaden (/generate) über gewünschte Skills und Topics

Speicherung von Pfaden in MongoDB

Abruf von Pfaden (/paths und /paths/{pathId})

Health-Check-Endpunkt (/healthz)

Integration mit externen Clients und OpenAI (mockbar für Tests)

Vollständig getestete API über pytest