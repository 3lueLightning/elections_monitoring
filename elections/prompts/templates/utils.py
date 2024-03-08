from elections import constants


def get_aliases(names: str | list[str]) -> str:
   if isinstance(names, str):
      names = [names]
   aliases = constants.POLITICIAN_ALIASES
   intro = """
   All these politicians listed in this section ARE PRESENT in this article: \n
   """
   aka_quote = "* {name} is also know by many other alises, such as: {aliases}."
   l = [
      aka_quote.format(name=politician, aliases=", ".join(aliases[politician])) 
      for politician in names
   ]
   return intro + "\n".join(l)
