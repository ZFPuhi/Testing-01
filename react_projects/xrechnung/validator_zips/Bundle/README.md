# XRechnung Bundle

Ein integriertes Bundle mit dem Spezifikationsdokument für den Standard [XRechnung](https://xeinkauf.de/xrechnung/) und unterstützende Komponenten.

## Überblick Bestandteile

| Name                               | Version im Bundle | Kommentar |
|------------------------------------|-------------------|-----------|
| XRechnung Specification            | 3.0.1       |           |
| XRechnung Syntax-Binding           | zu 3.0.1       | kein Änderungen, kompatibel zu XRechnung 3.0.x |
| Validator                          | 1.5.0           |           |
| XRechnung Validator Konfiguration  | 2023-11-15      |           |
| XRechnung Schematron               | 2.0.2           |           |
| XRechnung Visualization            | 2023-11-15           |           |
| XRechnung Testsuite                | 2023-09-22          |           |

## Änderungen zum letzten Release

### Spezifikation

keine Änderungen

Details siehe Anhang C. Versionshistorie der Spezifikation XRechnung 3.0.1

### Syntax-Binding

keine Änderungen

Details siehe Versionshistorie

### Validator

* keine Änderungen

Details siehe: https://github.com/itplr-kosit/validator/releases/tag/v1.5.0

### Validator Konfiguration XRechnung

* Jetzt mit CEN 1.3.11 und Schematron 2.0.2
* CII-SR-453 per custom level auf "error" erhöht
* Neue Unit Tests hinzugefügt

Details siehe: https://github.com/itplr-kosit/validator-configuration-xrechnung/releases/tag/release-2023-11-15

### XRechnung Schematron Regeln

* Bug in PEPPOL-EN16931-R055 in CII behoben
* Prüfregel BR-TMP-1 entfernt wegen neuer CII-SR-454 in CEN 1.3.11
* Prüfregel BR-DE-18a aus CII entfernt wegen neuer CII-SR-453 in CEN 1.3.11
* Ungültiger Code aus der CEF EAS Codeliste entfernt

Details siehe: https://github.com/itplr-kosit/xrechnung-schematron/releases/tag/release-2.0.2

### XRechnung Visualisierung

* Minimale Änderungen

Details siehe: https://github.com/itplr-kosit/xrechnung-visualization/releases/tag/v2023-11-15

### XRechnung Testsuite

* Keine Änderungen

Details siehe: https://github.com/itplr-kosit/xrechnung-testsuite/releases/tag/release-2023-09-22

## Bundle Bestandteile Details

### Validator (Prüftool)

Das Prüftool ist ein Programm, welches XML-Dateien (Dokumente) in Abhängigkeit von ihren Dokumenttypen gegen verschiedene Validierungsregeln (XML Schema und Schematron) prüft und das Ergebnis zu einem Konformitätsbericht (Konformitätsstatus *valid* oder *invalid*) mit einer Empfehlung zur Weiterverarbeitung (*accept*) oder Ablehnung (*reject*) aggregiert. Mittels Konfiguration kann bestimmt werden, welche der Konformitätsregeln durch ein Dokument, das zur Weiterverarbeitung empfohlen (*accept*) wird, verletzt sein dürfen.

Das Prüftool selbst ist fachunabhängig und kennt weder spezifische Dokumentinhalte noch Validierungsregeln. Diese werden im Rahmen einer Prüftool-Konfiguration definiert, welche zur Anwendung des Prüftools erforderlich ist.

Weitere Details auf der [Validator Projektseite](https://github.com/itplr-kosit/validator).

### Validator Konfiguration XRechnung

Eine eigenständige Konfiguration für den Standard [XRechnung](https://xeinkauf.de/xrechnung/) wird ebenfalls auf [GitHub bereitgestellt](https://github.com/itplr-kosit/validator-configuration-xrechnung) ([Releases](https://github.com/itplr-kosit/validator-configuration-xrechnung/releases)). Diese enthält alle notwendigen Ressourcen zu der Norm EN16931 (XML-Schema und [Schematron Regeln](https://github.com/CenPC434/validation) u.a.) und die [XRechnung Schematron Regeln](https://github.com/itplr-kosit/xrechnung-schematron) in ihren aktuellen Versionen.

Weitere Details auf der [Validator Konfiguration XRechnung Projektseite](https://github.com/itplr-kosit/validator-configuration-xrechnung).

### XRechnung Schematron Regeln

Technische Implementierung der Geschäftsregeln des Standards [XRechnung](https://xeinkauf.de/xrechnung/) in Schematron Rules für XML Validierung.

Weitere Details auf der [XRechnung Schematron Regeln Projektseite](https://github.com/itplr-kosit/xrechnung-schematron).

### XRechnung Visualisierung

XSL Transformatoren für die Generierung von HTML Web-Seiten und PDF Dateien.

Diese zeigen den Inhalt von elektronischen Rechnungen an, die dem Standard [XRechnung](https://xeinkauf.de/xrechnung/) entsprechen.

Weitere Details auf der [XRechnung Visualisierung Projektseite](https://github.com/itplr-kosit/xrechnung-visualization).

### XRechnung Testsuite

Valide Testdokumente des Standards [XRechnung](https://xeinkauf.de/xrechnung/).

Diese dienen dazu, bei Organisationen, die IT-Fachverfahren herstellen und betreiben, das Verständnis der [XRechnung-Spezifikation](https://xeinkauf.de/xrechnung/versionen-und-bundles/) zu fördern, indem die umfangreichen und komplexen Vorgaben und Besonderheiten der Spezifikation durch valide Testdokumente veranschaulicht werden. Die Testdokumente stehen zur freien Verfügung für die Einbindung in eigene Testverfahren.

Weitere Details auf der [XRechnung Testsuite Projektseite](https://github.com/itplr-kosit/xrechnung-testsuite).
