import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'landing_site.settings')
django.setup()

from pages.models import LegalDocument

def create_privacy_policy():
    slug = 'privacy-policy'
    title = 'Политика конфиденциальности'
    content = """
    <h2>1. Общие положения</h2>
    <p>Настоящая Политика конфиденциальности определяет порядок обработки и защиты информации о физических лицах, пользующихся услугами интернет-сайта Vassta Yacht Cybersecurity.</p>
    
    <h2>2. Сбор данных</h2>
    <p>Мы собираем только те персональные данные, которые вы предоставляете нам добровольно при заполнении форм обратной связи (имя, email, телефон).</p>
    
    <h2>3. Использование данных</h2>
    <p>Полученные данные используются исключительно для связи с вами и предоставления запрашиваемой информации об услугах.</p>
    
    <h2>4. Защита данных</h2>
    <p>Мы принимаем необходимые и достаточные организационные и технические меры для защиты персональной информации пользователя от неправомерного или случайного доступа.</p>
    
    <h2>5. Передача третьим лицам</h2>
    <p>Мы не передаем ваши персональные данные третьим лицам, за исключением случаев, предусмотренных законодательством.</p>
    """
    
    doc, created = LegalDocument.objects.get_or_create(
        slug=slug,
        defaults={
            'title': title,
            'content': content,
            'is_active': True
        }
    )
    
    if created:
        print(f"Created LegalDocument: {title}")
    else:
        print(f"LegalDocument {title} already exists. Updating content...")
        doc.title = title
        doc.content = content
        doc.is_active = True
        doc.save()
        print("Updated content.")

if __name__ == '__main__':
    create_privacy_policy()
