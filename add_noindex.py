import os
import glob
import re

files_to_check = ['crm.html'] + glob.glob('crm/*.html')

for filepath in files_to_check:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if '<meta name="robots"' not in content:
            # We want to insert it right after <head> or before <title>
            new_content = re.sub(r'(<head.*?>)', r'\1\n    <meta name="robots" content="noindex, nofollow">', content, count=1, flags=re.IGNORECASE)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Added noindex to {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
