# Define SFTP servers
SFTP_SERVERS=("192.168.56.201" "192.168.56.202" "192.168.56.203")
USERNAME="sftp"

CURRENT_IP=$(hostname -I | awk '{print $2}')
PASSWORD="pass"
# Loop through each SFTP server and upload the file
for SERVER in "${SFTP_SERVERS[@]}"; do
    if [ "$SERVER" != "$CURRENT_IP" ]; then
         # Use sshpass to provide the password for ssh-copy-id
        sshpass -p "$PASSWORD" ssh-copy-id -o StrictHostKeyChecking=no "$USERNAME@$SERVER"
        
        if [ $? -eq 0 ]; then
            echo "SSH key successfully copied to $SERVER"
        else
            echo "Failed to copy SSH key to $SERVER"
        fi
    fi 
done