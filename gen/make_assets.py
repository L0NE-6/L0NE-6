#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""马里奥主题：技能花园(蘑菇) + 痕迹卡片(金币计分板)，数据自动从仓库读取"""
import json, os, time, urllib.request, datetime

TOKEN = os.environ.get("GH_TOKEN", "")
OWNER = os.environ.get("GH_OWNER", "L0NE-6")
API = "https://api.github.com"

def get(url, tries=5):
    last = None
    for i in range(tries):
        try:
            headers = {
                "Accept": "application/vnd.github+json",
                "User-Agent": "profile-assets-gen",
                "Connection": "close",
            }
            if TOKEN:
                headers["Authorization"] = "Bearer " + TOKEN
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=45) as r:
                raw = r.read()
            return json.loads(raw.decode("utf-8"))
        except Exception as e:
            last = e
            time.sleep(1.5 * (i + 1))
    raise last

# 马里奥配色
PALETTE = ["#E52521", "#F8B800", "#00A800", "#2A5BD7", "#FF7B00", "#E52521", "#58D854", "#00A800"]

repos = get(f"{API}/users/{OWNER}/repos?per_page=100&sort=updated")
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

# ================= 技能花园（蘑菇生长条）=================
H = 108 + len(top) * 48
rows = []
for i, (name, size) in enumerate(top):
    pct = size / total * 100
    w = max(20, int(540 * pct / 100))
    y = 116 + i * 48
    c = PALETTE[i % len(PALETTE)]
    # 蘑菇图标（出现的最小方块拼的）
    mx = 44
    rows.append(f'''  <g transform="translate({mx},{y - 4})">
    <rect x="4" y="0" width="14" height="4" fill="{c}"/>
    <rect x="0" y="4" width="22" height="8" fill="{c}"/>
    <rect x="4" y="12" width="14" height="5" fill="#FFF3C4"/>
    <rect x="7" y="13.5" width="3" height="3" fill="#2A2A2A"/>
    <rect x="12" y="13.5" width="3" height="3" fill="#2A2A2A"/>
  </g>
  <text x="80" y="{y + 13}" font-size="15" font-weight="700" fill="#FFFFFF">{name}</text>
  <rect x="220" y="{y}" width="540" height="16" rx="3" fill="#3A2A1A" stroke="#8A4B00" stroke-width="1.5"/>
  <rect x="222" y="{y + 2}" width="{w}" height="12" rx="2" fill="{c}"/>
  <rect x="222" y="{y + 2}" width="{w}" height="5" rx="2" fill="#FFFFFF" opacity="0.28"/>
  <text x="782" y="{y + 13}" font-size="13" font-weight="700" fill="#FFD93B">{pct:.1f}%</text>''')

skills_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{H}" viewBox="0 0 900 {H}" font-family="'PingFang SC','Microsoft YaHei',sans-serif">
  <defs>
    <linearGradient id="mp" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#5C94FC"/><stop offset="100%" stop-color="#8FC0FF"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="896" height="{H - 4}" rx="6" fill="url(#mp)" stroke="#2A5BD7" stroke-width="3"/>
  <g transform="translate(28,26)">
    <rect x="0" y="0" width="34" height="34" fill="#8A4B00"/><rect x="3" y="3" width="28" height="28" fill="#F8B800"/>
    <text x="17" y="26" text-anchor="middle" font-size="22" font-weight="900" fill="#FFFFFF">?</text>
  </g>
  <text x="76" y="42" font-size="19" font-weight="900" fill="#FFFFFF" letter-spacing="2">技能花园 · POWER-UPS</text>
  <text x="76" y="62" font-size="12" font-weight="700" fill="#FFF3C4" letter-spacing="1">吃下蘑菇，能力就会长大 &#183; 根据仓库语言自动生长</text>
  <rect x="28" y="78" width="844" height="3" fill="#2A5BD7" opacity="0.5"/>
{chr(10).join(rows)}
</svg>
'''

# ================= 痕迹卡片（金币计分板）=================
user = get(f"{API}/users/{OWNER}")
created = datetime.datetime.strptime(user["created_at"][:10], "%Y-%m-%d")
days = (datetime.datetime.utcnow() - created).days

def coin_card(cx, cy, value, label):
    return f'''  <g transform="translate({cx},{cy})">
    <ellipse cx="0" cy="0" rx="30" ry="38" fill="#FFD93B" stroke="#C99A00" stroke-width="5">
      <animate attributeName="rx" values="30;6;30" dur="3.4s" repeatCount="indefinite"/>
    </ellipse>
    <ellipse cx="0" cy="0" rx="16" ry="22" fill="none" stroke="#C99A00" stroke-width="4" opacity="0.7">
      <animate attributeName="rx" values="16;3;16" dur="3.4s" repeatCount="indefinite"/>
    </ellipse>
    <text x="0" y="12" text-anchor="middle" font-size="26" font-weight="900" fill="#FFFFFF" stroke="#C99A00" stroke-width="1.5" paint-order="stroke">{value}</text>
    <text x="0" y="62" text-anchor="middle" font-size="13" font-weight="700" fill="#FFF3C4">{label}</text>
  </g>'''

traces_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="300" viewBox="0 0 900 300" font-family="'PingFang SC','Microsoft YaHei',sans-serif">
  <defs>
    <linearGradient id="gr" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#5C94FC"/><stop offset="100%" stop-color="#B8DBFF"/>
    </linearGradient>
    <linearGradient id="fl" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/><stop offset="100%" stop-color="#E52521"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="896" height="296" rx="6" fill="url(#gr)" stroke="#2A5BD7" stroke-width="3"/>
  <g fill="#FFFFFF" opacity="0.95">
    <g transform="translate(60,26)"><rect x="0" y="10" width="70" height="18"/><rect x="12" y="2" width="42" height="12"/></g>
    <g transform="translate(760,32)"><rect x="0" y="10" width="80" height="18"/><rect x="14" y="2" width="48" height="12"/></g>
  </g>
  <text x="450" y="52" text-anchor="middle" font-size="20" font-weight="900" fill="#FFFFFF" stroke="#E52521" stroke-width="5" paint-order="stroke" letter-spacing="3">&#9733; 走过的痕迹 &#9733;</text>
  <text x="450" y="76" text-anchor="middle" font-size="12" font-weight="700" fill="#FFF3C4" letter-spacing="1">每一枚金币，都是认真走过的一天</text>
{coin_card(146, 168, days, "天前开始冒险")}
{coin_card(348, 168, repo_count, "个关卡（仓库）")}
{coin_card(552, 168, star_total, "颗星星")}
{coin_card(754, 168, user.get("followers", 0), "位队友")}
  <g transform="translate(370,238)">
    <rect x="0" y="0" width="160" height="38" rx="4" fill="#8A4B00"/>
    <rect x="5" y="5" width="150" height="28" rx="2" fill="#F8B800"/>
    <text x="80" y="26" text-anchor="middle" font-size="16" font-weight="900" fill="#FFFFFF">&#9654; START</text>
  </g>
  <text x="450" y="292" text-anchor="middle" font-size="11" font-weight="700" fill="#2A5BD7">一个人单走一条路，也能通关</text>
</svg>
'''

os.makedirs("assets", exist_ok=True)
with open("assets/skills-auto.svg", "w", encoding="utf-8") as f:
    f.write(skills_svg)
with open("assets/traces.svg", "w", encoding="utf-8") as f:
    f.write(traces_svg)
print("generated mario skills-auto.svg + traces.svg")
print("languages:", [(n, round(s / total * 100, 1)) for n, s in top])
print("days:", days, "repos:", repo_count, "stars:", star_total)