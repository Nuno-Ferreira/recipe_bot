from tkinter import E


class QuotaError (Exception):
    pass


class MissingIngredientError(Exception):
    pass



class RecipesNotFoundError(Exception):
    pass



class InvalidRandomTagError(Exception):
    pass