import pathlib,shutil,zipfile,hashlib,json
R=pathlib.Path.cwd();out=R/'artifacts/Najdi-New-3D-Desktop';shutil.rmtree(out,ignore_errors=True);out.mkdir()
shutil.copytree(R/'dist',out/'web');shutil.rmtree(out/'web/assets/models',ignore_errors=True)
p=out/'web/assets/manifest.json';p.unlink(missing_ok=True)
shutil.copy(R/'scripts/desktop-server.mjs',out/'start.mjs');shutil.copy(R/'artifacts/relay-v4.cjs',out/'relay.cjs')
(out/'public').mkdir(exist_ok=True);shutil.copy(R/'public/build-integrity.json',out/'public/build-integrity.json')
for folder in ['config','maps']:shutil.copytree(R/'public'/folder,out/'public'/folder)
(out/'PLAY.bat').write_bytes(b'@echo off\r\ncd /d "%~dp0"\r\nwhere node >nul 2>nul\r\nif errorlevel 1 (\r\n echo Node.js is required. Install Node.js 24 or newer.\r\n pause\r\n exit /b 1\r\n)\r\nnode start.mjs\r\nif errorlevel 1 pause\r\n')
(out/'README-AR.txt').write_text('فك الضغط أولًا، ثم افتح PLAY.bat بالدبل كليك. يفتح المتصفح تلقائيًا على Windows.\nلا تحتاج npm أو كتابة أوامر أو تحميل حزم. تحتاج Node.js 24 أو أحدث.\nاترك النافذة السوداء مفتوحة أثناء اللعب. الإغلاق يوقف الخادم.\nالتجربة تستخدم حزمة مجسمات جديدة assets/najdi-v4 فقط.\nاختبار Windows الفعلي غير متاح في بيئة Linux؛ لا ندعي اختباره.\n',encoding='utf8')
files={str(p.relative_to(out)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(out.rglob('*'))if p.is_file()};(out/'SHA256.json').write_text(json.dumps(files,indent=2))
zpath=R/'artifacts/Najdi-New-3D-Desktop.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED)as z:
 for p in out.rglob('*'):
  if p.is_file():z.write(p,'Najdi-New-3D-Desktop/'+str(p.relative_to(out)))
print(zpath)
