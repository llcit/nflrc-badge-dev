
import os, random, string, hashlib, json

from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from django.conf import settings


def getRandomString(size=12, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def hashEmailAddress(email, salt):
    return 'sha256$' + hashlib.sha256(email + salt).hexdigest()


class Issuer(models.Model):
    # Issuing organization (e.g. CLT, NFLRC, etc.)
    guid = models.CharField(
        max_length=10, unique=True, help_text="This is auto generated.")
    name = models.CharField(max_length=128)
    initials = models.CharField(max_length=32)
    url = models.CharField(max_length=128)
    doc_path = models.CharField(max_length=512)
    desc = models.CharField(max_length=512)
    image = models.CharField(max_length=128)
    contact = models.CharField(max_length=128)
    jsonfile = models.URLField(max_length=1024, blank=True)

    def getJsonFilename(self):
        return 'issuing-org-' + self.guid + '.json'

    def getIssuerUrl(self):
        return os.path.join(self.url, settings.ISSUER_REPO, self.getJsonFilename())

    def getIssuerPath(self):
        return os.path.join(self.doc_path, settings.ISSUER_REPO, self.getJsonFilename())

    def writeIssuerFile(self):
        self.jsonfile = self.getIssuerUrl()
        data = json.dumps(self.serialize())
        f = open(self.getIssuerPath(), 'w')
        localFile = File(f)
        localFile.write(data)
        localFile.closed
        f.closed

    def deleteIssuerFile(self):
        # Remove the file from the filesystem.
        f = open(self.getIssuerPath(), 'w')
        localFile = File(f)
        if os.path.isfile(localFile.name):
            os.remove(localFile.name)

    def serialize(self, request=None):
        """Produce an Open Badge Infrastructure serialization of this Issuer"""
        data = {
            "name": self.name,
            "url": self.url,
            "image": self.image,
            "email": self.contact
        }
        return data

    def __unicode__(self):
        return self.name


class Badge(models.Model):
    guid = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=1024)
    image = models.URLField()
    description = models.CharField(max_length=128)
    criteria = models.URLField()
    issuer = models.ForeignKey(Issuer)
    created = models.DateField(auto_now=True, blank=False)
    jsonfile = models.URLField(max_length=1024, blank=True)

    def getJsonFilename(self):
        return 'badge-ref-' + self.issuer.initials + '-' + self.guid + '.json'

    def getBadgeUrl(self):
        return os.path.join(self.issuer.url, settings.BADGES_REPO, self.getJsonFilename())

    def getBadgePath(self):
        return os.path.join(self.issuer.doc_path, settings.BADGES_REPO, self.getJsonFilename())

    def writeBadgeFile(self):
        self.jsonfile = self.getBadgeUrl()
        data = json.dumps(self.serialize())
        f = open(self.getBadgePath(), 'w')
        localFile = File(f)
        localFile.write(data)
        localFile.closed
        f.closed

    def deleteBadgeFile(self):
        # Remove the file from the filesystem.
        f = open(self.getBadgePath(), 'w')
        localFile = File(f)
        if os.path.isfile(localFile.name):
            os.remove(localFile.name)

    def serialize(self, request=None):
        """Produce an Open Badge Infrastructure serialization of this Badge"""
        data = {
            "name": self.name,
            "description": self.description,
            "image": self.image,
            "criteria": self.criteria,
            "issuer": self.issuer.getIssuerUrl()
        }
        return data

    def __unicode__(self):
        return self.name


class Award(models.Model):

    """
    Stores a record of an awarded badge, related to :model:`badge.Badge`
    
    """
    guid = models.CharField(
        max_length=10, unique=True, help_text="This is auto generated.")
    email = models.CharField(max_length=1024,
                             help_text="Email for the recipient (use the email the user intends to use with their Mozilla Backpack account).")
    firstname = models.CharField(max_length=1024)
    lastname = models.CharField(max_length=1024)
    badge = models.ForeignKey(Badge)
    creator = models.ForeignKey(
        User, related_name="award_creator", blank=True, null=True,
        help_text="Specify yourself.")
    issuedOn = models.DateTimeField(auto_now_add=True, blank=False)
    evidence = models.URLField(max_length=1024,
                               help_text="URL that points a resource that provides evidence for this award.")
    modified = models.DateTimeField(auto_now=True, blank=False)
    claimCode = models.CharField(max_length=10, blank=True,
                                 help_text="This is auto generated. Send this to recipient so they may claim their badge.")
    salt = models.CharField(
        max_length=10, blank=True, help_text="This is auto generated.")
    jsonfile = models.URLField(max_length=1024, blank=True,
                               help_text="This is auto generated but is fully qualified url for the award assertion.")
    expires  = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('email', 'badge')

    def getJsonFilename(self):
        return 'awardee-' + self.guid + '.json'

    def getAssertionUrl(self):
        return os.path.join(self.badge.issuer.url, settings.AWARDS_REPO, self.getJsonFilename())

    def getAssertionPath(self):
        return os.path.join(self.badge.issuer.doc_path, settings.AWARDS_REPO, self.getJsonFilename())

    def writeAssertionFile(self):
        self.jsonfile = self.getAssertionUrl()
        data = json.dumps(self.serialize())
        f = open(self.getAssertionPath(), 'w')
        localFile = File(f)
        localFile.write(data)
        localFile.closed
        f.closed

    def deleteAssertionFile(self):
        # Remove the file from the filesystem.
        f = open(self.getAssertionPath(), 'w')
        localFile = File(f)
        if os.path.isfile(localFile.name):
            os.remove(localFile.name)

    def serialize(self, request=None):
        hashed = hashEmailAddress(self.email, self.salt)
        expiredate = ''
        try:
            expiredate = self.expires.strftime('%Y-%m-%d')
        except:
            expiredate = None

        identityObj = {
            "type": "email",
            "identity": hashed,
            "hashed": True,
            "salt": self.salt,
        }
        verifyObj = {
            "type": "hosted",
            "url": self.getAssertionUrl(),
        }
        assertion = {
            "uid": self.guid,
            "recipient": identityObj,
            "evidence": self.evidence,
            "issuedOn": self.issuedOn.strftime('%Y-%m-%d'),
            "badge": self.badge.getBadgeUrl(),
            "verify": verifyObj,
            "expires": expiredate,
        }
        return assertion

    def __unicode__(self):
        return self.email
