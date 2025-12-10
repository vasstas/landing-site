import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'landing_site.settings')
django.setup()

from pages.models import ProtectionStandard

def populate():
    print("Populating Protection Standards...")

    standards_data = [
        {
            "title_ru": "🛡️ Защита Приватности",
            "title_en": "🛡️ Privacy Protection",
            "description_ru": "Мы строим «Чистые зоны» на борту, используя строжайшие методики, разработанные для защиты конфиденциальной информации высшего уровня и коммерческой тайны.",
            "description_en": "We build \"Clean Zones\" on board using the strictest methodologies designed to protect top-level confidential information and trade secrets.",
            "order": 1
        },
        {
            "title_ru": "⚡ Оперативное Реагирование (IR)",
            "title_en": "⚡ Incident Response (IR)",
            "description_ru": "Выстраиваемая нами система киберзащиты обеспечивает автоматическое выявление, локализацию и нейтрализацию угроз, а также проведение цифровых расследований для быстрого восстановления систем.",
            "description_en": "The cyber defense system we build ensures automatic detection, localization, and neutralization of threats, as well as digital forensics for rapid system recovery.",
            "order": 2
        },
        {
            "title_ru": "✅ Практический Комплаенс",
            "title_en": "✅ Practical Compliance",
            "description_ru": "Мы готовим яхту к сертификации IACS/IMO, концентрируясь на реальной защите и отказоустойчивости систем, а не на бумажной бюрократии.",
            "description_en": "We prepare the yacht for IACS/IMO certification, focusing on real protection and system resilience, not paper bureaucracy.",
            "order": 3
        }
    ]

    # Clear existing to avoid duplicates if run multiple times (optional, but safer for dev)
    # ProtectionStandard.objects.all().delete() 

    for data in standards_data:
        standard, created = ProtectionStandard.objects.get_or_create(
            title_ru=data["title_ru"],
            defaults={
                "title_en": data["title_en"],
                "description_ru": data["description_ru"],
                "description_en": data["description_en"],
                "order": data["order"],
                "is_active": True
            }
        )
        
        if not created:
            # Update if exists
            standard.title_en = data["title_en"]
            standard.description_ru = data["description_ru"]
            standard.description_en = data["description_en"]
            standard.order = data["order"]
            standard.save()
            print(f"Updated standard: {standard.title}")
        else:
            print(f"Created standard: {standard.title}")

    print("Done!")

if __name__ == '__main__':
    populate()
