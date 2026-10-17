#!/usr/bin/env python3
"""Hard, evidence-structure gate for product claims (NOT evidence fact-checking).

Ensures published claims have properly dated evidence and disclosures. Humans
must independently verify whether the submitted evidence actually proves them.
"""
import argparse
import json
from pathlib import Path
import re
import sys
from datetime import date

DISCLOSURE_TERMS=('示意','概念','模擬','concept','illustrat','demo','prototype','experimental','beta')


def valid_date(value):
    try:
        parsed=date.fromisoformat(value)
        return parsed<=date.today()
    except (ValueError, TypeError):
        return False


def validate(claims, storyboard=None):
    errors=[]
    if not isinstance(claims,dict): return ['Claims must be a JSON object']
    if claims.get('schema_version')!='1.0': errors.append('schema_version must equal 1.0')
    if not isinstance(claims.get('product_id'),str) or not claims['product_id'].strip(): errors.append('product_id required')
    rows=claims.get('claims')
    if not isinstance(rows,list): return errors+['claims must be an array']
    ids={}
    for i,c in enumerate(rows):
        label=f'claims[{i}]'
        if not isinstance(c,dict): errors.append(f'{label}: must be object'); continue
        name=c.get('id')
        if not isinstance(name,str) or not re.fullmatch('[a-z0-9][a-z0-9-]*',name): errors.append(f'{label}: invalid id'); continue
        if name in ids: errors.append(f'duplicate claim ID {name}')
        ids[name]=c
        if not isinstance(c.get('claim'),str) or len(c['claim'].strip())<4: errors.append(f'{name}: missing claim text')
        implementation=c.get('implementation_status')
        data=c.get('data_status'); mode=c.get('display_mode')
        if implementation not in ('shipped','beta','experimental','planned','retired'): errors.append(f'{name}: invalid implementation_status')
        if data not in ('verified','illustrative','unknown'): errors.append(f'{name}: invalid data_status')
        if mode not in ('factual_demo','concept_demo','omitted'): errors.append(f'{name}: invalid display_mode')
        if type(c.get('approved_for_public_copy')) is not bool: errors.append(f'{name}: approved_for_public_copy must be boolean')
        evidence=c.get('evidence')
        if not isinstance(evidence,list): errors.append(f'{name}: evidence must be an array'); evidence=[]
        for j,item in enumerate(evidence):
            if not isinstance(item,dict) or not isinstance(item.get('source'),str) or not item['source'].strip() or item.get('evidence_type') not in ('approved_product_ui','release_note','implementation','test_result','approved_documentation','producer_attestation') or not valid_date(item.get('checked_at')):
                errors.append(f'{name}: evidence[{j}] requires source, allowed evidence_type and non-future ISO checked_at')
        if mode=='factual_demo':
            if implementation not in ('shipped','beta'): errors.append(f'{name}: factual_demo requires shipped/beta implementation')
            if data!='verified': errors.append(f'{name}: factual_demo requires verified data_status')
            if not c.get('approved_for_public_copy'): errors.append(f'{name}: factual_demo requires explicit public copy approval')
            if not evidence: errors.append(f'{name}: factual_demo requires dated evidence')
            if not isinstance(c.get('evidence_reviewer'),str) or len(c['evidence_reviewer'].strip())<2 or not valid_date(c.get('evidence_reviewed_at')):
                errors.append(f'{name}: factual_demo requires named producer evidence reviewer and review date')
        if mode=='concept_demo':
            disclosure=c.get('disclosure','')
            if not isinstance(disclosure,str) or not any(t in disclosure.lower() for t in DISCLOSURE_TERMS):
                errors.append(f'{name}: concept_demo requires recognizable on-screen disclosure')
            if c.get('approved_for_public_copy') is True and implementation in ('planned','retired'):
                errors.append(f'{name}: unshipped/retired claim cannot be approved as public factual copy')
        if mode=='omitted' and c.get('approved_for_public_copy') is True:
            errors.append(f'{name}: omitted claim must not be approved as public copy')
    if storyboard is not None:
        if not isinstance(storyboard,dict) or not isinstance(storyboard.get('scenes'),list):
            errors.append('storyboard must have scenes')
        else:
            for s in storyboard['scenes']:
                sid=s.get('id','?')
                refs=s.get('claim_refs',[])
                if not isinstance(refs,list): errors.append(f'{sid}: claim_refs must be a list'); continue
                for ref in refs:
                    if ref not in ids: errors.append(f'{sid}: unknown claim_refs {ref}')
                    elif ids[ref].get('display_mode')=='omitted': errors.append(f'{sid}: omitted claim {ref} must not appear')
                    elif ids[ref].get('display_mode')=='concept_demo':
                        disclosure=ids[ref].get('disclosure','')
                        all_copy=' '.join(s.get('on_screen_text',[]))
                        if disclosure not in all_copy:
                            errors.append(f'{sid}: concept claim {ref} requires exact on-screen disclosure {disclosure!r}')
                for e in s.get('events',[]):
                    if isinstance(e,dict):
                        for ref in e.get('claim_refs',[]):
                            if ref not in refs: errors.append(f'{sid}: event claim_ref {ref} absent from scene claim_refs')
    return errors


def load_and_validate(claims_file, storyboard_file=None):
    claims=json.loads(Path(claims_file).read_text(encoding='utf-8'))
    sb=json.loads(Path(storyboard_file).read_text(encoding='utf-8')) if storyboard_file is not None else None
    errors=validate(claims,sb)
    try:
        import jsonschema
        schema=json.loads((Path(__file__).resolve().parents[1]/'templates/product-claims.schema.json').read_text())
        errors.extend(f'schema: {err.message}' for err in jsonschema.Draft202012Validator(schema).iter_errors(claims))
    except ImportError:
        pass
    return errors


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('claims',type=Path);p.add_argument('--storyboard',type=Path)
    p.add_argument('--out',type=Path)
    a=p.parse_args()
    try: errors=load_and_validate(a.claims,a.storyboard)
    except (OSError,ValueError) as e: errors=[str(e)]
    result={'status':'BLOCKED' if errors else 'STRUCTURAL_TRUTH_GATE_CLEAR_WITH_PRODUCER_ATTESTATION',
            'errors':errors,'claims_file':str(a.claims),'evidence_independently_verified':False,
            'release_approval':not errors}
    if a.out:
        a.out.parent.mkdir(parents=True,exist_ok=True)
        a.out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(result,indent=2,ensure_ascii=False))
    return 1 if errors else 0

if __name__=='__main__':sys.exit(main())
