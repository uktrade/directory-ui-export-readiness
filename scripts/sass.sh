#!/bin/bash
# This script will render the project css files.

# put the path of library scss files we want to incluide
libraries="\
	--load-path core/static/vendor/css/bourbon \
"

# put the path of source code files we want to include, and where we want them
# to be exported to e.g., input.scss:output.css
input_output_map="\
	./core/static/styles/pages/casestudy.scss:core/static/styles/pages/casestudy.css \
	./core/static/styles/pages/home.scss:core/static/styles/pages/home.css \
	./core/static/styles/pages/article.scss:core/static/styles/pages/article.css \
	./core/static/styles/pages/triage.scss:core/static/styles/pages/triage.css \
	./core/static/styles/pages/article-list.scss:core/static/styles/pages/article-list.css \
"
prod_command="sass --style compressed"

eval $prod_command$libraries$input_output_map
