import os, glob, re
dirs = ['.', 'crm', 'app/pages']
for d in dirs:
    for fpath in glob.glob(os.path.join(d, '*.html')):
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Buscamos i18n.js sin versionar y lo versionamos
            if 'src="js/i18n.js"' in content:
                new_content = content.replace('src="js/i18n.js"', 'src="js/i18n.js?v=4.2.4"')
            elif 'src="../js/i18n.js"' in content:
                new_content = content.replace('src="../js/i18n.js"', 'src="../js/i18n.js?v=4.2.4"')
            elif 'src="../../js/i18n.js"' in content:
                new_content = content.replace('src="../../js/i18n.js"', 'src="../../js/i18n.js?v=4.2.4"')
            else:
                continue
                
            if new_content != content:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'Updated {fpath}')
        except Exception as e:
            print(f'Error {fpath}: {str(e)}')
