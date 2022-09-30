from io import StringIO
from html.parser import HTMLParser
import code
import importlib
import logging
import re
from tokenize import String
from urllib import response

from numpy import number

from spoonacular import API
from telegram.utils.helpers import escape_markdown

from nellie import config
from nellie import exceptions


class HTMLStripper(HTMLParser):

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, data):
        self.text.write(data)

    def get_data(self):
        return self.text.getvalue()

    def strip_tags(html):
        if not html:
            return

        stripper = HTMLStripper()
        stripper.feed(html)
        return stripper.get_data()

class SpoonacularFacade(object):

    def __init__(self, api_key=config.SPOONACULAR_KEY):
        self.client = API(api_key)
        logging.info("Client created!")

    def check_status_and_raise(self, response):
        content = response.json()
        if isinstance(content, list):
            return

        status = content.get("status")
        code = content.get("code")
        message = content.get("message")

        if status == "failure" and code = 402:
            raise exceptions.QuotaError(message)

    def get_recipe_ids_for_ingredients(self, ingredients, limit=config.RECIPE_LIMIT):
        response = self.client.search_recipes_by_ingredients(ingredients)
        self.check_status_and_raise(response)
        recipe_data = response.json()
        return [recipe["id"] for recipe in recipe_data[:limit]]

    def get_random_recipe(self, tags=None):
        response =self.client.get_random_recipes(tags=tags)
        self.check_status_and_raise(response)
        return response.json()["recipes"][0]

    def get_random_alcoholic_beverage_recipe_id(self):
        response = self.client.search_recipes_complex(
            "",
            type="drink",
            minAlcohol=7,
            sort="random",
            number=1
        )
        self.check_status_and_raise(response)
        return response.json()["results"][0]["id"]

    def get_recipes_for_ids(self, ids):
        logging.info(f"Getting recipes for the following ids: {ids}")
        ids_param = ','.join([str(_id) for _id in ids])
        response = self.client.get_recipe_information_bulk(ids_param)
        self.check_status_and_raise(response)
        recipes = response.json()
        return recipes

    @classmethod
    def format_recipe_title_link_as_markdown(cls, recipe_data):
        title = escape_markdown(strip_tags(recipe_data["title"]).strip(), 2)
        return f"**[{title}]({recipe_data['sourceUrl']})**"

    @classmethod
    def format_recipe_data_as_html(cls, recipe_data):
        ingredients = "\n".join([
            strip_tags(ingredient["originalString"]) for ingredient
            in recipe_data["extendedIngredients"]
        ])

        raw_instructions = recipe_data["instructions"]
        if not raw_instructions:
            instructions = "This recipe didn't have instructions! =O"
        else:
            instructions = re.sub(
                " +", " ",
                strip_tags(raw_instructions)).strip()

        formatted = (
            f"<b>{strip_tags(recipe_data['title'])}</b>\n"
            f"Cooktime: {recipe_data['readyInMinutes']} minutes\n\n"
            f"<u>Ingredients</u>\n"
            f"{ingredients}\n\n"
            f"<u>Instructions</u>\n"
            f"{instructions}"
        )

        return formatted