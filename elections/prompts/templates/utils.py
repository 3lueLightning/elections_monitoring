from elections import constants


def get_aliases(names: list[str]) -> str:
   aliases = constants.POLITICIAN_ALIASES
   intro = """
   These politicians in this article are also known by other names: \n
   """
   aka_quote = "* {name} is also know by many other alises, such as: {aliases}."
   l = [
      aka_quote.format(name=politician, aliases=", ".join(aliases[politician])) 
      for politician in names
   ]
   return intro + "\n".join(l)
