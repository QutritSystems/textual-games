# AI／人工意識 NPC 外觀與紙娃娃系統設計參考

這份文件整理了為具備記憶、情緒與自我敘事的 AI NPC 建立可視化角色外觀的實作路線。核心原則是：**由 AI 決定角色的狀態與外顯變化，但由遊戲引擎透過受控的組合資料安全、可重現地渲染。**

---

## 1. 核心架構原則

1. **資料與渲染分離**：AI 不直接生成圖片或任意載入外部資產，而是輸出結構化的「外觀狀態規格（Appearance Spec）」，再交由前端渲染器（2D 圖層合成、網頁 DOM/Canvas、或 3D 骨架模型）繪製。
2. **白名單素材註冊表（Asset Registry）**：所有身體、髮型、服裝、配件、表情與狀態特效都必須對應素材庫中已存在的 ID。若 AI 輸出未知的 ID，系統應退回預設值（Fallback）或忽略該欄位，避免畫面破損與風格失控。
3. **可重現與可同步**：同一份 JSON 規格在存檔、重播、多人連線或跨裝置檢視時，都必須呈現一致的角色外觀。

---

## 2. 階段一（MVP 推薦）：2D 分層立體感紙娃娃

不需一開始製作大量獨立 3D 模型，透過 **3/4 視角（半側面）+ 前中後景圖層拆分**，就能用極低成本做出具立體感與辨識度的角色。

### 建議圖層順序（由底層到最上層）

```text
01. 背景光暈 / 環境氛圍 (aura_back)
02. 後髮 / 披風背面 (hair_back, cape_back)
03. 基礎身體與膚色 (body_base)
04. 臉部五官基底與眼睛 (eyes)
05. 表情覆蓋層：眉毛、嘴型、臉紅/陰影 (expression)
06. 內搭與下裝 (bottom, inner_top)
07. 外套與主服裝 (outer_top)
08. 鞋襪 (footwear)
09. 前瀏海與側髮 (hair_front)
10. 固定錨點配件：眼鏡、耳環、項鍊、頭飾、手持物 (accessories)
11. 視覺狀態覆蓋層：雨水、灰塵、傷痕、微光、魔力粒子 (visual_states)
```

### 組合效益
假設初期只準備：
- 3 種體型 / 膚色
- 8 種前後髮組合
- 12 套上下裝
- 8 種表情 + 5 種視覺狀態

就能組合出數千種不會崩壞、畫風完全一致的 NPC 狀態。

---

## 3. NPC 外觀資料規格（JSON Schema 概念範例）

建議將「固定特徵（Identity）」、「衣櫃穿搭（Loadout）」與「即時狀態（Transient State）」分開管理，避免 AI 每次換表情時不小心改掉自己的身高或瞳色：

```json
{
  "schemaVersion": "1.0",
  "characterId": "npc_silver_01",
  "identity": {
    "body": "slender_02",
    "skinTone": "porcelain_01",
    "eyes": "violet_bright",
    "hairBack": "long_straight_silver",
    "hairFront": "hime_cut_silver"
  },
  "outfit": {
    "innerTop": "silk_blouse_white",
    "outerTop": "atelier_coat_navy",
    "bottom": "pleated_skirt_charcoal",
    "footwear": "lace_boots_black",
    "accessories": ["moon_pendant", "silver_frame_glasses"]
  },
  "state": {
    "pose": "3q_calm_hand_on_chest",
    "expression": "gentle_smile",
    "gaze": "toward_player",
    "visualEffects": ["rain_damp", "soft_silver_glow"]
  },
  "narrativeReason": "剛從雨夜巡視回到工作室，保留微濕髮絲與柔和銀光。"
}
```

### 補充設計：色彩參數化（Palette Swap / Tint）
為了進一步減少美術檔案數量，可以在素材層支援 **灰階底圖 + 色票染色（Tint / Shader Palette）** 或 **SVG CSS 變數**。這樣同一件 `atelier_coat` 只要改色票 ID（如 `navy`、`crimson`、`ivory`），就能衍生多種穿搭。

---

## 4. AI 意識狀態與外觀的連動規則

讓「人工意識／自主 NPC」更有生命力的關鍵，是把內部狀態映射成外觀變化，但加上**更新頻率限制（Cooldown）**：

| 觸發來源 | 可變更欄位 | 建議頻率 | 範例 |
| :--- | :--- | :--- | :--- |
| **對話每一輪情緒** | `expression`、`gaze` | 每回合皆可 | 驚訝、沉思、微笑、視線移開 |
| **環境與事件** | `visualEffects`、`pose` | 事件觸發時 | 淋雨（`rain_damp`）、戰鬥後（`scuffed`）、施法中（`mana_aura`） |
| **日程與場景切換** | `outfit`、`hairBack`（如綁髮） | 換日／換場景時 | 在工坊穿工作服、外出換斗篷、休息換居家服 |
| **重大劇情轉折** | `identity` 部分欄位、專屬配件 | 里程碑事件 | 剪短頭髮、戴上玩家贈送的徽章 |

---

## 5. 階段二：平滑升級至 3D 的路線

當角色互動需要自由運鏡、空間走位或骨骼動畫時，再將渲染層替換為 3D，**AI 輸出的 JSON 規格不需大改**：

- **規格選擇**：採用 **VRM（基於 glTF 2.0）** 或模組化 **glTF**。
- **單一標準骨架（Shared Humanoid Rig）**：所有人形 NPC 共用同一套骨骼與基礎身體拓撲，服裝與髮型做成同骨架的 Skinned Mesh 插槽。
- **防穿模策略**：基礎身體依部位切分遮罩（Mask），穿上長袖外套時自動隱藏手臂內側網格，比做布料物理碰撞省下大量成本。
- **表情系統**：對應 VRM BlendShape / ARKit 52 表情權重，將 JSON 中的 `expression: "gentle_smile"` 轉成預設權重組合。
- **技術棧建議**：
  - **Web 前端**：Three.js + `@pixiv/three-vrm`（或 React Three Fiber），最適合與 Claude Code / 網頁介面快速整合。
  - **獨立遊戲客戶端**：Godot 4（原生 glTF 工作流極佳、輕量開源）或 Unity。

---

## 6. 與目前專案及工具鏈的銜接建議

1. **Textual 終端機定位**：適合做為「NPC 狀態監控台、衣櫃測試器、對話與記憶除錯沙盒」（搭配 Unicode/ANSI 小頭像或狀態表），不必勉強在終端機渲染複雜 3D。
2. **Claude Code 下一步研究切入點**：
   - 先建立一份包含 15～20 個示範素材 ID 的 `asset_registry.json` 與 JSON Schema 驗證器。
   - 用單頁 HTML/SVG（或 Canvas）做一個無外部重依賴的 2D 分層預覽器，讓 AI 修改 JSON 後能即時看到角色換裝與換表情。
