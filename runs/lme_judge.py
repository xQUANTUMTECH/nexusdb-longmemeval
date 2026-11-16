"""LongMemEval official judging: the repo's own get_anscheck_prompt, judge gpt-4o-2024-08-06, temperature 0, max_tokens 10,
label = 'yes' in reply. Runs via OpenRouter. Budget stop (--max-usd).
  python lme_judge.py lme/hyp_gpt-4o-mini.jsonl
"""
import json, sys, time, argparse, threading, urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, "/workspace/LongMemEval/src/evaluation")
from evaluate_qa import get_anscheck_prompt  # official prompts

ap = argparse.ArgumentParser()
ap.add_argument("hyp")
ap.add_argument("--judge", default="openai/gpt-4o-2024-08-06")
ap.add_argument("--max-usd", type=float, default=1.5)
ap.add_argument("--data", default="lme/data.json")
a = ap.parse_args()
KEY = [l.split("=", 1)[1].strip() for l in open("/workspace/openrouter.env") if l.startswith("OPENROUTER_API_KEY")][0]
data = {d["question_id"]: d for d in json.load(open(a.data))}
hyps = {}
for l in open(a.hyp):
    r = json.loads(l); hyps[r["question_id"]] = r["hypothesis"]
outp = Path(a.hyp + ".eval-gpt-4o")
res = {json.loads(l)["question_id"]: json.loads(l) for l in outp.open()} if outp.exists() else {}
lock = threading.Lock(); spent = [0.0]


def judge(q):
    if q in res or spent[0] > a.max_usd: return
    d = data[q]
    p = get_anscheck_prompt(d["question_type"], d["question"], d["answer"], hyps[q], abstention="_abs" in q)
    body = {"model": a.judge, "temperature": 0, "max_tokens": 10, "messages": [{"role": "user", "content": p}]}
    for t in range(5):
        try:
            req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(body).encode(),
                                         headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json", "User-Agent": "lab-bench/1.0"})
            r = json.loads(urllib.request.urlopen(req, timeout=60).read())
            txt = r["choices"][0]["message"]["content"]; u = r.get("usage", {})
            row = {"question_id": q, "type": d["question_type"], "label": "yes" in txt.lower(), "judge": txt, "question": d["question"], "gold": str(d["answer"])[:500], "hypothesis": hyps[q][:1000], "judge_model": r.get("model"), "provider": r.get("provider")}
            with lock:
                spent[0] += u.get("prompt_tokens", 0) * 2.5 / 1e6 + u.get("completion_tokens", 0) * 10 / 1e6
                res[q] = row
                with outp.open("a") as f: f.write(json.dumps(row) + "\n")
            return
        except Exception as e:
            time.sleep(3 * (t + 1)); err = e
            print(f"retry {t+1} {q}: {type(e).__name__} {str(e)[:200]}", flush=True)
    print("fail", q, err, flush=True)


with ThreadPoolExecutor(8) as ex:
    list(ex.map(judge, list(hyps)))
by = defaultdict(list)
for r in res.values(): by[r["type"]].append(r["label"])
allv = [r["label"] for r in res.values()]
print(f"{Path(a.hyp).name}: accuracy {sum(allv)/len(allv):.4f} (n={len(allv)}) judge-spend ${spent[0]:.3f}")
for k, v in sorted(by.items()): print(f"  {k:28s} {sum(v)/len(v):.4f} ({len(v)})")
abs_ = [r["label"] for q, r in res.items() if "_abs" in q]
if abs_: print(f"  {'abstention':28s} {sum(abs_)/len(abs_):.4f} ({len(abs_)})")
