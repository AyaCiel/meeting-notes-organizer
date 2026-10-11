import sys
import anthropic

client = anthropic.Anthropic()

SYSTEM = """あなたは、営業の面談メモを整理するアシスタントです。
走り書きのメモを、次の5つの見出しで、この順番に整理します。

0. 基本情報：日時・相手・形式（メモに書かれているものだけ）
1. 事実：メモに書かれている、発言・数字・日付・決まったこと（そのまま、正確に）
2. 所感：書き手の印象や推測（「たぶん」「〜そう」「〜か？」など、確かでない内容）
3. 次のアクション：「誰が｜何を｜いつまでに」の形（メモに書かれているものだけ）
4. 未確認事項：メモに答えが書かれていない、確認が必要な点

守ること：
- メモにないことは、書かない。想像で補わない。分からない項目は「記載なし」と書く
- メモにない言葉を、足さない（例：メモが「時期は年度末あたりか？」なら、「導入時期」や「金額」などの語を加えない）
- 1つの文に事実と所感が混ざっているときは、分けて書く
- 数字・固有名詞・日付は、メモの表記のまま使う
- 見出しと箇条書きだけで、短く書く（表は使わない）。5つの見出し以外は、出力しない
"""

path = sys.argv[1] if len(sys.argv) > 1 else "sample_notes.txt"
with open(path, encoding="utf-8") as f:
    notes = f.read()

message = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=1200,
    system=SYSTEM,
    messages=[{"role": "user", "content": f"次の面談メモを整理してください。\n\n{notes}"}],
)

for block in message.content:
    if block.type == "text":
        print(block.text)
