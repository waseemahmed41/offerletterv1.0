class DatabaseRouter:
    """
    A router to control all database operations on models for different databases.
    Now using only default (SQLite) database for all operations.
    """
    
    route_app_labels = {'auth', 'admin', 'contenttypes', 'sessions', 'accounts', 'offers'}

    def db_for_read(self, model, **hints):
        """
        All models use default database.
        """
        return 'default'

    def db_for_write(self, model, **hints):
        """
        All models use default database.
        """
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations since all models are in the same database.
        """
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        All apps migrate to default database only.
        """
        return db == 'default'
