# PDF-GENERATOR FÜR ZUFÄLLIGE GEOMETRISCHE OBJEKTE
import log
log.log_execution()  # Logge die Ausführung dieses Programms

### fragt benutzter nach PDF namen
### fragt benutzter nach objekt anzahl
### fragt benutzter nach Objekt form
# kreis
## dreieck
### viereck
#### 5-eck
##### 6-eck

### erstellt auf basis der eingaben eine PDF datei mit den objekten
### objekte werden zufällig auf der seite verteilt
### obkete sind mit feiner schwarzer linie gezeichnet
### objekte sind weiss gefüllt
### PDF datei wird im gleichen ordner gespeichert wie das programm

def create_pdf():
    import random
    from fpdf import FPDF

    # PDF seiten größe in mm
    PAGE_WIDTH = 210
    PAGE_HEIGHT = 297

    # frage benutzer nach PDF basis-namen
    base_name = input("Geben Sie den Basis-Namen der PDF-Dateien ein (ohne .pdf): ")
    
    # frage benutzer nach anzahl der PDF-Versionen
    while True:
        try:
            pdf_count = int(input("Wie viele PDF-Versionen möchten Sie erstellen? (1-10): "))
            if 1 <= pdf_count <= 10:
                break
            else:
                print("Bitte eine Zahl zwischen 1 und 10 eingeben.")
        except ValueError:
            print("Ungültige Eingabe. Bitte eine Zahl eingeben.")

    # frage benutzer nach objekt anzahl
    while True:
        try:
            object_count = int(input("Geben Sie die Anzahl der Objekte pro PDF ein (1-20): "))
            if 1 <= object_count <= 20:
                break
            else:
                print("Bitte eine Zahl zwischen 1 und 20 eingeben.")
        except ValueError:
            print("Ungültige Eingabe. Bitte eine Zahl eingeben.")

    # frage benutzer nach objekt form
    shapes = {
        "1": "Kreis",
        "2": "Dreieck",
        "3": "Viereck",
        "4": "5-Eck",
        "5": "6-Eck"
    }

    print("Wählen Sie die Form der Objekte:")
    for key, value in shapes.items():
        print(f"{key}: {value}")

    while True:
        shape_choice = input("Geben Sie die Nummer der gewünschten Form ein (1-5): ")
        if shape_choice in shapes:
            shape = shapes[shape_choice]
            break
        else:
            print("Ungültige Eingabe. Bitte eine Zahl zwischen 1 und 5 eingeben.")

    print(f"\n🚀 Erstelle {pdf_count} PDF-Version(en) mit je {object_count} {shape} Objekten...")
    print("=" * 60)
    
    created_pdfs = []  # Liste der erstellten PDF-Dateien
    
    # Erstelle mehrere PDF-Versionen
    for version in range(1, pdf_count + 1):
        # PDF-Name für diese Version
        if pdf_count == 1:
            pdf_name = f"{base_name}.pdf"
        else:
            pdf_name = f"{base_name}_Version_{version}.pdf"
        
        print(f"📄 Erstelle Version {version}/{pdf_count}: {pdf_name}")
        
        # Neue PDF für diese Version erstellen
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=False, margin=0)
        pdf.set_draw_color(0, 0, 0)  # schwarze linie
        pdf.set_fill_color(255, 255, 255)  # weisse füllung

        # Erstelle die Objekte für diese Version (individuelle Verteilung!)
        for _ in range(object_count):
            x = random.randint(10, PAGE_WIDTH - 30)
            y = random.randint(10, PAGE_HEIGHT - 30)
            size = random.randint(15, 30)

            # Zeichne das gewählte Objekt an zufälliger Position
            if shape == "Kreis":
                # Kreis als Ellipse mit gleicher Breite und Höhe
                pdf.ellipse(x, y, size, size, style='DF')
            
            elif shape == "Dreieck":
                # Dreieck als Polygon mit 3 Punkten
                points = [
                    (x + size/2, y),           # Spitze oben
                    (x, y + size),             # Links unten
                    (x + size, y + size)       # Rechts unten
                ]
                # fpdf hat keine polygon Funktion, zeichne mit Linien
                pdf.line(points[0][0], points[0][1], points[1][0], points[1][1])
                pdf.line(points[1][0], points[1][1], points[2][0], points[2][1])
                pdf.line(points[2][0], points[2][1], points[0][0], points[0][1])
            
            elif shape == "Viereck":
                # Rechteck
                pdf.rect(x, y, size, size, style='DF')
            
            elif shape == "5-Eck":
                # Pentagon - 5 Punkte im Kreis
                import math
                center_x, center_y = x + size/2, y + size/2
                radius = size/2
                points = []
                for i in range(5):
                    angle = i * 2 * math.pi / 5 - math.pi/2  # Start oben
                    px = center_x + radius * math.cos(angle)
                    py = center_y + radius * math.sin(angle)
                    points.append((px, py))
                
                # Zeichne Pentagon mit Linien
                for i in range(5):
                    next_i = (i + 1) % 5
                    pdf.line(points[i][0], points[i][1], points[next_i][0], points[next_i][1])
            
            elif shape == "6-Eck":
                # Hexagon - 6 Punkte im Kreis
                import math
                center_x, center_y = x + size/2, y + size/2
                radius = size/2
                points = []
                for i in range(6):
                    angle = i * 2 * math.pi / 6 - math.pi/2  # Start oben
                    px = center_x + radius * math.cos(angle)
                    py = center_y + radius * math.sin(angle)
                    points.append((px, py))
                
                # Zeichne Hexagon mit Linien
                for i in range(6):
                    next_i = (i + 1) % 6
                    pdf.line(points[i][0], points[i][1], points[next_i][0], points[next_i][1])

        # Speichere diese PDF-Version
        try:
            pdf.output(pdf_name)
            created_pdfs.append(pdf_name)
            print(f"   ✅ {pdf_name} erfolgreich erstellt!")
        except Exception as e:
            print(f"   ❌ Fehler bei {pdf_name}: {e}")

    # Zusammenfassung aller erstellten PDFs
    print("=" * 60)
    print(f"🎉 ERFOLGREICH ABGESCHLOSSEN!")
    print(f"📊 {len(created_pdfs)} PDF-Version(en) erstellt")
    print(f"📄 Jede PDF enthält {object_count} {shape} Objekte")
    print(f"🎲 Jede Version hat eine individuelle, zufällige Objektverteilung")
    print(f"📁 Alle Dateien im aktuellen Verzeichnis gespeichert")
    print()
    print("📋 Erstellte Dateien:")
    for i, pdf_file in enumerate(created_pdfs, 1):
        print(f"   {i}. {pdf_file}")
    
    if len(created_pdfs) != pdf_count:
        print(f"\n⚠️  {pdf_count - len(created_pdfs)} Datei(en) konnten nicht erstellt werden.")


# Hauptprogramm
if __name__ == "__main__":
    print("=== 📄 PDF-GENERATOR FÜR GEOMETRISCHE OBJEKTE ===")
    print("Erstellt mehrere PDF-Versionen mit individuell verteilten geometrischen Formen")
    print("🎲 Jede Version hat eine einzigartige, zufällige Objektverteilung")
    print()
    
    try:
        create_pdf()
    except KeyboardInterrupt:
        print("\n❌ Programm abgebrochen")
    except Exception as e:
        print(f"❌ Ein Fehler ist aufgetreten: {e}")
