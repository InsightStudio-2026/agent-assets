---
name: business-model-audit
description: 商业模式生死审计；对项目 idea / APP 计划 / 母本进行红队尸检、付费验证、替代方案拷问、工程 ROI 裁剪，并输出 Pivot / Kill / Proceed 路由
argument-hint: "要审计什么项目或商业模式？"
disable-model-invocation: true
---


# /business-model-audit · 商业模式审计

**定位**：在投入工程资源前，对项目 idea、APP 设计、商业计划或母本进行商业生死审计。目标不是鼓励，而是把商业判断变成可验证假设、MVP 裁剪和下游路线。

**边界**：只做商业与工程 ROI 审计、验证计划和路线建议；不写业务代码，不替代 `/project-inception` 生成母本，不替代 `/specs-write` 写 feature spec，不静默修改 Authoritative SSOT。

**斜杠命令**：`/business-model-audit`

**上游 workflow**：`/project-steward`、`/project-inception`、`/grill-with-docs`。

**下游能力**：workflow：`/project-inception`、`/specs-write`、`/architecture-audit`、`/grill-with-docs`；skill：`prototype`。

**别名声明**：

- `<crt>` = `./competitor-research-template.md`
- `<drp>` = `./deep-research-prompt-template.md`
- `<bmar>` = `./report-template.md`
- `<imm>` = `./industry-manual.md`

---

## 懒加载契约

- **MUST read**:
  - `./decision-matrix.md`
  - `./competitor-research-template.md`
  - `./deep-research-prompt-template.md`
  - `./report-template.md`
  - `./industry-manual.md`
- 开始判定或执行 Phase 流程前，必须完整懒加载上述细节。

---

## 1. 阶段 1 — 证据收集

### 1.1 输入形态

用户可能提供：

- APP 设计或商业计划。
- 母本 / L1 SSOT。
- `/project-inception` 草案。
- 竞品、目标用户、定价想法。
- 技术路线或原型说明。
- 一句话模糊 idea。

### 1.2 最小澄清与高压盘问 (Grill-Me)

最多一次提出 3 个问题。优先列默认假设，不把问卷倒给用户。

优先级：

1. 谁是付费主体 (Buyer)，不只是使用者 (User)？
2. 用户现在用什么替代方案解决？（刚需痛点 vs 可有可无的痒点？）
3. 为什么是现在 (Why Now)？（环境、政策或技术发生了什么变化让此事变得可能？）
4. 能力圈与股权死局拷问：团队是否掌握了垄断资源？内部是否有绝对的一票否决权控制人（拒绝均分股权）以及离职退股机制？
5. 故事股排雷 (Story Stock Detection)：如果去掉所有宏大叙事热词，最基础的那笔单客交易是否能产生正现金流？
6. 如果 14 天内只能验证一个风险，最怕哪个假设是假的？

**强制挂载纪律**：如果用户对上述核心逻辑（特别是付费主体、控制权、护城河和核心差异化）语焉不详或给出含糊假设，**不要单方面放水推演，必须强制挂载 `grill-me` 引擎对用户进行高压追问**，直到榨干商业事实。

### 1.3 证据账本

输出：

```markdown
## 证据账本 (Evidence Ledger)
|  | 论断声明 (Claim) | 事实来源 (Source) | 证据类型 (Evidence Class) | 置信度 (Confidence) | 证伪商业风险 (Risk if false) |  |
|  | ------- | -------- | ---------------- | ------------ | --------------- |  |
|  | [Claim 声明] | user / file / inference | Observed / User-claimed / Inferred / Unknown | High / Medium / Low | [证伪时的商业风险说明] |  |
```

---

## 2. 阶段 2 — 红队事前尸检

假设一年后项目彻底失败，直接写尸检报告。

### 2.1 致命死因库 (Pre-mortem Library)

必须从以下类别挑出最可能致死的 3 支冷箭：

- **伪需求 / 低频陷阱**：用户说想要但没预算；或问题虽在，但发生频率极低，撑不起习惯、留存或付费。
- **替代方案碾压**：Excel、Notion、GPT 或廉价人工服务已足够，无切换动力。
- **大模型降维打击 (LLM Collateral Damage)**：所谓的“技术壁垒”或“内容护城河”，在下一个版本的通用大模型面前被顺手免费解决。
- **渠道寄生与 CAC 吞噬**：高度依赖单一平台（如仅靠 TikTok 买量 / App Store 推荐），或获客成本 (CAC) 随规模指数级上升，吞噬所有毛利。
- **卡在死亡谷 (Stuck in the middle)**：体验不如高价定制服务，价格又拼不过免费白嫖工具，上下不靠。
- **创始人契合度错位 (Poor Founder-Market Fit)**：团队既无该垂直行业的老钱人脉，又无技术代差优势，为什么是你们做？
- **资本市场反身性致死 (Reflexivity Death)**：如果是极度依赖外部输血、高杠杆或烧钱换规模的模式，一旦市场预期走弱导致融资失败，负面评价将直接导致业务实质性破产。
- **合规、信任与供应链崩盘**：用户不敢把关键数据交给新产品，或者核心组件/政策环境遭遇一剑封喉的监管收紧与断供。
- **金税四期税务暴雷**：模式的所谓“高毛利”建立在灰产、两套账或不合规避税上，在数据控税下面临毁灭性打击。
- **控制权僵局与过早大公司病**：创始人股权均分导致无法决策，或在未达 PMF 时设立复杂组织架构（PMO/公关/战略部）生生把现金流耗干。

### 2.2 输出

```markdown
## Red Team Pre-mortem
### Death Cause 1: <name>

- Why it kills:
- Evidence class:
- Current warning signs:
- What would disprove this concern:

### Death Cause 2: [死因 2]
### Death Cause 3: [死因 3]
```

---

## 2.3 商业模式原型与行业红旗 (Archetype Mapping)

基于收集到的证据，强制为项目分配主基因型，并挂载专属红旗警告。
**强制依赖**：如果被审计的项目属于具体的行业领域，代理必须查阅并引用 `<imm>` (`industry-manual.md`) 中的特定行业定量指标体系与致命红旗，结合以下大类原型进行深度映射：

- **科技互联网原型**：强考核网络效应、转换成本、LTV/CAC。
  - *专属红旗*：流量变现路径（货币化率）不清晰，或 LTV < CAC 亏本获客。
- **大消费与品牌原型**：强考核提价权、渠道压制力、高频复购。
  - *专属红旗*：无法产生品牌溢价（陷入价格战），或存货周转极慢。
- **医疗/硬科技原型**：强考核研发护城河、专利长效期、监管敏感度。
  - *专属红旗*：单一政策（如集采）可致利润归零，或研发成功率犹如抛硬币。
- **金融/重资产原型**：强考核杠杆率、系统性风险、资产质量（不良率）。
  - *专属红旗*：风险定价失控，或极度依赖外部资本输血。

**核心防伪与陷阱审计**：

1. **服务型企业/人员主导型陷阱**：审计公司是否以“人”而非“机构品牌/技术特许”为核心？如果是松散外包、顾问咨询或人员主导的服务型企业，核心高价值人才一旦流失即可带走高端客户，且企业大部分利润将被员工以高薪酬索取，股东几乎无法获得持续回报（如所罗门兄弟投行陷阱）。
2. **虚假护城河辨识**：绝对不要将“优质产品”、“高市场份额”、“卓越管理”误认为护城河。必须自证是否存在以下四大结构性护城河来源之一，否则一律判定为“无护城河”：
   - *无形资产*：拥有具备真实定价权（敢提价且客户不走）的品牌、多项发明专利组合（而非单一专利）、或多层地方/国家监管许可。
   - *转换成本*：工作流、数据或硬件深度嵌入客户流程，客户切换到对手的成本和风险极高。
   - *网络效应*：用户越多产品越有价值，且属于封闭网络，多一个用户可使其他用户价值非线性增长。
   - *成本优势*：拥有地理垄断、独特资源垄断或明显的固定成本分摊规模效应。

---

## 3. 阶段 3 — 受众、替代方案与转换成本审计

### 3.1 用户分层

区分：

- User：实际使用者。
- Buyer：付费或预算决策者。
- Champion：内部推动者。
- Blocker / 利益受损者：谁会在内部或外部强烈抵制你的产品（如 IT 部门、合规部门、传统渠道商）？如果你不知道你的敌人是谁，你就无法落地。
- Beneficiary：最终收益者。

### 3.2 替代方案与宏观生态位拷问

必须冷血回答：

- **巨头碾压定律**：为什么大厂（Google/字节/巨头竞品）不能在一个周末顺手把这个功能加进去？如果不做，是因为他们看不上（利基市场）还是技术做不到？
- **能力圈与非对称信息差审计 (Circle of Competence & Informational Edge)**：团队对痛点的理解是来源于一线真实操盘经验、独家行业资源，还是仅仅来自市调报告与大模型脑暴？如果只是后者，则毫无能力圈优势。
- **死亡谷陷阱**：本产品是否处于“Stuck in the middle”？（即：不如免费工具便宜，又不如高价私教/定制有效）。
- 这是止痛药（Must do）还是维生素（Nice to have）？用户今天不用本产品时怎么做？哪一点真的痛（会遭受实质性损失），而不只是“不优雅”？
- **企业消失测试 (Disappearance Test)**：如果你的企业明天突然消失，你的客户是否会因此面临业务瘫痪或遭受重创？如果客户能轻松找到替代方案而无明显痛感，说明护城河极浅。
- **客户依赖度三级连续谱定位**：将产品在客户心智中的地位进行冷血归类：
  - *刚需（不可延迟）*：没有就无法生活或运营，在衰退中也绝不能被砍掉。
  - *半刚需（可短期延迟）*：短期内可以忍受，但中长期必须解决（如车辆保养）。
  - *可选（可无限推迟）*：稍微遇到困难第一个被砍掉。注意：即使是可选产品，也必须验证目标客户群（如高净值人群）的消费刚性是否足以形成防守壁垒。
- 时机红利何在 (Why now)？为什么之前没有人解决这个问题？现在发生了什么变化让此事变得可行？
- 用户为什么会**现在**换，而不是继续忍？新产品引入的迁移、信任和协作成本是什么？
- 10 倍改进在哪里？若没有 10 倍，凭什么切入？

### 3.3 潜在竞争对手与穿透式调研 (Competitor Deep-Dive)

- **竞品罗列与穿透**：必须明确列出所有直接、间接的竞争对手或现有替代方案。审计不能基于想象，必须基于客观的市场事实。
- **“一企一档”底线约束**：对于每一个被列出的关键竞品/替代方案，都必须提供至少一份符合 `<crt>` 模板的《竞品调查报告》。若无竞品报告，则自检不通过，无法推进至 Spec。
- **代理自主调研机制（如无报告）**：
  - 如果用户未能提供竞品调查报告，IDE 代理应主动启动互联网探索，使用 `search_web` 和 `read_url_content` 等检索工具，直接调查竞品的官网、论坛反馈、第三方评测和公开商业数据，并根据 `<crt>` 模板自动生成竞品报告。
  - 对于极其复杂或受限于公开数据难以直接抓取的竞品，代理必须在自检中指出，并根据 `<drp>` 模板为用户生成专门面向 **Gemini Deep Research**的高精度调查提示词（调查提示词模板）。

### 3.4 输出

```markdown
## Audience / Alternative / Switching Audit

- Primary user:
- Buyer:
- Current alternatives / Competitors: [列出所有已识别的竞品与替代方案]
- Competitor Research Reports: [对每个竞品，必须提供对应的 <crt> 报告链接或嵌入内容；若使用 Gemini Deep Research 提示词，在此列出生成的提示词内容]
- Pain frequency:
- Pain intensity (Painkiller or Vitamin):
- Timing (Why now):
- Switching costs:
- 10x wedge or narrow beachhead:
- Macro niche defense (巨头防守空间):
- Verdict:

```

---

## 4. 阶段 4 — 单位经济模型、分发与护城河审计

### 4.1 商业闭环与单位经济模型 (Unit Economics)

强制算账（不谈数字的商业模式都是耍流氓）：

-**付费触发点与定价锚点**：用户在哪个时刻愿意掏钱？他们拿什么替代成本或收益与你的价格做比较？

- **金税四期完全合规压力测试**：在必须依法缴纳增值税、企业所得税(25%)、个税及附加税的底线之上，你的 LTV 和毛利是否依然能够打平 CAC 并盈利？（拒绝任何依赖“买卖发票/两套账”的财务模型）。
- **真实定价权与抗通胀测试**：如果你把价格提高 20%，你的客户是否会立刻流失到竞争对手那里？（如果会，说明你只有规模优势，毫无品牌/特许权壁垒）。
- **ToB 账期与现金循环危机 (Accounts Receivable Risk)**：如果客户是国企或大 B 端，虽然单子大不违约，但账期可能长达半年到一年以上。这种垫资做生意的模式，现金循环周期 (CCC) 能否撑住不破产？
- **人才垄断与防拆伙成本**：要想实现你的技术护城河或销售突破，必须要有与大厂抗衡的高薪预算（人才垄断）或防止核心团队单飞的股权红利代价。这笔隐性且巨大的成本是否已计入你的获客或研发固定成本中？
- **微观获客路径与 CAC 警戒线**：用户如何经历“知道、信任、试用、购买”的完整路径？生命周期价值 (LTV) 是否显著大于获客成本 (CAC) 的 3 倍？若 LTV 极低，是否有近零成本的自然增长渠道？
- **商业逻辑的安全边际测试**：如果获客成本翻倍或用户留存率减半，公司能否存活？如果主营业务失败，是否有残存的无形资产、IP 或清算价值（烟蒂股托底）？
- **增量利润转化率 (Incremental Profit Conversion Rate) 与维持性资本开支 (Maintenance CapEx) 审计**：
  - *增量转化率*：当企业营收增长 30% 时，利润能同步增长多少？是依靠固定成本分摊、利润暴增，还是需要等比例雇人、买流量，导致利润率毫无改善甚至恶化？
  - *维持性开支占比*：在企业的总资本开支 (CapEx) 中，有多少是为了“维持现状、防止客户流失和技术过时”而必须花的维持性资本开支？高折旧、高设备更新依赖的企业通常是毁灭价值的资本吞金兽。
- **核心业务放缓时的跨界并购/扩张动机**：管理层推出新产品或跨界收购的动机是什么？是否因为核心业务增长放缓，面临业绩焦虑而强行扩张？不相关的跨界收购（如麦当劳当年的非主业并购、全食超市收购维生素企业）往往因为缺乏核心护城河基因而导致极高的资产整合失败率 (Diworsification)。
- **经济商誉 vs 资本吞金兽**：增长是否依赖与之匹配的庞大资本开支 (CAPEX)？（高增长若需大量烧钱，实为毁灭价值）。
- **自由现金流效率与首单时间差 (Energy ROI & Time-to-First-Dollar)**：对于非 VC 驱动的项目，能否在 30 天内不靠买量、不靠融资榨出首笔收入或等价置换？
- **边际成本演进与边际架构成本 (Marginal Architecture Cost)**：随着用户达到 10 万，交付边际成本是趋于零（如单机/本地 All-in-One 架构的云端零成本优势），还是线性暴增（算力/客服/人力）？
- **扩张与留存驱动**：如何从单点使用扩大到企业座席/更多模块？为什么下个月还用？

### 4.2 护城河与网络效应测绘

只接受具体机制，拒绝“我们更用心”、“UI更好看”等空词。

可成立的顶级护城河候选：

- **单边/双边/多边网络效应**：是单边（如微信，用户越多越有价值）、双边（如淘宝，买卖方互相吸引）还是多边生态？多一个用户，对其他用户的价值是否成指数增加？
- **高转换成本 (Switching Costs)**：工作流深度嵌入、历史沉淀数据让用户走不掉。
- **独有数据飞轮**：真实闭环数据持续反哺模型，拉开与调用通用 API 者的体验代差。
- **无形资产的脆弱性与品牌门槛**：品牌或合规能否带来真正的定价权？警告：基于纯粹“消费者品味”或“口碑”的无形资产极度脆弱，一旦偏好改变可能瞬间清零且无实物资产保底。
- **工作流内生锁死 (Workflow Integration Lock-in)**：将本地数据库、IPC 通信与文件管理完美缝合，创造超越传统松散工具链 10 倍的单机操作效率，使用户数据和习惯被深度生态锁死。
- **极度垄断的分发渠道 / 牌照门槛**。
- **结构性的绝对成本优势**。

### 4.3 输出

```markdown
## 商业模式、分发渠道与护城河审计 (Revenue / Distribution / Moat Audit)

- 付费与商业化模式 (Monetization model):
- 单位经济学 - LTV vs CAC 设想 (Unit economics - LTV vs CAC hypothesis):
- 边际成本走向 (Marginal cost trajectory):
- 分发与触达设想 (Distribution hypothesis):
- 用户留存与自增长闭环 (Retention & Expansion loop):
- 护城河/网络效应候选机制 (Moat / Network effects candidate):
- 护城河阻力衰退半衰期 - 面对 LLM 进化 (Moat Decay Half-life - under LLM evolution):
- 审计结论 (Verdict):

```

---

## 4.5 阶段 4.5 — 公司治理、资本属性与退出路径审计

商业逻辑的成立不代表公司载体的安全。

- **股权与控制权底线**：团队是否有一名具备一票否决权（如 67% 或华为式 0.75% 绝对控制）的实际控制人？是否存在离职退股 (Vesting) 机制？（均分股权=死局）。
- **资本属性错位拷问**：
  - 如果项目是一门“稳健现金流/分红型生意”，直接切断 VC 风投路线，改走内生增长或债权。
  - 如果项目要融 VC 的钱（遵循“慕投管退”规律），你必须回答：10 倍回报的退出路径（IPO 或被巨头并购）在哪里？

### 4.5 输出

```markdown
## 公司治理与资本属性审计 (Governance & Capital Audit)

- 实际控制人与一票否决权 (Actual Controller - Yes/No & Veto power):
- 股权解锁与回购机制 (Vesting & Clawback mechanism - Yes/No):
- 资本属性分类 (Capital Nature - VC/Lifestyle/Debt):
- 退出路径 (Exit Path - IPO/M&A/Dividend):
- 审计结论 (Verdict):

```

---

## 5. 阶段 5 — 工程 ROI 与 MVP 裁剪

### 5.1 技术 ROI 审判

**核心理念**：节约是最好的盈利。不验证核心商业假设的过度架构或技术自嗨，都是在吞噬项目的生命线（Runway）。此外，需执行**架构摩擦力 (Structural Friction) 与安全边际审计**：凡是需要动到核心通信层、污染主 DB Schema、带来巨量维护债务的功能，在 MVP 验证期一律强制降级为纯手工向导 (Concierge) 或临时外挂 JSON，严禁为了“漂亮”而破坏主架构的纯净度。

逐项检查主要技术选择、平台选择、架构复杂度和自动化范围。

每项必须归类：

| Class | 含义 | 处理 |
| ------- | ------ | ------ |
| Revenue-critical | 直接影响付费、信任、转化或留存 | 保留 |
| Validation-critical | 没它无法验证关键假设 | 保留但限时 |
| Efficiency-critical | 显著降低交付或运营成本 | 需量化 |
| Nice-to-have | 有价值但不影响当前验证 | 延后 |
| Vanity Engineering | 技术美感大于商业收益 | 砍掉 |

### 5.2 MVP 截肢清单

必须输出：

```markdown
## MVP 裁剪与截肢清单 (MVP Amputation List)

> **战略即取舍**：强制要求用户写下“我们绝对不做哪类客户/哪个功能”。没有舍弃的战略不是战略。

### 保留 — 核心 20% 动作 (Keep — Core 20%)

- <功能 / 技术选择 (feature / tech choice)> — 商业决策理由 (because <business reason>)

### 立即砍掉 — 虚荣性、早熟或试图讨好所有人 (Cut Now — Vanity, premature, or "Try to please everyone")

- <功能 / 技术选择 (feature / tech choice)> — 削减理由 (because <why it burns runway or dilutes focus>)
- <组织架构臃肿 (organizational bloat)> — 强制组织扁平化，砍掉 MVP 阶段不需要的非产研、非销售部门（如 PMO、战略、公关），禁止大公司病。

### 延后 — 有价值但非现在必需 (Defer — Useful but not now)

- <功能 / 技术选择 (feature / tech choice)> — 重新评估触发条件 (revisit when <trigger>)

### 简化 — 寻求平替 (Simplify)

- 替代方案：将 <复杂做法 (complex approach)> 替换为 <极简做法 (simpler approach)> 直至触发 <验证阈值 (validation threshold)>

```

---

## 6. 阶段 6 — 关键假设与验证计划

### 6.1 关键假设

提取 3-7 条最可能推翻项目的假设。每条必须可证伪。

```markdown
## 关键设想与可证伪假设 (Critical Assumptions)

- CA-001: <具体假设 (assumption)>
  - 证伪条件 (Breaks if):
  - 最低所需证据 (Minimum evidence required):
  - 验证方法 (Validation method):
  - 时间盒限定 (Time box):
  - 资金/成本上限 (Cost limit):
  - 假设为真时的行动 (If true):
  - 假设为假时的行动 (If false):

```

### 6.2 验证方式优先级

优先低成本证据，不急着写产品：

1. 真实用户访谈，但必须问过去行为和现有支出，不问“你会不会用”。
2. 手工 concierge / spreadsheet prototype。
3. Landing page / waitlist / mock checkout。
4. 可点击原型。
5. 单路径技术 prototype。
6. 付费试点或 LOI。
7. 才是完整 MVP。

### 6.3 禁止伪验证

- **严禁虚构的 3 年财务预测**：拒绝任何基于拍脑袋的 Hockey-stick 增长率和转化率预测。必须回归到“完成一次真实交付”的底线成本核算。
- **Skin in the Game（风险共担）红线**：如果不交出核心生产数据（如账本、私密文本）、未签联调备忘录或支付意向金，用户的口头称赞就是伪需求。未拿到“高代价”数据或承诺的验证实验只能判定为 `Low Confidence`。
- 不把“朋友说不错”当验证。
- 不把问卷意向当付费证据。
- 不把下载、点赞、收藏当留存或付费证据。
- 不把技术 demo 跑通当商业成立。

---

## 7. 阶段 7 — 审判结论与路由

### 7.1 评分

给 1-10 分，并拆分：

```markdown
## 细分维度评分 (Score)

- 需求真实性与痛点强度 (Problem intensity): /10
- 受众可触达性 (Audience reachability): /10
- 付费意愿与能力 (Willingness to pay): /10
- 行业时机与创始人契合度 (Timing & Founder-Market Fit): /10
- 差异化与壁垒 (Differentiation): /10
- 分发可行性 (Distribution feasibility): /10
- 工程 ROI (Engineering ROI): /10
- 公司治理与财税合规 (Governance & Tax compliance): /10
- 综合总分 (Overall): /10 (*注：若能力圈与非对称信息差审计未通过，此处强制扣除 3 分*)

```

### 7.2 裁定

只能选一个主裁定：

| Verdict | 含义 | 默认路线 | HG-*绑定 |
| --------- | ------ | ---------- | ---------- |
| Kill | 商业或用户假设太弱，不值得继续投入 | 停止；如已有母本，建议记录放弃原因 | `S-HG-1 GATE_NOT_REQUIRED`（决策性 Kill、不触发 spec gate） |
| Pivot | 核心方向需改，不能按原计划推进 | `/project-inception` 修订母本或重建立项 | `HG-STRAT-{slug}-pivot`（母本级 strategic pivot）；packet F-HG-1~8 必齐；R-INH-1 继承 Gate A |
| Validate First | 方向可能成立，但关键假设未验证 | `prototype` skill、用户访谈或 concierge 验证 | `HG-STRAT-{slug}-validate` + 如需真实动作 → `HG-IRREV-*` packet |
| Amputate then Proceed | 保留核心 20%，砍掉冗余后再推进 | `/project-inception` 修订 MVP 后再 `/specs-write` | `HG-STRAT-{slug}-amputate`（MVP 边界重定）+ `HG-DESIGN-*`（如涉技术边界调整） |
| Proceed to Spec | 商业闭环足够清楚，可进入实现规格 | `/specs-write` | `S-HG-1 GATE_NOT_REQUIRED`（本 workflow 内无未决 HG-*）；`DAG-N-AUDIT-{slug}-business` Done 传递给下游 |

### 7.3 审计报告输出规范 (Report Format)

- **输出底线约束**：商业模式生死审计完成后，必须完整输出一份报告。报告的文档结构与所有必填字段必须严格遵循 `<bmar>` 定义的标准模板。
- **参考模板**：关于完整报告模板的内容和各部分的详细说明，请完整阅读并参考 [report-template.md](./templates/report-template.md)。

### 7.4 关卡判定

| Gate | 命中条件 | 动作 |
| ------ | ---------- | ------ |
| Gate A Strategy | Pivot、Kill、目标用户、商业模式或 MVP 边界需要用户裁决 | 给强推荐 + ≤2 备选，等待批准 |
| Gate B Critical Design | 技术路线必须大幅简化或重选，影响后续架构 | 给推荐方案 + 代价，等待批准 |
| Gate C Real-World Side Effect | 需要真实用户调研、真实付费、公开页面、生产账号或对外承诺 | 停下请求批准；批准后仍只形成可交接执行计划，本 workflow 不执行真实动作 |
| N/A | 只输出审计报告，不产生外部副作用 | 报告后停止；若用户要求继续，也只能进入已推荐下游 workflow 入口，不能执行真实外部动作 |

---

## 8. 路由规则

- `Kill`：不进入 `/specs-write`；若项目已有 Authoritative SSOT，只建议新增 decision log，不静默修改。
- `Pivot`：进入 `/project-inception` 修订定位、目标用户、MVP 和商业闭环。
- `Validate First`：优先 `prototype` skill 或手工实验；实验完成后再回来复审。
- `Amputate then Proceed`：先通过 `/project-inception` 或 `/grill-with-docs` 修上游，再派生 spec。
- `Proceed to Spec`：只有付费主体、替代方案、MVP 边界和关键假设都足够清楚时，才推荐 `/specs-write`。
- 技术复杂度是主要风险时，可先推荐 `/architecture-audit`，但不得绕过商业假设验证。

---

## 9. 禁用行为 (Forbidden Actions)

- 不提供空泛鼓励。
- 不把愿景、热情或技术可行性当商业可行性。
- 不伪造竞品、市场规模、用户数据或付费证据。
- 不在付费主体未知时推荐进入 `/specs-write`。
- 不把所有功能都塞进 MVP。
- 不把 Windows 原生、AI、自动化、本地优先、跨平台等技术偏好当作天然护城河。
- 不静默修改 Authoritative SSOT。
- 不替用户执行真实发布、真实收费、真实外联或生产账号操作。
- 不把 `Proceed` 解读为可以直接写代码；实现仍必须走下游合同。

---

## 10. 快速自检清单

报告前自检：

- [ ] 是否把事实、用户声称、推断和未知分开？
- [ ] 是否明确当前替代方案、竞争对手并列出清单？
- [ ] 是否为每个关键竞品/替代方案提供了至少一份符合 `<crt>` 模板的独立调查报告（或提供代理自主调研成果/出具 `<drp>` 深度调查提示词）？
- [ ] 是否拷问了“巨头为什么不顺手做掉”和“生态位防御”？
- [ ] 是否执行了 **“企业消失测试 (Disappearance Test)”**并判定了客户依赖度分级？
- [ ] 是否针对所谓的护城河进行了**“四大结构性护城河防伪扫描”**并排除了虚假优势？
- [ ] 是否评估了**“人员主导型/服务型陷阱”**导致股东利润被蚕食的风险？
- [ ] 是否审查了**“增量利润转化率”**，并剥离了需要大量维持性资本开支的资本吞金兽模式？
- [ ] 是否拷问了核心放缓时的 **“跨界瞎折腾与并购动机”**？
- [ ] 是否评估了高负债或高资本依赖下的 **“反身性融资困境”**（市场负面预期直接反向塑造并杀死基本面事实）？
- [ ] 是否查阅了 `<imm>` (`industry-manual.md`)，执行了行业原型映射并拉响了特定红旗？
- [ ] 是否明确使用者、付费者、推动者和阻碍者（利益受损者）？
- [ ] 是否指出了最可能导致失败的死因（含故事股、税务暴雷、控制权僵局与反身性风险）？
- [ ] 是否拷问了金税四期底线利润、人才真实获取成本及真实定价权？
- [ ] 是否通过了控制权排雷，并确保资本属性与退出路径不发生错配？
- [ ] 是否执行了“扁平化的智慧”，在 MVP 阶段砍掉了大公司病式的组织架构？
- [ ] 是否把商业与治理风险转成了可证伪的假设？
- [ ] 是否给出最小验证实验和决策规则？
- [ ] 是否输出 Keep / Cut / Defer / Simplify？
- [ ] 是否给出唯一主裁定和下游路线？
- [ ] 遇到假设模糊时，是否硬性挂载了 `grill-me` 追问？
- [ ] 是否严守了边界，避免直接进入实现或写代码？

## 支撑资源

- [competitor-research-template.md](./templates/competitor-research-template.md)
- [decision-matrix.md](./references/decision-matrix.md)
- [deep-research-prompt-template.md](./templates/deep-research-prompt-template.md)
- [industry-manual.md](./references/industry-manual.md)
- [report-template.md](./templates/report-template.md)
