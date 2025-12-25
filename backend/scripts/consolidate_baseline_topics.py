import pandas as pd
import json
from pathlib import Path

# Define the mapping from LLM-generated topics to baseline topics
TOPIC_MAPPING = {
    # 1. Desinformation & Falschmeldungen
    "Desinformation & Falschmeldungen": [
        "Desinformation",
        "Desinformation und Kommunikation",
        "Desinformation gegen Frauen",
        "Manipulierte Videos",
        "KI-generierte Desinformation",
        "Falschmeldungen über Prominente",
        "US-Mexiko-Beziehungen",
    ],
    
    # 2. Wahlen & Wahlkampf
    "Wahlen & Wahlkampf": [
        "Wahlbetrug",
        "Wahlberichterstattung",
        "Bundestagswahl",
        "Wahlumfragen",
        "Europawahl",
        "Wahlsicherheit",
        "Desinformation in Wahlen",
        "KI im Wahlkampf",
        "Wahlmanipulation",
        "Briefwahl",
    ],
    
    # 3. Ukraine-Konflikt
    "Ukraine-Konflikt": [
        "Ukraine-Krieg",
        "Desinformation Ukraine-Krieg",
        "Ukraine-Hilfe",
    ],
    
    # 4. Krisengebiete & Geopolitik
    "Krisengebiete & Geopolitik": [
        "Nahost-Konflikt",
        "Nahostkonflikt",
        "Iran-USA-Konflikt",
        "Gazastreifen",
        "Russland-Afrika",
        "Russland-Sanktionen",
        "Russische Präsidentschaftswahl",
        "Syrien-Konflikt",
        "Syrien",
        "Erdbeben",
    ],
    
    # 5. Künstliche Intelligenz
    "Künstliche Intelligenz": [
        "Künstliche Intelligenz",
        "KI-generierte Videos",
    ],
    
    # 6. Klima & Umwelt
    "Klima & Umwelt": [
        "Klimawandel",
        "Windkraft",
        "Insekten als Nahrungsmittel",
        "Hochwasser",
        "Hochwasserschutz",
        "Unwetter",
    ],
    
    # 7. Migration & Asyl
    "Migration & Asyl": [
        "Geflüchtete",
        "Sozialbetrug",
        "Migration",
        "Asylpolitik",
        "Asyl und Geflüchtete",
        "Flüchtlingsunterbringung",
        "Asylleistungen",
        "Abschiebung",
    ],
    
    # 8. Gesundheit & Wissenschaft
    "Gesundheit & Wissenschaft": [
        "COVID-19-Impfung",
        "Corona-Impfungen",
        "Ernährung",
        "Gesundheit",
        "Wissenschaftskommunikation",
        "5G-Mobilfunk",
        "Gesundheit von Politikern",
    ],
    
    # 9. Extremismus & Sicherheit
    "Extremismus & Sicherheit": [
        "Rechtsextremismus",
        "Verfassungsschutz",
        "Anschlag Magdeburg",
        "Evangelikale Missionierung",
        "Kriminalität in Schwimmbädern",
        "Messerkriminalität",
        "Kriminalität in Schwimmbädern",
    ],
    
    # 10. Politik & Regierung
    "Politik & Regierung": [
        "Ministergehälter",
        "Religiöse Feiertage",
        "Waffenstationierung",
        "Bürgergeld",
        "Rentenpolitik",
        "Versammlungsrecht",
        "Kindergeld",
        "Krankenhausfinanzierung",
        "Fachkräftemangel",
        "Sexualstraftaten",
        "Sparvermögen",
        "Politikeraussagen",
        "Steuern",
        "Tag der Deutschen Einheit",
        "Pressefreiheit",
    ],
    
    # 11. Verschwörungstheorien
    "Verschwörungstheorien": [
        "Verschwörungstheorien",
        "Russische Propaganda",
        "Holocaust",
        "Entwicklungshilfe",
    ],
    
    # 12. Online-Sicherheit & Betrug
    "Online-Sicherheit & Betrug": [
        "Datendiebstahl",
        "Phishing",
        "Kettenbriefe",
        "Datenschutz",
        "Satire",
        "Social Media",
        "Social Media Monitoring",
        "Falschidentifikation in Sozialen Medien",
        "Fußball-WM",
        "Amoklauf",
        "Spionage",
        "Charlie Kirk",
    ],
}

def create_reverse_mapping(topic_mapping):
    """Create a reverse mapping from specific topics to baseline topics."""
    reverse_map = {}
    for baseline_topic, specific_topics in topic_mapping.items():
        for specific_topic in specific_topics:
            reverse_map[specific_topic] = baseline_topic
    return reverse_map

def consolidate_topics(input_csv: str, output_csv: str, mapping_json: str):
    """
    Consolidate LLM-generated topics into baseline topics.
    
    Args:
        input_csv: Path to the input CSV with llm_topic column
        output_csv: Path to save the output CSV with baseline_topic column
        mapping_json: Path to save the topic mapping documentation
    """
    # Read the CSV
    print(f"Reading {input_csv}...")
    df = pd.read_csv(input_csv)
    
    # Create reverse mapping
    reverse_map = create_reverse_mapping(TOPIC_MAPPING)
    
    # Apply mapping
    df['baseline_topic'] = df['llm_topic'].map(reverse_map)
    
    # Check for unmapped topics
    unmapped = df[df['baseline_topic'].isna()]['llm_topic'].unique()
    if len(unmapped) > 0:
        print(f"\n⚠️  Warning: {len(unmapped)} unmapped topics found:")
        for topic in unmapped:
            count = len(df[df['llm_topic'] == topic])
            print(f"  - '{topic}' ({count} articles)")
    
    # Save the consolidated CSV
    print(f"\nSaving consolidated data to {output_csv}...")
    df.to_csv(output_csv, index=False)
    
    # Save the mapping documentation
    print(f"Saving topic mapping to {mapping_json}...")
    with open(mapping_json, 'w', encoding='utf-8') as f:
        json.dump(TOPIC_MAPPING, f, ensure_ascii=False, indent=2)
    
    # Print statistics
    print("\n" + "="*60)
    print("CONSOLIDATION STATISTICS")
    print("="*60)
    
    print(f"\nTotal articles: {len(df)}")
    print(f"Total unique LLM topics: {df['llm_topic'].nunique()}")
    print(f"Total baseline topics: {len(TOPIC_MAPPING)}")
    print(f"Successfully mapped: {df['baseline_topic'].notna().sum()}")
    print(f"Unmapped: {df['baseline_topic'].isna().sum()}")
    
    print("\nBaseline topic distribution:")
    print("-" * 60)
    baseline_counts = df['baseline_topic'].value_counts().sort_values(ascending=False)
    for baseline_topic, count in baseline_counts.items():
        percentage = (count / len(df)) * 100
        print(f"  {baseline_topic:.<45} {count:>3} ({percentage:>5.1f}%)")
    
    print("\n✅ Consolidation complete!")
    print(f"Output files:")
    print(f"  - {output_csv}")
    print(f"  - {mapping_json}")

if __name__ == '__main__':
    input_file = "../llm_generated_topics_sample.csv"
    output_file = "../llm_generated_topics_baseline.csv"
    mapping_file = "../topic_baseline_mapping.json"
    
    consolidate_topics(input_file, output_file, mapping_file)

