test:
	@sudo -u postgres psql -c "CREATE DATABASE test2"
	@-pytest
	@sudo -u postgres psql -c "DROP DATABASE test2"
