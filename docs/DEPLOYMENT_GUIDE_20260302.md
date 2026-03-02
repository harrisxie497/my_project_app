# 服务器部署操作文档

## 📅 日期
2026-03-02

## 📋 修改内容概述

本次修改包含以下内容：

### 1. 电话号码添加前缀0功能
- **M列（輸入者電話番号）**：添加 `add_prefix_zero` 参数，自动为不以0开头的电话号码添加前缀0
- **Z列（電話番号）**：添加 `add_prefix_zero` 参数，自动为不以0开头的电话号码添加前缀0

### 2. 日本人名生成优化
- 降低日本人名生成的重复度
- 添加常见日本姓氏和名字列表
- 要求同一批次中虚构名字互不相同

### 3. 日本地址格式优化
- 保留建筑名称和房间号
- 删除了"可以去掉丁目和番地后面所有的内容"的指令

---

## 📁 修改的文件列表

### 代码文件
1. `backend/app/services/field_handlers.py`
   - 修改 `normalize_copy_then_regex` 函数，添加 `add_prefix_zero` 参数

2. `backend/app/services/field_handlers_v2.py`
   - 修改 `policy_copy_regex` 处理，传递 `add_prefix_zero` 参数

### 数据库更新脚本
3. `backend/update_m_column_add_prefix_zero.py`
   - 更新M列配置，添加 `add_prefix_zero` 参数

4. `backend/update_z_column_add_prefix_zero.py`
   - 更新Z列配置，添加 `add_prefix_zero` 参数

5. `backend/update_name_and_address_prompts.py`
   - 更新日本人名和日本地址的提示词

---

## 🚀 部署步骤

### 步骤1：备份当前代码和数据库

```bash
# 备份代码
cd /path/to/japan
git pull origin master
git branch backup-$(date +%Y%m%d)
git push origin backup-$(date +%Y%m%d)

# 备份数据库
mysqldump -h 172.18.207.224 -u app -papp123456 demo > backup_$(date +%Y%m%d).sql
```

---

### 步骤2：拉取最新代码

```bash
cd /path/to/japan
git pull origin master
```

---

### 步骤3：更新数据库配置

#### 3.1 更新M列配置（輸入者電話番号）

```bash
cd /path/to/japan/backend
python update_m_column_add_prefix_zero.py
```

**预期输出**：
```
====================================================================================================
更新M列配置，添加add_prefix_zero参数
====================================================================================================

当前配置：
  ID: 13
  文件类型: CUSTOMS
  目标列: M
  规则参数: {"policy_copy_regex": {"regex": "^\\d{9,11}$", "required": true, "remove_dash": true, "remove_leading_trailing_spaces": true, "remove_middle_spaces": true}}
  规则参数类型: <class 'str'>

✅ M列配置已更新
  新的规则参数: {'policy_copy_regex': {'regex': '^\\d{9,11}$', 'required': True, 'remove_dash': True, 'add_prefix_zero': True, 'remove_middle_spaces': True, 'remove_leading_trailing_spaces': True}}

====================================================================================================
更新完成
====================================================================================================
```

#### 3.2 更新Z列配置（電話番号）

```bash
python update_z_column_add_prefix_zero.py
```

**预期输出**：
```
====================================================================================================
更新Z列配置，添加add_prefix_zero参数
====================================================================================================

当前配置：
  ID: 26
  文件类型: CUSTOMS
  目标列: Z
  规则参数: {"policy_copy_regex": {"regex": "^\\d{9,11}$", "required": true, "remove_dash": true, "remove_leading_trailing_spaces": true, "remove_middle_spaces": true}}
  规则参数类型: <class 'str'>

✅ Z列配置已更新
  新的规则参数: {'policy_copy_regex': {'regex': '^\\d{9,11}$', 'required': True, 'remove_dash': True, 'add_prefix_zero': True, 'remove_middle_spaces': True, 'remove_leading_trailing_spaces': True}}

====================================================================================================
更新完成
====================================================================================================
```

#### 3.3 更新日本人名和日本地址提示词

```bash
python update_name_and_address_prompts.py
```

**预期输出**：
```
====================================================================================================
更新日本人名和日本地址的提示词
====================================================================================================

====================================================================================================
更新 policy_ai_text_ja_clean（日本人名清理）
====================================================================================================

当前 schema_json: {...}

✅ policy_ai_text_ja_clean 已更新

====================================================================================================
更新 policy_ai_text_dress_clean（日本地址清理）
====================================================================================================

当前 schema_json: {...}

✅ policy_ai_text_dress_clean 已更新

====================================================================================================
更新完成！
====================================================================================================
```

---

### 步骤4：验证更新结果

#### 4.1 验证M列配置

```bash
python check_m_column_config.py
```

**预期结果**：
```
M列配置:
  ID: 13
  目标列: M
  操作类型: COPY
  字段类型: FORMAT
  规则引用: ['policy_copy_regex']
  规则参数: {'policy_copy_regex': {'regex': '^\\d{9,11}$', 'required': True, 'remove_dash': True, 'add_prefix_zero': True, 'remove_middle_spaces': True, 'remove_leading_trailing_spaces': True}}
```

#### 4.2 验证Z列配置

```bash
python check_z_m_columns_config.py
```

**预期结果**：
```
Z列配置:
  ID: 26
  目标列: Z
  操作类型: COPY
  字段类型: FORMAT
  规则引用: ['policy_copy_regex']
  规则参数: {'policy_copy_regex': {'regex': '^\\d{9,11}$', 'required': True, 'remove_dash': True, 'add_prefix_zero': True, 'remove_middle_spaces': True, 'remove_leading_trailing_spaces': True}}
```

#### 4.3 验证日本人名提示词

```bash
python check_policy_ai_text_ja_clean.py
```

**预期结果**：
```
system_prompt: 你是一个日本海关资料审核专家，你需要整理日文收件人名是否符合日本人名格式。

要求：
1. 移除敬语和称谓（様、様、先生、様方等）
2. 去掉假名（平假名/片假名），把括号以及括号内的内容去掉
3. 如果有多个名字，只保留第一个
4. 如果明显不是日本人名（例如：公司名，中文名，英文名，地址名），请虚构一个日本人名。

虚构日本人名时请遵守以下规则：
- 使用常见的日本姓氏（如：佐藤、鈴木、高橋、田中、伊藤、渡辺、山本、中村、小林、加藤等）
- 使用常见的日本名字（如：太郎、花子、健一、美咲、大輔、由美、翔太、麻衣、拓也、優子等）
- 姓氏和名字之间用空格分隔（如：佐藤 太郎）
- 每次生成时请使用不同的姓氏和名字组合，避免重复
- 如果同一批次中有多个需要虚构的名字，请确保它们互不相同
```

#### 4.4 验证日本地址提示词

```bash
python query_rule_definition_policy_ai_text_dress_clean.py
```

**预期结果**：
```
system_prompt: 你是一个日本海关资料审核专家，你需要整理日文收件人地址是否符合日本地址格式。

要求：
1. 日本地址地址层级完整的是，都道府县 → 市/区 → 町/地区 → 丁目/番地，最后的一定是丁目和番地。
2. 你需要整理地址，并且都道府县和市/区之间用空格隔开，其他层级之间也用空格隔开。
3. 如果地址中不包含丁目和番地，你需要随机虚构一个常见的门牌号码，例如：1-1-1；门牌号码左右和中间都不用保留空格。
4. 保留丁目和番号后面的建筑名称和房间号（如"CORE高梨one 201号室"、"マンション101号室"等），不要删除这些信息。
5. 建筑名称和房间号与门牌号之间用空格分隔（如"20-11 CORE高梨one 201号室"）。
```

---

### 步骤5：功能测试

#### 5.1 测试电话号码添加前缀0

```bash
python test_m_column_prefix_zero.py
```

**预期结果**：
```
测试用例 1: 以0开头的电话号码
  输入: '09012345678'
  期望: '09012345678'
  ✅ 通过: 结果 = '09012345678'

测试用例 2: 不以0开头的电话号码
  输入: '9012345678'
  期望: '09012345678'
  ✅ 通过: 结果 = '09012345678'

测试用例 3: 带横杠的电话号码
  输入: '090-1234-5678'
  期望: '09012345678'
  ✅ 通过: 结果 = '09012345678'

测试用例 4: 带空格的电话号码
  输入: ' 9012345678  '
  期望: '09012345678'
  ✅ 通过: 结果 = '09012345678'

测试用例 5: 空值
  输入: ''
  期望: None
  ✅ 通过: 正确抛出异常 - 值不匹配正则表达式：^\d{9,11}$

测试用例 6: None值
  输入: None
  期望: None
  ✅ 通过: 结果 = None

测试用例 7: 不添加前缀0（add_prefix_zero=False）
  输入: '9012345678'
  期望: '9012345678'
  ✅ 通过: 结果 = '9012345678'

测试结果: 通过 7/7, 失败 0/7
```

#### 5.2 测试实际数据

上传包含以下测试数据的Excel文件：

**电话号码测试**：
- `09012345678` → 应保持不变
- `9012345678` → 应变为 `09012345678`
- `090-1234-5678` → 应变为 `09012345678`

**日本人名测试**：
- `Raj Merani` → 应生成不同的日本人名（如：佐藤 太郎）
- `张三` → 应生成不同的日本人名（如：鈴木 花子）

**日本地址测试**：
- `長崎県 佐世保市高梨町 20-11 CORE高梨one 201号室` → 应保留建筑名称和房间号
- `東京都渋谷区道玄坂1-10-25 マンション101号室` → 应保留建筑名称和房间号

---

### 步骤6：重启服务（如果需要）

```bash
# 如果使用Docker
docker-compose restart backend

# 如果使用systemd
sudo systemctl restart japan-backend

# 如果使用supervisor
sudo supervisorctl restart japan-backend
```

---

## 🔄 回滚方案

### 回滚数据库配置

如果需要回滚数据库配置，可以使用以下SQL语句：

```sql
-- 回滚M列配置
UPDATE field_pipelines
SET rule_params_json = '{"policy_copy_regex": {"regex": "^\\\\d{9,11}$", "required": true, "remove_dash": true, "remove_leading_trailing_spaces": true, "remove_middle_spaces": true}}'
WHERE target_col = 'M' AND file_type = 'CUSTOMS';

-- 回滚Z列配置
UPDATE field_pipelines
SET rule_params_json = '{"policy_copy_regex": {"regex": "^\\\\d{9,11}$", "required": true, "remove_dash": true, "remove_leading_trailing_spaces": true, "remove_middle_spaces": true}}'
WHERE target_col = 'Z' AND file_type = 'CUSTOMS';

-- 回滚日本人名提示词
UPDATE rule_definitions
SET schema_json = '{"desc": "收件人名清理", "configurable_params": {"system_prompt": "你是一个日本海关资料审核专家，你需要整理日文收件人名是否符合日本人名格式。\\n要求：\\n1. 移除敬语和称谓（ 様、様、先生、様方等）\\n2. 去掉假名（平假名/片假名），把括号以及括号内的内容去掉\\n3. 如果有 多个名字，只保留第一个\\n4. 如果明显不是日本人名（例如：公司名，中文名，英文名，地址名），随 机虚构一个常见日本人名。\\n请严格遵守以下规则：\\n1. 输入数据是一个 JSON 数组，数组每个对象有 字段\\"index\\"和\\"context\\"。\\n你需要处理的是context里面的内容，处理完成之后 ，输出同样长度的JSON 数组，index保持不变，context为处理之后的值。\\n\\n例如输入：\\n[\\n  {\\"index\\": \\"1\\", \\"context\\": \\"Raj Merani\\"},\\n  {\\"index\\": \\"1\\", \\"context\\": \\"SOJIRO TSUJIMOTO\\"},\\n  ...\\n]\\n 例如输出：\\n[\\n  {\\"index\\": \\"1\\", \\"context\\": \\"鈴木 健一\\"},\\n  {\\"index\\": \\"1\\", \\"context\\": \\"北島 敬子\\"},\\n  ...\\n]\\n2. 输出数组的长度必须严格等于输入数组的长度。\\n3. 不允许 删除、合并、省略任何输入行，只允许修改指定字段的内容。\\n4. 不要添加任何额外的解释、前言或后 记。"}}'
WHERE rule_ref = 'policy_ai_text_ja_clean';

-- 回滚日本地址提示词
UPDATE rule_definitions
SET schema_json = '{"desc": "收件人地址清理和格式化", "configurable_params": {"system_prompt": "你是一个日本海关资料审核专家，你需要整理日文收件人地址是否符合日本地址格式。\\n要求：\\n1. 日本 地址地址层级完整的是，都道府县 → 市/区 → 町/地区 → 丁目/番地，最后的一定是丁目和番地。\\n2.  你需要整理地址，并且都道府县和市/区之间用空格隔开，其他层级之间也用空格隔开，可以去掉丁目和 番地后面所有的内容。\\n3. 如果地址中不包含丁目和番地，你需要随机虚构一个常见的门牌号码，例如 ：1-1-1； 门牌号码左右和中间都不用保留空格。\\n请严格遵守以下规则：\\n1. 输入数据是一个 JSON  数组，数组每个对象有字段\\"index\\"和\\"context\\"。\\n你需要处理的是context里面的内容，处理完成之后 ，输出同样长度的JSON 数组，index保持不变，context为处理之后的值。\\n\\n例如输入：\\n[\\n  {\\"index\\": \\"1\\", \\"context\\": \\"沖縄県 糸満市 字糸満 ２２５２番地\\"},\\n  {\\"index\\": \\"1\\", \\"context\\": \\"2-25-1 Sumiyoshi Okinawa City Okinawa\\"},\\n  ...\\n]\\n例如输出：\\n[\\n  {\\"index\\": \\"1\\", \\"context\\": \\"沖縄県糸満市字糸満2252-1\\"},\\n  {\\"index\\": \\"1\\", \\"context\\": \\"沖 縄県沖縄市住吉2-25-1\\"},\\n  ...\\n]\\n2. 输出数组的长度必须严格等于输入数组的长度。\\n3. 不允许删除、合并、省略任何输入行，只允许修改指定字段的内容。\\n4. 不要添加任何额外的解释、前言或后 记。"}}'
WHERE rule_ref = 'policy_ai_text_dress_clean';
```

### 回滚代码

```bash
# 回滚到上一个版本
git reset --hard HEAD~1

# 或者回滚到特定版本
git reset --hard <commit-hash>

# 推送回滚
git push -f origin master
```

---

## 📊 验证清单

- [ ] 备份完成
- [ ] 代码拉取成功
- [ ] M列配置更新成功
- [ ] Z列配置更新成功
- [ ] 日本人名提示词更新成功
- [ ] 日本地址提示词更新成功
- [ ] M列配置验证通过
- [ ] Z列配置验证通过
- [ ] 日本人名提示词验证通过
- [ ] 日本地址提示词验证通过
- [ ] 电话号码测试通过
- [ ] 日本人名测试通过
- [ ] 日本地址测试通过
- [ ] 服务重启成功
- [ ] 实际数据测试通过

---

## 📞 联系方式

如有问题，请联系：
- 开发团队：[联系方式]
- 数据库管理员：[联系方式]
- 运维团队：[联系方式]

---

## 📝 备注

1. 所有脚本都需要在Python虚拟环境中运行
2. 数据库连接信息已硬编码在脚本中，如需修改请更新脚本
3. 建议在非高峰期进行部署
4. 部署前请务必完成备份
5. 部署后请进行充分测试
