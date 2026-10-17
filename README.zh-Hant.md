# Unified Motion Director

**Codex 產品敘事與精密動態影像 Skill。** 由產品功能理解、主張證據查核、分鏡時間線、Remotion 動畫製作，到實際影片嘅雙獨立 Agent 驗收，統一成一套可以追溯嘅工作流程。

<p align="center"><img src="./assets/readme/workflow.svg" width="100%" alt="創意導演、分鏡、Remotion 影片製作、影片解碼驗證與獨立評審流程。"></p>

[English](README.md) · [Skill 指示](SKILL.md) · [更新紀錄](CHANGELOG.md) · [來源授權](ATTRIBUTION.md)

## v1.7 有咩提升

- **產品敘事理解**：由功能因果關係推導畫面，而唔係盲目加入特效。
- **產品真實性 Hard Gate**：產品主張必須提供證據，實驗／示意功能必須保留揭示。
- **音樂分析**：根據實際音訊提出節拍及 Drop 候選，不冒稱已人工核實。
- **語義動態文字**：繁體中文以詞組／短句分段，重點數字與文字保留閱讀時間。
- **Motion Grammar**：把 UI、數據、路徑、數字同品牌串成有資訊意義嘅轉場。
- **手機可讀性檢查**：從真實版面幾何資料檢查字級、邊界同停留時長；審美仍由獨立評審決定。

保留原有審美 **55%**、整體 **45%**，總分 ≥85、兩名評審各 ≥80 嘅驗收要求。真實性屬**獨立阻擋條件**，唔可以用高審美分數抵消。

## 安裝

```bash
python3 scripts/install_codex.py --user --apply
# 或安裝到專案
python3 scripts/install_codex.py --project /path/to/project --apply
```

Skill 不會自動安裝 [Remotion Plugin](https://chatgpt.com/plugins/remotion)。可使用已連接嘅 Plugin、官方 Remotion CLI，或其他已支援嘅動畫後端。

## 執行流程

**產品證據 → 真實性檢查 → 創意導演 → 分鏡與時間線 → Remotion／動畫引擎 → MP4 → 技術及可讀性檢查 → 雙獨立評審 → 驗收**

```bash
python3 scripts/validate_storyboard.py /path/to/film/storyboard.json
python3 scripts/product_truth.py /path/to/film/claims.json --storyboard /path/to/film/storyboard.json
python3 scripts/analyze_music.py /path/to/audio.wav --out /path/to/film/beat-analysis.json
python3 scripts/production_router.py /path/to/film/storyboard.json --out /path/to/film/handoff
python3 scripts/remotion_plugin_bridge.py prepare /path/to/film/storyboard.json --out /path/to/film/remotion-handoff
python3 scripts/motion_preflight.py /path/to/film/final.mp4 --layout-manifest /path/to/film/layout.json --out /path/to/film/preflight.json
```

音樂節拍偵測係候選結果；字體幾何檢查係預警。佢哋都唔會自動宣稱已聽完整首歌曲或已評審影片視覺品質。程式測試使用中立技術 fixture，Repo 唔包含任何特定品牌宣傳案例。

深入規格見 [產品敘事](references/product-storytelling.md)、[動態文字](references/kinetic-typography.md)、[動效語法](references/product-motion-patterns.md)、[視覺 Presets](references/visual-presets.md)、[驗收](references/independent-acceptance.md)。

## 測試及授權

```bash
python3 -m unittest discover -s tests -v
```

原始編排程式及文件以 [MIT](LICENSE) 授權；引用技法及第三方媒體另外遵守原作者授權，詳見 [ATTRIBUTION.md](ATTRIBUTION.md)。通過自動測試唔代表已實際製作 MP4、調用 Remotion Plugin 或完成獨立 AI 審美評審。
