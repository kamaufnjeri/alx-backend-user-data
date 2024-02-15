import os

# Get the value of a specific environmental variable
auth_type = os.getenv("AUTH_TYPE")

# Check if the variable is set
if auth_type:
    print("AUTH_TYPE is set to:", auth_type)
else:
    print("AUTH_TYPE is not set.")
