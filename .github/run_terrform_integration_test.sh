# replace the creds
cd ./teflo_terraform_workspace
sed "s/access_key_place_holder/$1/g" variables.tf.tmpl > variables
sed "s/access_secret_place_holder/$2/g" variables > variables.tf

