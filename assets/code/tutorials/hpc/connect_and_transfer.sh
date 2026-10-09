# Local terminal: replace YOUR_NETID with your account name.
ssh YOUR_NETID@spark-login.chtc.wisc.edu

# Copy a file to your home directory (run from the local terminal).
scp input.csv YOUR_NETID@spark-login.chtc.wisc.edu:/home/YOUR_NETID/

# Copy results back to the current local directory.
scp YOUR_NETID@spark-login.chtc.wisc.edu:/scratch/YOUR_NETID/results.zip .
