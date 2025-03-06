### 学城
支持拼音首字母、全拼检索。
- `km` -学城搜索，默认显示搜索历史，输入关键字会自动提示。
- `mykm` -打开我的学城空间
- `kmh`  - [h]istory 最近浏览文档
- `kme`  - latest [e]dit 最近编辑文档
- `kmq`  - [q]uick access 快速访问文档
- `kmc`  - [c]ellections 收藏文档 
- `kmm`  - [m]entioned @我的文档
- `kmt`  - commen[t]ed 我评论的文档
- `kmr`  - [r]eceived 我大象收到的文档
- `kmsp` - 索引指定空间的所有的文档，用于快速索引和跳转，默认为我的空间。
    1. **复制** ：在workflow中进行复制 ScriptFilter和Open Url组件。
    2. **修改参数和快捷键**： 双击ScriptFilter，修改文档id和快捷键，第三个参数为缓存时间（小时），第四个参数为学城空间id，如：`"$1" "$mis" 48 223`
    3. **运行** 通过输入步骤2中的快捷键触发索引和检索

- `kmp` - 索引指定文档及其所有子目录文档，用于快速索引和跳转，可以在工作流中根据参数自定义扩展：
    1. **复制** ：在workflow中进行复制 ScriptFilter和Open Url组件。
    2. **修改参数和快捷键**： 双击ScriptFilter，修改文档id和快捷键，第三个参数为缓存时间（小时），第四个为学城文档id（学城文档链接中的数字），如：`"$1" "$mis" 48 1202053621`
    3. **运行** 通过输入步骤2中的快捷键触发索引和检索

### ONES
- `ones` - 我的ones列表
- `onesp` - 最近查看的ones空间


### Jumper
- `jp` - 根据ip或主机名打开jumper web shell。
    - 按住cmd打开终端跳转，需按wiki配置：[Jumper终端免登录](https://km.sankuai.com/page/545430795)​​
- `host` - 根据ip或主机关键字查询，并跳转jumper
    - 按住cmd复制到剪切板

### 日志中心（新）：
- `log` - 我的日志列表 【缓存】
- `logak` - 按appkey访问日志中心【缓存】

### Eagle
- `es` 我的集群列表
- `esg` 我的集群组列表

### appkey通用跳转
* `ak` - 复制appkey
* `sak`（[s]earch [a]pp[k]ey） - 根据关键字搜索appkey，回车复制appkey
* `akm` ([a]pp[k]ey [m]embers) - 根据appkey搜索负责人，回车复制mis
- `option +[M]embers` - 根据剪贴板内的appkey搜索负责人，快捷键可自定义，回车复制mis
- `oc` - octo线上环境，按住cmd到线下环境
- `rh` - rhino线上环境，按住cmd到线下环境
- `lion` - lion线上环境，按住lion到线下环境
    - `lk` - 可通过lk先输入key再选择appkey查看指定配置项
- `git` - code线上环境，只包含我的appkey，更全发布项请使用repo(repository)指令
- `plus` - 我的发布项【新】，只包含我的appkey，更全发布项请使用dp(deploy)指令
- `pl` - 我的发布项列表【老】【已废弃】
- `avt` - [a][v]a[t]ar ：跳转avatar
- `trace` - mtrace，输入traceid跳转， 按住cmd到线下环境
- `logak` - 新日志中心，logcenter 2.0
- `lion` - lion指令
### Avatar
- `srv` - 查询avatar服务，可以根据ip或主机名查询，跳转avatar
- `avt` - [a][v]a[t]ar ：跳转avatar
### Raptor监控
- `rpt` - [r]a[p][t]or 线上环境，按住cmd到测试环境
- `rptp` - [r]a[p][t]or [p]roblom 线上环境，按住cmd到测试环境
- `rptb` - [r]a[p][t]or [b]usiness 线上环境，按住cmd到测试环境
- `rptt` - [r]a[p][t]or [t]ransaction 线上环境，按住cmd到测试环境
- `rpd` raptor dashboard 收藏的raptor大盘
    - 回车跳转大盘，
    - 按住cmd显示大盘图表。
- `srpd` 搜索大盘
    - 回车跳转大盘，
    - 按住cmd显示大盘图表。
- `rfd` raptor front dashboard 前端监控大盘，使用前需使用cfp(change front project)指令选择前端项目。
### RDS：
- `db` - rds集群列表
    - 直接回车后查看集群下的db列表
        - 按住cmd后回车到db详情页
        - 回车后到sql执行页面
    - 按住cmd跳转到rds集群信息页面
- `dbt` - rds集群列表【测试环境】
    - 直接回车后查看集群下的db列表
        - 按住cmd后回车到db详情页
        - 回车后到sql执行页面
    - 按住cmd跳转到rds集群信息页面
- `sdb` ([S]earch db) 根据关键字搜索db
- `rds` - rds集群列表，直接到监控页
### Cellar：
- `cl` - [C]ellar [L]ist集群组列表
    - 回车查看集群组下集群，再回车查看集群
- `scl` - 按照appkey搜索集群
- `tl` - [T]air cluster [L]ist 列表，跳转集群详情页
### squirrel：
- `sq` - squirrel集群列表，跳转集群详情页 【本地缓存】
- `ssq` - [S]earch [Sq]uirrel 搜索集群
- `ssqg` - [S]earch [Sq]uirrel [G]roup 搜索集群组
- `sqg` - [sq]uirrel  [g]roup 集群组
    - 直接回车后查看集群组下集群列表
        - 按住cmd后回车到集群组详情页
        - 回车后直接到集群详情页
### mafka
- `mq` - Mafka queue topic列表，回车跳转详情页 ，模糊匹配字段：appkey、topic、描述。
- `smq` - [S]earch [M]afka [q]ueue topic，回车跳转详情页
- `mqc` - [M]afka [q]ueue [C]onsumer group ,消费组列表，跳转详情页,模糊匹配字段：消费组、appkey、topic、描述
- `smqc` - [S]earch [M]afka [q]ueue [c]onsumer 搜索消费组，跳转详情页
### Cargo
- `cg` - cargo 个人泳道列表 【本地缓存】
- `scg`  -  [s]earch [c]ar[g]o 根据编排名称或泳道搜索，跳转泳道详情。

### Code git
- `repo` - git [repo]sitory  我的仓库列表，跳转代码仓库详情。 模糊匹配字段：仓库名、发布项
    - 按住cmd创建PR
- `dp` - [d]e[p]loy 跳转发布页 模糊匹配字段：仓库名、发布项
- `prl` - [p]ull [r]equest [l]ist  代码评审列表 模糊匹配字段：仓库名、发布项
- `git` - code线上环境，只包含我的appkey，更全发布项请使用repo(repository)指
- `plus` - 我的发布项【新】，只包含我的appkey，更全发布项请使用dp(deploy)指令

### 日志中心：
#### logcenter 2.0 （raptor）
- `log` - 我的日志列表 【缓存】
- `logak` - 按appkey访问日志中心【缓存】
#### 原logcenter
- `lc` - logcenter我的日志列表 【缓存】
- `lca` - logcenter所有日志列表 【缓存】
- `lct` - logcenter [T]est环境我的日志列表 【测试环境】
- `lcat` - logcenter [T]est环境所有日志列表 【测试环境】

### Oceanus：
- `ou` - oceanus站点
### Domain：
- `dom` - 我的站点 模糊匹配字段：域名、内网/外网、线上/线下、描述
- `sdom` 搜索站点
### Radar：
- `rad` - 我的雷达事件
- `rado` 组织下的雷达事件，在alfred环境变量中设置radorg_org_id（radar全部时间选择组织后，url中最后一个orgid）
### Shepherd：
- `shp` 我的api列表 模糊匹配字段：api名称、路径、分组名、描述
- `shpt` 我的api列表 【测试环境】
- `shpg` 我的api group列表 
- `shpgt` 我的api group列表 【测试环境】
- `sshp` 搜索 Shepherd API及分组，感谢liuyulong06贡献。
### 云图：
- `ytf` 搜藏的云图
- `yth` 最近浏览云图
### crane
- `cr` 任务数大于0的appkey列表
    - 按住cmd跳转测试环境
- `task` 任务数大于0的appkey列表
    - 回车显示列表下的具体任务
    - 按住cmd跳转测试环境
### Eagle
- `es` 我的集群列表
- `esg` 我的集群组列表

### COE:
- `coef` 收藏的COE  
- `scoe` 搜索COE

### Jumper
- `jp` - 根据ip或主机名打开jumper web shell。
    - 按住cmd打开终端跳转，需按wiki配置：[Jumper终端免登录](https://km.sankuai.com/page/545430795)​​
- `host` - 根据ip或主机关键字查询，并跳转jumper
    - 按住cmd复制到剪切板


### 到家digger监控：
- `dg` - 查询收藏的监控大盘 【本地缓存】
- `sdg` - 关键字搜索大盘

### 到家FSD
- `fsd` 打开fsd新建交付页面
- `fsdlist` 跟我相关的交付计划
- `fsdplan` 跟我相关的上线计划
### 系统指令：
- `cc` - clear cache 清除缓存：如发现数据不是最新，可尝试清除缓存。
实用工具
- `ts` -日期转为时间戳（支持毫秒），并复制到剪贴板
- `tsnow` -当前时间的时间戳，并复制到剪贴板
- `tstoday` - 当天的时间戳，并复制到剪贴板
- `fts`  -时间戳转为日期，并复制到剪贴板
### 其他
- `mis` - 查询mis，回车后打开大象聊天框
- `xmzl` 小美智能助理