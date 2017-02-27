from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='logosCompanys', blank=True, null=True)

    url = models.URLField(blank=True)
    url_cv = models.URLField(blank=True)

    contact_person = models.CharField(max_length=200, blank=True)
    contact_email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=12, blank=True)

    def __str__(self):
        return self.name


class Edition(models.Model):
    year = models.CharField(max_length=4, unique=True)

    title = models.CharField(max_length=200, blank=True)
    slogan = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.year


class Speaker(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    company = models.ForeignKey(Company, blank=True, null=True)
    picture = models.ImageField(upload_to='speakers', blank=True, null=True)
    personal_web = models.URLField(blank=True)

    contact_email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=12, blank=True)

    twitter_profile = models.URLField(blank=True)
    facebook_profile = models.URLField(blank=True)
    linkedin_profile = models.URLField(blank=True)
    googleplus_profile = models.URLField(blank=True)
    github_profile = models.URLField(blank=True)
    gitlab_profile = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Track(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    room = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class SessionFormat(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Session(models.Model):
    edition = models.ForeignKey(Edition, related_name='sessions')
    code = models.CharField(max_length=6)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    format = models.ForeignKey(SessionFormat, blank=True, null=True)
    track = models.ManyToManyField(Track, blank=True)
    url = models.URLField(blank=True)  # Registro externo
    video = models.URLField(blank=True)

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    companies = models.ManyToManyField(Company, blank=True)
    speakers = models.ManyToManyField(Speaker, blank=True)

    class Meta:
        unique_together = ('edition', 'code')
        ordering = ['start_date']

    def __str__(self):
        return self.title
