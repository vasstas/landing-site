import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'landing_site.settings')
django.setup()

from pages.models import Service

def populate_services():
    services_data = [
        {
            "title": "🔒 VIP Privacy Shield",
            "description": "Защита смартфонов и ноутбуков владельца, создание безопасных каналов для конфиденциальных переговоров, защита от цифровой слежки.",
            "order": 1
        },
        {
            "title": "📡 Навигация и OT-Security",
            "description": "Изоляция критических систем (ECDIS, Engine Control), защита от спуфинга GPS и контроль удаленного доступа к машинному отделению.",
            "order": 2
        },
        {
            "title": "👁️ 24/7 Мониторинг и Реагирование",
            "description": "Постоянная кибер-охрана, немедленная нейтрализация угроз, расследования инцидентов (Digital Forensics).",
            "order": 3
        },
        {
            "title": "📜 Pre-Compliance & Crew Training",
            "description": "Подготовка к инспекциям IACS/IMO, обучение экипажа процедурам кибербезопасности и противодействию фишингу.",
            "order": 4
        }
    ]

    print("Populating Services...")
    
    # Clear existing services to avoid duplicates if run multiple times
    Service.objects.all().delete()

    for item in services_data:
        service = Service(
            title=item["title"],
            description=item["description"],
            order=item["order"],
            is_active=True
        )
        # Since RU is default, these will be saved to title_ru and description_ru as well if using modeltranslation
        # But to be safe and explicit with modeltranslation:
        service.title_ru = item["title"]
        service.description_ru = item["description"]
        
        # For EN and EL, we might want to add translations later, but for now we'll just leave them empty 
        # or copy the RU text if we want fallbacks. 
        # Let's copy to EN and EL to avoid empty spots, user can edit them later.
        service.title_en = item["title"]
        service.description_en = item["description"]
        
        service.title_el = item["title"]
        service.description_el = item["description"]

        service.save()
        print(f"Created service: {service.title}")

    print("Done!")

if __name__ == '__main__':
    populate_services()
