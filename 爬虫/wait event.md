## `postgresql ~ wait_event`

[postgresql文档](https://www.postgresql.org/docs/11/monitoring-stats.html#WAIT-EVENT-TABLE). 

| 等待事件名称wait_event              | 描述                                                         | 等待事件类型wait_event_type |
| ----------------------------------- | ------------------------------------------------------------ | --------------------------- |
| `ShmemIndexLock`                    | 等待在共享内存中查找或分配空间。                             | `LWLock`                    |
| `OidGenLock`                        | 等待分配或分配OID。                                          |                             |
| `XidGenLock`                        | 等待分配或分配交易ID。                                       |                             |
| `ProcArrayLock`                     | 等待在事务结束时获取快照或清除事务ID。                       |                             |
| `SInvalReadLock`                    | 等待从共享的失效队列中检索或删除邮件。                       |                             |
| `SInvalWriteLock`                   | 等待在共享的失效队列中添加消息。                             |                             |
| `WALBufMappingLock`                 | 等待替换WAL缓冲区中的页面。                                  |                             |
| `WALWriteLock`                      | 等待WAL缓冲区写入磁盘。                                      |                             |
| `ControlFileLock`                   | 等待读取或更新控制文件或创建新的WAL文件。                    |                             |
| `CheckpointLock`                    | 等待执行检查点。                                             |                             |
| `CLogControlLock`                   | 等待读取或更新事务状态。                                     |                             |
| `SubtransControlLock`               | 等待读取或更新子事务信息。                                   |                             |
| `MultiXactGenLock`                  | 等待读取或更新共享的多重状态。                               |                             |
| `MultiXactOffsetControlLock`        | 等待读取或更新multixact偏移映射。                            |                             |
| `MultiXactMemberControlLock`        | 等待读取或更新multixact成员映射。                            |                             |
| `RelCacheInitLock`                  | 等待读取或写入关系缓存初始化文件。                           |                             |
| `CheckpointerCommLock`              | 等待管理fsync请求。                                          |                             |
| `TwoPhaseStateLock`                 | 等待读取或更新准备好的事务的状态。                           |                             |
| `TablespaceCreateLock`              | 等待创建或删除表空间。                                       |                             |
| `BtreeVacuumLock`                   | 等待读取或更新B树索引的真空相关信息。                        |                             |
| `AddinShmemInitLock`                | 等待管理共享内存中的空间分配。                               |                             |
| `AutovacuumLock`                    | Autovacuum工作人员或发射器等待更新或读取autovacuum工作人员的当前状态。 |                             |
| `AutovacuumScheduleLock`            | 等待确保它为真空选择的桌子仍然需要吸尘。                     |                             |
| `SyncScanLock`                      | 等待在表上获取扫描的起始位置以进行同步扫描。                 |                             |
| `RelationMappingLock`               | 等待更新用于将目录存储到filenode映射的关系映射文件。         |                             |
| `AsyncCtlLock`                      | 等待读取或更新共享通知状态。                                 |                             |
| `AsyncQueueLock`                    | 等待阅读或更新通知消息。                                     |                             |
| `SerializableXactHashLock`          | 等待检索或存储有关可序列化事务的信息。                       |                             |
| `SerializableFinishedListLock`      | 等待访问已完成的可序列化事务列表。                           |                             |
| `SerializablePredicateLockListLock` | 等待对可序列化事务持有的锁列表执行操作。                     |                             |
| `OldSerXidLock`                     | 等待读取或记录冲突的可序列化事务。                           |                             |
| `SyncRepLock`                       | 等待读取或更新有关同步副本的信息。                           |                             |
| `BackgroundWorkerLock`              | 等待阅读或更新后台工作人员状态。                             |                             |
| `DynamicSharedMemoryControlLock`    | 等待读取或更新动态共享内存状态。                             |                             |
| `AutoFileLock`                      | 等待更新`postgresql.auto.conf`文件。                         |                             |
| `ReplicationSlotAllocationLock`     | 等待分配或释放复制槽。                                       |                             |
| `ReplicationSlotControlLock`        | 等待读取或更新复制槽状态。                                   |                             |
| `CommitTsControlLock`               | 等待读取或更新事务提交时间戳。                               |                             |
| `CommitTsLock`                      | 等待读取或更新事务时间戳的最后一个值集。                     |                             |
| `ReplicationOriginLock`             | 等待设置，删除或使用复制源。                                 |                             |
| `MultiXactTruncationLock`           | 等待读取或截断多重信息。                                     |                             |
| `OldSnapshotTimeMapLock`            | 等待读取或更新旧快照控制信息。                               |                             |
| `BackendRandomLock`                 | 等待生成一个随机数。                                         |                             |
| `LogicalRepWorkerLock`              | 等待逻辑复制工作程序的操作完成。                             |                             |
| `CLogTruncationLock`                | 等待截断预写日志或等待预写日志截断完成。                     |                             |
| `clog`                              | 在clog（事务状态）缓冲区上等待I / O.                         |                             |
| `commit_timestamp`                  | 在提交时间戳缓冲区上等待I / O.                               |                             |
| `subtrans`                          | 等待I / O子事务缓冲区。                                      |                             |
| `multixact_offset`                  | 在multixact偏移缓冲区上等待I / O.                            |                             |
| `multixact_member`                  | 在multixact_member缓冲区上等待I / O.                         |                             |
| `async`                             | 在异步（通知）缓冲区上等待I / O.                             |                             |
| `oldserxid`                         | 等待oldserxid缓冲区上的I / O.                                |                             |
| `wal_insert`                        | 等待将WAL插入内存缓冲区。                                    |                             |
| `buffer_content`                    | 等待在内存中读取或写入数据页。                               |                             |
| `buffer_io`                         | 等待数据页面上的I / O.                                       |                             |
| `replication_origin`                | 等待读取或更新复制进度。                                     |                             |
| `replication_slot_io`               | 在复制槽上等待I / O.                                         |                             |
| `proc`                              | 等待读取或更新快速路径锁定信息。                             |                             |
| `buffer_mapping`                    | 等待将数据块与缓冲池中的缓冲区相关联。                       |                             |
| `lock_manager`                      | 等待添加或检查后端锁，或等待加入或退出锁定组（由并行查询使用）。 |                             |
| `predicate_lock_manager`            | 等待添加或检查谓词锁定信息。                                 |                             |
| `parallel_query_dsa`                | 等待并行查询动态共享内存分配锁。                             |                             |
| `tbm`                               | 等待TBM共享迭代器锁。                                        |                             |
| `parallel_append`                   | 在并行追加计划执行期间等待选择下一个子计划。                 |                             |
| `parallel_hash_join`                | 等待在并行哈希计划执行期间分配或交换一块内存或更新计数器。   |                             |
| `relation`                          | 等待获得关系的锁定。                                         | `Lock`                      |
| `extend`                            | 等待延长关系。                                               |                             |
| `page`                              | 等待获取关系页面上的锁定。                                   |                             |
| `tuple`                             | 等待获取元组的锁定。                                         |                             |
| `transactionid`                     | 等待交易完成。                                               |                             |
| `virtualxid`                        | 等待获取虚拟xid锁。                                          |                             |
| `speculative token`                 | 等待获得投机插入锁定。                                       |                             |
| `object`                            | 等待获取非关系数据库对象的锁定。                             |                             |
| `userlock`                          | 等待获取用户锁定。                                           |                             |
| `advisory`                          | 等待获取咨询用户锁。                                         |                             |
| `BufferPin`                         | 等待获取缓冲区上的引脚。                                     |                             |
| `BufferPin`                         | `ArchiverMain`                                               | Activity                    |
| `AutoVacuumMain`                    | 在autovacuum发射器过程的主循环中等待。                       |                             |
| `BgWriterHibernate`                 | 等待在后台作家过程中，冬眠。                                 |                             |
| `BgWriterMain`                      | 等待在背景作家处理背景工作者主循环。                         |                             |
| `CheckpointerMain`                  | 在checkpointer过程的主循环中等待。                           |                             |
| `LogicalApplyMain`                  | 在逻辑应用程序的主循环中等待。                               |                             |
| `LogicalLauncherMain`               | 在逻辑启动程序进程的主循环中等待。                           |                             |
| `PgStatMain`                        | 在统计信息收集器进程的主循环中等待。                         |                             |
| `RecoveryWalAll`                    | 在恢复时从任何类型的源（本地，存档或流）等待WAL。            |                             |
| `RecoveryWalStream`                 | 在恢复期间从流中等待WAL。                                    |                             |
| `SysLoggerMain`                     | 在syslogger进程的主循环中等待。                              |                             |
| `WalReceiverMain`                   | 在WAL接收器进程的主循环中等待。                              |                             |
| `WalSenderMain`                     | 等待WAL发送者进程的主循环。                                  |                             |
| `WalWriterMain`                     | 在WAL编写器进程的主循环中等待。                              |                             |
| `ClientRead`                        | 等待从客户端读取数据。                                       | `Client`                    |
| `ClientWrite`                       | 等待将数据写入客户端。                                       |                             |
| `LibPQWalReceiverConnect`           | 等待WAL接收器建立与远程服务器的连接。                        |                             |
| `LibPQWalReceiverReceive`           | 在WAL接收器中等待从远程服务器接收数据。                      |                             |
| `SSLOpenServer`                     | 尝试连接时等待SSL。                                          |                             |
| `WalReceiverWaitStart`              | 等待启动过程发送流复制的初始数据。                           |                             |
| `WalSenderWaitForWAL`               | 等待WAL在WAL发送过程中刷新。                                 |                             |
| `WalSenderWriteData`                | 在WAL发送器进程中处理来自WAL接收器的回复时等待任何活动。     |                             |
| `Extension`                         | 等待延期。                                                   | `Extension`                 |
| `BgWorkerShutdown`                  | 等待后台工作者关闭。                                         | `IPC`                       |
| `BgWorkerStartup`                   | 等待后台工作者启动。                                         |                             |
| `BtreePage`                         | 等待继续并行B树扫描变得可用所需的页码。                      |                             |
| `ClogGroupUpdate`                   | 等待组长更新交易结束时的交易状态。                           |                             |
| `ExecuteGather`                     | 执行`Gather` 节点时等待子进程的活动。                        |                             |
| `Hash/Batch/Allocating`             | 等待选定的Parallel Hash参与者分配哈希表。                    |                             |
| `Hash/Batch/Electing`               | 选择并行哈希参与者以分配哈希表。                             |                             |
| `Hash/Batch/Loading`                | 等待其他Parallel Hash参与者完成加载哈希表。                  |                             |
| `Hash/Build/Allocating`             | 等待选定的Parallel Hash参与者分配初始哈希表。                |                             |
| `Hash/Build/Electing`               | 选择并行哈希参与者以分配初始哈希表。                         |                             |
| `Hash/Build/HashingInner`           | 等待其他Parallel Hash参与者完成内部关系的散列。              |                             |
| `Hash/Build/HashingOuter`           | 等待其他Parallel Hash参与者完成对外部关系的分区。            |                             |
| `Hash/GrowBatches/Allocating`       | 等待选出的Parallel Hash参与者分配更多批次。                  |                             |
| `Hash/GrowBatches/Deciding`         | 选择并行哈希参与者以决定未来的批量增长。                     |                             |
| `Hash/GrowBatches/Electing`         | 选择并行哈希参与者以分配更多批次。                           |                             |
| `Hash/GrowBatches/Finishing`        | 等待当选的Parallel Hash参与者决定未来的批量增长。            |                             |
| `Hash/GrowBatches/Repartitioning`   | 等待其他Parallel Hash参与者完成重新分区。                    |                             |
| `Hash/GrowBuckets/Allocating`       | 等待选出的Parallel Hash参与者完成分配更多桶。                |                             |
| `Hash/GrowBuckets/Electing`         | 选择并行哈希参与者以分配更多存储桶。                         |                             |
| `Hash/GrowBuckets/Reinserting`      | 等待其他Parallel Hash参与者完成将元组插入新桶。              |                             |
| `LogicalSyncData`                   | 等待逻辑复制远程服务器发送数据以进行初始表同步。             |                             |
| `LogicalSyncStateChange`            | 等待逻辑复制远程服务器更改状态。                             |                             |
| `MessageQueueInternal`              | 等待其他进程附加在共享消息队列中。                           |                             |
| `MessageQueuePutMessage`            | 等待将协议消息写入共享消息队列。                             |                             |
| `MessageQueueReceive`               | 等待从共享消息队列接收字节。                                 |                             |
| `MessageQueueSend`                  | 等待将字节发送到共享消息队列。                               |                             |
| `ParallelBitmapScan`                | 等待并行位图扫描初始化。                                     |                             |
| `ParallelCreateIndexScan`           | 等待并行`CREATE INDEX`工作者完成堆扫描。                     |                             |
| `ParallelFinish`                    | 等待并行工作者完成计算。                                     |                             |
| `ProcArrayGroupUpdate`              | 等待组长在交易结束时清除交易ID。                             |                             |
| `ReplicationOriginDrop`             | 等待复制源变为非活动状态以便删除。                           |                             |
| `ReplicationSlotDrop`               | 等待复制槽变为非活动状态以便删除。                           |                             |
| `SafeSnapshot`                      | 等待`READ ONLY DEFERRABLE` 事务的快照。                      |                             |
| `SyncRep`                           | 在同步复制期间等待远程服务器的确认。                         |                             |
| `BaseBackupThrottle`                | 在限制活动时在基本备份期间等待。                             | `Timeout`                   |
| `PgSleep`                           | 正在等待的过程中`pg_sleep`。                                 |                             |
| `RecoveryApplyDelay`                | 等待在恢复期间应用WAL因为它被延迟了。                        |                             |
| `BufFileRead`                       | 等待从缓冲文件中读取。                                       | `IO`                        |
| `BufFileWrite`                      | 等待写入缓冲文件。                                           |                             |
| `ControlFileRead`                   | 等待从控制文件中读取。                                       |                             |
| `ControlFileSync`                   | 等待控制文件达到稳定存储。                                   |                             |
| `ControlFileSyncUpdate`             | 等待控制文件的更新以达到稳定的存储。                         |                             |
| `ControlFileWrite`                  | 等待写入控制文件。                                           |                             |
| `ControlFileWriteUpdate`            | 等待写入更新控制文件。                                       |                             |
| `CopyFileRead`                      | 在文件复制操作期间等待读取。                                 |                             |
| `CopyFileWrite`                     | 在文件复制操作期间等待写入。                                 |                             |
| `DataFileExtend`                    | 等待关系数据文件被扩展。                                     |                             |
| `DataFileFlush`                     | 等待关系数据文件达到稳定存储。                               |                             |
| `DataFileImmediateSync`             | 等待关系数据文件立即同步到稳定存储。                         |                             |
| `DataFilePrefetch`                  | 等待关系数据文件的异步预取。                                 |                             |
| `DataFileRead`                      | 等待从关系数据文件中读取。                                   |                             |
| `DataFileSync`                      | 等待关系数据文件的更改以达到稳定的存储。                     |                             |
| `DataFileTruncate`                  | 等待关系数据文件被截断。                                     |                             |
| `DataFileWrite`                     | 等待写入关系数据文件。                                       |                             |
| `DSMFillZeroWrite`                  | 等待将零字节写入动态共享内存后备文件。                       |                             |
| `LockFileAddToDataDirRead`          | 在向数据目录锁定文件添加行时等待读取。                       |                             |
| `LockFileAddToDataDirSync`          | 在向数据目录锁定文件添加行时，等待数据达到稳定存储。         |                             |
| `LockFileAddToDataDirWrite`         | 在向数据目录锁定文件添加行时等待写入。                       |                             |
| `LockFileCreateRead`                | 在创建数据目录锁定文件时等待读取。                           |                             |
| `LockFileCreateSync`                | 在创建数据目录锁定文件时等待数据达到稳定存储。               |                             |
| `LockFileCreateWrite`               | 在创建数据目录锁定文件时等待写入。                           |                             |
| `LockFileReCheckDataDirRead`        | 在重新检查数据目录锁定文件期间等待读取。                     |                             |
| `LogicalRewriteCheckpointSync`      | 在检查点期间等待逻辑重写映射以达到稳定存储。                 |                             |
| `LogicalRewriteMappingSync`         | 在逻辑重写期间等待映射数据以达到稳定存储。                   |                             |
| `LogicalRewriteMappingWrite`        | 在逻辑重写期间等待写入映射数据。                             |                             |
| `LogicalRewriteSync`                | 等待逻辑重写映射以达到稳定存储。                             |                             |
| `LogicalRewriteWrite`               | 等待写入逻辑重写映射。                                       |                             |
| `RelationMapRead`                   | 等待读取关系映射文件。                                       |                             |
| `RelationMapSync`                   | 等待关系映射文件达到稳定存储。                               |                             |
| `RelationMapWrite`                  | 等待写入关系映射文件。                                       |                             |
| `ReorderBufferRead`                 | 在重新排序缓冲区管理期间等待读取。                           |                             |
| `ReorderBufferWrite`                | 在重新排序缓冲区管理期间等待写入。                           |                             |
| `ReorderLogicalMappingRead`         | 在重新排序缓冲区管理期间等待读取逻辑映射。                   |                             |
| `ReplicationSlotRead`               | 等待从复制槽控制文件中读取。                                 |                             |
| `ReplicationSlotRestoreSync`        | 等待复制槽控制文件在恢复到内存时达到稳定存储。               |                             |
| `ReplicationSlotSync`               | 等待复制槽控制文件以达到稳定存储。                           |                             |
| `ReplicationSlotWrite`              | 等待写入复制槽控制文件。                                     |                             |
| `SLRUFlushSync`                     | 在检查点或数据库关闭期间等待SLRU数据达到稳定存储。           |                             |
| `SLRURead`                          | 等待读取SLRU页面。                                           |                             |
| `SLRUSync`                          | 在页面写入后等待SLRU数据达到稳定存储。                       |                             |
| `SLRUWrite`                         | 等待写入SLRU页面。                                           |                             |
| `SnapbuildRead`                     | 等待读取序列化历史目录快照。                                 |                             |
| `SnapbuildSync`                     | 等待序列化历史目录快照以达到稳定存储。                       |                             |
| `SnapbuildWrite`                    | 等待写入序列化历史目录快照。                                 |                             |
| `TimelineHistoryFileSync`           | 等待通过流复制接收的时间线历史文件以达到稳定存储。           |                             |
| `TimelineHistoryFileWrite`          | 等待写入通过流复制接收的时间线历史文件。                     |                             |
| `TimelineHistoryRead`               | 等待读取时间轴历史文件。                                     |                             |
| `TimelineHistorySync`               | 等待新创建的时间轴历史文件以达到稳定存储。                   |                             |
| `TimelineHistoryWrite`              | 等待写入新创建的时间轴历史文件。                             |                             |
| `TwophaseFileRead`                  | 等待读取两阶段状态文件。                                     |                             |
| `TwophaseFileSync`                  | 等待两阶段状态文件达到稳定存储。                             |                             |
| `TwophaseFileWrite`                 | 等待写入两阶段状态文件。                                     |                             |
| `WALBootstrapSync`                  | 等待WAL在引导期间达到稳定存储。                              |                             |
| `WALBootstrapWrite`                 | 等待在引导期间写入WAL页面。                                  |                             |
| `WALCopyRead`                       | 通过复制现有WAL段创建新的WAL段时等待读取。                   |                             |
| `WALCopySync`                       | 等待通过复制现有WAL段创建的新WAL段以达到稳定存储。           |                             |
| `WALCopyWrite`                      | 通过复制现有的WAL段创建新的WAL段时等待写入。                 |                             |
| `WALInitSync`                       | 等待新初始化的WAL文件达到稳定存储。                          |                             |
| `WALInitWrite`                      | 初始化新的WAL文件时等待写入。                                |                             |
| `WALRead`                           | 等待从WAL文件中读取。                                        |                             |
| `WALSenderTimelineHistoryRead`      | 在walsender timeline命令期间等待时间轴历史文件的读取。       |                             |
| `WALSyncMethodAssign`               | 在分配WAL同步方法时等待数据达到稳定存储。                    |                             |
| `WALWrite`                          | 等待写入WAL文件。                                            |                             |



