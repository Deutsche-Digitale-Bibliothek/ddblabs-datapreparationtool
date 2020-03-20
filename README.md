![Data Preparation Tool](https://github.com/olivergoetze/datapreparationtool/raw/master/dpt_screenshot.png "Data Preparation Tool")

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/validify) 

Das DDB Data Preparation Tool ist eine Open-Source-Anwendung zur Aufbereitung von Daten im [EAD(DDB)-Format](https://wiki.deutsche-digitale-bibliothek.de/pages/viewpage.action?pageId=19010180) für den Ingest in die Deutsche Digitale Bibliothek und das Archivportal-D. Es wird vornehmlich zur Datenanalyse und -anpassung in der Fachstelle Archiv verwendet, soll aber auch der Validierung von Exportdateien durch Datengeber, Schnittstellenentwickler und Softwarehersteller dienen.

### Installation
#### Windows
Sie können die aktuelle Version des Data Preparation Tools unter [Releases](https://github.com/Deutsche-Digitale-Bibliothek/ddblabs-datapreparationtool/releases) herunterladen. Das Tool läuft ohne zusätzliche Software-Installation. Es wird in einer 32- und 64-bit-Version bereitgestellt; letztere Version sollte bevorzugt verwendet werden.

#### Linux und macOS
##### Voraussetzungen
- Python 3.5+
- [PyQt5](https://pypi.org/project/PyQt5/)
- [PyQtWebEngine](https://pypi.org/project/PyQtWebEngine/)
- [lxml](https://pypi.org/project/lxml/)
- [requests](https://pypi.org/project/requests/)
- [loguru](https://pypi.org/project/loguru/)
- [validify](https://pypi.org/project/validify/)
- [pandas](https://pypi.org/project/pandas/)

```
git clone https://github.com/Deutsche-Digitale-Bibliothek/ddblabs-datapreparationtool.git .
python3 main_gui.py
```


### Weiterführende Informationen ...
... finden Sie [hier](https://wiki.deutsche-digitale-bibliothek.de/display/DFD/DDB+Data+Preparation+Tool).

Bei Fragen können Sie sich gerne an die [Fachstelle Archiv der Deutschen Digitalen Bibliothek](https://pro.deutsche-digitale-bibliothek.de/fachstelle-archiv) wenden
