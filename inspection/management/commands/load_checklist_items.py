from django.core.management.base import BaseCommand
from inspection.models import ChecklistItems


class Command(BaseCommand):
    help = 'Load initial checklist items for equipment inspection'

    def handle(self, *args, **options):
        # Sample checklist items in both English and Arabic
        checklist_items = [
            "مستوى زيت المحرك (Engine oil level)",
            "مستوى سائل التبريد (Coolant level)",
            "مستوى زيت الفرامل (Brake fluid level)",
            "ضغط الإطارات (Tire pressure)",
            "حالة الإطارات والعجلات (Tire and wheel condition)",
            "الأضواء والإشارات (Lights and signals)",
            "المرايا (Mirrors)",
            "حزام الأمان (Safety belt)",
            "أدوات السلامة (Safety equipment)",
            "نظافة الزجاج الأمامي والخلفي (Windshield cleanliness)",
            "مستوى الوقود (Fuel level)",
            "حالة البطارية (Battery condition)",
            "نظام التكييف (Air conditioning system)",
            "حالة المقود (Steering condition)",
            "نظام الفرامل (Brake system)",
            "الأصوات غير الطبيعية (Unusual sounds)",
            "التسربات (Leakages)"
        ]

        for i, item_desc in enumerate(checklist_items, 1):
            checklist_item, created = ChecklistItems.objects.get_or_create(
                item_description=item_desc,
                defaults={'sort_order': i}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created checklist item: "{item_desc}"')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Checklist item already exists: "{item_desc}"')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Finished loading checklist items. Total items: {ChecklistItems.objects.count()}')
        )