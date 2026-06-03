# JLPT Lyrics Lesson

把日语歌词整理成 JLPT 备考材料的 Codex Skill。

用户提供歌名、歌手、备考等级和歌词后，本 skill 会生成两份 Word 文档：

- `JLPT歌词学习讲义.docx`
- `JLPT应试训练.docx`

当前版本优先验证“歌词学习 + JLPT 题型训练”的生成质量。歌词需要用户提供，或来自你自己配置的授权/本地歌词库。

## Features

- 按指定 JLPT 等级生成材料：`N5 / N4 / N3 / N2 / N1`
- 生成歌词学习讲义：
  - 日语歌词原文
  - 汉字假名标注
  - 自然中文译文
  - 生词表
  - 语法点讲解
  - 学习提示
- 生成 JLPT 应试训练：
  - 文字・词汇
  - 语法
  - 读解
  - 信息检索
  - 答案与解析
- 避免无效题型：
  - 不做整首歌词默写
  - 不做大段歌词挖空
  - 不做模拟听力题
- 支持本地歌词库检索：
  - JSONL
  - JSON
  - CSV

## Current MVP Flow

当前最小可用流程：

1. 用户输入歌名、歌手、备考等级。
2. 用户提供歌词文本。
3. Codex 根据歌词整理学习内容和题目。
4. 运行脚本生成两份 DOCX。

示例：

```text
歌名：Mad World
歌手：ONE OK ROCK
备考等级：N5
歌词：...
```

## Skill Usage

在 Codex 中使用：

```text
Use $jlpt-lyrics-lesson to create N5 study materials for "Mad World" by ONE OK ROCK. I will paste the lyrics below.
```

如果已经配置本地歌词库，也可以只提供：

```text
歌名：セプテンバーさん
歌手：RADWIMPS
备考等级：N3
```

## Generate DOCX From JSON

脚本入口：

```bash
python scripts/generate_jlpt_lyrics_docs.py input.json --out-dir outputs
```

最小 JSON 示例：

```json
{
  "song_title": "セプテンバーさん",
  "song_title_cn": "九月",
  "artist": "RADWIMPS",
  "target_level": "N3",
  "source_note": "基于用户提供文本整理",
  "lyrics": [
    {
      "ja": "君（きみ）が笑（わら）える理由（りゆう）なら",
      "zh": "如果那是能让你笑出来的理由，"
    }
  ],
  "vocabulary": [
    {
      "word": "理由",
      "kana": "りゆう",
      "meaning": "理由",
      "pos": "名词",
      "jlpt": "N4",
      "usage": "「笑える理由」表示能笑出来的原因。"
    }
  ],
  "grammar": [
    {
      "pattern": "N なら",
      "jlpt": "N4",
      "explanation": "表示假定条件。",
      "lyric_context": "君が笑える理由なら。",
      "example": "君となら大丈夫です。"
    }
  ],
  "study_tips": [
    "这份材料按 N3 备考筛选。"
  ],
  "drill_sections": [
    {
      "title": "A 卷：N3 文字・词汇",
      "tasks": [
        {
          "title": "问题 1：汉字读法",
          "instruction": "选择划线词的正确读法。",
          "columns": ["No.", "题干", "选项", "答"],
          "rows": [
            ["1", "理由なら、僕が見つける。", "A りゆう  B りよう  C りゅう  D りゆ", ""]
          ]
        }
      ]
    }
  ],
  "answers": [
    {
      "title": "A 卷答案",
      "items": ["问题 1：1 A。"]
    }
  ]
}
```

输出文件名会包含备考等级：

```text
セプテンバーさん_RADWIMPS_N3_JLPT歌词学习讲义.docx
セプテンバーさん_RADWIMPS_N3_JLPT应试训练.docx
```

## Local Lyrics Library

可以用本地歌词库实现“用户只输入歌名 + 歌手 + 等级”的流程。

JSONL 示例：

```json
{"song_title":"セプテンバーさん","artist":"RADWIMPS","language":"ja","lyrics":"...","source":"user_provided","license_status":"user_provided"}
```

设置环境变量：

```bash
export JLPT_LYRICS_LIBRARY=/path/to/lyrics.jsonl
```

Windows PowerShell：

```powershell
$env:JLPT_LYRICS_LIBRARY="C:\path\to\lyrics.jsonl"
```

检索歌词：

```bash
python scripts/resolve_lyrics.py --title "セプテンバーさん" --artist "RADWIMPS"
```

## Lyrics Rights

歌词通常受版权保护。这个仓库不内置歌词，也不建议直接抓取公开歌词网站内容。

推荐顺序：

1. 用户自己提供歌词。
2. 使用你拥有或已授权的本地歌词库。
3. 商业上线时接授权歌词服务。
4. 查不到歌词时再让用户粘贴或上传。

可调研的授权方向：

- Musixmatch
- LyricFind
- PetitLyrics / SyncPower
- JASRAC 相关授权信息

## Repository Structure

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── jlpt_question_types.md
│   └── lyrics_sources.md
└── scripts/
    ├── generate_jlpt_lyrics_docs.py
    └── resolve_lyrics.py
```

## Roadmap

- Add a small curated test lyrics library.
- Add examples for N5/N4/N3/N2/N1.
- Add a simple web form MVP.
- Add licensed lyrics provider adapters.
- Add automated DOCX render QA in CI.

## Status

Early MVP. The current focus is validating the quality of generated Japanese learning materials before building a full web product.
