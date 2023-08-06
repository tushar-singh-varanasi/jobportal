from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            # Joining_Date=Joining_Date,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            # Joining_Date=Joining_Date,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    # Joining_Date= models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["date_of_birth"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    

Categories_CHOICES=(
    ('marketing','marketing'),
    ('Information Tech','Information Tech'),
    ('Construction','Construction'),
    (' Graphic design',' Graphic design'),
)


class Recruiter(models.Model):
    Company_Name=models.CharField(max_length=180)
    Position=models.CharField(max_length=150)
    job_description=models.TextField()
    date=models.DateField(auto_now_add=True)
    Salary=models.IntegerField(null=True,blank=True)
    Categories=models.CharField(choices=Categories_CHOICES,max_length=100,blank=True)
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True)
    
   

class Candidate(models.Model):
    Name=models.CharField(max_length=150)
    DOB=models.DateField()
    mobile=models.CharField(max_length=12)
    Resume=models.FileField(upload_to='resume/',max_length=300,null=True)
    user=models.OneToOneField(MyUser,on_delete=models.CASCADE,null=True)
    Experience=models.IntegerField()
    Location=models.CharField(max_length=180)

class Apply(models.Model):
    message=models.TextField(blank=True)
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True)
    Recruit=models.ForeignKey(Recruiter,on_delete=models.CASCADE)
    jobseeker=models.ForeignKey(Candidate,on_delete=models.CASCADE)

