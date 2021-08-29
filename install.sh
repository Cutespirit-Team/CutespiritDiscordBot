# install requirements
cd ./CutespiritDiscordBot/

echo "check for the requirements..."
pip install -r requirments.txt
echo "OK"

# execute
cd ./src
echo "try to run ctbot by python..."
python -m ctbot
echo "deleting install.sh file"
rm -rf install.sh
echo "All Down."
echo "(C) Cutespirit 2021 \nMade By Cutespirit. email: service@cutespirit.org ."
echo "Thank You for installing! Enjoy!"
