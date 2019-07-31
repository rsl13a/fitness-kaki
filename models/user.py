from models.base_model import BaseModel
from flask import flash
import peewee as pw
from playhouse.hybrid import hybrid_property
import re
from werkzeug.security import generate_password_hash, check_password_hash
from config import S3_LOCATION, DEFAULT_IMAGE

class User(BaseModel):
    first_name = pw.CharField(null=False)
    last_name = pw.CharField(null=False)
    username = pw.CharField(unique=True, index=True)
    password = pw.CharField(null=False)
    email = pw.CharField(unique=True)
    profile_image = pw.CharField(default=DEFAULT_IMAGE)
    private=pw.BooleanField(default=False)

    #this model should return True if user is authenticated. But what sort of authentications do you normally do? 2FA?
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True

    @hybrid_property
    def profile_image_url(self):
        return S3_LOCATION + self.profile_image

    def validate(self):
        if self.username!='' and self.password!='' and self.email!='' and self.first_name!='' and self.last_name!='':
            duplicate_email = User.get_or_none(User.email == self.email)
            duplicate_username = User.get_or_none(User.username == self.username)            
            if duplicate_username: #add duplicate_username!=self.username?
                self.errors.append('Username not unique')
            
            if duplicate_email:
                self.errors.append('Email not unique')
        else:
            self.errors.append('Fields cannot be empty')

#password too short pops up when submitting empty form. Why???