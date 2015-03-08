MANAGE=../manage.py

models:
	${MANAGE} graph_models abstract_component knowledge exercises practice smartoo -g > models.dot
	dot -Tpdf models.dot -o models.pdf
