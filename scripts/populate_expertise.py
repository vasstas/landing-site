import os
import sys
import django
from django.core.files.base import ContentFile
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'landing_site.settings')
django.setup()

from pages.models import ExpertiseCard

def populate():
    data = [
        {
            "order": 1,
            "image_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            "title_ru": "Сетевая Архитектура",
            "short_description_ru": "Глубокая сегментация сетей (VLANs), изоляция OT/IT систем, внедрение промышленных фаерволов и IDS/IPS систем.",
            "full_content_ru": "<p>Мы проектируем сетевую архитектуру с учетом специфики морских судов. Разделение сетей на сегменты (Гостевая, Экипаж, Управление судном, Развлечения) предотвращает горизонтальное перемещение злоумышленников.</p><ul><li>Сегментация VLAN</li><li>Промышленные фаерволы</li><li>IDS/IPS системы</li></ul>",
            
            "title_en": "Network Architecture",
            "short_description_en": "Deep network segmentation (VLANs), isolation of OT/IT systems, implementation of industrial firewalls and IDS/IPS systems.",
            "full_content_en": "<p>We design network architecture tailored to maritime vessels. Network segmentation (Guest, Crew, Vessel Control, Entertainment) prevents lateral movement of attackers.</p><ul><li>VLAN Segmentation</li><li>Industrial Firewalls</li><li>IDS/IPS Systems</li></ul>",

            "title_el": "Αρχιτεκτονική Δικτύου",
            "short_description_el": "Βαθιά τμηματοποίηση δικτύου (VLANs), απομόνωση συστημάτων OT/IT, εφαρμογή βιομηχανικών τειχών προστασίας και συστημάτων IDS/IPS.",
            "full_content_el": "<p>Σχεδιάζουμε αρχιτεκτονική δικτύου προσαρμοσμένη στα θαλάσσια σκάφη. Η τμηματοποίηση δικτύου (Επισκέπτες, Πλήρωμα, Έλεγχος Σκάφους, Ψυχαγωγία) αποτρέπει την πλευρική μετακίνηση των επιτιθέμενων.</p><ul><li>Τμηματοποίηση VLAN</li><li>Βιομηχανικά Τείχη Προστασίας</li><li>Συστήματα IDS/IPS</li></ul>",
        },
        {
            "order": 2,
            "image_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            "title_ru": "Защита Спутниковой Связи",
            "short_description_ru": "Шифрование каналов VSAT/Starlink, защита от перехвата и подмены сигнала, контроль трафика на уровне шлюза.",
            "full_content_ru": "<p>Спутниковые каналы - основная уязвимость яхты. Мы обеспечиваем шифрование всего трафика и защиту от атак Man-in-the-Middle.</p>",

            "title_en": "Satellite Communications Protection",
            "short_description_en": "Encryption of VSAT/Starlink channels, protection against signal interception and spoofing, traffic control at the gateway level.",
            "full_content_en": "<p>Satellite channels are a yacht's main vulnerability. We ensure encryption of all traffic and protection against Man-in-the-Middle attacks.</p>",

            "title_el": "Προστασία Δορυφορικών Επικοινωνιών",
            "short_description_el": "Κρυπτογράφηση καναλιών VSAT/Starlink, προστασία από υποκλοπή και πλαστογράφηση σήματος, έλεγχος κίνησης σε επίπεδο πύλης.",
            "full_content_el": "<p>Τα δορυφορικά κανάλια είναι η κύρια ευπάθεια ενός σκάφους. Διασφαλίζουμε την κρυπτογράφηση όλης της κίνησης και την προστασία από επιθέσεις Man-in-the-Middle.</p>",
        },
        {
            "order": 3,
            "image_url": "https://images.unsplash.com/photo-1569263979104-865ab7cd8d13?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            "title_ru": "Безопасность Навигации",
            "short_description_ru": "Аудит и защита ECDIS, радаров и систем управления судном от GPS-спуфинга и внешнего вмешательства.",
            "full_content_ru": "<p>Защита навигационных систем от GPS-спуфинга и взлома. Аудит ECDIS и радаров.</p>",

            "title_en": "Navigation Safety",
            "short_description_en": "Audit and protection of ECDIS, radars, and vessel control systems from GPS spoofing and external interference.",
            "full_content_en": "<p>Protection of navigation systems from GPS spoofing and hacking. Audit of ECDIS and radars.</p>",

            "title_el": "Ασφάλεια Πλοήγησης",
            "short_description_el": "Έλεγχος και προστασία ECDIS, ραντάρ και συστημάτων ελέγχου σκαφών από πλαστογράφηση GPS και εξωτερικές παρεμβολές.",
            "full_content_el": "<p>Προστασία συστημάτων πλοήγησης από πλαστογράφηση GPS και παραβίαση. Έλεγχος ECDIS και ραντάρ.</p>",
        },
        {
            "order": 4,
            "image_url": "https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            "title_ru": "Контроль Доступа",
            "short_description_ru": "Биометрическая аутентификация, строгие политики доступа (Zero Trust), физическая защита серверных комнат.",
            "full_content_ru": "<p>Внедрение принципов Zero Trust. Биометрия и строгий контроль физического доступа к критическим узлам.</p>",

            "title_en": "Access Control",
            "short_description_en": "Biometric authentication, strict access policies (Zero Trust), physical protection of server rooms.",
            "full_content_en": "<p>Implementation of Zero Trust principles. Biometrics and strict physical access control to critical nodes.</p>",

            "title_el": "Έλεγχος Πρόσβασης",
            "short_description_el": "Βιομετρικός έλεγχος ταυτότητας, αυστηρές πολιτικές πρόσβασης (Zero Trust), φυσική προστασία αιθουσών διακομιστών.",
            "full_content_el": "<p>Εφαρμογή αρχών Zero Trust. Βιομετρικά στοιχεία και αυστηρός έλεγχος φυσικής πρόσβασης σε κρίσιμους κόμβους.</p>",
        },
        {
            "order": 5,
            "image_url": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            "title_ru": "Реагирование на Инциденты",
            "short_description_ru": "Круглосуточный мониторинг (SOC), автоматическое обнаружение аномалий и готовые сценарии реагирования на атаки.",
            "full_content_ru": "<p>Наш SOC работает 24/7. Мы обнаруживаем аномалии в реальном времени и немедленно реагируем.</p>",

            "title_en": "Incident Response",
            "short_description_en": "24/7 monitoring (SOC), automatic anomaly detection, and ready-made attack response scenarios.",
            "full_content_en": "<p>Our SOC operates 24/7. We detect anomalies in real-time and respond immediately.</p>",

            "title_el": "Αντιμετώπιση Περιστατικών",
            "short_description_el": "24/7 παρακολούθηση (SOC), αυτόματη ανίχνευση ανωμαλιών και έτοιμα σενάρια αντιμετώπισης επιθέσεων.",
            "full_content_el": "<p>Το SOC μας λειτουργεί 24/7. Ανιχνεύουμε ανωμαλίες σε πραγματικό χρόνο και αντιδρούμε άμεσα.</p>",
        }
    ]

    # Clear existing cards to avoid duplicates/confusion during development
    ExpertiseCard.objects.all().delete()

    for item in data:
        print(f"Creating {item['title_en']}")
        card = ExpertiseCard(
            order=item['order'],
            
            title_ru=item['title_ru'],
            short_description_ru=item['short_description_ru'],
            full_content_ru=item['full_content_ru'],

            title_en=item['title_en'],
            short_description_en=item['short_description_en'],
            full_content_en=item['full_content_en'],

            title_el=item['title_el'],
            short_description_el=item['short_description_el'],
            full_content_el=item['full_content_el'],
        )
        
        try:
            response = requests.get(item['image_url'])
            if response.status_code == 200:
                card.image.save(f"expertise_{item['order']}.jpg", ContentFile(response.content), save=False)
        except Exception as e:
            print(f"Failed to download image for {item['title_en']}: {e}")
        
        card.save()

if __name__ == '__main__':
    populate()
