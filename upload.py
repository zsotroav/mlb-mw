import os
from auth import auth, S, URL

# Step
directory = 'up'
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        print(f)
        # Step 4: Post request to upload a file directly
        PARAMS_FILE = {
            "action": "upload",
            "filename": filename,
            "format": "json",
            "token": auth(),
            "ignorewarnings": 1
        }

        FILE = {'file':(filename, open(f, 'rb'), 'multipart/form-data')}

        R = S.post(URL, files=FILE, data=PARAMS_FILE)
        print(R.json())
