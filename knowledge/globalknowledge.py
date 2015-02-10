# NOTE: presunuto do knowledge.models
#from __future__ import unicode_literals
#from knowledge.models import KnowledgeBuilder, KnowledgeGraph, Topic

## we will use our KnowledgeGraph model to store global knowledge
## (one row for one term), so we need a special identifier for the behavior
#GLOBAL_KNOWLEDGE_BUILDER_BEHAVIOR = 'global-knowledge'


#class GlobalKnowledge(KnowledgeGraph):
#    """
#    Provides interface for quering DBpedia. It's a descendant of KnowledgeGraph
#    model, so all access methods are already implemented there.
#    """

#    # NOTE: Pro jednoduchost vyvoje nepouzivam specializovane grafove DB (napr.
#    # Virtuoso nebo 4Store), ve kterych bych mel nahranou celou DB. Pozdeji to
#    # tak mozna udelam, ale je to pomerne narocne a vyzaduje dostatek
#    # prostredku (ma to cenu jedine na laboratornich serverech, jinak ne).
#    # Soucasne reseni je pouzit verejny pristupovy bod jako zdroj informaci a
#    # lokalni relacni DB pro jejich ulozeni.
#    # TODO: cachovani dotazu (mapovani pres hash dotazu)

#    # TODO: convenience functions, such as label()
#    # (using knowledge.utils.sparql.label)
#    # NOTE: Probably I will need the same convenience functions for
#    # KnowledgeGraph and for GlobalKnowledge, so 2 solutions are: use
#    # inheritance / vse definovat v utils)
