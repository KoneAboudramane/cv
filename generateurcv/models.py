from django.db import models
from django.db import models




class UtilisateurSite(models.Model):
    nom_complet = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    password = models.CharField(max_length=128)
    date_inscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom_complet} ({self.email})"


class Temoignage(models.Model):
    utilisateur = models.ForeignKey(UtilisateurSite, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_post = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Témoignage de {self.utilisateur.nom_complet}"


#logo
class Sitelogo(models.Model):
    logo_texte = models.CharField(max_length=100, blank=True, null=True)
    logo_image = models.ImageField(upload_to='logos/', blank=True, null=True)

    def __str__(self):
        return self.logo_texte or "Logo du site"


# 🔹 Modèle représentant les modèles de CV
class ModeleCV(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image_preview = models.ImageField(upload_to='modele_preview/', blank=True, null=True)
    fichier_template = models.CharField(max_length=255, blank=True, null=True)  # Ex: "cv_templates/modele1.html"

    def __str__(self):
        return self.nom

# 🔹 Modèle principal de CV
class CV(models.Model):
    utilisateur = models.ForeignKey(
        UtilisateurSite,
        on_delete=models.CASCADE,
        related_name='cvs'
    )
    titre = models.CharField(max_length=255)  # Ex: nom du fichier template
    version = models.IntegerField(default=1)

    full_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=255, blank=True)  # ✅ Adresse
    website = models.URLField(blank=True)                   # ✅ Site web
    nationality = models.CharField(max_length=100, blank=True)  # ✅ Nationalité

    summary = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photo/', blank=True, null=True)

    html_url = models.URLField(blank=True, null=True)
    preview_image = models.TextField(blank=True, null=True)

    modele = models.ForeignKey(ModeleCV, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titre} (v{self.version}) - {self.utilisateur.email}"
    utilisateur = models.ForeignKey(
        UtilisateurSite,
        on_delete=models.CASCADE,
        related_name='cvs'
    )
    titre = models.CharField(max_length=255)  # Ex: nom du fichier template
    version = models.IntegerField(default=1)
    full_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    summary = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photo/', blank=True, null=True)  # ✅ ⬅️ change ici
    
    html_url = models.URLField(blank=True, null=True)  # 👉 URL de la page à l'origine de l'enregistrement
    preview_image = models.TextField(blank=True, null=True)  # 👉 image base64 du rendu CV
    

    modele = models.ForeignKey(ModeleCV, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titre} (v{self.version}) - {self.utilisateur.email}"

# 🔹 Expérience
class Experience(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='experiences')
    position = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    date = models.CharField(max_length=100)  # "YYYY-MM" ou "YYYY-MM à YYYY-MM"
    description = models.TextField()

    def __str__(self):
        return f"{self.position} chez {self.company}"

# 🔹 Formation
class Education(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='education')
    degree = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    date = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.degree} à {self.institution}"

# 🔹 Compétence
class Skill(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name} (niveau {self.level})"

# 🔹 Langue
class Language(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='languages')
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.level})"

# 🔹 Loisirs
class Interest(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='interests')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



from django.db import models

class SectionTitre(models.Model):
    titre_header = models.CharField(max_length=255, default="À propos de CV Craft Magic")
    titre_mission = models.CharField(max_length=255, default="Notre Mission")
    titre_histoire = models.CharField(max_length=255, default="Notre Histoire")
    titre_equipe = models.CharField(max_length=255, default="Notre Équipe")
    titre_valeurs = models.CharField(max_length=255, default="Nos Valeurs")

    def __str__(self):
        return "Titres des sections À propos"


class AproposHeader(models.Model):
    description = models.TextField()

    def __str__(self):
        return "Header description"


class Mission(models.Model):
    texte_1 = models.TextField()
    texte_2 = models.TextField(blank=True)

    def __str__(self):
        return "Mission details"


class Histoire(models.Model):
    texte_1 = models.TextField()
    texte_2 = models.TextField(blank=True)

    def __str__(self):
        return "Histoire details"


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)

    def __str__(self):
        return self.name


class Valeur(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.titre


class HeroSection(models.Model):
    titre = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.titre or "Section Hero"

class HeroImage(models.Model):
    hero_section = models.ForeignKey(HeroSection, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photo/')

    def __str__(self):
        return f"Image for {self.hero_section.titre or 'Hero'}"
    

class Choisircv(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title