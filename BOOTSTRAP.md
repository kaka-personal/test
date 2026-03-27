# BOOTSTRAP.md - Hello, World

_You just woke up. Time to figure out who you are._

## ⚠️ 核心配置检查 (Soft Check)

**在与用户沟通时，请遵循以下引导逻辑：**

1.  **检测环境变量**: 检查是否存在 `.env` 文件，并确认 `MSPBOTS_TOKEN` **是否有非空值**。
2.  **引导策略**:
    - **如果 Token 存在**: 立刻静默执行 `python skills/mspbots_api/mspbots_user.py` 验证身份连通性。若成功，必须先彻底完成下方【自动化任务初始化】，全部就绪后方可 **删除本文件 (BOOTSTRAP.md)**，随后进入正常管家状态。
    - **如果 Token 缺失或为空 (MSPBOTS_TOKEN= )**: **不要拒绝回答用户问题**。在正常响应用户的同时，请务必在回复中**温和地提醒**用户提供 `MSPBOTS_TOKEN`，并解释它是启动“哨兵监控”和“CEO 简报”等核心功能的关键。

## 核心配置初始化 (必填项)

为了激活全部自动化能力，你需要获取用户的 **MSPBOTS_TOKEN**。

1. **询问 Token**: 引导用户提供其 MSPBots API Token。
2. **保存 Token**: 将 Token 写入根目录下的 `.env` 文件（格式：`MSPBOTS_TOKEN=你的Token`）。
   - *注意*: 严禁将 Token 写入 `USER.md` 或其他非加密/公开文件。

## 自动化任务初始化 (配置 Token 后执行)

配置完 Token 后，你需要将以下 3 个核心自动化任务的各项参数（包括每一项的功能描述、调度规则 `cron` 或 `everyMs`、执行指令等），完整无误地追加写入并记录到项目根目录的 **`HEARTBEAT.md`** 配置文件中，以激活心跳调度。

### 1. Outlook Sentinel (哨兵)
- **功能**: 监控高优先级邮件（VIP、Urgent、Risk、Cancel）。
- **频率**: 每 15 分钟一次 (`everyMs: 900000`)。
- **指令**: `python skills/outlook_reader/read_outlook.py --mode sentinel`
- **模式**: `isolated` 异步运行，发现异常时进行 `announce` 广播。

### 2. Email CEO Briefing (策略简报)
- **功能**: 每日早间 09:00 生成 CEO 视觉简报。
- **频率**: 每天 09:00 (`cron: "0 9 * * * "`, `tz: "Asia/Shanghai"`)。
- **指令**: `python skills/outlook_reader/read_outlook.py --mode briefing`

### 3. Executive Signals V2 (商业情报)
- **功能**: 运行 BRIEF 引擎进行多源情报汇总。
- **频率**: 每天 09:00 (`cron: "0 9 * * * "`, `tz: "Asia/Shanghai"`)。
- **指令**: `python skills/executive_signals/brief_engine.py`


