class DatabaseRouter(object): 
    def db_for_read(self, model, **hints):
        "Point all operations on subscriptions model to 'testdatabase'"
        if model.__name__ == 'Subscriptions' or model.__name__ == "SubscriptionDetails":
            return 'testdatabase'
        return 'default'

    def db_for_write(self, model, **hints):
        "Point all operations to 'default' database"
        return 'default'
    
    def allow_syncdb(self, db, model):
        if db == 'testdatabase' or model.__name__ == "Subscriptions" or model.__name__ == "SubscriptionDetails":
            return False # we're not using syncdb on our flask database
        else: # but all other models/databases are fine
            return True