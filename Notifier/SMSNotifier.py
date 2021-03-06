# -*- coding: utf-8 -*-
from AbstractNotifier import AbstractNotifier
from twilio.rest import TwilioRestClient
    
class SMSNotifier(AbstractNotifier):
    account_sid = "AC6bb045ccc703d566fb983b7f760ec4c1"#AC6f519fcf4071615f570f2b10fe7a4a30" # Your Account SID from www.twilio.com/console
    auth_token  = "c67926c27533534a954ff080f40f4021"#d95781c0a8c685b8ddc7568d9ba28fe8"  # Your Auth Token from www.twilio.com/console

    def notify(self, crop_production_id,disease_name, risk_rate):
        # récupèrer les clients concernés par l'alerte
        clients=self.data_access.getCropProductionOwners(crop_production_id)
        crop_production_name = self.data_access.getCropProductionName(crop_production_id)
        # récupérer le nom de la maladie 
        msgtext= "Attention Il y a un risque de "+ disease_name+" dans votre culture "+crop_production_name+" avec un taux de "+str(risk_rate)
        print msgtext
        # envoi de l'alerte à tous les clients concernés
        for client in clients:
            print client
            if(client[-3]):
                phone_sms = client[-1]
                twilioClient = TwilioRestClient(self.account_sid, self.auth_token)        
                twilioClient.messages.create(body=msgtext,
                    to=phone_sms,     # phone_sms value
                    from_="+12512629352")#"+13175762039") # Twilio number 
                
                print "sms sent"
            else: print "sms notif are not activated"

