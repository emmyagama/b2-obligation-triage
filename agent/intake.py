import hashlib, json
from datetime import datetime, timezone
from .cache import canonical

def begin(db, external_ref, document_id, intake_party, context, channel, versions):
    request={'external_ref':external_ref,'document_id':document_id,'intake_party':intake_party,'business_context':context,'channel':channel}
    digest=hashlib.sha256(canonical(request).encode()).hexdigest()
    with db:
        db.execute('BEGIN IMMEDIATE')
        existing=db.execute('SELECT request_hash,run_id FROM idempotency WHERE key=?',(external_ref,)).fetchone()
        if existing:
            if existing['request_hash'] != digest: raise ValueError('idempotency key reused with different request')
            return existing['run_id'],True
        now=datetime.now(timezone.utc).isoformat()
        intake=db.execute('INSERT INTO intakes(external_ref,document_id,intake_party,business_context,channel,received_at) VALUES(?,?,?,?,?,?)',(external_ref,document_id,intake_party,context,channel,now)).lastrowid
        run=db.execute("INSERT INTO runs(intake_id,model,prompt_version,schema_version,corpus_version,started_at,status) VALUES(?,?,?,?,?,?,'failed')",(intake,versions['model'],versions['prompt_version'],versions['schema_version'],versions['corpus_version'],now)).lastrowid
        db.execute('INSERT INTO idempotency(key,request_hash,run_id,created_at) VALUES(?,?,?,?)',(external_ref,digest,run,now))
    return run,False
