#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""根据仓库语言自动生成技能花园 + 生成中文唯美痕迹卡片"""
import json, os, time, urllib.request, urllib.error, datetime

TOKEN = os.environ.get("GH_TOKEN", "")
OWNER = os.environ.get("GH_OWNER", "L0NE-6")
API = "https://api.github.com"

def get(url, tries=5):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={
                "Authorization": "Bearer " + TOKEN,
                "Accept": "application/vnd.github+json",
                "User-Agent": "profile-assets-gen",
                "Connection": "close",
            })
            with urllib.request.urlopen(req, timeout=45) as r:
                raw = r.read()
            return json.loads(raw.decode("utf-8"))
        except Exception as e:
            last = e
            time.sleep(1.5 * (i + 1))
    raise last

PALETTE = ["#F9A8D4", "#C4B5FD", "#A7F3D0", "#BAE6FD", "#FDE68A", "#DDD6FE", "#FBCFE8", "#99F6E4"]

repos = get(f"{API}/user/repos?per_page=100&affiliation=owner")
langs, star_total, repo_count = {}, 0, 0
for repo in repos:
    if repo.get("fork"):
        continue
    repo_count += 1
    star_total += repo.get("stargazers_count", 0)
    try:
        data = get(f"{API}/repos/{OWNER}/{repo['name']}/languages")
    except Exception:
        continue
    for k, v in data.items():
        langs[k] = langs.get(k, 0) + v

total = sum(langs.values()) or 1
top = sorted(langs.items(), key=lambda x: -x[1])[:6]
if not top:
    top = [("Python", 1)]

H = 96 + len(top) * 46
rows = []
for i, (name, size) in enumerate(top):
    pct = size / total * 100
    w = max(18, int(560 * pct / 100))
    y = 108 + i * 46
    c = PALETTE[i % len(PALETTE)]
    rows.append(f'''  <text x="40" y="{y + 13}" font-size="15" fill="#F5EDFF">{name}</text>
  <rect x="210" y="{y}" width="560" height="15" rx="7.5" fill="#332a56"/>
  <rect x="210" y="{y}" width="{w}" height="15" rx="7.5" fill="{c}" opacity="0.85" filter="url(#sgl)"/>
  <rect x="210" y="{y}" width="{w}" height="15" rx="7.5" fill="{c}"/>
  <text x="790" y="{y + 13}" font-size="13" fill="#C9BEE8">{pct:.1f}%</text>''')

skills_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{H}" viewBox="0 0 900 {H}" font-family="'PingFang SC','Microsoft YaHei',sans-serif">
  <defs>
    <filter id="sgl" x="-20%" y="-200%" width="140%" height="500%"><feGaussianBlur stdDeviation="4"/></filter>
  </defs>
  <rect x="2" y="2" width="896" height="{H - 4}" rx="18" fill="#241c3f" fill-opacity="0.92" stroke="#C4B5FD" stroke-opacity="0.32" stroke-width="1.5"/>
  <text x="40" y="52" font-size="18" font-weight="600" fill="#FFFFFF" letter-spacing="2">&#10022; 技能花园</text>
  <text x="40" y="76" font-size="12" fill="#C9BEE8">SKILL GARDEN &#183; 根据仓库语言自动生长</text>
{chr(10).join(rows)}
</svg>
'''

user = get(f"{API}/users/{OWNER}")
created = datetime.datetime.strptime(user["created_at"][:10], "%Y-%m-%d")
days = (datetime.datetime.utcnow() - created).days

traces_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="270" viewBox="0 0 900 270" font-family="'PingFang SC','Microsoft YaHei',sans-serif">
  <defs>
    <linearGradient id="tg" x1="0%" x2="100%"><stop offset="0%" stop-color="#F9A8D4"/><stop offset="50%" stop-color="#C4B5FD"/><stop offset="100%" stop-color="#A7F3D0"/></linearGradient>
    <filter id="tgl" x="-30%" y="-200%" width="160%" height="500%"><feGaussianBlur stdDeviation="4"/></filter>
    <radialGradient id="thalo"><stop offset="0%" stop-color="#C4B5FD" stop-opacity="0.22"/><stop offset="100%" stop-color="#C4B5FD" stop-opacity="0"/></radialGradient>
  </defs>
  <rect x="2" y="2" width="896" height="266" rx="18" fill="#241c3f" fill-opacity="0.92" stroke="#C4B5FD" stroke-opacity="0.32" stroke-width="1.5"/>
  <ellipse cx="450" cy="60" rx="300" ry="70" fill="url(#thalo)"/>
  <text x="450" y="58" text-anchor="middle" font-size="19" font-weight="600" fill="url(#tg)" letter-spacing="3" filter="url(#tgl)" opacity="0.5">&#10022; 走过的痕迹</text>
  <text x="450" y="58" text-anchor="middle" font-size="19" font-weight="600" fill="url(#tg)" letter-spacing="3">&#10022; 走过的痕迹</text>
  <text x="450" y="82" text-anchor="middle" font-size="12" fill="#C9BEE8">每一天都算数 &#183; EVERY STEP COUNTS</text>
  <g transform="translate(150,168)">
    <text text-anchor="middle" font-size="30" font-weight="700" fill="#F9A8D4">{days}</text>
    <text y="26" text-anchor="middle" font-size="13" fill="#C9BEE8">天前遇见 GitHub</text>
  </g>
  <g transform="translate(350,168)">
    <text text-anchor="middle" font-size="30" font-weight="700" fill="#C4B5FD">{repo_count}</text>
    <text y="26" text-anchor="middle" font-size="13" fill="#C9BEE8">个小仓库</text>
  </g>
  <g transform="translate(550,168)">
    <text text-anchor="middle" font-size="30" font-weight="700" fill="#A7F3D0">{star_total}</text>
    <text y="26" text-anchor="middle" font-size="13" fill="#C9BEE8">颗星星</text>
  </g>
  <g transform="translate(750,168)">
    <text text-anchor="middle" font-size="30" font-weight="700" fill="#BAE6FD">{user.get("followers", 0)}</text>
    <text y="26" text-anchor="middle" font-size="13" fill="#C9BEE8">位同行者</text>
  </g>
  <line x1="230" y1="120" x2="230" y2="200" stroke="#C4B5FD" stroke-opacity="0.18"/>
  <line x1="430" y1="120" x2="430" y2="200" stroke="#C4B5FD" stroke-opacity="0.18"/>
  <line x1="630" y1="120" x2="630" y2="200" stroke="#C4B5FD" stroke-opacity="0.18"/>
  <text x="450" y="246" text-anchor="middle" font-size="12" fill="#A99BD6">&#127769; 一个人单走一条路，也在慢慢发光</text>
</svg>
'''

os.makedirs("assets", exist_ok=True)
with open("assets/skills-auto.svg", "w", encoding="utf-8") as f:
    f.write(skills_svg)
with open("assets/traces.svg", "w", encoding="utf-8") as f:
    f.write(traces_svg)
print("generated skills-auto.svg + traces.svg")
print("languages:", [(n, round(s / total * 100, 1)) for n, s in top])
print("days:", days, "repos:", repo_count, "stars:", star_total)