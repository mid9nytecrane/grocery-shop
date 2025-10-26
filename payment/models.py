from django.db import models
from django.contrib.auth.models import User
from payment.paystack import Paystack
import uuid





class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10,blank=True, null=True, decimal_places=2)
    reference = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=250)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.user} - {self.amount}"


    
    def amount_value(self):
        return int(self.amount) * 100
    

    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.reference, self.amount)
        print(f"\nresult amount: {result['amount']}")
        if status:
            print(f"results after status: { result['amount']/100}")
            r = result['amount']/100
            print(type(r))
            print(f"self.amount: {self.amount}")
            print(type(self.amount))
            if (result['amount'] / 100) == float(self.amount):
                self.verified = True 
                self.save()

        if self.verified:
            return True 
        else:
            return False 
        
