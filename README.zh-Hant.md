# Unified Motion Director

**為 Codex 設計的統一動態影像導演 Skill。** 從創意、視覺風格、分鏡與時間線，到程式動畫、影片渲染與雙獨立評審，提供一套具備可追溯驗收結果的製作流程。

<p align="center"><img src="./assets/readme/workflow.svg" width="100%" alt="Unified Motion Director 流程：導演及分鏡、Remotion 製作、輸出驗證、兩名獨立評審。"></p>

[English](README.md) · [Skill 指示](SKILL.md) · [分鏡示例](examples/parkgo/storyboard.json) · [來源及授權](ATTRIBUTION.md)

## 主要功能

整套系統以一份**共用時間線**為中心，避免導演分鏡、Remotion 動畫與音效各自使用不同時間碼。

| 階段 | 功能 |
| --- | --- |
| 創意導演 | 整理需求、敘事主軸、審美方向及鏡頭語言 |
| 分鏡設計 | 產生結構化 `storyboard.json`、鏡頭交接與時間線 |
| 動畫製作 | 按需求選擇 Remotion、HTML `seek(t)` 或 Three.js 模擬 |
| 技術檢查 | 解碼影片、檢查時間線、異常影格及檔案校驗碼 |
| 獨立評審 | 審美及整體完成度由兩個分開上下文的子 Agent 評估 |
| 驗收 | 未達標時提出具體修正；無足夠證據不會宣稱完成 |

**本專案重視實際成果，而不是只生成一份華麗 Prompt。** 可重現的畫面、真實素材、明確聲畫節奏及可查核的評分，都是交付標準的一部分。

## 安裝

需要 **Python 3.11 或以上**。下載或複製本 Repository，於根目錄執行：

```bash
python3 scripts/install_codex.py --user --apply
```

此指令安裝 Skill 到 `~/.agents/skills/unified-motion-director/`，並在 `~/.codex/agents/` 加入審美及整體評審 Agent。僅安裝至某個專案亦可：

```bash
python3 scripts/install_codex.py --project /path/to/project --apply
```

不加 `--apply` 只預覽變更；已有安裝時，必須明確使用 `--force` 才會覆蓋。

Remotion Plugin 是**選用的獨立安裝項目**：[官方 Plugin](https://chatgpt.com/plugins/remotion)。沒有 Plugin，亦可使用本地 Remotion CLI，或選擇 HTML/Three.js 路線；Skill 不會假裝已調用外部 Plugin。

## 首次使用

在 Codex 內輸入：

```text
$unified-motion-director

為我的 App 製作 15 秒產品動畫，採用簡潔、留白充分的設計。
先完成創意導演、分鏡及共用時間線，再交 Remotion 實作。
渲染後執行技術檢查，啟動兩個互不參與製作的子 Agent，
分別評審審美與整體品質。若未達 85 分，修正並重新驗收。
不可將概念分鏡或未確認的輸出當成已完成影片。
```

## Remotion 交接

Skill 會建立版本固定的時間線和交接資料：

```bash
python3 scripts/remotion_plugin_bridge.py prepare \
  examples/parkgo/storyboard.json \
  --out /tmp/parkgo-remotion-handoff
```

輸出 `remotion-handoff.json`、`shared-timeline.json` 和 `REMOTION_PLUGIN_TASK.md`。完成真正影片輸出後，使用 `scripts/remotion_plugin_bridge.py verify` 核對實際檔案、影片時長、分鏡版本及 SHA-256。驗證成功**只代表可以進入正式品質審查**，並不代表 Plugin 已實際運行或影片審美合格。完整命令見 [英文 README](README.md#shared-timeline--remotion-handoff)。

## 獨立驗收

評分採 **審美 55% + 整體 45%**；總分至少 **85/100**，兩位評審各至少 **80/100**，沒有重大問題及證據缺漏方可通過。評審必須檢查與最終檔案雜湊值一致的實際輸出，不能自行編造分數。參閱 [獨立驗收規格](references/independent-acceptance.md)。

## 示例及限制

專案附有 **ParkGo 15 秒產品影片規劃示例**：[導演 Brief](examples/parkgo/BRIEF.md)、[設計方向](examples/parkgo/LOOK.md)、[分鏡 JSON](examples/parkgo/storyboard.json)、[HTML 分鏡板](examples/parkgo/storyboard-board.html)、[Remotion 交接](examples/parkgo/remotion-handoff/REMOTION_PLUGIN_TASK.md)。**這是規劃素材，不代表已完成 MP4 影片。**

已進行 **25 項本地測試**，包括合成影片及技術合約驗證；尚未以本專案實際完成跨 Plugin 的影片製作及真實 Codex 子 Agent 審美評分。第三方原始碼、音樂、影片、字體與授權須分別處理。這套 Skill 不等同取得 Opus 5.5 未公開的思考或模型權重。

## 開發與授權

```bash
python3 -m unittest discover -s tests -v
```

部分測試需 `ffmpeg`／`ffprobe`，缺少時會略過相關個案。原創整合程式依 [MIT](LICENSE) 授權。上游引用、作者及各項授權邊界見 [ATTRIBUTION.md](ATTRIBUTION.md)，版本更新見 [CHANGELOG.md](CHANGELOG.md)。
