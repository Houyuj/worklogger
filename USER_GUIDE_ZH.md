# WorkLogger 用户指南

WorkLogger 是面向个人科研与研发管理者的桌面端本地工具。界面保持英文；本指南用中文解释推荐工作流。

## 先记住四类对象

| 对象 | 用途 |
| --- | --- |
| Project | 一个持续的研究项目或研发方向。 |
| Annual / Monthly / Weekly Goal | Project 下的规划层级：年度方向、月度可交付目标、周内具体承诺。 |
| Task | 某天需要推进的最小行动。 |
| Protocol | 可复用的实验方案、重复性流程或研究记录；不局限于“实验”。 |

## 每日：先快速记录，再归类

在 **Today** 的 Quick add 中写入标题和日期即可创建任务。默认值为：

- Priority：`Normal`
- Work status：`Unclassified`

`Unclassified` 不是收件箱，也不是普通标签；它表示任务尚未归入具体年度、月度或周目标。使用搜索的 All time + Unclassified 可以集中查看这类任务。

### 批量归到周目标

1. 在 Today 列表下方点击 **Select tasks**。
2. 直接点击任务行即可选中或取消选中，不会打开编辑面板。
3. 点击上方本周 Weekly Goal 胶囊，或打开 **Manage Projects & Goals** 后点击目标 Week。

系统会补全父级关系，并将这些任务的状态切换为 `Planned`。

## Protocol：需要时再关联

Quick add 下方的 **Link to Protocol (Optional)** 提供三种低摩擦方式：

- 输入标题搜索并关联现有 Protocol；
- 勾选 **Create a copy**，保存任务后生成副本并打开编辑；
- 在下拉第一项选择 **+ Create new Protocol**，保存任务后创建并打开新的 Protocol。

任务界面按当前产品规则只显示一个主 Protocol，降低误关联风险。

### 编辑 Protocol

进入 **Protocols** 后：

- **Quick Edit** 只保留 `Protocol Title`、`Status`、`Progress note`。
- 方案、图片、实验记录、结果与结论都写入 Protocol 正文。
- 相似方案优先 Duplicate；标题中的 `Copy` 由你主动删除时，表示该副本已接管为本次新的设计或结果。

## 管理 Projects & Goals

在 Today 中展开 **Manage Projects & Goals**，用树状结构在正确位置创建：

`Project → Annual → Month → Week`

不要为了“以后可能需要”而先建大量节点。通常月度目标较稳定，周目标的创建更频繁。

### Archive 与 Delete

- **Archive**：保留已有任务、Protocol 和报告历史；勾选 **Include archived** 后可 Restore。
- **Delete**：仅适用于没有子节点、任务或历史关联的空节点。已使用的内容应 Archive，不应 Delete。

## Reports 与 Gantt

### Reports

Reports 用于周度或月度关键汇报前检查任务、进度和缺项。

- Weekly / Monthly / Annual 报表均可导出 Excel；Excel 是便于继续整理和制作 PPT 的主格式。
- PDF 用于不希望他人修改的分享版本。
- 报表中的 Protocol 图标会在新标签页打开原始 Protocol，方便取用图片与结果。

### Gantt

Gantt 用于偶尔确认月度目标的时间分布、进度和空档。

- Year view 显示 52 或 53 个 ISO 周，不会把第 53 周折到行首。
- Month view 侧重当前月的 Weekly Goals。
- 左侧目标行与右侧时间条会同步高度。

## 数据与备份

数据保存在 `data/worklogger.db`。它不会进入 Git，也不会被推送到 GitHub。

手工备份前先退出应用，然后复制数据库文件：

```powershell
Copy-Item .\data\worklogger.db .\data\worklogger.db.backup
```

恢复时先退出 WorkLogger，再把备份覆盖回 `data/worklogger.db`。

## 推荐节奏

1. 每天先 Quick add，不要求立刻填满上下文。
2. 一天或一周内集中选择 Unclassified 任务，批量归到 Weekly Goal。
3. 需要实验设计或记录时再打开 Protocol，不让富文本编辑阻塞任务创建。
4. 月度汇报前在 Reports 检查缺项，导出 Excel；需要只读分享时再导出 PDF。
