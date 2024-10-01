from django.utils import timezone
from django.http.response import HttpResponse
from user.models import CustomUser as User, Wallet


def send_salary():
    """
    This is a method to send the user salary.
    this function will call from the cron jab on the perticular time
    """
    vip_users = User.objects.filter(vip_level__in=['1', '2', '3', '4', '5', '6', '7'])
    today = timezone.datetime.now()

    if not Wallet.objects.filter(
        pay_type = "Salary",
        created_at__date=today.date()).exists() and vip_users.exists():
        wallete_create = []
        for user in vip_users:
            amount = 0
            if user.vip_level == "1":
                amount = 400
            elif user.vip_level == "2":
                amount = 800
            elif user.vip_level == "3":
                amount = 1400
            elif user.vip_level == "4":
                amount = 2500
            elif user.vip_level == "5":
                amount = 3500
            elif user.vip_level == "6":
                amount = 5000
            
            if amount > 0:
                wallete_create.append(
                    Wallet(
                        user = user,
                        amount = amount,
                        pay_type = "Salary",
                        status = "Success",
                        pay_method = "Automatic",
                        remark = "Daily salary credit"
                    ))
        
        if wallete_create:
            Wallet.objects.bulk_create(objs=wallete_create, batch_size=10)
            print("Salary sent successfuly.")
            msg = "Salary sent successfuly."

    else:
        print("Today salary has been alredy sent.")
        msg = "Today salary has been alredy sent."
    msg = "Executed.."
    # return HttpResponse(msg)
