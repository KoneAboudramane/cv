from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import InscriptionForm, CVForm
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CV, Choisircv, Experience, Education, HeroSection, Skill, Language, Interest, TeamMember, Temoignage
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .forms import InscriptionForm
from .models import UtilisateurSite
from .models import AproposHeader, Mission, Histoire, Valeur, TeamMember
from django.views.decorators.csrf import csrf_exempt
from django.templatetags.static import static
from .models import SectionTitre  # si ce n'est pas déjà importé
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CV, Experience, Education, Skill, Language, Interest
from django.http import JsonResponse
from .models import UtilisateurSite, CV, Experience, Education, Skill, Language, Interest



from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from weasyprint import HTML

@csrf_exempt
def generate_pdf(request):
    if request.method == 'POST':
        html = request.POST.get('html', '')
        pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf()

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="cv.pdf"'
        return response
    return HttpResponse("Méthode non autorisée", status=405)



# Create your views here.

def home(request):
    hero = HeroSection.objects.prefetch_related('images').first()
    features = Choisircv.objects.all()
    temoignages = Temoignage.objects.select_related('utilisateur').order_by('-date_post')

    if request.method == 'POST':
        contenu = request.POST.get('contenu', '').strip()
        utilisateur_id = request.session.get('utilisateur_id')  # On récupère l'utilisateur de la session

        if contenu and utilisateur_id:
            try:
                utilisateur = UtilisateurSite.objects.get(id=utilisateur_id)
                Temoignage.objects.create(utilisateur=utilisateur, contenu=contenu)
                return redirect('index')  # Redirection après le POST
            except UtilisateurSite.DoesNotExist:
                # Utilisateur non trouvé
                pass

    context = {
        'hero': hero,
        'features': features,
        'temoignages': temoignages,
    }
    return render(request, 'generateurcv/index.html', context)

# Inscription utilisateur site
def register_view(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Inscription réussie. Vous pouvez maintenant vous connecter.")
            return redirect('login')
    else:
        form = InscriptionForm()
    return render(request, 'generateurcv/register.html', {'form': form})

# Connexion utilisateur site
def auth_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = UtilisateurSite.objects.get(email=email)
            if check_password(password, user.password):
                request.session['utilisateur_id'] = user.id
                return redirect('index')
            else:
                messages.error(request, "Mot de passe incorrect.")
        except UtilisateurSite.DoesNotExist:
            messages.error(request, "Email non reconnu.")
    return render(request, 'generateurcv/login.html')

#déconnexion
@require_POST
@csrf_protect
def logout_view(request):
    request.session.flush()
    return redirect('index')  # Redirige vers la page de connexion après déconnexion

#profil
def dashboard_view(request):
    utilisateur_id = request.session.get('utilisateur_id')
    if not utilisateur_id:
        return redirect('login')  # Pas connecté

    utilisateur = UtilisateurSite.objects.get(id=utilisateur_id)
    return render(request, 'generateurcv/dashboard.html', {
        'UtilisateurSite': utilisateur
    })

    

@csrf_exempt
def update_profile(request):
    utilisateur_id = request.session.get('utilisateur_id')
    if not utilisateur_id:
        return JsonResponse({'error': 'Utilisateur non connecté'}, status=401)

    if request.method == 'POST':
        utilisateur = UtilisateurSite.objects.get(id=utilisateur_id)

        nom = request.POST.get('name')
        supprimer_photo = request.POST.get('remove_photo')

        if nom:
            utilisateur.nom_complet = nom

        if supprimer_photo == 'true':
            if utilisateur.photo:
                utilisateur.photo.delete(save=False)
            utilisateur.photo = None

        if request.FILES.get('image'):
            utilisateur.photo = request.FILES['image']

        utilisateur.save()

        return JsonResponse({
            'message': 'Profil mis à jour',
            'photoUrl': utilisateur.photo.url if utilisateur.photo else static('generateurcv/images/default-user.png')
        })

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
 
  

def edit_profile_view(request):
    return render(request, 'generateurcv/edit_profile.html')


def templates_view(request):
    return render(request, 'generateurcv/templates.html')

def modelecv_view(request):
    return render(request, 'generateurcv/cv/modelecv.html')

def partials_nav_view(request):
    return render(request, 'generateurcv/partials.nav')



def about_view(request):
    titres = SectionTitre.objects.first()
    header = AproposHeader.objects.first()
    mission = Mission.objects.first()
    histoire = Histoire.objects.first()
    valeurs = Valeur.objects.all()
    team = TeamMember.objects.all()

    context = {
        'titres': titres,
        'header': header,
        'mission': mission,
        'histoire': histoire,
        'valeurs': valeurs,
        'team': team,
    }

    return render(request, 'generateurcv/about.html', context)


def pricing_view(request):
    pricing_plans = [
        {
            "name": "Gratuit",
            "price": "0€",
            "description": "Idéal pour commencer avec des fonctionnalités de base",
            "features": [
                "3 modèles de CV",
                "2 modèles de lettres de motivation",
                "Exportation PDF",
                "1 CV et 1 lettre de motivation sauvegardés"
            ],
            "cta": "Commencer gratuitement",
            "popular": False
        },
        {
            "name": "Standard",
            "price": "9,99€",
            "description": "Pour les chercheurs d'emploi actifs",
            "features": [
                "Tous les modèles de CV",
                "Tous les modèles de lettres de motivation",
                "Exportation PDF et Word",
                "Jusqu'à 10 CV et lettres sauvegardés",
                "Conseils personnalisés"
            ],
            "cta": "Obtenir le plan Standard",
            "popular": True
        },
        {
            "name": "Pro",
            "price": "19,99€",
            "description": "Pour les professionnels et freelances",
            "features": [
                "Tous les modèles premium",
                "Exportation dans tous les formats",
                "CV et lettres illimités",
                "Suppression du filigrane",
                "Conseils personnalisés avancés",
                "Support prioritaire"
            ],
            "cta": "Obtenir le plan Pro",
            "popular": False
        }
    ]
    return render(request, 'generateurcv/pricing.html', { 'pricing_plans': pricing_plans })


# Optionnel : liste des CV disponibles (ou scanner les fichiers)
AVAILABLE_CVS = {f'cv{i}': f'generateurcv/cv/cv{i}.html' for i in range(1, 17)}

def cv_view(request, cv_name):
    template = AVAILABLE_CVS.get(cv_name)
    if not template:
        raise Http404("CV non trouvé")
    return render(request, template)




def save_cv(request):
    if request.method == 'POST':
        try:
            utilisateur_id = request.session.get('utilisateur_id')
            if not utilisateur_id:
                return JsonResponse({'success': False, 'message': 'Utilisateur non connecté.'})

            utilisateur = UtilisateurSite.objects.get(id=utilisateur_id)
            cv_data_raw = request.POST.get('cv_data')
            cv_data = json.loads(cv_data_raw)

            photo_file = request.FILES.get('photo')
            preview_image = request.POST.get('preview_image')
            page_url = request.POST.get('page_url')  # 👉 récupération de l’URL de la page d’origine

            cv = CV.objects.create(
                utilisateur=utilisateur,
                titre="CV Sans Titre",
                full_name=cv_data['personalInfo']['fullName'],
                title=cv_data['personalInfo']['title'],
                email=cv_data['personalInfo']['email'],
                phone=cv_data['personalInfo']['phone'],
                address=cv_data['personalInfo'].get('address', ''),         # ✅
                website=cv_data['personalInfo'].get('website', ''),         # ✅
                nationality=cv_data['personalInfo'].get('nationality', ''), # ✅
                summary=cv_data['personalInfo']['summary'],
                photo=photo_file if photo_file else None,
                preview_image=preview_image,
                html_url=page_url,
            )


            for exp_data in cv_data.get('experience', []):
                start = exp_data.get('startDate', '').strip()
                end = exp_data.get('endDate', '').strip()
                is_current = exp_data.get('isCurrent', False)
                date_str = f"Depuis {start}" if is_current else f"{start} - {end}" if end else start

                Experience.objects.create(
                    cv=cv,
                    position=exp_data['position'],
                    company=exp_data['company'],
                    date=date_str,
                    description=exp_data['description']
                )

            for edu_data in cv_data.get('education', []):
                start = edu_data.get('startDate', '').strip()
                end = edu_data.get('endDate', '').strip()
                is_current = edu_data.get('isCurrent', False)
                date_str = f"Depuis {start}" if is_current else f"{start} - {end}" if end else start

                Education.objects.create(
                    cv=cv,
                    degree=edu_data['degree'],
                    institution=edu_data['institution'],
                    date=date_str,
                    description=edu_data['description']
                )

            for skill_data in cv_data.get('skills', []):
                Skill.objects.create(
                    cv=cv,
                    name=skill_data['name'],
                    level=skill_data['level']
                )

            for lang_data in cv_data.get('languages', []):
                Language.objects.create(
                    cv=cv,
                    name=lang_data['name'],
                    level=lang_data['level']
                )

            for interest_data in cv_data.get('interests', []):
                Interest.objects.create(
                    cv=cv,
                    name=interest_data['name']
                )

            return JsonResponse({'success': True, 'cv_id': cv.id})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'})


from django.http import JsonResponse
from .models import CV

def historique_cvs(request):
    utilisateur_id = request.session.get('utilisateur_id')
    if not utilisateur_id:
        return JsonResponse({'success': False, 'message': 'Non connecté'}, status=403)

    cvs = CV.objects.filter(utilisateur_id=utilisateur_id).order_by('-created_at')

    data = [
        {
            'id': cv.id,
            'titre': cv.titre,
            'preview_image': cv.preview_image,
            'date': cv.created_at.strftime('%d/%m/%Y'),
            'html_url': cv.html_url,  # 🧠 CHAMP EXACT
        }
        for cv in cvs
    ]

    return JsonResponse({'success': True, 'cvs': data})

# views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import CV

def get_cv_data(request, cv_id):
    cv = get_object_or_404(CV.objects.prefetch_related(
        'experiences', 'education', 'skills', 'languages', 'interests'
    ), id=cv_id)

    return JsonResponse({
        "success": True,
        "cv": {
            "full_name": cv.full_name,
            "title": cv.title,
            "email": cv.email,
            "phone": cv.phone,
            "summary": cv.summary,
            "address": cv.address,         # ✅
            "website": cv.website,         # ✅
            "nationality": cv.nationality, # ✅
            "photo": cv.photo.url if cv.photo else '',
            "experiences": [
                {
                    "position": e.position,
                    "company": e.company,
                    "date": e.date,
                    "description": e.description
                } for e in cv.experiences.all()
            ],
            "education": [
                {
                    "degree": e.degree,
                    "institution": e.institution,
                    "date": e.date,
                    "description": e.description
                } for e in cv.education.all()
            ],
            "skills": [
                {"name": s.name, "level": s.level}
                for s in cv.skills.all()
            ],
            "languages": [
                {"name": l.name, "level": l.level}
                for l in cv.languages.all()
            ],
            "interests": [
                {"name": i.name}
                for i in cv.interests.all()
            ]
        }
    })


import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import CV, Experience, Education, Skill, Language, Interest
from django.core.files.base import ContentFile
import base64

def update_related_objects(cv, model, related_data, related_name, fields):
    # Supprimer les anciens
    getattr(cv, related_name).all().delete()
    
    # Créer les nouveaux
    for item in related_data:
        obj_data = {f: item.get(f, '') for f in fields}
        model.objects.create(cv=cv, **obj_data)


@csrf_exempt
@require_http_methods(["POST"])
def update_cv(request, pk):
    if request.POST.get('_method') != 'PUT':
        return JsonResponse({'success': False, 'message': 'Méthode non autorisée'}, status=405)

    try:
        cv = CV.objects.get(pk=pk)
    except CV.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'CV introuvable'}, status=404)

    try:
        cv_data = json.loads(request.POST.get('cv_data', '{}'))
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'JSON invalide'}, status=400)

    personal = cv_data.get('personalInfo', {})

    cv.full_name = personal.get('fullName', '')
    cv.title = personal.get('title', '')
    cv.email = personal.get('email', '')
    cv.phone = personal.get('phone', '')
    cv.summary = personal.get('summary', '')

    cv.address = personal.get('address', '')           # ✅
    cv.website = personal.get('website', '')           # ✅
    cv.nationality = personal.get('nationality', '')   # ✅

    cv.html_url = request.POST.get('page_url', '')

    if 'photo' in request.FILES:
        cv.photo = request.FILES['photo']

    preview_b64 = request.POST.get('preview_image')
    if preview_b64 and preview_b64.startswith('data:image'):
        _, b64data = preview_b64.split(';base64,')
        cv.preview_image = b64data

    cv.save()

    update_related_objects(cv, Experience, cv_data.get('experience', []), 'experiences',
                           ['position', 'company', 'date', 'description'])
    update_related_objects(cv, Education, cv_data.get('education', []), 'education',
                           ['degree', 'institution', 'date', 'description'])
    update_related_objects(cv, Skill, cv_data.get('skills', []), 'skills',
                           ['name', 'level'])
    update_related_objects(cv, Language, cv_data.get('languages', []), 'languages',
                           ['name', 'level'])
    update_related_objects(cv, Interest, cv_data.get('interests', []), 'interests',
                           ['name'])

    return JsonResponse({'success': True, 'message': 'Mise à jour réussie'})



# Vue pour afficher tous les CV d'un utilisateur
def liste_cvs(request):
    user_cvs = CV.objects.filter(UtilisateurSite=request.user)
    return render(request, 'generateurcv/cv/liste_cvs.html', {'user_cvs': user_cvs})

# Vue pour voir, modifier ou dupliquer un CV
def gestion_cv(request, cv_id=None):
    if cv_id:
        cv = get_object_or_404(CV, id=cv_id, UtilisateurSite=request.user)
    else:
        cv = None

    if request.method == 'POST':
        form = CVForm(request.POST, instance=cv)
        if form.is_valid():
            # Si c'est une nouvelle version ou une modification d'un CV existant
            cv = form.save(commit=False)
            cv.version += 1  # Incrémente la version
            cv.save()
            return redirect('cv:liste_cvs')
    else:
        form = CVForm(instance=cv)

    return render(request, 'generateurcv/cv/gestion_cv.html', {'form': form, 'cv': cv})

# Vue pour dupliquer un CV
def dupliquer_cv(request, cv_id):
    cv = get_object_or_404(CV, id=cv_id, UtilisateurSite=request.user)
    cv.pk = None  # Crée un nouveau CV avec les mêmes informations
    cv.version = 1  # La version commence à 1 pour la duplication
    cv.titre = f"{cv.titre} (Copie)"
    cv.save()
    return redirect('cv:liste_cvs')




#lettre
def lettre1_View(request):
    return render(request, 'generateurcv/lettres/lettre1.html')

def lettre2_View(request):
    return render(request, 'generateurcv/lettres/lettre2.html')

def lettre3_View(request):
    return render(request, 'generateurcv/lettres/lettre3.html')

def lettre4_View(request):
    return render(request, 'generateurcv/lettres/lettre4.html')

def lettre5_View(request):
    return render(request, 'generateurcv/lettres/lettre5.html')

def lettre6_View(request):
    return render(request, 'generateurcv/lettres/lettre6.html')

def lettre7_View(request):
    return render(request, 'generateurcv/lettres/lettre7.html')

def lettre8_View(request):
    return render(request, 'generateurcv/lettres/lettre8.html')