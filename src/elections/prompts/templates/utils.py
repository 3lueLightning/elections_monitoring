from elections import constants


def old_get_aliases(names: str | list[str]) -> str:
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


def get_aliases(surnames: str | list[str]) -> str:
   surnames_to_names = {surname: name for name, surname in constants.SURNAMES.items()}
   
   if isinstance(surnames, str):
      surnames = [surnames]
   
   aliases = constants.PARTIES
   intro = """
   All these politicians listed in this section ARE PRESENT in this article, \
   and must be present in the sentiment analysis. Note that sometimes they \
   are only refered to by their last name: \n
   """
   aka_quote = "* {name}: {party}"
   l = [
      aka_quote.format(
         name=surnames_to_names.get(politician, politician),
         party=aliases[surnames_to_names.get(politician, politician)]
      ) 
      for politician in surnames
   ]
   return intro + "\n".join(l)
