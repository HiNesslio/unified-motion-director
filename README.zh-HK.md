# Unified Motion Director v1.6 for Codex — Remotion Collaborative Edition

**用途：**將概念 → 藝術指導 → 導演敘事 → 分鏡 → 動作設計 → 音樂節奏 → 程式實作 → 實際渲染 → **雙子 Agent 獨立評分與驗收**，統一成一條生產線。以繁體中文／粵語指令可以操作，成果可以是分鏡、HTML/SVG、Remotion 或可渲染影片專案。

## 不是另一份 Claude Motion Playbook

Playbook 已研究 233 個 Opus 5.5 動畫、137 種技法，本 Skill **唔重新抄寫技術百科**。它以 Playbook 為參考索引，補上導演判斷、故事、電影語法、分鏡規格、鏡頭與聲畫編排，並可選擇接上 Motion Director / Motion Composer 開源工作流程，同時加入 Hype-yolo `claude-motion-skill` 嘅原始碼輔助動畫製作路由。

**關於 Opus 審美：**將「可見作品中可重現嘅創作手法」轉成可執行製作原則；無法匯出另一模型未公開的思考過程，亦不保證生成與其相同的作品。

## v1.6：ChatGPT 官方 Remotion Plugin 協同製作

**官方插件：** https://chatgpt.com/plugins/remotion ；Codex 使用指引：https://www.remotion.dev/docs/ai/codex-plugin 。Remotion 官方已提供可安裝的 Codex Plugin；**需要另外安裝**，本 Skill ZIP 唔會自動安裝插件，亦唔會直接呼叫其他 ChatGPT session 嘅 Plugin。

一個 Codex workspace 使用兩套能力：**`$unified-motion-director` 係創意導演（概念、分鏡、審美方向）**，**`$remotion` 係動畫製作部門（React composition、Studio 預覽、聲畫製作同 MP4 輸出）**。兩位原有獨立 Juror 只喺最終影片渲染完成後驗收，避免自己評自己。

| 節點 | 單一責任人 | 真正交接成果 |
|---|---|---|
| 導演 | Unified Motion Director | BRIEF.md、LOOK.md、storyboard.json、素材真實性清單 |
| 對接 | Codex | remotion-handoff.json、shared-timeline.json、REMOTION_PLUGIN_TASK.md |
| 製作 | Remotion Plugin（可用時）或官方 CLI | 原始碼、Studio 預覽、草稿、音效同 MP4 |
| 驗收 | Codex 主 Agent + 2 位獨立 Juror | 技術預驗收、審美 55%＋整體 45%、修正紀錄 |

**產生交接資料（無須安裝 Plugin 都可用）：**

```bash
python3 scripts/remotion_plugin_bridge.py prepare \
  examples/parkgo/storyboard.json \
  --out /tmp/parkgo-remotion-handoff
```

喺有安裝 Remotion Plugin 嘅 Codex 對話中，可要求「`$unified-motion-director` 按 REMOTION_PLUGIN_TASK.md 執導，交 `$remotion` 實作、預覽同輸出，再由兩個獨立 Juror 評分」。Plugin 建立實際作品後，產生 `remotion-result.json`（範例見 `templates/remotion-result.example.json`）；再執行：

```bash
python3 scripts/remotion_plugin_bridge.py verify \
  --handoff /tmp/parkgo-remotion-handoff/remotion-handoff.json \
  --result /path/to/remotion-result.json \
  --project /path/to/video-project \
  --out /tmp/parkgo-remotion-verification.json
```

核對同一份分鏡 SHA、影片存在、檔案 SHA 及 ffprobe 片長；**驗證成功只代表可開始 QA，不代表插件已被成功調用或審美合格**。仲要進行 `motion_preflight.py` 及真正獨立雙 Agent 驗收。官方 Plugin 未可用時，可改安裝 `npx skills add remotion-dev/skills` 並經本地 Remotion CLI 製作，前提係執行環境許可。

詳見 `references/remotion-plugin-collaboration.md`（包括 Remotion Studio、WebMCP 的條件、分工及失敗處理）。

## v1.5：加入兩套可執行技術工作流

已分析 [howseen-ai/claude-motion-design](https://github.com/howseen-ai/claude-motion-design) 同 [whaleyxbt/claude-motion](https://github.com/whaleyxbt/claude-motion) 嘅公開 SKILL、渲染程式碼、審查同聲效系統。兩個專案 MIT，個別媒體授權及 Remotion 授權另外核對。**本 ZIP 唔打包上游原始碼或者音樂素材。**

- **Howseen 路線 `html-seek`**：以 `seek(t)` 驅動畫面，先做關鍵影格同草稿，確認真正配樂嘅 drop 後再做 shutter subframes、pops scan、最終編碼 QA。
- **Whaley 路線 `remotion`**：React UI/文字場景，`timeline.json` 統一分鏡同音效時序，節點 contact sheet、程序化 SFX、音量與 transients 審查。
- **Whaley 路線 `web-sim`**：適合 3D 內部穿越鏡頭、粒子或 agent/物理模擬；先預計算狀態，再按 `render(t)` 對任何時刻生成一致影格。

新增 Python 生產規劃工具（只寫交接檔，不自動執行來源 Repo）：

```bash
python3 scripts/production_router.py examples/parkgo/storyboard.json --engine auto --out /tmp/parkgo-v15-plan
# 輸出：shared-timeline.json、production-plan.json、PRODUCTION_HANDOFF.md
```

新增已編碼 MP4 技術預驗收（有 FFmpeg/ffprobe 才能執行）：

```bash
python3 scripts/motion_preflight.py /path/to/final.mp4 \
  --storyboard /path/to/storyboard.json --out /tmp/preflight.json
```

會檢查大小、FPS、片長、有冇音軌、第一影格是否近全黑，以及按原生 FPS（最高 60fps）抽查疑似單幀 flash/pop（對上分鏡切換點）。**Pop 只係嫌疑訊號，唔等於錯誤。** 結果畀製作 Agent 修正，再交原有兩個真正獨立嘅審美/整體 Juror（55/45）。冇實際渲染同獨立模型時，不可以聲稱完成驗收。

## Codex 安裝（原生格式）

本版本專門畀 **Codex App、Codex CLI、Codex IDE extension** 使用，包含 Codex `SKILL.md`、`agents/openai.yaml` 介面 metadata，同埋兩個真正獨立嘅 Codex 專用 `.toml` 子 Agent。

解壓後進入解壓所得的 Skill 資料夾執行（先預覽、再安裝）：

```bash
python3 scripts/install_codex.py --user
python3 scripts/install_codex.py --user --apply
# 從舊版（v1.4）覆蓋升級時，先確認目的地可安全替換：
python3 scripts/install_codex.py --user --apply --force
```

此指令將本 Skill 放入 `~/.agents/skills/unified-motion-director/`，兩位評審放入 `~/.codex/agents/`。如只想為單一專案使用：

```bash
python3 scripts/install_codex.py --project /path/to/project --apply
```

對應目錄係 `PROJECT/.agents/skills/unified-motion-director/` 同 `PROJECT/.codex/agents/`。如果目的地已存在，安裝器不會靜默覆蓋；有意更新先加 `--force`。安裝後可重啟 Codex / 重新整理 Skills。

安裝成功可喺 Codex 輸入 `$unified-motion-director`。例：「$unified-motion-director 幫我完成 15 秒產品動畫，渲染後派兩個獨立 Agent 做審美、整體評分同修正。」

## 外部專案可選安裝

```bash
python3 scripts/source_manager.py --status
python3 scripts/source_manager.py --plan
python3 scripts/source_manager.py --install   # 只在你自己同意、檢查後才執行
```

安裝指令只會複製公開第三方 Repo 至 `external/`，**不會代你執行其依賴安裝、build 或 shell script**。請先審閱並遵照第三方官方 README 安裝對應軟件。沒安裝外部專案時，本 Skill 仍可規劃導演、分鏡、QA 及產生一般程式碼。

## 常用指令

**A／導演模式：**「請用 unified-motion-director 幫我策劃一段 20 秒產品影片。先給三個創意方向、LOOK card、分鏡及配樂節奏，不要急著渲染。」

**B／一氣呵成模式：**「請用 unified-motion-director 依照已提供的品牌素材建立 15 秒 9:16 宣傳片；先整理劇本與分鏡，再按環境能力產生預覽、渲染及 QA 報告。所有未能真正執行的步驟必須註明。」

**C／作品批評模式：**「審閱我嘅 MP4 / storyboard，按照導演、審美、動態、節奏、輸出品質指出最重要 5 個修改，提供重新編排的時間線。」

## 分鏡資料格式

`templates/storyboard.schema.json` 定義每個鏡頭的時間、目的、UI／真實資料狀態、主體、鏡頭移動、轉場接合、聲音節拍及連續性。以下命令可驗證：

```bash
python3 scripts/validate_storyboard.py examples/parkgo/storyboard.json
python3 scripts/storyboard_board.py examples/parkgo/storyboard.json --output /tmp/storyboard.html
```

產生的 `storyboard.html` 是供人審視的分鏡板，**不是完成影片**。

## 參考來源

- https://github.com/PHY041/claude-motion-playbook — Playbook 233 案例／137 技法，文件與分類 CC BY 4.0；模板 CC0。
- https://github.com/abdullatif06/claude-motion-director — 以 HyperFrames 為實作引擎的導演／動畫渲染工作流（MIT）。
- https://github.com/designbysuren/motion-composer-skill — 商品廣告／敘事／動畫技術路由（MIT）。
- https://prompt-motion.com — 原創作品與提示詞由其個別創作者擁有，不包含在本 ZIP。

詳見 `ATTRIBUTION.md`。本檔案沒有聲稱與任何上游專案或 Anthropic 有正式合作關係。

## 利用現成 137 技法（不複製技術庫）

克隆 Playbook 後可直接搜尋上游的技法說明與實作線索：

```bash
python3 scripts/technique_lookup.py --query "shared element morph UI" --limit 5
python3 scripts/technique_lookup.py --query "字體 轉場 音樂"
```

搜尋器會註明上游來源，並讀取 `external/claude-motion-playbook/docs/techniques.md`。未下載上游內容時，會顯示缺失資訊及官方連結，不會假裝已搜尋。這可令現有 Playbook 持續作為實際技法資料源，而新 Skill 專注做統合導演。


## 繼承 v1.4：Codex 原生獨立子 Agent 驗收

保留 v1.3 雙評審權重：視覺審美 55% + 全片整體 45%；最終 ≥85 分、兩位各 ≥80、無阻擋項先 PASS。其餘依舊 REVISE / REWORK / BLOCKED / HOLD_EVIDENCE / NEEDS_ADJUDICATION。每次重新渲染都重新 SHA 同驗收，最多兩輪修改。

**首選：由 Codex 主對話真正 spawn 兩個自訂 subagent**：`motion-aesthetic-juror` 專注美學，`motion-holistic-juror` 專注敘事節奏及執行。兩者唔睇對方分數，審查已輸出 MP4 嘅真實影格；唔係導演模擬分身。兩份 JSON 分開交回主 Agent，主 Agent 寫入同一 review bundle，再進行程式驗收。

```bash
python3 scripts/review_gate.py prepare /path/to/final.mp4 \
  --out /path/to/review-v1 \
  --brief /path/to/BRIEF.md \
  --storyboard /path/to/storyboard.json \
  --audio-policy required --rights-status confirmed

# Codex 已開兩個獨立 subagent 並已分別寫好 JSON 時：
python3 scripts/review_gate.py aggregate --bundle /path/to/review-v1

# 另一種方式：若已安裝登入 Codex CLI，可啟動兩個獨立 Codex exec 會話：
python3 scripts/review_gate.py run \
  --bundle /path/to/review-v1 --project /path/to/project
```

後者係兩個獨立 CLI session，唔係 Codex App 入面 spawn 自訂 subagent；佢會將 contact sheet 同至少 8 張完整影格以 `--image` 直接傳畀各評審。**音訊只有 metadata 唔等於聽過音樂**：如未能審聽音訊，不能用假分數取代，驗收必須 HOLD_EVIDENCE。`--rights-status confirmed` 亦只係製作者經授權核對後嘅聲明。

如果冇真 MP4、冇影格存取能力或冇獨立 reviewer context，唔可以聲稱已評分。單元測試係合成樣本測試，唔代表真正審美評分。

完整規格：`references/independent-acceptance.md`、`templates/juror-report.schema.json`。Codex 官方文件：https://developers.openai.com/codex/skills 與 https://developers.openai.com/codex/multi-agent 。

## v1.2：加入 Hype-yolo 原始碼輔助製作

本版新增 `references/source-assisted-production.md`、`scripts/hype_motion_bridge.py`、`templates/ADAPTATION.md`。用戶不止要「Opus 感」，仲需要真正保留材質、輪廓、骨架同動態機制；呢套流程會先搜尋可以執行嘅源碼，再由導演統一畫面、改寫故事和實測渲染。

GitHub: https://github.com/Hype-yolo/claude-motion-skill （檢查到 0.4.0-beta.1；**唔包含**上游源碼／模型）

```bash
python3 scripts/source_manager.py --status
python3 scripts/hype_motion_bridge.py --status
python3 scripts/hype_motion_bridge.py --plan --storyboard examples/parkgo/storyboard.json
python3 scripts/hype_motion_bridge.py --handoff --storyboard examples/parkgo/storyboard.json --output /tmp/parkgo-handoff.json
```

`--plan` 只輸出需要先查閱嘅上游命令；`--handoff` 產生逐鏡選型、重用、改編及驗證清單，**不會自行下載或執行外部程式**。實際啟用 Hype-yolo 渲染器前，要獨立安裝 Node.js 22+、FFmpeg/ffprobe、Playwright 等依賴、核對第三方模型許可，並參照其官方文件。其發佈測試主要在 macOS；Windows/Linux 未有對等實機驗證。

## v1.1：加入兩大 Opus 5.5 公開作品集研究

本版加入：

- `references/opus-gallery-learning.md`：整合 Prompt Motion 與 Skillry 公開案例嘅創作思路，分類構圖／連續變形／攝影機／節奏／技術／審查。
- `references/opus-casebook.md`：有明確來源鏈接的研究案例索引，將「Prompt 所要求嘅效果」與「真正看過影片觀察到嘅效果」分開。
- `templates/REFERENCE_REVIEW.md`：原片與 Skillry remake 嘅逐鏡比較表及證據級別。
- `scripts/video_reference_sheet.py`：如果你提供獲授權嘅原片 MP4，抽取影格、產生有時間碼嘅圖片 contact sheet，支援逐段實際分析。

**重要限制：** 2026-10-17 網頁檢索可讀到公開 Prompt、作品 metadata 同部分 poster，但**無法直接播放兩站全部影片並逐幀觀察**。所以研究檔案僅對公開文字提出技法推導；唔會冒稱完成影片審美評分。若提供下載到本地的影片，先可以做真實視覺 QA；要驗證音樂同畫面同步，更需要音訊。

```bash
python3 scripts/video_reference_sheet.py /path/to/legally-obtained-video.mp4 --out reference-review
```
