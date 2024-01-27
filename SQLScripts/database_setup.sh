#!/bin/bash

# execute like this
# sudo -u postgres bash database-setup.sh database.config

# your config file must look like
#username=some_user
#password=some_password
#dbname=DatabaseName
#host=localhost
#port=5432

if [ "$#" -ne 1 ]; then
  echo "Please provide only config file name"
else
	filename="$1"
	if [ -f $filename ]; then
		echo "Reading $filename file"
		source $filename

		if [ -z $username ]; then
			echo "username variable is blank or not set in $filename"
		elif [ -z $password ]; then
			echo "password variable is blank or not set in $filename"
		elif [ -z $dbname ]; then
			echo "dbname variable is blank or not set in $filename"
		elif [ -z $host ]; then
			echo "host variable is blank or not set in $filename"
		elif [ -z $port ]; then
			echo "port variable is blank or not set in $filename"
		else
			echo "username = $username"
			echo "password = $password"
			echo "dbname = $dbname"
			echo "host = $host"
			echo "port = $port"

			echo "Database $dbname and user $username will be dropped if exist already"
			echo "Do you want to proceed? (y/n)"

			read answer

			if [ "$answer" = "n" ]; then
				echo "Terminating script. Nothing was changed"
			else
				if [ "$( psql -tAc "SELECT 1 FROM pg_database WHERE datname='$dbname'" )" = '1' ]; then
					echo "Database $dbname already exists"
					psql -c "DROP DATABASE \"$dbname\";"
				fi

				if [ "$( psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='$username'" )" = '1' ]; then
					echo "User $username already exists"
					psql -c "DROP USER $username;"
				fi

				init_script_path="initDB.sql"
				if [ -f $init_script_path ]; then
					psql -c "CREATE DATABASE \"$dbname\";"
					echo "Database $dbname created successfully"
					psql -c "CREATE USER $username WITH ENCRYPTED PASSWORD '$password';"
					echo "User $username created successfully"
					psql -c "GRANT ALL PRIVILEGES ON DATABASE \"$dbname\" TO $username;"
					echo "Rights to manage $dbname database granted to $username user"
					psql -f "$init_script_path" "postgresql://$username:$password@$host:$port/$dbname"
					echo "Initialization script $init_script_path executed successfully"
				else
					echo "Database creation script $creation_script_path not found"
				fi
			fi
		fi
	else
		echo "File $filename does not exist."
	fi
fi