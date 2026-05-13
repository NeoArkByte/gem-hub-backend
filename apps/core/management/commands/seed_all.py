import random
import uuid
from django.core.management.base import BaseCommand
from django.apps import apps
from faker import Faker

class Command(BaseCommand):
    help = 'Seeds Gems, Jobs, and Applications using Enums and linked ForeignKeys'

    def handle(self, *args, **options):
        fake = Faker()
        
        # 1. Dynamic Model Loading
        Profile = apps.get_model('core', 'Profile')
        GemListing = apps.get_model('gems', 'GemListing')
        Job = apps.get_model('jobs', 'Job')
        Application = apps.get_model('jobs', 'Application')

        # 2. Get or Create the specific Profile using your provided UUID
        target_auth_uuid = "86c56dfb-eee7-4ec9-87f9-649f747ac70a"
        user_profile, _ = Profile.objects.get_or_create(
            profile_id=target_auth_uuid,
            defaults={
                "id": uuid.uuid4(),
                "username": f"gem_trader_{random.randint(1, 999)}",
                "email": f"tester_{random.randint(1, 99)}@gemhub.com",
                "role": "USER"
            }
        )

        # 3. Seed GEMS
        self.stdout.write("--- Starting Gem Seeding ---")
        for i in range(1, 11):
            try:
                GemListing.objects.create(
                    gem_id=uuid.uuid4(), # Matches your model field
                    owner=user_profile,
                    name=f"{random.choice(['Sapphire', 'Ruby', 'Emerald'])}",
                    carat=round(random.uniform(0.5, 8.0), 2),
                    price=float(random.randint(800, 10000)),
                    description=fake.paragraph(nb_sentences=3),
                    image_url=f"https://picsum.photos/seed/gem{i}/600/400",
                    location=f"{fake.city()}, Sri Lanka",
                    seller_phone=fake.phone_number()[:15],
                    status=random.choice(GemListing.GemStatus.values)
                )
                self.stdout.write(f"Created Gem {i}/10")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to create Gem {i}: {e}"))

        # 4. Seed JOBS & Applications
        self.stdout.write("--- Starting Job & Application Seeding ---")
        for i in range(1, 11):
            try:
                # Create the Job
                new_job = Job.objects.create(
                    job_id=uuid.uuid4(), # Matches your model field
                    employer=user_profile,
                    title=f"Expert {fake.job()}",
                    company_info=fake.company(),
                    salary=float(random.randint(40000, 120000)),
                    tags="Gemology, Certification, Full-time",
                    logo_color=random.randint(0, 16777215),
                    status=random.choice(Job.JobStatus.values)
                )
                self.stdout.write(f"Created Job {i}/10")

                # Create an Application for THIS specific job
                Application.objects.create(
                    application_id=uuid.uuid4(), # Matches your model field
                    job=new_job, 
                    applicant=user_profile,
                    phone=fake.phone_number()[:15],
                    expected_salary=new_job.salary + 5000.0,
                    cv_url=f"https://example.com/cvs/resume_{i}.pdf",
                    status=random.choice(Application.ApplicationStatus.values)
                )
                self.stdout.write(f"   -> Created Application for Job #{i}")

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed at Job/App index {i}: {e}"))

        self.stdout.write(self.style.SUCCESS('Seeding complete with updated Enum values!'))