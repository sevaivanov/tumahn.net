# Controllers -> Views ("/templates/")

import os
from django.shortcuts import HttpResponse, render_to_response
from kedfilms import utils
from .models import User, Section, Subsection, Skill, Photo

IMG_DIR = "frontend/static/frontend/img/"
KEDFILMS_FOUNDER = User.objects.get(nick = "kedfilms-founder")
HOME_SECTION = Section.objects.get(name = "Home")

def home(request):
	# CS: Computer Science
	computerscience_skills_subcategories = {}
	computerscience_filterargs = {
      "category": "CS",
      "owner": KEDFILMS_FOUNDER
    }
	for skill in Skill.objects.all().filter(**computerscience_filterargs).distinct():
		computerscience_skills_subcategories[str(skill.subcategory)] = skill.get_subcategory_display()

	return render_to_response(
        "frontend/home.html",{
		    "title" : HOME_SECTION.title,
		    "subtitle" : HOME_SECTION.subtitle,
            "rd_section": Subsection.objects.all().filter(
                section = HOME_SECTION,
                name = "r&d"
            )[0],
            "articles_section": Subsection.objects.all().filter(
                section = HOME_SECTION,
                name = "articles"
            )[0],
            "videos_section": Subsection.objects.all().filter(
                section = HOME_SECTION,
                name = "videos"
            )[0],
            "photos_section": Subsection.objects.all().filter(
                section = HOME_SECTION,
                name = "photos"
            )[0],
            "skills_section": "ABILITIES",
            "computerscience_skills_subcategories": computerscience_skills_subcategories,
		    "computerscience_skills": Skill.objects.all().filter(**computerscience_filterargs)
	    }
    )

def articles(request):
    return render_to_response(
        "frontend/articles.html",{
            "title": "Articles",
            "subtitle": "Subtitle"
        }
    )

# categories: ((GN,General), (PF,Portfolio))
def photos(request):
    if os.path.exists(IMG_DIR):
        return render_to_response(
            "frontend/photos.html",{
                "title": "Photos",
                "subtitle": "Take a closer look...",
                "portfolio_title": "Porfolio",
                "portfolio_images": Photo.objects.all().filter(category = "PF"),
                "general_title": "General",
                "general_images": Photo.objects.all().filter(category = "GN")
        }
    )
