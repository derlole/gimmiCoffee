# gimmiCoffee

## Flash server für einfache kommunikation mit dem ESP.
### server.py definiert das routing und die rückgaben u.a. auch die befehle die gespeichert werden die von der webseite kommenspäter erfolgt hier auch die auswertung ob die kaffeemaschiene bereit ist usw.

### templates sind die webseiten, welche wir zurückgeben hier nur index.js später werden das vielleicht mehrere.

### static sind die subfiles für die html seiten z.B. ist hier js und css also die funtkionen der webseite und das styling so muss man nicht alles ins html knüppeln ist so n bissi cooler.

# Funktioniert an ende wie?
### ein static server mit offener ip und offenem Port 80 hostet auf localhost:3060 den server per nginx und proxy_pass wird der localhost an die öffentlichkeit übermittelt (eine doman kann man wenn man will dazwischenschalkten um nicht die ip eingeben zu müssen.)

### zuletzt fragt der esp regelmäßig den nun öffentlichen zugänglichen Server nach Befehlen an und wenn der server welche hat wird er sie dem esp zurückgeben, wenn er keine hat gibt er ihm 'null'.

## klingt kompliziert ist aber die einfachste möglichkeit.

### die Zeilen code halten sich auch in grenzen.

### von hier aus ist nun auch eine möglichkeit mit echtem SQL server sqlite oder mongoDB möglich, da dieser server sowohl selbst als sql server fungieren kann sqlite dateien sind hier sowieso kein problem und https:// verbindungen sind für echtes python auch kein problem mehr.

## Mögliche Daten zum Speichern und wiedergeben:
### welcher nutzer hat wann wasser nachgefüllt
### welcher nutzer hat wann Bohnen nachgefüllt
### welcher nutzer hat wann einen kaffee bestellt
### welcher nutzer hat wann die maschine eingeschlatet
### 

