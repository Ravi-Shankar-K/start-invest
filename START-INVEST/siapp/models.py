from django.db import models

# Create your models here.

class Entrepreneurs(models.Model):
    reg_no = models.CharField(db_column='REG_NO', primary_key=True, max_length=15)  # Field name made lowercase.
    company_name = models.CharField(db_column='COMPANY_NAME', unique=True, max_length=20)  # Field name made lowercase.
    category = models.CharField(db_column='CATEGORY', max_length=15)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=150, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', unique=True, max_length=40)  # Field name made lowercase.
    target_amt = models.IntegerField(db_column='TARGET_AMT')  # Field name made lowercase.
    amt_collected = models.IntegerField(db_column='AMT_COLLECTED', blank=True, null=True)  # Field name made lowercase.
    acc_no = models.BigIntegerField(db_column='ACC_NO', unique=True)  # Field name made lowercase.
    acc_holder_name = models.CharField(db_column='ACC_HOLDER_NAME', max_length=15)  # Field name made lowercase.
    ifsc_code = models.CharField(db_column='IFSC_CODE', max_length=10)  # Field name made lowercase.
    mobile_no = models.BigIntegerField(db_column='MOBILE_NO', unique=True, blank=True, null=True)  # Field name made lowercase.
    e_name = models.CharField(db_column='E_NAME', unique=True, max_length=15)  # Field name made lowercase.
    e_password = models.CharField(db_column='E_PASSWORD', max_length=20)  # Field name made lowercase.
    logo = models.FileField(db_column='LOGO',upload_to='logos/', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.company_name

    class Meta:
        managed = False
        db_table = 'entrepreneurs'


class Investors(models.Model):
    name = models.CharField(db_column='NAME', max_length=15)  # Field name made lowercase.
    user_name = models.CharField(db_column='USER_NAME', primary_key=True, max_length=15)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', unique=True, max_length=40)  # Field name made lowercase.
    password = models.CharField(db_column='PASSWORD', max_length=15)  # Field name made lowercase.
    mobile_no = models.BigIntegerField(db_column='MOBILE_NO', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.user_name

    class Meta:
        managed = False
        db_table = 'investors'


class Registrations(models.Model):
    reg_no = models.CharField(db_column='REG_NO', primary_key=True, max_length=15)  # Field name made lowercase.
    company_name = models.CharField(db_column='COMPANY_NAME', unique=True, max_length=20)  # Field name made lowercase.
    category = models.CharField(db_column='CATEGORY', max_length=15)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=150, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', unique=True, max_length=40)  # Field name made lowercase.
    target_amt = models.IntegerField(db_column='TARGET_AMT')  # Field name made lowercase.
    acc_no = models.BigIntegerField(db_column='ACC_NO', unique=True, blank=True, null=True)  # Field name made lowercase.
    acc_holder_name = models.CharField(db_column='ACC_HOLDER_NAME', max_length=15)  # Field name made lowercase.
    ifsc_code = models.CharField(db_column='IFSC_CODE', max_length=10)  # Field name made lowercase.
    mobile_no = models.BigIntegerField(db_column='MOBILE_NO', unique=True, blank=True, null=True)  # Field name made lowercase.
    user_name = models.CharField(db_column='USER_NAME', unique=True, max_length=15)  # Field name made lowercase.
    password = models.CharField(db_column='PASSWORD', max_length=20)  # Field name made lowercase.
    logo = models.FileField(db_column='LOGO',upload_to='logos/', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.company_name

    class Meta:
        managed = False
        db_table = 'registrations'


class Transactions(models.Model):
    user_name = models.ForeignKey(Investors, models.DO_NOTHING, db_column='USER_NAME')  # Field name made lowercase.
    invested_amt = models.IntegerField(db_column='INVESTED_AMT', blank=True, null=True)  # Field name made lowercase.
    reg_no = models.OneToOneField(Entrepreneurs, models.DO_NOTHING, db_column='REG_NO', primary_key=True)  # Field name made lowercase.

    def __str__(self):
        return str(self.user_name) + "-" + str(self.reg_no)
    
    class Meta:
        managed = False
        db_table = 'transactions'
        unique_together = (('reg_no', 'user_name'),)

