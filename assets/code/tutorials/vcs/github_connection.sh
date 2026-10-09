# Create a key only if you do not already have a suitable one.
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add the PUBLIC .pub key to GitHub using its SSH setup guide.
# Then test the connection.
ssh -T git@github.com
