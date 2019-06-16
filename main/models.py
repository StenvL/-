from django.db import models as m

class Executor(m.Model):
    executor_UID = m.BigIntegerField()
    executor_name = m.CharField(max_length = 256)
    is_actual = m.BooleanField()
    # рейтинги пересчитваются по команде, чтобы не перегружать сервер
    damage_rating = m.FloatField() # итоговый рейтинг по тяжести последствий (больше - хуже)
    reaction_speed_rating = m.FloatField() # итоговый рейтинг по медлительности реагирования (больше - лучше)
    @classmethod
    def add(self, name, actual):
        Executor.objects.update_or_create(
            executor_UID = id(self),
            executor_name = name,
            is_actual = actual,
            damage_rating = 0,
            reaction_speed_rating =0
        )

class Status(m.Model): # выполнено, не выполнено, выполняется
    SUID = m.BigIntegerField()
    status_name = m.CharField(max_length = 100)
    @classmethod
    def add(self, name):
        Status.objects.update_or_create(
            status_UID=id(self),
            status_name=name,
        )
class TerritoryType(m.Model): # двор и т.д.
    territory_type_UID = m.BigIntegerField()
    territory_name = m.CharField(max_length = 100)
    @classmethod
    def add(self, name):
        TerritoryType.objects.update_or_create(
            territory_type_UID=id(self),
            territory_name=name,
        )
class Client(m.Model): # заказчик
    client_UID = m.BigIntegerField()
    client_name = m.CharField(max_length = 256)
    @classmethod
    def add(self, name):
        Client.objects.update_or_create(
            client_UID=id(self),
            client_name=name,
        )
class JobType(m.Model):
    job_type_UID = m.BigIntegerField()
    job_type_name = m.CharField(max_length = 100)
    @classmethod
    def add(self, name):
        JobType.objects.update_or_create(
            job_type_UID=id(self),
            job_type_name=name,
        )
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
    @classmethod
    def add(self, executor):
        Contract.objects.update_or_create(
            contract_UID=id(self),
            executor_UID = Executor.objects.filter(executor_name = executor)

        )
class Claim(m.Model): # жалобы / инциденты по контракту
    claim_UID = m.BigIntegerField()
    contract_UID = m.ForeignKey(Contract, on_delete = m.CASCADE)
    comment = m.CharField(max_length = 256)  # замечание в читаемом виде
    comment_date = m.DateTimeField()
    fix_date = m.DateTimeField()
    damage = m.BigIntegerField()

class Request(m.Model): #заявки от людей на сайте (по ним инициируется проект, если несколько заявок за раз - значит, вовремя не отреагировали)
    # id не нужен, т.к. поиск осуществляется по всем заявкам сразу
    fio = m.CharField(max_length = 256)
    phone = m.BigIntegerField()
    email = m.CharField(max_length=100)
    address = m.CharField(max_length = 256) # места проблемы
    job_type_uid = m.ForeignKey(JobType, on_delete = m.CASCADE)
    comment = m.CharField(max_length = 256)

class DataManager(m.Manager):
    #####
    # временное решение, далее будет нормализовано
    #####
    @classmethod
    def add_data(self, territory_name, planned_length, money, job_type_name, executor_name, year, accident_type, accident_weight, shift_weight, shift_days):
        new_id = 1
        if (Everything.objects.all().count()>0):
            new_id = Everything.objects.all().order_by("-id")[0].id+1
        entry = Everything(new_id, territory_name, planned_length, money, job_type_name, executor_name, year, accident_type, accident_weight, shift_weight, shift_days)
        entry.save()

    @classmethod
    def add_company(self, company_name, foundation_date):
        new_id = 1
        if (Company.objects.all().count() > 0):
            new_id = Company.objects.all().order_by("-id")[0].id + 1
        entry = Company(new_id, company_name, foundation_date)
        entry.save()
    #not implemented yet
    @classmethod
    def add_contract(self, address, territory_type, client, job_type, year, status, money, contract_id, executor, start_date, end_date, claim, claim_date, fix_date, fixed_too_late, claims_during_fixes, final_claims_after_fix):
        pass
        #Executor.add(executor)
        #Contract.add(executor)
'''class Everything(m.Model):
    address = m.CharField(max_length=256)  # адрес объекта
    territory_name = m.CharField(max_length=100)
    client_name = m.CharField(max_length=256)
    job_type_name = m.CharField(max_length=100)
    year = m.IntegerField()
    status_name = m.CharField(max_length=100)
    money = m.FloatField()  # сумма контракта
    contract_ID = m.CharField(max_length=10)  # в текстовом виде, из-за неровных входных данных "15 от 12.03" и т.п.
    executor_name = m.CharField(max_length=256)
    real_start_date = m.DateTimeField()
    real_end_date = m.DateTimeField()
    comment = m.CharField(max_length=256)  # замечание в читаемом виде
    comment_date = m.DateTimeField()
    fix_date = m.DateTimeField()
    fixed_too_late = m.BigIntegerField()
    claims_during_fixes = m.BigIntegerField()
    final_claims_after_fix = m.BigIntegerField()

    # рейтинги пересчитваются по команде, чтобы не перегружать сервер
    damage_rating = m.FloatField(default = 0)  # итоговый рейтинг по тяжести последствий (больше - хуже)
    reaction_speed_rating = m.FloatField(default = 0)  # итоговый рейтинг по медлительности реагирования (больше - лучше)
    damage = m.BigIntegerField(default = 0)
'''
class Everything(m.Model):
    territory_name = m.CharField(max_length=100)
    planned_length = m.BigIntegerField()
    money = m.FloatField()
    job_type_name = m.CharField(max_length=100)
    executor_name = m.CharField(max_length=256)
    year = m.IntegerField()
    accident_type = m.CharField(max_length=256)
    accident_weight = m.BigIntegerField()
    shift_weight = m.BigIntegerField()
    shift_days = m.BigIntegerField()
class Company(m.Model):
    executor_name = m.CharField(max_length = 100)
    foundation_date = m.BigIntegerField()

'''
1. сложность проекта = Contract.money // учесть время?
2. кол-во обращений в процессе Contract.claims_during_fixes
3. рейтинг проблем - рейтинг по тяжести последствий. (в Executor.damage_rating) из замечания
* ПОИСК ВСТРЕЧАЕМОСТИ В СТРОКЕ
шум, неудобства                                     1
просрок, не в срок -------------                    2
не понлностью, не в полном объёме ----------        3
травма, несчастный случай                           4
не выполнено, смерть, умер ------------             5
рейт = Contract.claims_during_fixes + Contract.final_claims_after_fix + ЗАЯВКИ(на сайте).всего
#4. рейтинг по скорости реагирования (в Executor.reaction_speed_ratiыng)
4. рейтинг проблем по гарантийному сроку (кол-во обр. по рез-м работы) - Contract.final_claims_after_fix
5. доверие - просрок по замечаниям

ИТОГОВЫЙ РЕЙТИНГ = срзнач(все)
Графики: суммарный рейтинг от времени для каждой компании
'''