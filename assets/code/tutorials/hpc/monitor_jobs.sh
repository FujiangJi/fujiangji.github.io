# Slurm: submit, inspect the queue, and review accounting.
sbatch submit_job.sh
squeue -u "$USER"
sacct -j JOB_ID --format=JobID,State,Elapsed,MaxRSS

# Inspect the logs for your job.
cat research_JOB_ID.out
cat research_JOB_ID.err

# HTCondor: run on your assigned HTC access point.
condor_q
condor_status
