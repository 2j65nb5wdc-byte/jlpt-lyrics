---
name: jlpt-lyrics-lesson
description: "Create Japanese lyric learning materials for a specific JLPT level. Use when the user provides or identifies a Japanese song and asks for a Word/DOCX lesson, lyric translation handout, vocabulary and grammar extraction, JLPT question design, graded worksheet, exam-style drills, or a reusable Japanese song-learning platform/template. Requires a target level such as N5, N4, N3, N2, or N1, and produces two DOCX files: a level-focused study handout and a level-focused written exam-style worksheet. Avoids listening simulation and rote lyric memorization."
---

# JLPT Lyrics Lesson

## Purpose

Turn Japanese lyrics into two teaching artifacts for one target JLPT level:

1. A lyric study handout: Japanese lyric lines with kana notes, natural Chinese translation, level-relevant vocabulary, grammar explanations, and study tips.
2. A written JLPT-style worksheet: vocabulary, grammar, reading, and information-search tasks calibrated to the user's target level.

Do not generate N5-N1 all at once unless the user explicitly asks for a multi-level teacher edition.

Only process lyrics the user provided or lyrics from a configured source the user has rights to use. Do not scrape or reproduce copyrighted lyrics from the web without an appropriate license.

## Required Inputs

Ask for any missing item before generating documents:

- Song title.
- Artist.
- Target JLPT level: `N5`, `N4`, `N3`, `N2`, or `N1`.
- Lyrics, or permission to look up lyrics from a configured local/licensed lyrics source.

If the user gives only title, artist, and level, resolve lyrics through the configured lyrics library. See `references/lyrics_sources.md`.

For product work, do not make "paste lyrics manually" the primary user path. Treat it as a fallback after source lookup, provider lookup, or user-authorized import/OCR fails.

## Workflow

1. Resolve lyrics:
   - Prefer user-provided lyrics.
   - Otherwise use a configured local/licensed lyrics source.
   - If no source is configured, ask the user to paste the lyrics.
2. Normalize the Japanese text for learning:
   - Correct obvious kana/kanji annotation errors.
   - Add kana in parentheses after kanji, for example `君（きみ）`.
   - Preserve lyric-like phrasing, but note uncertain corrections in the final response.
3. Produce natural Chinese translations line by line.
4. Extract only target-level teaching points:
   - Vocabulary: include mostly the target level and one adjacent lower level for scaffolding.
   - Grammar: prioritize patterns likely to matter for the target level.
   - Mark advanced items as "拓展" only when they are essential to the lyric.
5. Design the worksheet using written JLPT-style task types for the target level. Do not include listening simulation, lyric memorization, whole-line lyric blank filling, or "write the lyric from memory" tasks.
6. Create a JSON payload and run `scripts/generate_jlpt_lyrics_docs.py` to generate DOCX files.
7. If the Documents skill and LibreOffice are available, render the DOCX for visual QA. If rendering is unavailable, structurally inspect the DOCX and say so.

## Level Calibration

Use the user's target level as the organizing constraint.

- `N5`: kana/kanji readings, basic particles, basic verbs/adjectives, simple sentence meaning.
- `N4`: common verb forms, conditionals, `て` expressions, basic conjunctions, short-context comprehension.
- `N3`: nuance in common grammar, compound verbs, synonym replacement, sentence ordering, short reading.
- `N2`: written-style expressions, abstract vocabulary, discourse connectors, integrated reading.
- `N1`: advanced vocabulary, literary/figurative phrasing, subtle usage distinction, dense reading.

Do not label a worksheet section `N5-N3` or `N4-N2` unless the user asked for a range. Prefer titles such as `N3 文字・词汇` and `N3 语法`.

## Question Design

Use `references/jlpt_question_types.md` when designing the worksheet.

Default worksheet sections:

- `A 卷：<LEVEL> 文字・词汇`: kanji reading, contextual word choice, synonym replacement, usage.
- `B 卷：<LEVEL> 语法`: grammar form choice, sentence ordering, passage grammar.
- `C 卷：<LEVEL> 读解`: short reading, information search, integrated comprehension.
- `答案与解析`: concise answers and short explanations.

Avoid:

- Listening scripts or simulated listening tasks.
- Whole-lyric memorization.
- Large lyric cloze tasks whose only skill is recall.
- Mechanical translation without a tested grammar or comprehension target.

## DOCX Generation

Create a UTF-8 JSON file with this shape:

```json
{
  "song_title": "セプテンバーさん",
  "song_title_cn": "九月",
  "artist": "RADWIMPS",
  "target_level": "N3",
  "source_note": "基于用户提供文本整理",
  "lyrics": [
    {"ja": "君（きみ）が笑（わら）える理由（りゆう）なら", "zh": "如果那是能让你笑出来的理由，"}
  ],
  "vocabulary": [
    {"word": "繋ぐ", "kana": "つなぐ", "meaning": "连接；牵系", "pos": "动词", "jlpt": "N3", "usage": "歌词中指人与人、季节与回忆之间的连接。"}
  ],
  "grammar": [
    {"pattern": "N なら", "jlpt": "N4", "explanation": "表示假定条件。", "lyric_context": "君が笑える理由なら。", "example": "君となら大丈夫です。"}
  ],
  "study_tips": ["这份材料按 N3 备考筛选，N2 以上表达只作为拓展理解。"],
  "drill_sections": [
    {
      "title": "A 卷：N3 文字・词汇",
      "tasks": [
        {
          "title": "问题 1：汉字读法",
          "instruction": "选择划线词的正确读法。",
          "columns": ["No.", "题干", "选项", "答"],
          "rows": [["1", "夢を描いた。", "A ゆめ  B よめ  C ゆみ  D ゆうめ", ""]]
        }
      ]
    }
  ],
  "answers": [
    {"title": "A 卷答案", "items": ["问题 1：1 A。"]}
  ]
}
```

Run:

```bash
python scripts/generate_jlpt_lyrics_docs.py input.json --out-dir outputs
```

The script writes:

- `<song>_<artist>_<level>_JLPT歌词学习讲义.docx`
- `<song>_<artist>_<level>_JLPT应试训练.docx`

## Quality Bar

- Keep translation natural, not word-for-word when that would be awkward.
- Treat JLPT levels as teaching estimates, not official labels.
- Favor recognition, interpretation, and use over memorization.
- Keep all worksheet tasks aligned to the requested level.
- Keep tables readable: short stems, clear options, concise explanations.
- Put answers at the end so worksheets can be printed separately.
