import hashlib as lib
import os
import json

record = 'check.json'         # where we keep previous hash data
look = 'files_to_monitor'  # folder containing files to check

# calculate SHA256 hash of a file
def get_file_hash(path):
    hash = lib.sha256()
    with open(path, 'rb') as n:
        while True:
            ready = n.read(8192)
            if not ready:
                break
            hash.update(ready)
    return hash.hexdigest()

# read saved hashes from last run
def prev():
    if not os.path.exists(record):
        return {}
    with open(record, 'r') as f:
        return json.load(f)

# save current hashes for next time
def curr(hashes):
    with open(record, 'w') as f:
        json.dump(hashes, f, indent=2)

# main logic to compare old and new hashes
def change():
    previous = prev()
    current = {}
    something_changed = False

    for root, _, files in os.walk(look):
        for fname in files:
            full_path = os.path.join(root, fname)
            hash_val = get_file_hash(full_path)
            relative = os.path.relpath(full_path, look)
            current[relative] = hash_val

            if relative not in previous:
                print(f"[NEW]      {relative}")
                something_changed = True
            elif previous[relative] != hash_val:
                print(f"[CHANGED]  {relative}")
                something_changed = True

    # check for any deleted files
    for old_file in previous:
        if old_file not in current:
            print(f"[DELETED]  {old_file}")
            something_changed = True

    curr(current)

    if not something_changed:
        print("✅ All files are unchanged. (Nice!)")

# run the checker
if __name__ == '__main__':
    change()