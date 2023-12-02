from django.db.models.signals import pre_save 
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Project, CompanyNames, PaymentFirms, ProjectNames, Expenses, JobHistory, Incomes, Supplier, Clients
from django.db import models

@receiver(pre_save, sender=Project)
def update_related_models(sender, instance, **kwargs):
    company_name = instance.CompanyName
    project_name = instance.ProjectName
    project_code = instance.ProjectCode
    # MyCompanyNames kontrolü
    my_company_names = CompanyNames.objects.filter(CompanyName=company_name)
    if not my_company_names.exists():
        CompanyNames.objects.create(CompanyName=company_name)

    # PaymentFirms kontrolü
    payment_firms = PaymentFirms.objects.filter(PaymentFirmsName=company_name)
    if not payment_firms.exists():
        PaymentFirms.objects.create(PaymentFirmsName=company_name)
    
    project_names = ProjectNames.objects.filter(ProjectName=project_name)
    if not project_names.exists():
        ProjectNames.objects.create(ProjectName=project_name,ProjectCode=project_code )


@receiver(pre_save, sender=Expenses)
def update_payment_firms(sender, instance, **kwargs):
    company_name_paying = instance.CompanyName_Paying_Expenses


    if company_name_paying:
        # PaymentFirms kontrolü
        payment_firms = PaymentFirms.objects.filter(PaymentFirmsName=company_name_paying)
        if not payment_firms.exists():
            PaymentFirms.objects.create(PaymentFirmsName=company_name_paying)

@receiver(pre_save, sender=Expenses)
def update_expenses_company_name(sender, instance, **kwargs):
    project_name_copy = instance.ProjectName_Expenses_Copy

    if project_name_copy:
        try:
            project = Project.objects.get(ProjectName=project_name_copy)
            # Expenses modelinin CompanyName alanını Project'in CompanyName ile güncelle
            instance.ProjectName_Expenses = project.ProjectName
        except Project.DoesNotExist:
            # Eğer ilgili Project bulunamazsa, hata mesajı yazdırabilirsiniz.
            print(f"Project with ProjectName {instance.ProjectName_Expenses} not found.")
        

    # Eğer Expenses modelinde ProjectName doluysa
    if instance.ProjectName_Expenses:
        # İlgili Project'i bul
        try:
            project = Project.objects.get(ProjectName=instance.ProjectName_Expenses)
            # Expenses modelinin CompanyName alanını Project'in CompanyName ile güncelle
            instance.CompanyName_Expenses = project.CompanyName
        except Project.DoesNotExist:
            # Eğer ilgili Project bulunamazsa, hata mesajı yazdırabilirsiniz.
            print(f"Project with ProjectName {instance.ProjectName_Expenses} not found.")
    
    if instance.Amount_Expenses is not None and instance.Dollar_Rate_Expenses is not None:
        # Calculate the new value for Amount_TL_Expenses
        amount_tl_expenses = instance.Amount_Expenses / instance.Dollar_Rate_Expenses
        # Update the instance with the new value
        instance.Amount_TL_Expenses = amount_tl_expenses

@receiver(pre_save, sender=JobHistory)
def update_jobhistory_company_name(sender, instance, **kwargs):

    project_name_copy = instance.ProjectName_JobHistory_Copy

    if project_name_copy:
        try:
            project = Project.objects.get(ProjectName=project_name_copy)
            # Expenses modelinin CompanyName alanını Project'in CompanyName ile güncelle
            instance.ProjectName_JobHistory = project.ProjectName
        except Project.DoesNotExist:
            # Eğer ilgili Project bulunamazsa, hata mesajı yazdırabilirsiniz.
            print(f"Project with ProjectName {instance.ProjectName_JobHistory} not found.")
    # Eğer Expenses modelinde ProjectName ve CompanyName doluysa
    if instance.ProjectName_JobHistory:
        # İlgili Project'i bul
        try:
            project = Project.objects.get(ProjectName=instance.ProjectName_JobHistory)
            # Expenses modelinin CompanyName alanını Project'in CompanyName ile güncelle
            instance.CompanyName_JobHistory = project.CompanyName
        except Project.DoesNotExist:
            # Eğer ilgili Project bulunamazsa, hata mesajı yazdırabilirsiniz.
            print(f"Project with ProjectName {instance.ProjectName_JobHistory} not found.")
    
    if instance.Amount_JobHistory is not None and instance.Dollar_Rate_JobHistory is not None:
        # Calculate the new value for Amount_TL_Expenses
        amount_tl_JobHistory = instance.Amount_JobHistory / instance.Dollar_Rate_JobHistory
        # Update the instance with the new value
        instance.Amount_TL_JobHistory = amount_tl_JobHistory

    company_name_job = instance.CompanyName_Job_JobHistory
    if company_name_job:
        # PaymentFirms kontrolü
        payment_firms = PaymentFirms.objects.filter(PaymentFirmsName=company_name_job)
        if not payment_firms.exists():
            PaymentFirms.objects.create(PaymentFirmsName=company_name_job)

@receiver(pre_save, sender=Incomes)
def update_Incomes_Tl(sender, instance, **kwargs):
    project_name_copy = instance.ProjectName_Incomes_Copy

    if project_name_copy:
        try:
            project = Project.objects.get(ProjectName=project_name_copy)
            # Expenses modelinin CompanyName alanını Project'in CompanyName ile güncelle
            instance.ProjectName_Incomes = project.ProjectName
        except Project.DoesNotExist:
            # Eğer ilgili Project bulunamazsa, hata mesajı yazdırabilirsiniz.
            print(f"Project with ProjectName {instance.ProjectName_Incomes} not found.")
    
    if instance.Amount_Incomes is not None and instance.Dollar_Rate_Incomes is not None:
        # Calculate the new value for Amount_TL_Expenses
        amount_usd_Incomes = instance.Amount_Incomes / instance.Dollar_Rate_Incomes
        # Update the instance with the new value
        instance.Amount_Usd_Incomes = amount_usd_Incomes

@receiver(post_save, sender=Clients)
def update_projects_with_client_name(sender, instance, **kwargs):
    
    # Eğer CompanyName_Clients değiştiyse
    if instance.CompanyName_Clients != instance.CompanyName_Clients_New and instance.CompanyName_Clients_New:
        # Yeni CompanyName ile eşleşen Project'leri bul
        matching_projects = Project.objects.filter(CompanyName=instance.CompanyName_Clients)

        # Bulunan Project'leri CompanyName_Clients_New ile güncelle
        for project in matching_projects:
            project.CompanyName = instance.CompanyName_Clients_New
            project.save()

        # CompanyName_Clients_New boşsa CompanyName_Clients ile doldur
        if not instance.CompanyName_Clients_New:
            instance.CompanyName_Clients_New = instance.CompanyName_Clients

        # Son olarak CompanyName_Clients'ı CompanyName_Clients_New ile güncelle
        instance.CompanyName_Clients = instance.CompanyName_Clients_New
        instance.save()

@receiver(post_save, sender=Supplier)
def update_expenses_with_supplier_name(sender, instance, **kwargs):
    
    # Eğer CompanyName_Clients değiştiyse
    if instance.CompanyName_Supplier != instance.CompanyName_Supplier_New and instance.CompanyName_Supplier_New:
        # Yeni CompanyName ile eşleşen Project'leri bul
        matching_expenses = Expenses.objects.filter(CompanyName_Paying_Expenses=instance.CompanyName_Supplier)
        matching_jobhistory = JobHistory.objects.filter(CompanyName_Job_JobHistory=instance.CompanyName_Supplier)


        # Bulunan Project'leri CompanyName_Clients_New ile güncelle
        for expenses in matching_expenses:
            expenses.CompanyName_Paying_Expenses = instance.CompanyName_Supplier_New
            expenses.save()
        # Bulunan Project'leri CompanyName_Clients_New ile güncelle
        for jobhistory in matching_jobhistory:
            jobhistory.CompanyName_Job_JobHistory = instance.CompanyName_Supplier_New
            jobhistory.save()

    
        # Son olarak CompanyName_Clients'ı CompanyName_Clients_New ile güncelle
        instance.CompanyName_Supplier = instance.CompanyName_Supplier_New
        instance.save()
