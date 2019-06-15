from django.db import models as m

class Executor(m.Model):
    executor_UID = m.BigIntegerField()
    executor_name = m.CharField(max_length = 256)
    is_actual = m.BooleanField()
    # рейтинги пересчитваются по команде, чтобы не перегружать сервер
    rating = m.FloatField() # итоговый рейтинг по тяжести последствий (больше - хуже)
    rating = m.FloatField() # итоговый рейтинг по медлительности реагирования (больше - лучше)
class Status(m.Model): # выполнено, не выполнено, выполняется
    SUID = m.BigIntegerField()
    status_name = m.CharField(max_length = 100)
class TerritoryType(m.Model): # двор и т.д.
    territory_type_UID = m.BigIntegerField()
    territory_name = m.CharField(max_length = 100)
class Client(m.Model): # заказчик
    client_UID = m.BigIntegerField()
    client_name = m.CharField(max_length = 256)
class JobType(m.Model):
    job_type_UID = m.BigIntegerField()
    job_type_name = m.CharField(max_length = 100)
class Contract(m.Model): # контракт
    contract_UID = m.BigIntegerField()
    executor_UID = m.ForeignKey(Executor, on_delete = m.CASCADE) # исполнитель
    client_UID = m.ForeignKey(Client, on_delete = m.CASCADE) # заказчик
    address = m.CharField(max_length = 256) # адрес объекта
    job_type_UID = m.ForeignKey(JobType, on_delete = m.CASCADE) # тип работ
    year = m.IntegerField()
    status = m.ForeignKey(Status, on_delete = m.CASCADE)
    money = m.FloatField() # сумма контракта

    contract_ID = m.CharField(max_length = 10) # в текстовом виде, из-за неровных входных данных "15 от 12.03" и т.п.
    real_start_date = m.DateTimeField()
    real_end_date = m.DateTimeField()
    fixed_too_late = m.BigIntegerField()
    claims_during_fixes = m.BigIntegerField()
    final_claims_after_fix = m.BigIntegerField()
class Claim(m.Model): # жалобы по контракту
    claim_UID = m.BigIntegerField()
    contract_UID = m.ForeignKey(Contract, on_delete = m.CASCADE)
    comment = m.CharField(max_length = 256)  # замечание в читаемом виде
    comment_date = m.DateTimeField()
    fix_date = m.DateTimeField()
'''
class DataManager(m.Manager):
    @classmethod
    def add_contract(self, address, territory_type, client, job_type, ):
        if Note.objects.filter(title=title).exists():
            Note.objects.get(title=title).delete()
            note = Note(title=title, text=text, public=public)
            note.save()
        else:
            note = Note(title=title, text=text, public=public)
            note.save()
        return note
'''