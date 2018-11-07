build: docker_test

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

test_requirements:
	pip install -r requirements_test.txt

FLAKE8 := flake8 . --exclude=migrations,.venv,node_modules
PYTEST := pytest . -v --ignore=node_modules --cov=. --cov-config=.coveragerc --capture=no $(pytest_args)
COLLECT_STATIC := python manage.py collectstatic --noinput
COMPILE_TRANSLATIONS := python manage.py compilemessages
CODECOV := \
	if [ "$$CODECOV_REPO_TOKEN" != "" ]; then \
	   codecov --token=$$CODECOV_REPO_TOKEN ;\
	fi

translations:
	$(DEBUG_SET_ENV_VARS) && python manage.py makemessages -a

compile_translations:
	$(DEBUG_SET_ENV_VARS) && python manage.py compilemessages

test:
	$(COLLECT_STATIC) && $(COMPILE_TRANSLATIONS) && $(FLAKE8) && $(PYTEST) && $(CODECOV)

DJANGO_WEBSERVER := \
	python manage.py collectstatic --noinput && \
	python manage.py runserver 0.0.0.0:$$PORT

django_webserver:
	$(DJANGO_WEBSERVER)

DOCKER_COMPOSE_REMOVE_AND_PULL := docker-compose -f docker-compose.yml -f docker-compose-test.yml rm -f && docker-compose -f docker-compose.yml -f docker-compose-test.yml pull
DOCKER_COMPOSE_CREATE_ENVS := python ./docker/env_writer.py ./docker/env.json ./docker/env.test.json

docker_run:
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL) && \
	docker-compose up --build

DOCKER_SET_DEBUG_ENV_VARS := \
	export DIRECTORY_UI_EXPORT_READINESS_API_CLIENT_CLASS_NAME=unit-test; \
	export DIRECTORY_UI_EXPORT_READINESS_API_SIGNATURE_SECRET=debug; \
	export DIRECTORY_UI_EXPORT_READINESS_API_CLIENT_BASE_URL=http://api.trade.great:8000; \
	export DIRECTORY_UI_EXPORT_READINESS_SSO_SIGNATURE_SECRET=api_signature_debug; \
	export DIRECTORY_UI_EXPORT_READINESS_SSO_API_CLIENT_BASE_URL=http://sso.trade.great:8003/; \
	export DIRECTORY_UI_EXPORT_READINESS_SSO_PROXY_LOGIN_URL=http://sso.trade.great:8004/accounts/login/; \
	export DIRECTORY_UI_EXPORT_READINESS_SSO_PROXY_LOGOUT_URL=http://sso.trade.great:8004/accounts/logout/?next=http://exred.trade.great:8007; \
	export DIRECTORY_UI_EXPORT_READINESS_SSO_PROXY_SIGNUP_URL=http://sso.trade.great:8004/accounts/signup/; \
	export DIRECTORY_UI_EXPORT_READINESS_SSO_PROFILE_URL=http://profile.trade.great:8006/about/; \
	export DIRECTORY_UI_EXPORT_READINESS_SSO_PROXY_REDIRECT_FIELD_NAME=next; \
	export DIRECTORY_UI_EXPORT_READINESS_SSO_SESSION_COOKIE=debug_sso_session_cookie; \
	export DIRECTORY_UI_EXPORT_READINESS_SESSION_COOKIE_SECURE=false; \
	export DIRECTORY_UI_EXPORT_READINESS_PORT=8001; \
	export DIRECTORY_UI_EXPORT_READINESS_SECRET_KEY=debug; \
	export DIRECTORY_UI_EXPORT_READINESS_DEBUG=true; \
	export DIRECTORY_UI_EXPORT_READINESS_COMPANIES_HOUSE_API_KEY=debug; \
	export DIRECTORY_UI_EXPORT_READINESS_GOOGLE_TAG_MANAGER_ID=GTM-NLJP5CL; \
	export DIRECTORY_UI_EXPORT_READINESS_GOOGLE_TAG_MANAGER_ENV=&gtm_auth=S2-vb6_RF_jGWu2WJIORdQ&gtm_preview=env-5&gtm_cookies_win=x; \
	export DIRECTORY_UI_EXPORT_READINESS_UTM_COOKIE_DOMAIN=.trade.great; \
	export DIRECTORY_UI_EXPORT_READINESS_CORS_ORIGIN_ALLOW_ALL=true; \
	export DIRECTORY_UI_EXPORT_READINESS_COMPANIES_HOUSE_CLIENT_ID=debug-client-id; \
	export DIRECTORY_UI_EXPORT_READINESS_COMPANIES_HOUSE_CLIENT_SECRET=debug-client-secret; \
	export DIRECTORY_UI_EXPORT_READINESS_SECURE_HSTS_SECONDS=0; \
	export DIRECTORY_UI_EXPORT_READINESS_PYTHONWARNINGS=all; \
	export DIRECTORY_UI_EXPORT_READINESS_PYTHONDEBUG=true; \
	export DIRECTORY_UI_EXPORT_READINESS_HEADER_FOOTER_URLS_GREAT_HOME=http://exred.trade.great:8007/; \
	export DIRECTORY_UI_EXPORT_READINESS_HEADER_FOOTER_URLS_FAB=http://buyer.trade.great:8001; \
	export DIRECTORY_UI_EXPORT_READINESS_HEADER_FOOTER_URLS_SOO=http://soo.trade.great:8008; \
	export DIRECTORY_UI_EXPORT_READINESS_HEADER_FOOTER_URLS_CONTACT_US=http://contact.trade.great:8009/directory/; \
	export DIRECTORY_UI_EXPORT_READINESS_COMPONENTS_URLS_FAS=http://supplier.trade.great:8005/; \
	export DIRECTORY_UI_EXPORT_READINESS_SECURE_SSL_REDIRECT=false; \
	export DIRECTORY_UI_EXPORT_READINESS_HEALTH_CHECK_TOKEN=debug; \
	export DIRECTORY_UI_EXPORT_READINESS_COMTRADE_API_TOKEN=DEBUG; \
	export DIRECTORY_UI_EXPORT_READINESS_RECAPTCHA_PUBLIC_KEY=6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI; \
	export DIRECTORY_UI_EXPORT_READINESS_RECAPTCHA_PRIVATE_KEY=6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe; \
	export DIRECTORY_UI_EXPORT_READINESS_CMS_URL=http://cms.trade.great:8010; \
	export DIRECTORY_UI_EXPORT_READINESS_CMS_SIGNATURE_SECRET=debug; \
	export DIRECTORY_UI_EXPORT_READINESS_FEATURE_CMS_ENABLED=true; \
	export DIRECTORY_UI_EXPORT_READINESS_PRIVACY_COOKIE_DOMAIN=.trade.great; \
	export DIRECTORY_UI_EXPORT_READINESS_FEATURE_UKEF_LEAD_GENERATION_ENABLED=true; \
	export DIRECTORY_UI_EXPORT_READINESS_FEATURE_HIGH_POTENTIAL_OPPORTUNITIES_ENABLED=true; \
	export DIRECTORY_UI_EXPORT_READINESS_UKEF_FORM_SUBMIT_TRACKER_URL=http://go.pardot.com/l/590031/2018-08-16/5kj25l; \
	export DIRECTORY_UI_EXPORT_READINESS_DIRECTORY_FORMS_API_BASE_URL=http://forms.trade.great:8011; \
	export DIRECTORY_UI_EXPORT_READINESS_DIRECTORY_FORMS_API_API_KEY=debug; \
	export DIRECTORY_UI_EXPORT_READINESS_DIRECTORY_FORMS_API_SENDER_ID=debug; \
	export DIRECTORY_UI_EXPORT_READINESS_FEATURE_PROTOTYPE_PAGES_ENABLED=true; \
	export DIRECTORY_UI_EXPORT_READINESS_FEATURE_NEWS_SECTION_ENABLED=true; \
	export DIRECTORY_UI_EXPORT_READINESS_FEATURE_PROTOTYPE_HEADER_FOOTER_ENABLED=true; \
	export DIRECTORY_UI_EXPORT_READINESS_FEATURE_EU_EXIT_FORMS_ENABLED=true; \
	export DIRECTORY_UI_EXPORT_READINESS_EU_EXIT_ZENDESK_SUBDOMAIN=debug; \
	export DIRECTORY_UI_EXPORT_READINESS_DIRECTORY_FORMS_API_API_KEY_EUEXIT=debug; \
	export DIRECTORY_UI_EXPORT_READINESS_DIRECTORY_FORMS_API_SENDER_ID_EUEXIT=debug


docker_test_env_files:
	$(DOCKER_SET_DEBUG_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS)

DOCKER_REMOVE_ALL := \
	docker ps -a | \
	grep directoryui_ | \
	awk '{print $$1 }' | \
	xargs -I {} docker rm -f {}

docker_remove_all:
	$(DOCKER_REMOVE_ALL)

docker_debug: docker_remove_all
	$(DOCKER_SET_DEBUG_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	docker-compose pull && \
	docker-compose build && \
	docker-compose run --service-ports webserver make django_webserver

docker_webserver_bash:
	docker exec -it directoryui_webserver_1 sh

docker_test: docker_remove_all
	$(DOCKER_SET_DEBUG_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL) && \
	docker-compose -f docker-compose-test.yml build && \
	docker-compose -f docker-compose-test.yml run sut

docker_build:
	docker build -t ukti/directory-ui-export-readiness:latest .

DEBUG_SET_ENV_VARS := \
	export PORT=8007; \
	export SECRET_KEY=debug; \
	export DEBUG=true ;\
	export API_SIGNATURE_SECRET=debug; \
	export API_CLIENT_BASE_URL=http://api.trade.great:8000; \
	export SSO_SIGNATURE_SECRET=api_signature_debug; \
	export SSO_API_CLIENT_BASE_URL=http://sso.trade.great:8003/; \
	export SSO_PROXY_LOGIN_URL=http://sso.trade.great:8004/accounts/login/; \
	export SSO_PROXY_LOGOUT_URL=http://sso.trade.great:8004/accounts/logout/?next=http://exred.trade.great:8007; \
	export SSO_PROXY_SIGNUP_URL=http://sso.trade.great:8004/accounts/signup/; \
	export SSO_PROFILE_URL=http://profile.trade.great:8006/about/; \
	export SSO_PROXY_REDIRECT_FIELD_NAME=next; \
	export SSO_SESSION_COOKIE=debug_sso_session_cookie; \
	export SESSION_COOKIE_SECURE=false; \
	export COMPANIES_HOUSE_API_KEY=debug; \
	export GOOGLE_TAG_MANAGER_ID=GTM-NLJP5CL; \
	export GOOGLE_TAG_MANAGER_ENV=&gtm_auth=S2-vb6_RF_jGWu2WJIORdQ&gtm_preview=env-5&gtm_cookies_win=x; \
	export UTM_COOKIE_DOMAIN=.trade.great; \
	export CORS_ORIGIN_ALLOW_ALL=true; \
	export COMPANIES_HOUSE_CLIENT_ID=debug-client-id; \
	export COMPANIES_HOUSE_CLIENT_SECRET=debug-client-secret; \
	export SECURE_HSTS_SECONDS=0; \
	export PYTHONWARNINGS=all; \
	export PYTHONDEBUG=true; \
	export HEADER_FOOTER_URLS_GREAT_HOME=http://exred.trade.great:8007/; \
	export HEADER_FOOTER_URLS_FAB=http://buyer.trade.great:8001; \
	export HEADER_FOOTER_URLS_SOO=http://soo.trade.great:8008; \
	export HEADER_FOOTER_URLS_CONTACT_US=http://contact.trade.great:8009/directory/; \
	export COMPONENTS_URLS_FAS=http://supplier.trade.great:8005/; \
	export SERVICES_EXOPPS_ACTUAL=http://opportunities.export.great.gov.uk; \
	export SECURE_SSL_REDIRECT=false; \
	export HEALTH_CHECK_TOKEN=debug; \
	export DIRECTORY_UI_EXPORT_READINESS_COMTRADE_API_TOKEN=DEBUG; \
	export RECAPTCHA_PUBLIC_KEY=6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI; \
	export RECAPTCHA_PRIVATE_KEY=6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe; \
	export LANDING_PAGE_VIDEO_URL=thing.com; \
	export CMS_URL=http://cms.trade.great:8010; \
	export CMS_SIGNATURE_SECRET=debug; \
	export FEATURE_CMS_ENABLED=true; \
	export FEATURE_PERFORMANCE_DASHBOARD_ENABLED=true; \
	export FEATURE_SEARCH_ENGINE_INDEXING_DISABLED=true; \
	export REDIS_URL=redis://localhost:6379; \
	export PRIVACY_COOKIE_DOMAIN=.trade.great; \
	export FEATURE_UKEF_LEAD_GENERATION_ENABLED=true; \
	export FEATURE_HIGH_POTENTIAL_OPPORTUNITIES_ENABLED=true; \
	export UKEF_FORM_SUBMIT_TRACKER_URL=http://go.pardot.com/l/590031/2018-08-16/5kj25l; \
	export DIRECTORY_FORMS_API_BASE_URL=http://forms.trade.great:8011; \
	export FEATURE_PROTOTYPE_PAGES_ENABLED=true; \
	export FEATURE_NEWS_SECTION_ENABLED=true; \
	export FEATURE_EU_EXIT_FORMS_ENABLED=true; \
	export FEATURE_PROTOTYPE_HEADER_FOOTER_ENABLED=false; \
	export FEATURE_EU_EXIT_FORMS_ENABLED=true; \
	export EU_EXIT_ZENDESK_SUBDOMAIN=debug

debug_webserver:
	$(DEBUG_SET_ENV_VARS) && $(DJANGO_WEBSERVER)

debug_pytest:
	$(DEBUG_SET_ENV_VARS) && $(COLLECT_STATIC) && $(PYTEST)

debug_test:
	$(DEBUG_SET_ENV_VARS) && $(COLLECT_STATIC) && $(FLAKE8) && $(PYTEST) --cov-report=html

debug_test_last_failed:
	make debug_test pytest_args='-v --last-failed'

debug_manage:
	$(DEBUG_SET_ENV_VARS) && ./manage.py $(cmd)

debug_shell:
	$(DEBUG_SET_ENV_VARS) && ./manage.py shell

debug: test_requirements debug_test

heroku_deploy_dev:
	./docker/install_heroku_cli.sh
	docker login --username=$$HEROKU_EMAIL --password=$$HEROKU_TOKEN registry.heroku.com
	~/bin/heroku-cli/bin/heroku container:push web --app directory-ui-exp-readiness-dev
	~/bin/heroku-cli/bin/heroku container:release web --app directory-ui-exp-readiness-dev

integration_tests:
	cd $(mktemp -d) && \
	git clone https://github.com/uktrade/directory-tests && \
	cd directory-tests && \
	make docker_integration_tests

compile_requirements:
	pip-compile requirements.in
	pip-compile requirements_test.in

upgrade_requirements:
	pip-compile --upgrade requirements.in
	pip-compile --upgrade requirements_test.in

new_redirect:
	python scripts/add_new_redirect.py

.PHONY: build clean test_requirements docker_run docker_debug docker_webserver_bash docker_test debug_webserver debug_test debug heroku_deploy_dev heroku_deploy_demo
