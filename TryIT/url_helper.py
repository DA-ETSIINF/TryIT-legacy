from django.conf import settings

def create_context(obj = {}):
    if ('urls' in obj):
        print("You cannot have urls key in your context")
        return
    context = obj.copy()
    context["urls"] = {
        "tickets_sale": settings.TICKETS_SALE,
        "activities": settings.ACTIVITIES,
        "workshops": settings.WORKSHOPS,
        "contests": settings.CONTESTS,
        "last_editions": settings.LAST_EDITIONS,
        "volunteers": settings.REGISTER_VOLUNTEERS,
        "register_companies": settings.REGISTER_COMPANIES,
        "contact": settings.CONTACT
    }
    return context
