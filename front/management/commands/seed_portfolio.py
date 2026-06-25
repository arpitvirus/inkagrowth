from django.core.management.base import BaseCommand

from front.models import PortfolioProject


DEMO_PROJECTS = [
    {
        "business_name": "Satrang Makeover",
        "business_category": "Women Salon & Bridal Makeup Studio",
        "location": "Shakti Nagar, Chandausi",
        "service_type": PortfolioProject.SERVICE_GOOGLE_MAPS_SEO,
        "services_provided": "Google Maps SEO, Social Media Management, Meta Ads Strategy, Website Recommendation",
        "focus_keyword": "Best salon in Chandausi, Bridal makeup artist in Chandausi, Women salon in Chandausi, Makeup artist in Shakti Nagar Chandausi",
        "short_description": "A local visibility project for a bridal makeup and salon brand serving customers in Shakti Nagar and nearby Chandausi areas.",
        "client_overview": "Satrang Makeover is a women salon and bridal makeup studio focused on local discovery, trust, and enquiry growth.",
        "problem": "The business needed stronger visibility for high-intent salon and bridal makeup searches in Chandausi.",
        "strategy": "Inkagrowth planned Google Business Profile improvements, keyword targeting, content direction, social media consistency, and Meta Ads awareness.",
        "work_done": "Business audit, local keyword planning, profile optimization guidance, content topics, competitor checks, and campaign planning.",
        "keywords_targeted": "Best salon in Chandausi, Bridal makeup artist in Chandausi, Women salon in Chandausi, Makeup artist in Shakti Nagar Chandausi",
        "result_summary": "The project focuses on improving local visibility, bridal makeup enquiries, and trust across search and social channels.",
        "before_inkagrowth": "Limited local keyword targeting, inconsistent content direction, and weak discovery for bridal makeup searches.",
        "after_inkagrowth": "Clear local SEO plan, stronger service positioning, improved content themes, and a better enquiry path.",
        "keywords_targeted_count": 4,
        "search_visibility": "Improving",
        "leads_generated": 18,
        "campaigns_run": 2,
        "testimonial_text": "Inkagrowth helped us understand how local search and social media can bring more relevant enquiries.",
        "testimonial_person_name": "Demo Client",
        "testimonial_person_designation": "Owner",
    },
    {
        "business_name": "LensCraft Optical",
        "business_category": "Optical Store",
        "location": "Chandausi",
        "service_type": PortfolioProject.SERVICE_LOCAL_SEO,
        "services_provided": "Google Maps SEO, Social Media Management, Local SEO",
        "focus_keyword": "Best opticals in Chandausi, Optical shop in Chandausi, Eye care center in Chandausi",
        "short_description": "A local SEO and social visibility project for an optical store serving eyewear and eye-care customers.",
        "client_overview": "LensCraft Optical is a demo optical store case study built around local search trust and store visit enquiries.",
        "problem": "The store needed clearer local discovery for optical, eyewear, and eye-care related searches.",
        "strategy": "Inkagrowth focused on Google Maps signals, service keywords, review trust, and social content that highlights product categories.",
        "work_done": "Local SEO audit, Google Maps content plan, category keyword mapping, social media calendar, and enquiry CTA improvements.",
        "keywords_targeted": "Best opticals in Chandausi, Optical shop in Chandausi, Eye care center in Chandausi",
        "result_summary": "The goal is stronger local discovery and more store-visit intent from search and social media.",
        "before_inkagrowth": "Low category visibility and limited service-specific local content.",
        "after_inkagrowth": "Sharper local keyword targeting, stronger business profile content, and clearer trust signals.",
        "keywords_targeted_count": 3,
        "search_visibility": "Growing",
        "profile_views": 420,
        "direction_requests": 31,
        "calls_received": 26,
    },
    {
        "business_name": "CarePlus Clinic",
        "business_category": "Multi-speciality Clinic",
        "location": "Chandausi",
        "service_type": PortfolioProject.SERVICE_WEBSITE,
        "services_provided": "Website Development, Local SEO, Google Maps Optimization, Social Media Strategy",
        "focus_keyword": "Best clinic in Chandausi, Doctor in Chandausi, Healthcare services in Chandausi",
        "short_description": "A healthcare website and local SEO project focused on trust, services, and patient enquiry clarity.",
        "client_overview": "CarePlus Clinic is a demo multi-speciality clinic case study for healthcare website positioning and local discovery.",
        "problem": "The clinic needed a clearer digital presence that explained services and supported patient enquiries.",
        "strategy": "Inkagrowth planned a service-led website structure, local SEO basics, Google Maps optimization, and trust-focused social content.",
        "work_done": "Website structure planning, service page messaging, local keyword mapping, contact CTA planning, and Google Maps recommendations.",
        "keywords_targeted": "Best clinic in Chandausi, Doctor in Chandausi, Healthcare services in Chandausi",
        "result_summary": "The project supports better patient trust, clearer healthcare information, and stronger local search discovery.",
        "before_inkagrowth": "Unclear service presentation and limited local search structure.",
        "after_inkagrowth": "Clearer website flow, stronger service pages, and a better path from discovery to contact.",
        "keywords_targeted_count": 3,
        "search_visibility": "Improving",
        "calls_received": 34,
        "leads_generated": 22,
    },
    {
        "business_name": "Power Fit Gym",
        "business_category": "Fitness & Gym Center",
        "location": "Chandausi",
        "service_type": PortfolioProject.SERVICE_META_ADS,
        "services_provided": "Meta Ads, Lead Generation, Branding, Social Media Management",
        "focus_keyword": "Best gym in Chandausi, Fitness center in Chandausi, Gym membership in Chandausi",
        "short_description": "A Meta Ads and lead generation project for a fitness center promoting memberships and brand awareness.",
        "client_overview": "Power Fit Gym is a demo fitness center case study for social media, branding, and paid lead generation.",
        "problem": "The gym needed more membership enquiries and stronger awareness among local fitness audiences.",
        "strategy": "Inkagrowth planned offer-led Meta Ads, social media creative themes, lead capture messaging, and brand trust content.",
        "work_done": "Audience planning, offer messaging, campaign structure, creative direction, social content topics, and lead flow recommendations.",
        "keywords_targeted": "Best gym in Chandausi, Fitness center in Chandausi, Gym membership in Chandausi",
        "result_summary": "The project focuses on generating membership interest, improving social presence, and strengthening the gym brand.",
        "before_inkagrowth": "Scattered social posts, limited campaign structure, and unclear membership lead flow.",
        "after_inkagrowth": "Focused campaigns, better offer messaging, stronger brand content, and clearer lead generation.",
        "keywords_targeted_count": 3,
        "search_visibility": "Awareness-focused",
        "leads_generated": 45,
        "campaigns_run": 3,
    },
]


class Command(BaseCommand):
    help = "Seed four safe demo portfolio projects without creating duplicates."

    def handle(self, *args, **options):
        created_count = 0
        skipped_count = 0

        for project_data in DEMO_PROJECTS:
            project, created = PortfolioProject.objects.get_or_create(
                business_name=project_data["business_name"],
                defaults={
                    **project_data,
                    "status": PortfolioProject.STATUS_COMPLETED,
                    "is_featured": created_count < 3,
                    "display_order": created_count + skipped_count + 1,
                },
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created demo project: {project.business_name}"))
            else:
                skipped_count += 1
                self.stdout.write(f"Skipped existing project: {project.business_name}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Portfolio seed complete. Created {created_count}, skipped {skipped_count}."
            )
        )
