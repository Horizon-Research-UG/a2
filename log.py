###
# LOG DATEI - ANFORDERUNGEN UND FUNKTIONEN
###
# WIRD VON ANDEREN FILES GELADEN
# LOGGT JEDES MAL WENN EIN PROGRAMM GETESTET/AUSGEFÜHRT WIRD
#
# DIE INFOS IN EINE LOG DATEI:
## AUFRUFNUMMER (fortlaufend nummeriert)
## AUFRUFDATUM 
## DATEINAME (des aufrufenden Programms)
## DATEIPFAD (vollständiger Pfad)
#
# LIEST DIE LOG DATEI UM DIE AUFRUFE FORTLAUFEND ZU NUMMERIEREN
# BEI FILE NAME UND PATH: BEZIEHT SICH AUF DAS PROGRAMM, WELCHES DIE LOG DATEI AUFRUFT
# NEUESTER EINTRAG STEHT IMMER OBEN
###

import os
import datetime
import inspect

# === KONFIGURATION ===
LOG_FILE = "program_log.txt"  # Name der Log-Datei

# === MODUL 1: AUFRUFENDES PROGRAMM ERMITTELN ===
def get_caller_info():
    """Findet heraus, welches Programm die Log-Funktion aufgerufen hat"""
    frame = inspect.currentframe()  # Aktueller Frame
    try:
        # 2 Ebenen zurück gehen: diese Funktion -> log_execution -> aufrufendes Programm
        caller_frame = frame.f_back.f_back
        if caller_frame is None:
            return "Unbekannt", "Unbekannt"
        
        # Dateipfad aus dem Frame extrahieren
        file_path = caller_frame.f_code.co_filename
        file_name = os.path.basename(file_path)  # Nur der Dateiname ohne Pfad
        return file_name, file_path
    finally:
        del frame  # Speicher freigeben

# === MODUL 2: AUFRUFNUMMER ERMITTELN ===
def get_next_call_number():
    """Schaut in ALLE Log-Dateien und findet die höchste Nummer für fortlaufende Zählung"""
    max_number = 0
    
    # Liste aller möglichen Log-Dateien
    possible_log_files = [
        LOG_FILE,  # Aktuelle Log-Datei
        "sub/program_log.txt",  # Alte Log-Datei im sub Verzeichnis
        os.path.join("sub", "program_log.txt")  # Alternative Pfad-Schreibweise
    ]
    
    # Durchsuche alle Log-Dateien nach der höchsten Nummer
    for log_file in possible_log_files:
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                # Durchsuche alle Datenzeilen
                for line in lines:
                    if line.strip() and not line.startswith('#'):
                        parts = line.split('\t')
                        if len(parts) >= 1:
                            try:
                                number = int(parts[0])
                                max_number = max(max_number, number)
                            except ValueError:
                                continue
            except Exception:
                continue  # Bei Fehlern diese Datei überspringen
    
    return max_number + 1  # Nächste Nummer nach der höchsten gefundenen

# === MODUL 3: HAUPTFUNKTION - LOG EINTRAG ERSTELLEN ===
def log_execution():
    """DIESE FUNKTION WIRD VON ANDEREN PROGRAMMEN AUFGERUFEN"""
    
    # Schritt 1: Aufrufnummer ermitteln (fortlaufend)
    call_number = get_next_call_number()
    
    # Schritt 2: Aktuelles Datum und Zeit holen
    current_time = datetime.datetime.now()
    date_str = current_time.strftime("%Y-%m-%d")  # Format: 2025-10-08
    time_str = current_time.strftime("%H:%M:%S")  # Format: 14:30:25
    
    # Schritt 3: Welches Programm ruft uns auf? (Name und Pfad)
    file_name, file_path = get_caller_info()
    
    # Schritt 4: Log-Zeile zusammenbauen (mit Tabs getrennt)
    new_entry = f"{call_number}\t{date_str}\t{time_str}\t{file_name}\t{file_path}\n"
    
    # Schritt 5: In Datei schreiben
    try:
        # Falls Log-Datei noch nicht existiert, erstelle Header
        if not os.path.exists(LOG_FILE):
            create_log_file_with_header()
        
        # WICHTIG: Neuen Eintrag OBEN einfügen (nicht anhängen)
        insert_entry_at_top(new_entry)
        
        print(f"✓ Log-Eintrag #{call_number} erstellt für: {file_name}")
        
    except Exception as e:
        print(f"✗ Fehler beim Schreiben in Log-Datei: {e}")


# === MODUL 4: LOG-DATEI HEADER ERSTELLEN ===
def create_log_file_with_header():
    """Erstellt eine neue Log-Datei mit schönem Header"""
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write("# NeuroGames Program Execution Log\n")
        f.write("# Aufrufnummer\tDatum\tZeit\tDateiname\tDateipfad\n")
        f.write("#" + "="*80 + "\n")


# === MODUL 5: EINTRAG OBEN EINFÜGEN ===
def insert_entry_at_top(new_entry):
    """Fügt den neuen Eintrag oben in die Log-Datei ein"""
    # Alle existierenden Zeilen lesen
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        existing_lines = f.readlines()
    
    # Header-Zeilen finden (die mit # beginnen)
    header_lines = []
    data_lines = []
    
    for line in existing_lines:
        if line.startswith('#'):
            header_lines.append(line)
        else:
            data_lines.append(line)
    
    # Datei neu schreiben: Header + neuer Eintrag + alte Einträge
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        # Header schreiben
        f.writelines(header_lines)
        # Neuen Eintrag oben einfügen
        f.write(new_entry)
        # Alle alten Einträge darunter
        f.writelines(data_lines)

# === MODUL 6: LOG-DATEI ANZEIGEN ===
def read_log():
    """Zeigt alle Log-Einträge aus allen Log-Dateien schön formatiert an"""
    print("=== 📋 PROGRAMM-AUSFÜHRUNGSLOG ===")
    
    # Alle Log-Einträge sammeln
    all_entries = []
    
    # Liste aller möglichen Log-Dateien
    possible_log_files = [
        LOG_FILE,
        "sub/program_log.txt",
        os.path.join("sub", "program_log.txt")
    ]
    
    # Sammle Einträge aus allen Log-Dateien (ohne Duplikate)
    seen_entries = set()  # Um Duplikate zu vermeiden
    
    for log_file in possible_log_files:
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                for line in lines:
                    if line.strip() and not line.startswith('#'):
                        parts = line.strip().split('\t')
                        if len(parts) >= 4:
                            try:
                                number = int(parts[0])
                                date = parts[1]
                                time = parts[2]
                                filename = parts[3]
                                filepath = parts[4] if len(parts) > 4 else ''
                                
                                # Eindeutiger Schlüssel für Duplikat-Erkennung
                                entry_key = (number, date, time, filename)
                                
                                if entry_key not in seen_entries:
                                    seen_entries.add(entry_key)
                                    all_entries.append({
                                        'number': number,
                                        'date': date,
                                        'time': time,
                                        'filename': filename,
                                        'filepath': filepath
                                    })
                            except ValueError:
                                continue
            except Exception:
                continue
    
    if not all_entries:
        print("❌ Keine Log-Einträge gefunden.")
        return
    
    # Sortiere nach Nummer (höchste zuerst = neueste zuerst)
    all_entries.sort(key=lambda x: x['number'], reverse=True)
    
    # Schön formatiert anzeigen
    print(f"{'Nr':<4} {'Datum':<12} {'Zeit':<10} {'Datei':<15}")
    print("=" * 50)
    
    for entry in all_entries:
        # Kürze den Pfad für bessere Lesbarkeit
        short_path = entry['filename']  # Nur Dateiname anzeigen
        print(f"{entry['number']:<4} {entry['date']:<12} {entry['time']:<10} {short_path:<15}")
        
    print(f"\n📊 Gesamt: {len(all_entries)} Ausführungen")


# === MODUL 7: LOG-STATISTIKEN ANZEIGEN ===
def get_log_stats():
    """Zeigt Statistiken über alle Programmausführungen"""
    # Prüfen ob Log-Datei existiert
    if not os.path.exists(LOG_FILE):
        print("❌ Keine Log-Datei gefunden.")
        return
    
    try:
        # Alle Zeilen der Log-Datei lesen
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Nur Datenzeilen (keine Kommentare mit #)
        data_lines = [line for line in lines if line.strip() and not line.startswith('#')]
        
        if not data_lines:
            print("❌ Keine Log-Einträge gefunden.")
            return
        
        print(f"=== 📊 LOG-STATISTIKEN ===")
        print(f"Anzahl Ausführungen: {len(data_lines)}")
        
        # WICHTIG: Da neuester Eintrag oben steht:
        # data_lines[0] = neueste Ausführung
        # data_lines[-1] = älteste Ausführung
        if data_lines:
            newest_parts = data_lines[0].split('\t')   # Erste Zeile = neueste
            oldest_parts = data_lines[-1].split('\t')  # Letzte Zeile = älteste
            
            if len(newest_parts) >= 3 and len(oldest_parts) >= 3:
                print(f"Neueste Ausführung: {newest_parts[1]} {newest_parts[2].strip()}")
                print(f"Älteste Ausführung: {oldest_parts[1]} {oldest_parts[2].strip()}")
        
        # Zählen welche Programme am häufigsten ausgeführt wurden
        programs = {}
        for line in data_lines:
            parts = line.split('\t')
            if len(parts) >= 4:
                program = parts[3]  # Spalte 4 = Dateiname
                programs[program] = programs.get(program, 0) + 1
        
        # Top 5 Programme anzeigen
        if programs:
            print("\n🏆 Häufigste Programme:")
            for program, count in sorted(programs.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {program}: {count}x")
                
    except Exception as e:
        print(f"❌ Fehler beim Analysieren der Log-Datei: {e}")


# === VERWENDUNG IN ANDEREN PROGRAMMEN ===
# Beispiel:
# from log import log_execution
# log_execution()  # Am Anfang des Programms aufrufen




