source venv/bin/activate
rm -rf servermanager.sqlite migrations
python -m manager db init
python -m manager db migrate
python -m manager db upgrade
python -m manager init_static_data
python -m manager init_test_data
