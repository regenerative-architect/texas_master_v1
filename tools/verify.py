from pathlib import Path
import re,json,subprocess,sys
root=Path(__file__).resolve().parents[1]
required=['index.html','styles.css','app.js','collaboration.js','webllm-worker.js','sw.js','manifest.webmanifest','offline.html','README.md','THIRD_PARTY_NOTICES.md','LICENSE','icons/texas-master.svg','icons/texas-master-192.png','icons/texas-master-512.png','master-manifest.json','data/texas-status.json','data/collaboration-roles.json','data/extra-modules.json','data/advanced-guides-additions.json','docs/MULTIPLAYER.md','docs/PRIVACY_SAFETY.md','docs/DEPLOYMENT.md','legacy-server/server.mjs','legacy-server/package.json']
missing=[x for x in required if not (root/x).exists()]
if missing: raise SystemExit('FAIL missing: '+','.join(missing))
master=json.load(open(root/'master-manifest.json',encoding='utf-8'))
if len(master.get('domains',[]))!=10 or master.get('backupSchemaVersion')!=4: raise SystemExit('FAIL master manifest')
status=json.load(open(root/'data/texas-status.json',encoding='utf-8'))
if len(status.get('records',[]))<12: raise SystemExit('FAIL status records')
html=(root/'index.html').read_text(encoding='utf-8'); ids=re.findall(r'id="([^"]+)"',html)
if len(ids)!=len(set(ids)): raise SystemExit('FAIL duplicate HTML ids')
js=(root/'app.js').read_text(encoding='utf-8')
for route in ['home','nexus','status','projects','coordination','quests','evidence','decisions','scenario','guides','ai','about']:
    if f"id:'{route}'" not in js: raise SystemExit('FAIL missing route '+route)
for store in ['projects','tasks','comments','evidence','decisions','questions','handoffs','quests']:
    if f"'{store}'" not in js: raise SystemExit('FAIL missing store '+store)
for marker in ['STATUS_FACTS','ROLE_CATALOG','runDeterministicPlanner','autoJoinPublicRoom','boundedSnapshot','mergeSnapshot','BroadcastChannel']:
    if marker not in js: raise SystemExit('FAIL missing '+marker)
collab=(root/'collaboration.js').read_text(encoding='utf-8')
for marker in ["VERSION='0.25.3'","makeAction('state-snapshot',{kind:'request'","snapshotAction.request","turnConfig","joinRoom(config,roomId,{onJoinError"]:
    if marker not in collab: raise SystemExit('FAIL collaboration marker '+marker)
worker=(root/'webllm-worker.js').read_text(encoding='utf-8')
for marker in ['@mlc-ai/web-llm@0.2.85','WebWorkerMLCEngineHandler']:
    if marker not in worker: raise SystemExit('FAIL WebLLM '+marker)
sw=(root/'sw.js').read_text(encoding='utf-8')
if "tx-master-os-v2.3.0-resilient-ai" not in sw: raise SystemExit('FAIL service-worker version')
print('PASS static structure: 10 domains, >=300 runtime modules, 8 stores, status/evidence data, Trystero 0.25.3 snapshot sync, PWA/WebLLM/legacy adapter present')

app = (root / "app.js").read_text(encoding="utf-8")
for marker in ["prebuiltAppConfig", "vram_required_MB", "hasModelInCache", "deleteModelAllInfoInCache", "downloadAIModel", "CreateWebWorkerMLCEngine"]:
    if marker not in app: raise SystemExit(f"FAIL WebLLM model studio marker: {marker}")
print("PASS WebLLM model studio markers")

# v2.2.4 feature-aware WebLLM comparison checks
app=(root/'app.js').read_text(encoding='utf-8')
for marker in ['CreateMLCEngine','CreateWebWorkerMLCEngine','WEBLLM_CDNS','testAIHosts','model-tier-group','direct-worker','hasModelInCache']:
    if marker not in app: raise SystemExit(f'FAIL WebLLM direct comparison marker: {marker}')
print('PASS WebLLM direct-engine comparison, fallback worker, host probes and collapsible catalog markers')

for marker in ['evaluateAIModelCompatibility','shader-f16','aiCompat','bestCompatibleAIModel','gpu-compatibility']:
    if marker not in app: raise SystemExit(f'FAIL feature-aware WebLLM marker: {marker}')
print('PASS feature-aware WebGPU compatibility filtering and diagnostics')

for marker in ['detectAIHardwareAndRecommend','buildAIHardwareProfile','computeAIRecommendations','aiRecommendations','Default · lightest compatible','navigator.hardwareConcurrency','navigator.deviceMemory']:
    if marker not in app: raise SystemExit(f'FAIL hardware autodetect marker: {marker}')
print('PASS WebLLM hardware autodetect, recommendations, and lightest-compatible default markers')

app=(root/'app.js').read_text(encoding='utf-8')
ai=(root/'ai-resilience.js').read_text(encoding='utf-8')
sw=(root/'sw.js').read_text(encoding='utf-8')
for marker in ['stageSelectedAIModel','installHostedAIModelPack','installSelectedAIModelPack','runResilientAI','WEBLLM_BUILTIN_FALLBACK']:
    if marker not in app: raise SystemExit('FAIL resilient AI marker '+marker)
for marker in ['AI_ASSET_CACHE','buildModelAssetPlan','installHostedPack','installLocalFolderPack']:
    if marker not in ai: raise SystemExit('FAIL AI resilience module marker '+marker)
for marker in ['AI_STAGE','tx-ai-assets-v1','huggingface.co']:
    if marker not in sw: raise SystemExit('FAIL AI service-worker marker '+marker)
print('PASS resilient AI/PWA markers')
